import time

import ccxt
import numpy as np
import pandas as pd
import pandas_ta as ta
import telegram
from ccxt.base.errors import ExchangeError
from ccxt.bybit import bybit as BybitExchange
from pytorch_tabnet.tab_model import TabNetClassifier
from tqdm import tqdm


class TabNetBybitTrader:
    STOP_LOSS_PERCENT = 3
    TAKE_PROFIT_PERCENT = 0.75

    def __init__(self, symbol: str, bybit_credential: dict, telegram_credential: dict, tabnet_zip_dir: str, ):
        # init exchange
        self._exchange: BybitExchange = ccxt.bybit({
            'enableRateLimit': True,
            "apiKey": bybit_credential["api_key"],
            "secret": bybit_credential["api_secret"],
        })
        # update exchange info
        self._exchange.load_markets()

        # save market info
        self._symbol = symbol
        self._symbol_id = self._exchange.market(self._symbol)['id']  # get id by symbol

        # set leverage
        self._set_leverage(buy_leverage=1, sell_leverage=1)

        # load trained model
        self._tn = TabNetClassifier()
        self._tn.load_model(tabnet_zip_dir)

        # define telegram bot
        self._telebot = telegram.Bot(token=telegram_credential["token"])
        self._telegram_chat_id = telegram_credential["chat_id"]

    ####################################
    # Data Processing specific Methods #
    ####################################

    def _get_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self._exchange.fetch_ohlcv(self._symbol, timeframe='4h', limit=200))
        df = df.rename(columns={0: 'timestamp',
                                1: 'open',
                                2: 'high',
                                3: 'low',
                                4: 'close',
                                5: 'volume'})
        return df

    def _create_timestamps(self, df: pd.DataFrame) -> pd.DataFrame:
        dates = df['timestamp'].values
        timestamp = []
        for i in range(len(dates)):
            date_string = self._exchange.iso8601(int(dates[i]))
            date_string = date_string[:10] + " " + date_string[11:-5]
            timestamp.append(date_string)
        df['datetime'] = timestamp
        df = df.drop(columns={'timestamp'})
        df.set_index(pd.DatetimeIndex(df["datetime"]), inplace=True)
        return df

    @staticmethod
    def _preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
        # add datetime information
        hours = []
        days = []
        months = []
        years = []
        for dt in tqdm(df['datetime']):
            hour = pd.to_datetime(dt).hour
            day = pd.to_datetime(dt).day
            month = pd.to_datetime(dt).month
            year = pd.to_datetime(dt).year
            hours.append(hour)
            days.append(day)
            months.append(month)
            years.append(year)
        df['Hours'] = hours
        df['Days'] = days
        df['Months'] = months
        df['Years'] = years
        print("=== Feature Engineering ===")

        # add rvi
        df['RVI'] = df.ta.rvi(lookahead=False)

        # inertia
        df['inertia'] = df.ta.inertia(lookahead=False)

        # differencing
        for l in range(1, 24):
            for col in ['open', 'high', 'low', 'close', 'volume']:
                val = df[col].values
                val_ret = [None for _ in range(l)]
                for i in range(l, len(val)):
                    if val[i - l] == 0:
                        ret = 1
                    else:
                        ret = val[i] / val[i - l]
                    val_ret.append(ret)
                df[f'{col}_change_{l}'] = val_ret

        # ebsw
        df['ebsw'] = df.ta.ebsw(lookahead=False)
        # rsi
        df['RSI'] = df.ta.rsi(lookahead=False)
        # rsx
        df['RSX'] = df.ta.rsx(lookahead=False)
        # chaikin money flow
        df['cmf'] = df.ta.cmf(lookahead=False)
        # volume weighted average price
        df['vwap'] = df.ta.vwap(lookahead=False)
        # holt-winter moving average
        df['hwma'] = df.ta.hwma(lookahead=False).values
        # fibonacci's weighted moving average
        df['fwma'] = df.ta.fwma(lookahead=False).values
        # add average directional movement index
        df = pd.concat([df, df.ta.adx(lookahead=False)], axis=1)
        # add ultimate oscillator
        df['uo'] = df.ta.uo(lookahead=False)
        # moving average convergence divergence
        df = pd.concat([df, df.ta.macd(lookahead=False)], axis=1)
        # bollinger bands
        df = pd.concat([df, df.ta.bbands(lookahead=False)], axis=1)
        # exponential moving averages
        df['EMA10'] = df.ta.ema(length=10, lookahead=False)
        df['EMA30'] = df.ta.ema(length=30, lookahead=False)
        df['EMA60'] = df.ta.ema(length=60, lookahead=False)

        df = df.dropna()
        df = df.drop(columns={'datetime', 'Years'})
        return df

    #################
    # Miscellaneous #
    #################

    def _send_tele_message(self, text: str):
        self._telebot.sendMessage(chat_id=self._telegram_chat_id, text=text)

    #############################
    # Exchange specific Methods #
    #############################

    def _set_leverage(self, buy_leverage: int, sell_leverage: int):
        try:
            self._exchange.private_post_private_linear_position_set_leverage({
                "symbol": self._symbol_id,
                "buy_leverage": buy_leverage,
                "sell_leverage": sell_leverage,
            })
        except ExchangeError:
            # if leverage not changed, bybit throws error thus ignore
            pass

    def _position_exists(self):
        positions = self._exchange.private_get_private_linear_position_list(
            {
                "symbol": self._symbol_id
            })["result"]
        buy_position_exists = positions[0]["size"] != 0
        sell_position_exists = positions[1]["size"] != 0
        return buy_position_exists or sell_position_exists

    def _get_best_bid_ask(self):
        # Get best bid/ask price to achieve immediate limit order
        orderbook = self._exchange.fetch_order_book(symbol=self._symbol)
        max_bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
        min_ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
        return max_bid, min_ask

    def _place_best_buy_limit_order(self, qty: float, reduce_only: bool, **kwargs):
        max_bid, min_ask = self._get_best_bid_ask()
        self._exchange.private_post_private_linear_order_create({
            "symbol": self._symbol_id,  # get id by symbol
            "side": "Buy",
            "order_type": "Limit",
            "price": self._exchange.price_to_precision(symbol=self._symbol, price=min_ask),
            "qty": self._exchange.amount_to_precision(symbol=self._symbol, amount=qty),
            "time_in_force": "GoodTillCancel",
            "reduce_only": reduce_only,
            "close_on_trigger": False,
            **kwargs,
        })

    def _place_best_sell_limit_order(self, qty: float, reduce_only: bool, **kwargs):
        max_bid, min_ask = self._get_best_bid_ask()
        self._exchange.private_post_private_linear_order_create({
            "symbol": self._symbol_id,
            "side": "Sell",
            "order_type": "Limit",
            "price": self._exchange.price_to_precision(symbol=self._symbol, price=max_bid),
            "qty": self._exchange.amount_to_precision(symbol=self._symbol, amount=qty),
            "time_in_force": "GoodTillCancel",
            "reduce_only": reduce_only,
            "close_on_trigger": False,
            **kwargs
        })

    def execute_trade(self):
        # run trade (4 hour cycle: 1 -> 5 -> 9 -> 1 ...)
        iteration = 0
        move = 0  # -1: short, 1: long
        action = {0: 'long', 1: 'short', 2: 'hold'}

        high_leverage = False

        while True:
            self._send_tele_message(f"==== Trade Iteration {str(iteration)} ====")

            t0 = time.time()

            if high_leverage:
                self._send_tele_message("resetting leverage...")
                leverage = 1
                self._set_leverage(buy_leverage=leverage, sell_leverage=leverage)

            high_leverage = False
            ### make prediction ###
            df = self._get_df()
            df = self._create_timestamps(df)
            df = self._preprocess_data(df)
            x = df.values[-2].reshape((-1, df.shape[1]))
            pred = float(self._tn.predict(x).item())
            prob = np.max(self._tn.predict_proba(x))

            if prob > 0.9:
                high_leverage = True
                self._send_tele_message(
                    f"TabNet predicted class {action[int(pred)]} with probability {prob}. Resetting leverage to 5x.")
                leverage = 5
                self._set_leverage(buy_leverage=leverage, sell_leverage=leverage)
            elif prob <= 0.9:
                self._send_tele_message(
                    f"TabNet predicted class {action[int(pred)]} with probability {prob}. Using 1x leverage.")

            ### open position ###
            if pred == 1.0:
                ### short ###
                self._send_tele_message("Choosing Short Position!")
                if iteration >= 0:
                    if not self._position_exists():
                        self._send_tele_message("no positions open... stop loss or take profit was probably triggered.")
                    else:
                        if move == 1:
                            self._send_tele_message("Closing previous long position and opening short position...")
                            ### long was chosen, so we take short to close position ###
                            self._place_best_sell_limit_order(qty=qty, reduce_only=True)

                        elif move == -1:
                            self._send_tele_message("Closing previous short position and opening short position...")
                            ### short was chosen, so we take long to close position ###
                            self._place_best_buy_limit_order(qty=qty, reduce_only=True)

                    ### after closing the position, we need to recalculate quantity and cash status ###
                    max_bid, min_ask = self._get_best_bid_ask()
                    cur_price = (max_bid + min_ask) / 2

                    # get balance
                    balances = self._exchange.fetch_balance({"coin": "USDT"})["info"]
                    usdt = balances['result']['USDT']['available_balance']
                    self._send_tele_message("current cash status = " + str(usdt))

                    ### set stop loss and take profit ###
                    qty = self._exchange.amount_to_precision(symbol=self._symbol,
                                                             amount=float(usdt) / float(cur_price) * leverage)
                    stop_loss = self._exchange.price_to_precision(symbol=self._symbol,
                                                                  price=float(cur_price) * (
                                                                      1 - self.TAKE_PROFIT_PERCENT / 100))
                    take_profit = self._exchange.price_to_precision(symbol=self._symbol,
                                                                    price=float(cur_price) * (
                                                                        1 + self.STOP_LOSS_PERCENT / 100))

                    ### take short position as predicted ###
                    self._place_best_sell_limit_order(
                        qty=qty,
                        reduce_only=False,
                        stop_loss=take_profit,  # reversed for short
                        take_profit=stop_loss
                    )

                ### reset move only if first iteration ###
                if iteration == 0:
                    move = -1

            elif pred == 0.0:
                ### long ###
                self._send_tele_message("Choosing Long Position!")
                if iteration >= 0:
                    if not self._position_exists():
                        self._send_tele_message("no positions open... stop loss or take profit was probably triggered.")
                    else:
                        if move == -1:
                            self._send_tele_message("Closing previous short position and opening long position...")
                            ### short was chosen, so we take long to close position ###
                            self._place_best_buy_limit_order(qty=qty, reduce_only=True)

                        elif move == 1:
                            self._send_tele_message("Closing previous long position and opening long position...")
                            ### long was chosen, so we take short to close position ###
                            self._place_best_sell_limit_order(qty=qty, reduce_only=True)

                    ### after closing the position, we need to recalculate quantity and cash status ###
                    max_bid, min_ask = self._get_best_bid_ask()
                    cur_price = (max_bid + min_ask) / 2

                    # get balance
                    balances = self._exchange.fetch_balance({"coin": "USDT"})["info"]
                    usdt = balances['result']['USDT']['available_balance']
                    self._send_tele_message("current cash status = " + str(usdt))

                    ### set stop loss and take profit ###
                    qty = self._exchange.amount_to_precision(symbol=self._symbol,
                                                             amount=float(usdt) / float(cur_price) * leverage)
                    stop_loss = self._exchange.price_to_precision(symbol=self._symbol,
                                                                  price=float(cur_price) * (
                                                                      1 - self.STOP_LOSS_PERCENT / 100))
                    take_profit = self._exchange.price_to_precision(symbol=self._symbol,
                                                                    price=float(cur_price) * (
                                                                        1 + self.TAKE_PROFIT_PERCENT / 100))

                    ### take long position as predicted ###
                    self._place_best_buy_limit_order(
                        qty=qty,
                        reduce_only=False,
                        stop_loss=stop_loss,
                        take_profit=take_profit
                    )

                ### reset move only if first iteration ###
                if iteration == 0:
                    move = 1

            elif pred == 2.0:
                self._send_tele_message("not much volatility. Skipping this round")

            iteration += 1
            self._send_tele_message("waiting for the next 4 hours")
            elapsed = time.time() - t0
            time.sleep(60 * 60 * 4 - elapsed)

