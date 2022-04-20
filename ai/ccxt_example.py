import ccxt
from pprint import pprint
from ccxt.base.errors import ExchangeError

if __name__ == '__main__':
    # List up all methods available.
    pprint(dir(ccxt.bybit()))  # Python

    # Some exchange allows sandbox mode
    # Bybit does not have SANDBOX MODE for Futures API
    SANDBOX_MODE = False

    # define session and set leverage
    bybit_api_key = ""
    bybit_api_secret = ""

    exchange = ccxt.bybit({
        'enableRateLimit': True,
        "apiKey": bybit_api_key,
        "secret": bybit_api_secret,
    })
    exchange.set_sandbox_mode(SANDBOX_MODE)  # enable sandbox mode

    # First, call to update the latest info. Data will be cached
    exchange.load_markets()

    # Always calculate price/amount using CCXT's XX_to_precision
    symbol = 'BTC/USDT'
    amount = 1.2345678  # amount in base currency BTC
    price = 87654.321  # price in quote currency USDT
    formatted_amount = exchange.amount_to_precision(symbol, amount)
    formatted_price = exchange.price_to_precision(symbol, price)
    print(formatted_price, formatted_amount)

    # Orderbook
    orderbook = exchange.fetch_order_book(symbol=symbol)
    print(orderbook)

    # Best limit price
    max_bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    min_ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
    print(max_bid, min_ask)

    # OHLCV
    # ohlcv = exchange.fetch_ohlcv(symbol, '1d')

    # USDT Futures
    # set leverage
    try:
        exchange.private_post_private_linear_position_set_leverage({
            "symbol": exchange.market(symbol)['id'],  # get id by symbol
            "buy_leverage": 1,
            "sell_leverage": 1,
        })
    except ExchangeError as e:
        pass

    # fetch positions for one market
    buy_position = exchange.fetch_positions(symbols=[symbol])[0]
    buy_position_size = buy_position["size"]
    sell_position = exchange.fetch_positions(symbols=[symbol])[1]
    sell_position_size = sell_position["size"]
    print(buy_position_size, sell_position_size)

    # create linear active order (USDT Perpetual)
    # See https://bybit-exchange.github.io/docs/linear/#t-placeactive

    # If initial position, reduce_only = False
    # If there is current position and if you want to close this position, use reduce_only = True

    # Best Limit Buy (using max_bid)
    print(exchange.private_post_private_linear_order_create({
        "symbol": exchange.market(symbol)['id'],  # get id by symbol
        "side": "Buy",
        "order_type": "Limit",
        "price": exchange.price_to_precision(symbol=symbol, price=min_ask),
        "qty": exchange.amount_to_precision(symbol=symbol, amount=0.001),
        "time_in_force": "GoodTillCancel",
        "reduce_only": False,
        "close_on_trigger": False,
    }))

    # # Best Limit Sell (using min_ask)
    print(exchange.private_post_private_linear_order_create({
        "symbol": exchange.market(symbol)['id'],  # get id by symbol
        "side": "Sell",
        "order_type": "Limit",
        "price": exchange.price_to_precision(symbol=symbol, price=max_bid),
        "qty": exchange.amount_to_precision(symbol=symbol, amount=0.001),
        "time_in_force": "GoodTillCancel",
        "reduce_only": True,
        "close_on_trigger": False,
    }))
