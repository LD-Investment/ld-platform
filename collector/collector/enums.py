from enum import Enum


class RmqExchangeName(Enum):
    """RabbitMQ Exchange Name"""

    COLLECTOR = "ldbot.collector"


class RmqQueueName(Enum):
    """RabbitMQ Queue Name (= routing key)"""

    # Data Collector
    ORDERBOOK_1S = "orderbook_1s"
    ORDERBOOK_1M = "orderbook_1m"


class TradeSymbol(Enum):
    BTC_USDT = "BTC/USDT"
    ETH_USDT = "ETH/USDT"
    XRP_USDT = "XRP/USDT"
    BNB_USDT = "BNB/USDT"
    BCH_USDT = "BCH/USDT"
