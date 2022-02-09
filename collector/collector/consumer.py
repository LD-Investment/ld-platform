import asyncio
import json
import logging
import os
from asyncio.events import AbstractEventLoop
from time import sleep

import aio_pika
import sentry_sdk

from .enums import RmqQueueName

logger = logging.getLogger(__name__)


class CollectorConsumer:  # pylint: disable=R0903
    """
    Exchange Orderbook subscriber from RabbitMQ message queue
    """

    PREFETCH_COUNT = 10
    MAX_CONN_RETRIAL = 10

    def __init__(self, rmq_host: str, queue_name: RmqQueueName):
        # read environment variables
        self._mode = os.environ.get("COLLECTOR_MODE")
        self._sentry_dsn = os.environ.get("SENTRY_DSN", None)
        self._sentry_trace_sample_rate = float(
            os.environ.get("SENTRY_TRACE_SAMPLE_RATE", 1.0)
        )

        # enable sentry
        if self._sentry_dsn:
            logger.info("Sentry enabled)")
            sentry_sdk.init(
                self._sentry_dsn, traces_sample_rate=self._sentry_trace_sample_rate
            )

        # Localhost: amqp://guest:guest@localhost
        self.rmq_host: str = rmq_host
        self.queue_name: str = queue_name.value

        # TODO: connect database according to COLLECTOR_MODE

    def run(self):
        # Run loop
        loop: AbstractEventLoop = asyncio.get_event_loop()
        _conn = loop.run_until_complete(self._main_loop(loop))
        try:
            loop.run_forever()
        finally:
            loop.run_until_complete(_conn.close())

    async def _main_loop(self, loop: AbstractEventLoop):
        count = 0
        while True:
            try:
                count += 1
                _conn = await aio_pika.connect_robust(self.rmq_host, loop=loop)
                break
            except ConnectionError as e:
                if count > self.MAX_CONN_RETRIAL:
                    logger.error("Connection failed to establish")
                    raise e
                logger.info(f"Connection trial: {count}")
                sleep(5)

        logger.info("Connection established for consuming")
        # Creating channel
        channel = await _conn.channel()

        # Maximum message count which will be processing at the same time.
        await channel.set_qos(prefetch_count=self.PREFETCH_COUNT)

        # Declaring queue
        queue = await channel.declare_queue(self.queue_name, auto_delete=True)
        await queue.consume(self._consume)
        return _conn

    async def _consume(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                symbol = message.headers_raw["symbol"].decode()
                msg = json.loads(message.body.decode())
                msg["symbol"] = symbol
                timestamp = msg["timestamp"]
                logger.info("Received orderbook(%s) | %s", symbol, timestamp)

                if msg.get("nonce"):
                    del msg["nonce"]

                # TODO: persist to db

            except Exception as err:  # pylint: disable=W0703
                logger.error(err)
