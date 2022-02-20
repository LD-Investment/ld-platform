import asyncio
import json
import logging
import os
from asyncio.events import AbstractEventLoop
from decimal import Decimal
from time import sleep

import aio_pika
import boto3
import sentry_sdk

from .enums import RmqQueueName

logger = logging.getLogger(__name__)


class CollectorConsumer:  # pylint: disable=R0903
    """
    Exchange Orderbook subscriber from RabbitMQ message queue
    """

    PREFETCH_COUNT = 10
    MAX_CONN_RETRIAL = 10
    AWS_DYNAMODB_TABLE = "1sec_orderbook_binance"

    def __init__(self, rmq_host: str, queue_name: RmqQueueName):
        # read environment variables
        self._mode = os.environ.get("COLLECTOR_MODE")
        self._sentry_dsn = os.environ.get("SENTRY_DSN", None)
        self._sentry_trace_sample_rate = float(
            os.environ.get("SENTRY_TRACE_SAMPLE_RATE", 1.0)
        )

        # enable sentry
        if self._sentry_dsn:
            logger.info("Sentry enabled")
            sentry_sdk.init(
                self._sentry_dsn, traces_sample_rate=self._sentry_trace_sample_rate
            )

        # Localhost: amqp://guest:guest@localhost
        self.rmq_host: str = rmq_host
        self.queue_name: str = queue_name.value

        # AWS DynamoDB
        if self._mode == "local":
            self._dynamodb = boto3.resource(
                "dynamodb", endpoint_url="http://dynamodb-local:8000"
            )
            logger.info("AWS local DynamoDB enabled")
        else:
            self._dynamodb = boto3.resource(
                "dynamodb",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )
            logger.info("AWS prod DynamoDB enabled")

        # check table
        self._create_dynamo_db_local_table_if_not_exists()
        self._dynamodb_table = self._dynamodb.Table(self.AWS_DYNAMODB_TABLE)
        logger.info(f"Using AWS dynamoDB table: '{self.AWS_DYNAMODB_TABLE}'")

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

                del msg["datetime"]
                if msg.get("nonce"):
                    del msg["nonce"]

                # convert float to Decimal
                data = json.loads(json.dumps(msg), parse_float=Decimal)
                data["id"] = data["symbol"] + "-" + str(data["timestamp"])
                self._dynamodb_table.put_item(Item=data)
                logger.info("Received and saved orderbook(%s) | %s", symbol, timestamp)

            except Exception as e:  # pylint: disable=W0703
                logger.error(e)

    def _create_dynamo_db_local_table_if_not_exists(self):
        if not self._dynamodb:
            raise RuntimeError("Please initialize DynamoDB instance first!")

        table_names = [table.name for table in self._dynamodb.tables.all()]
        if self._mode == "local":
            if self.AWS_DYNAMODB_TABLE in table_names:
                logger.info(
                    f"DynamoDB table({self.AWS_DYNAMODB_TABLE}) already exists. Skipping..."
                )
                return
            logger.info(
                f"DynamoDB table({self.AWS_DYNAMODB_TABLE}) does not exist. Now creating one."
            )
            self._dynamodb.create_table(
                AttributeDefinitions=[
                    {
                        "AttributeName": "id",
                        "AttributeType": "S",
                    },
                    {
                        "AttributeName": "timestamp",
                        "AttributeType": "N",
                    },
                ],
                KeySchema=[
                    {
                        "AttributeName": "id",
                        "KeyType": "HASH",
                    },
                    {
                        "AttributeName": "timestamp",
                        "KeyType": "RANGE",
                    },
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
                TableName=self.AWS_DYNAMODB_TABLE,
            )
            logger.info(
                f"Successfully created DynamoDB table({self.AWS_DYNAMODB_TABLE})."
            )
        else:
            # if mode is prod, user should create table via AWS console
            raise RuntimeError(
                f"DynamoDB table({self.AWS_DYNAMODB_TABLE}) does not exist. Please create one."
            )
