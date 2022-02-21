import argparse
import logging

from .consumer import CollectorConsumer
from .enums import RmqQueueName, TradeSymbol
from .logger import LOG_FORMAT
from .producer import CollectorProducer

RMQ_SERVER_CONTAINER_NAME = "collector-rmqserver"
RMQ_SERVER_HOST = f"amqp://guest:guest@{RMQ_SERVER_CONTAINER_NAME}:5672"
RUN_MODE_CHOICES = ["producer", "consumer"]
RUN_SYMBOL_CHOICES = ["BTC_USDT", "ETH_USDT", "XRP_USDT", "BNB_USDT", "BCH_USDT"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--mode", required=True, choices=RUN_MODE_CHOICES, help="Mode to run collector"
    )
    parser.add_argument(
        "-s", "--symbol", required=False, choices=RUN_SYMBOL_CHOICES, help="Symbol to run producer"
    )
    parser.add_argument(
        "-v", "--verbose", default=False, action="store_true", help="Log verbosely"
    )
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO, format=LOG_FORMAT
    )

    if args.mode == "producer":
        if not args.symbol:
            raise RuntimeError("You should provide SYMBOL to run producer. (E.g BTC_USDT)")
        pub = CollectorProducer(
            rmq_host=RMQ_SERVER_HOST,
            queue_name=RmqQueueName.ORDERBOOK_1S,
            symbol=getattr(TradeSymbol, args.symbol),
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
