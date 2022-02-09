import asyncio
import json
import logging
import os
import time
from asyncio.events import AbstractEventLoop
from time import sleep

import aio_pika
import ccxtpro
import sentry_sdk
from aio_pika.channel import Channel
from aio_pika.message import Message
from ccxtpro.base.order_book import OrderBook

from .enums import RmqQueueName, TradeSymbol

logger = logging.getLogger(__name__)


class CollectorProducer:  # pylint: disable=R0903
    """
    Exchange Orderbook producer to RabbitMQ message queue using CCXT Pro Websocket API interface.
    """

    MAX_CONN_RETRIAL = 10

    def __init__(
        self,
        rmq_host: str,
        queue_name: RmqQueueName,
        symbol: TradeSymbol,
        interval_sec: int = 1,
    ):
        # read environment variables
        self._mode = os.environ.get("COLLECTOR_MODE")
        self._sentry_dsn = os.environ.get("SENTRY_DSN", None)
        self._sentry_trace_sample_rate = float(
            os.environ.get("SENTRY_TRACE_SAMPLE_RATE", 1.0)
        )

        # enable sentry
        if not self._sentry_dsn:
            sentry_sdk.init(
                self._sentry_dsn, traces_sample_rate=self._sentry_trace_sample_rate
            )

        # Localhost: amqp://guest:guest@localhost
        self.rmq_host: str = rmq_host
        self.queue_name = queue_name
        self.symbol: str = symbol.value
        self.interval_sec = interval_sec

        self.exchange = ccxtpro.binance(
            {
                "enableRateLimit": True,  # required according to the Manual
            }
        )

    def run(self):
        # Run loop
        logger.info("Starting RabbitMQ async producer.")
        loop: AbstractEventLoop = asyncio.get_event_loop()
        loop.run_until_complete(self._main_loop(loop))
        loop.close()

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

        logger.info("Connection established for producing")
        async with _conn:
            channel = await _conn.channel()
            before_msec = None
            while True:
                try:
                    order_book: OrderBook = await self.exchange.watch_order_book(
                        self.symbol, limit=100
                    )
                    cur_msec = order_book["timestamp"]

                    # there is a chance of None
                    if not cur_msec:
                        cur_msec = self._current_milli_epoch_time()

                    if not before_msec:
                        before_msec = cur_msec
                        continue

                    # publish to RMQ server
                    await self._publish(self.symbol, channel, order_book)
                except Exception as err:  # pylint: disable=W0703
                    logger.error(err)

                # sleep by adjustment adjust network RTT
                sleep_interval = self.interval_sec
                diff = (cur_msec - before_msec) / 1000
                if diff > self.interval_sec:
                    sleep_interval = round(2 * self.interval_sec - diff, 2)
                before_msec = cur_msec
                await asyncio.sleep(sleep_interval)

    async def _publish(self, symbol: str, channel: Channel, orderbook: dict):
        # preprocess
        datetime = orderbook["datetime"]
        logger.info(
            f'{datetime} {symbol} | ask[0]:{orderbook["asks"][0]} |bid[0]:{orderbook["bids"][0]}'
        )
        await channel.default_exchange.publish(
            message=Message(
                headers={"symbol": symbol}, body=json.dumps(orderbook).encode()
            ),
            routing_key=self.queue_name.value,
        )

    @staticmethod
    def _current_milli_epoch_time():
        # e.g 1644398437664
        return round(time.time() * 1000)
