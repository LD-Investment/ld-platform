import time
from datetime import datetime
from pprint import pprint

import ccxt

if __name__ == "__main__":
    start_date = "2017-01-01"
    end_date = "2021-12-31"

    ccxt.bybit(
        {
            "option": {
                "defaultType": "future",
            }
        }
    )

    # BINANCE
    binance = ccxt.binance({"option": {"defaultMarket": "futures"}})
    start = (
        int(
            time.mktime(
                datetime.strptime(start_date + " 00:00", "%Y-%m-%d %H:%M").timetuple()
            )
        )
        * 1000
    )
    end = (
        int(
            time.mktime(
                datetime.strptime(end_date + " 23:59", "%Y-%m-%d %H:%M").timetuple()
            )
        )
        * 1000
    )

    res = binance.fapiData_get_globallongshortaccountratio(
        {
            "symbol": "BTCUSDT",
            "period": "5m",
            # "startTime": start,
            # "endTime": end,
            "limit": 1,
        }
    )
    pprint(res)
    timestamp_seconds = int(res[0]["timestamp"]) / 1000
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp_seconds)))

    # BYBIT
    bybit = ccxt.bybit({"enableRateLimit": True})
    # pprint(dir(bybit))
    res = bybit.public_get_v2_public_account_ratio(
        {"symbol": "BTCUSD", "period": "5min", "limit": 1}
    )
    pprint(res)

    timestamp_seconds = int(res["result"][0]["timestamp"])
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp_seconds)))
