import numpy as np
import pandas as pd
from tqdm import tqdm
import time
import datetime
import ccxt
import pyupbit
import telegram
import matplotlib.pyplot as plt

# setup Upbit
access = "<ACCESS KEY>"
secret = "<SECRET KEY>"
upbit = pyupbit.Upbit(access, secret)

# setup telegram
token = "<TELEGRAM TOKEN>"
chat_id = "<CHAT ID>"
telegram_bot = telegram.Bot(token=token)

# define global variables
gamma = 0.05  # upbit commissions
w = 5  # window size for mean reversion models
threshold = 0.005  # for deciding if it's the right timing to invest
model_selector_w = 85  # duration that the GMA model selector refers to
assets = [
    "KRW-BTC",
    "KRW-ETH",
    "KRW-DOT",
    "KRW-LINK",
    "KRW-WAXP",
    "KRW-MANA",
    "KRW-MATIC",
    "KRW-SAND",
    "KRW-SOL",
    "KRW-AAVE",
    "KRW-STX",
    "KRW-XTZ",
]
m = len(assets)
init_seed = upbit.get_balance("KRW")

# compute geometric mean of array x
def geometric_mean(x):
    x = np.asarray(x)
    return x.prod() ** (1 / len(x))


# simplex projection
# simplex projection
def simplex_proj(y):
    """Projection of y onto simplex."""
    m = len(y)
    bget = False
    s = sorted(y, reverse=True)
    tmpsum = 0.0
    for ii in range(m - 1):
        tmpsum = tmpsum + s[ii]
        tmax = (tmpsum - 1) / (ii + 1)
        if tmax >= s[ii + 1]:
            bget = True
            break
    if not bget:
        tmax = (tmpsum + s[m - 1] - 1) / m
    y = np.asarray(y)
    return np.maximum(y - tmax, 0.0)


# Transaction Cost Optimization
def tco(x, current_portfolio, x_pred, trx_fee_pct=gamma, eta=10):
    lambd = 10 * trx_fee_pct
    updated_portfolio = np.multiply(current_portfolio, x) / np.dot(current_portfolio, x)
    vt = x_pred / np.dot(updated_portfolio, x_pred)
    v_t_ = np.mean(vt)
    b_1 = eta * (vt - np.dot(v_t_, 1))
    b_ = updated_portfolio + np.sign(b_1) * np.maximum(
        np.zeros(len(b_1)), np.abs(b_1) - lambd
    )
    proj = simplex_proj(b_)
    return proj


def get_cash():
    s = upbit.get_balance("KRW")
    for i in range(m):
        while True:
            try:
                value = upbit.get_balance(assets[i]) * pyupbit.get_current_price(
                    assets[i]
                )
                s += value
                break
            except Exception as e:
                print(e)
                time.sleep(3)
    return s


# trade logic
cash_amount = get_cash()
defensive_bah_portfolio = [1 / m for _ in range(m)]
defensive_tco_portfolio = [1 / m for _ in range(m)]
defensive_cash_status = [cash_amount]
defensive_bah_returns = []
defensive_tco_returns = []
choice = 0  # 0: Uniform BAH, 1: Cash Agent, 2: TCO
bah_cnt, ca_cnt, tco_cnt = 0, 0, 0
iterations = 0

while True:
    t0 = time.time()
    text = (
        "============================= Trade {} =============================".format(
            iterations
        )
    )
    telegram_bot.sendMessage(chat_id=chat_id, text=text)
    dfs = []
    for ticker in tqdm(assets, position=0, leave=True):
        while True:
            try:
                df = pyupbit.get_ohlcv(ticker, interval="minute60")
                df = df.iloc[-1::-10][::-1]
                dfs.append(df)
                break
            except Exception as e:
                print("Error occured when scraping past data for {}".format(ticker))
                print(e)
                time.sleep(3)
        time.sleep(1)

    price_data = np.concatenate(
        [dfs[i]["close"].values.reshape((-1, 1)) for i in range(m)], axis=1
    )

    # calculate current returns
    current_returns = []
    for i in range(m):
        ret = price_data[-1, i] / price_data[-2, i]
        current_returns.append(ret)

    # next price prediction using moving average
    predicted_returns = []
    for i in range(m):
        moving_avg = np.mean(price_data[-w:, i])
        ret = moving_avg / price_data[-1, i]
        predicted_returns.append(ret)

    if iterations > 0:
        # sell
        # only sell when we have chosen tco before
        # uniform bah and cash agent do not require selling
        if choice == 2:
            for i in range(m):
                while True:
                    try:
                        unit = upbit.get_balance(assets[i])
                        upbit.sell_market_order(assets[i], unit)
                        break
                    except Exception as e:
                        text = "Error occured when selling {}... waiting for the issue to be resolved".format(
                            assets[i]
                        )
                        telegram_bot.sendMessage(chat_id=chat_id, text=text)
                        print(e)
                        time.sleep(3)
                time.sleep(1)

        # store cash amount
        cash_amount = get_cash()
        defensive_cash_status.append(cash_amount)
        text = "current cash amount = ${}".format(cash_amount)
        telegram_bot.sendMessage(chat_id=chat_id, text=text)
        text = (
            "model stats \n"
            + "UNIFORM BAH count: {}\n".format(bah_cnt)
            + "TCO count: {}\n".format(tco_cnt)
            + "CASH AGENT count: {}\n".format(ca_cnt)
        )
        telegram_bot.sendMessage(chat_id=chat_id, text=text)

        # store returns for each models
        defensive_bah_returns.append(
            np.sum([x * y for x, y in zip(defensive_bah_portfolio, current_returns)])
        )
        if len(defensive_bah_returns) > model_selector_w:
            defensive_bah_returns.pop(0)

        defensive_tco_returns.append(
            np.sum([x * y for x, y in zip(defensive_tco_portfolio, current_returns)])
        )
        if len(defensive_tco_returns) > model_selector_w:
            defensive_tco_returns.pop(0)

    if iterations == 0:
        # very first trade
        # buy
        # default for first trade is uniform bah
        cash_amount = get_cash()
        text = "current cash amount = ${}".format(cash_amount)
        telegram_bot.sendMessage(chat_id=chat_id, text=text)
        bah_cnt += 1
        choice = 0
        # update tco portfolio
        defensive_tco_portfolio = tco(
            current_returns, defensive_tco_portfolio, predicted_returns
        )
        # buy according to uniform bah
        for i in range(m):
            while True:
                try:
                    upbit.buy_market_order(
                        assets[i],
                        cash_amount * (1 - gamma / 100) * defensive_bah_portfolio[i],
                    )
                    break
                except Exception as e:
                    text = "Error occured when buying {}... waiting for the issue to be resolved".format(
                        assets[i]
                    )
                    telegram_bot.sendMessage(chat_id=chat_id, text=text)
                    print(e)
                    time.sleep(3)
            time.sleep(1)

    elif iterations > 0:
        # update tco portfolio
        defensive_tco_portfolio = tco(
            current_returns, defensive_tco_portfolio, predicted_returns
        )

        gma_profits_bah = geometric_mean(defensive_bah_returns)
        gma_profits_tco = geometric_mean(defensive_tco_returns)

        best_profits = (
            gma_profits_bah if gma_profits_bah > gma_profits_tco else gma_profits_tco
        )
        best_choice = 0 if gma_profits_bah > gma_profits_tco else 2

        if best_profits > 1 + threshold:
            bah_cnt += best_choice == 0
            tco_cnt += best_choice == 2
            if choice == 1:
                # we open positions based on the best portfolio
                best_portfolio = (
                    defensive_bah_portfolio
                    if best_choice == 0
                    else defensive_tco_portfolio
                )
                for i in range(m):
                    while True:
                        try:
                            upbit.buy_market_order(
                                assets[i],
                                cash_amount * (1 - gamma / 100) * best_portfolio[i],
                            )
                            break
                        except Exception as e:
                            text = "Error occured when buying {}... waiting for the issue to be resolved".format(
                                assets[i]
                            )
                            telegram_bot.sendMessage(chat_id=chat_id, text=text)
                            print(e)
                            time.sleep(3)
                    time.sleep(1)
            choice = best_choice  # set to best choice
        else:
            ca_cnt += 1
            if choice == 0 or choice == 2:
                # close previously opened unform bah or tco
                for i in range(m):
                    while True:
                        try:
                            unit = upbit.get_balance(assets[i])
                            upbit.sell_market_order(assets[i], unit)
                            break
                        except Exception as e:
                            text = "Error occured when selling {}... waiting for the issue to be resolved".format(
                                assets[i]
                            )
                            telegram_bot.sendMessage(chat_id=chat_id, text=text)
                            print(e)
                            time.sleep(3)
                    time.sleep(1)
            choice = 1  # set to cash agent
    iterations += 1
    text = "waiting for the next rebalancing period (10hrs)"
    telegram_bot.sendMessage(chat_id=chat_id, text=text)
    elapsed = time.time() - t0
    time.sleep(60 * 60 * 10 - elapsed)
