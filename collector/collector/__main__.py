import argparse
import logging

from .consumer import CollectorConsumer
from .enums import RmqQueueName, TradeSymbol
from .logger import LOG_FORMAT
from .producer import CollectorProducer

RMQ_SERVER_CONTAINER_NAME = "collector-rmqserver"
RMQ_SERVER_HOST = f"amqp://guest:guest@{RMQ_SERVER_CONTAINER_NAME}:5672"
RUN_CHOICES = ["producer", "consumer"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--mode", required=True, choices=RUN_CHOICES, help="Mode to run collector"
    )
    parser.add_argument(
        "-v", "--verbose", default=False, action="store_true", help="Log verbosely"
    )
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO, format=LOG_FORMAT
    )

    if args.mode == "producer":
        pub = CollectorProducer(
            rmq_host=RMQ_SERVER_HOST,
            queue_name=RmqQueueName.ORDERBOOK_1S,
            symbol=TradeSymbol.BTC_USDT,
        )
        pub.run()

    elif args.mode == "consumer":
        con = CollectorConsumer(
            rmq_host=RMQ_SERVER_HOST,
            queue_name=RmqQueueName.ORDERBOOK_1S,
        )
        con.run()
    else:
        raise RuntimeError("Invalid option. Aborting..")
