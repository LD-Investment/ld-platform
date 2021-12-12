import asyncio
import dataclasses
import logging
from asyncio.events import AbstractEventLoop
from enum import Enum
from typing import Any, Dict

import aio_pika
import ccxtpro
from ccxt.base.errors import ExchangeError  # pylint: disable=no-name-in-module
from ccxtpro.base.order_book import OrderBook

from ld_platform.apps.bots.models import Bot
from ld_platform.shared.resolvers import CompiledBotSetting
from ld_platform.trading_bots.interface import IBot, IBotDefaultSetting

# Margin TTadak bot

logger = logging.getLogger(__name__)


class TtadakBot(IBot):
    """
    TtadakBot is margin-based high-frequency scalping bot that creates two opposite
    order at the same time. (long, short) or (short, long). For more info about bot
    mechanism, please refer the documentation.

    To use Binance USD Future M API,
    # You should pick the following:
         1. which API you want to trade (fapi)
         2. which specific margin mode you want (CROSSED or ISOLATED)
         3. which specific position mode you want (Hedged or One-way)

    # For this bot, we will use ISOLATED / HEDGE mode
    """

    NAME = Bot.NameChoices.TTADAK
    TYPE = Bot.TypeChoices.MANUAL
    DEFAULT_SETTING = IBotDefaultSetting(
        symbol="BTC/USDT",  # BTC/USDT, XRP/USDT ...
        leverage_level=100,  # x20, x50, x125 ...
        target_profit_per_game=1,  # target profit in percent per each game.
        asset_amount_per_game=1,  # Target trade amount per game. (min amount is different per symbol)
        stop_loss_rate=30,  # Stop Loss CallbackRate(%).
    )
    MARGIN_TYPE = "ISOLATED"
    DUAL_SIDE_POSITION = False  # True: hedge, False: one-way

    def __init__(self, bot_setting: CompiledBotSetting):
        super(TtadakBot, self).__init__(bot_setting, logger)
        self._bot_setting = bot_setting
        self.exchange = ccxtpro.binance(
            {
                "apiKey": self._bot_setting.exchange_api_key,
                "secret": self._bot_setting.exchange_api_secret,
                "enableRateLimit": True,
                "options": {
                    "defaultType": "future",
                },
            }
        )

    def run(self):
        # validate exchange setting
        pass

    def stop(self):
        pass

    def buy_game(self):
        print("Buy Game triggered!")

    def sell_game(self):
        print("Sell Game triggered!")

    def _change_setting(self, new_setting):
        self._setting = new_setting
        pass


"""
Archived TtadakBot (Telegram MVP)
"""


class State(Enum):
    """
    Bot application states
    """

    RUNNING = 1
    STOPPED = 2
    RELOAD_CONFIG = 3

    def __str__(self):
        return f"{self.name.lower()}"


class GameType(Enum):
    """Game Position Type.
    BUY: Long -> Short
    SELL: Short -> Long
    """

    BUY = "buy"  # long
    SELL = "sell"  # short


class RmqExchangeName(Enum):
    """RabbitMQ Exchange Name"""

    TTADAK_BOT = "ldbot.ttadak"


class RmqQueueName(Enum):
    """RabbitMQ Queue Name (= routing key)"""

    # Data Collector
    TELEGRAM_BOT_COMMAND = "ttadak.telegram_bot_command"


@dataclasses.dataclass
class BotSetting:
    API_KEY = "api_key"
    SECRET = "secret"
    SYMBOL = "symbol"
    LEVERAGE_LEVEL = "leverage_level"
    TARGET_PROFIT_PER_G = "target_profit_per_game"
    TRADE_AMT_PER_G = "trade_amount_per_game"
    STOP_LOSS_RATE = "stop_loss_rate"

    @property
    def confidential_keys(self) -> list:
        return [
            self.API_KEY,
            self.SECRET,
        ]

    @property
    def config_keys(self) -> list:
        return [
            self.SYMBOL,
            self.LEVERAGE_LEVEL,
            self.TARGET_PROFIT_PER_G,
            self.TRADE_AMT_PER_G,
            self.STOP_LOSS_RATE,
        ]

    def translate(self, key: str) -> str:
        return {
            self.SYMBOL: "거래코인",
            self.LEVERAGE_LEVEL: "레버리지 레벨",
            self.TARGET_PROFIT_PER_G: "게임당 목표수익률",
            self.TRADE_AMT_PER_G: "게임당 주문 수량(BTC)",
            self.STOP_LOSS_RATE: "스탑로스 rate(%)",
        }[key]


LOG_FORMAT = (
    "%(levelname) -5s %(process) -7s %(asctime) -20s %(name) -35s %(funcName) "
    "-10s %(lineno) -5d: %(message)s"
)


class TtaDakException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message

    def __json__(self):
        return {"msg": self.message}


class _ArchivedTTadakBot:
    MARGIN_TYPE = "ISOLATED"
    DUAL_SIDE_POSITION = False  # True: hedge, False: one-way

    def __init__(
        self,
        bn_apikey: str,
        bn_secret: str,
        symbol: str,
        leverage_level: int,
        target_profit_per_game: float,
        trade_amount_per_game: float,
        stop_loss_rate: float,
        rmq_host: str,
        rmq_queue_name: str,
        debug: bool = False,
    ):
        """
        TtaDak Bot Class.

        :param bn_apikey: Binance API key
        :param bn_secret: Binance API secret
        :param symbol: BTC/USDT, XRP/USDT ...
        :param leverage_level: x20, x50, x125 ...
        :param target_profit_per_game: Target profit in percent per Ttadak Trade.
            If you enter long position at X price, then sell position will be
            X * (1 + profit_percent / 100 / leverage_level).
        :param trade_amount_per_game: float: Target trade amount per game. Default Unit is BTC but it
            depends on the symbol.
        :param stop_loss_rate: float: Stop Loss CallbackRate(%).
        :param rmq_host: RabbitMQ server host.
        :param rmq_queue_name: RabbitMQ Queue name (or routing key) from which to consume.
        """
        # bot state(TODO: should be inherited from BaseBotClass)
        self.state = State.STOPPED

        # user setting
        self._apikey = bn_apikey
        self._secret = bn_secret
        # configurable setting
        self.symbol = symbol
        self.maker_fee_bp = None
        self.leverage_level = leverage_level
        self.target_profit_per_game = (
            target_profit_per_game  # target profit per ttadak trade
        )
        self.target_profit_per_game_bp = target_profit_per_game / 100
        self.trade_amount_per_game = trade_amount_per_game
        self.stop_loss_rate = stop_loss_rate  # in percent

        # bot setting
        self._loop: AbstractEventLoop or None = None
        self.market = None
        self.exchange = None

        # rabbitMQ setting
        self.rmq_host = rmq_host
        self.rmq_queue_name = rmq_queue_name

        # logging setting
        level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=level, format=LOG_FORMAT)

        # initialize settings
        self._loop = asyncio.get_event_loop()
        self._loop.run_until_complete(self._initialize())

    def run(self) -> None:
        logger.info("Starting bot!!")
        self._loop.run_until_complete(self._trade_loop(self._loop))

    def stop(self) -> None:
        logger.info("Stopping bot!!")
        if self._loop:
            self._loop.close()

    async def _initialize(self) -> None:
        self.exchange = ccxtpro.binance(
            {
                "apiKey": self._apikey,
                "secret": self._secret,
                "enableRateLimit": True,
                "options": {
                    "defaultType": "future",
                },
            }
        )
        # load binance market infos
        await self.exchange.load_markets()
        self.market = self.exchange.market(self.symbol)
        self.maker_fee_bp = self.market["maker"]

        # set margin/position mode
        await self._adjust_margin_mode()
        await self._adjust_position_mode()
        await self._adjust_leverage_level()

    async def _trade_loop(self, loop: AbstractEventLoop) -> None:
        # create RabbitMQ async connection
        _conn = await aio_pika.connect_robust(self.rmq_host, loop=loop)

        async with _conn:
            # Creating channel
            channel = await _conn.channel()
            # Declaring queue
            queue = await channel.declare_queue(self.rmq_queue_name, auto_delete=True)

            # async loop over messages
            async with queue.iterator() as queue_iter:
                # Cancel consuming after __aexit__
                async for message in queue_iter:
                    async with message.process():
                        logger.info("Received command from telegram bot!")
                        game_type = message.body.decode()
                        logger.info(f"Received game_type: {game_type}")

                        if game_type not in ["buy", "sell"]:
                            break

                    # execute trade
                    gt = GameType.BUY if game_type == "buy" else GameType.SELL
                    # NOTE: enable below if want to test
                    # await self._fake_trade(gt)
                    await self._execute_trade(gt)

    @staticmethod
    async def _fake_trade(game_type: GameType):
        # some IO job
        logger.info(f"Fake Call: {game_type}")
        await asyncio.sleep(1)

    async def _execute_trade(self, game_type: GameType):
        try:
            # fetch orderbook
            logger.info("Executing trade.")
            ob: OrderBook = await self.exchange.watch_order_book(self.symbol, limit=5)
            logger.info("Successfully got Orderbook info. Now entering position.")

            # create order
            await self._enter_position(game_type=game_type, orderbook=ob)
            logger.info(f"Successfully entered position. Game type({game_type})")

        except Exception as e:
            logger.error(f"Error occurred while executing trade. {e}")

    async def _enter_position(
        self, game_type: "GameType", orderbook: OrderBook
    ) -> None:
        """
        :param game_type: PositionType.BUY or PositionType.SELL
        :param orderbook: Orderbook data fetched from Binance exchange
        """
        # check min amount
        min_amount = self.market["limits"]["amount"]["min"]
        if self.trade_amount_per_game < min_amount:
            raise TtaDakException(f"Amount should be greater than {min_amount}!")

        logger.info(f"Received orderbook: {orderbook}")
        min_ask: list = orderbook["asks"][1]  # index1 to avoid Taker fee
        max_bid: list = orderbook["bids"][1]  # index1 to avoid Taker fee

        # LONG position
        if game_type == GameType.BUY:
            buy_price = min_ask[0]
            sell_price = self._calculate_bep_price(
                game_type=game_type,
                P=buy_price,
                R=self.target_profit_per_game_bp,
                F=self.maker_fee_bp,
                L=self.leverage_level,
            )
            # place order is important
            await self._place_order(
                side="buy",
                price=buy_price,
                amount=self.trade_amount_per_game,
                params={"callbackRate": self.stop_loss_rate},
            )
            await self._place_order(
                side="sell", price=sell_price, amount=self.trade_amount_per_game
            )

        # SHORT position
        elif game_type == GameType.SELL:
            sell_price = max_bid[0]
            buy_price = self._calculate_bep_price(
                game_type=game_type,
                P=sell_price,
                R=self.target_profit_per_game_bp,
                F=self.maker_fee_bp,
                L=self.leverage_level,
            )
            # place order is important
            await self._place_order(
                side="sell",
                price=sell_price,
                amount=self.trade_amount_per_game,
                params={"callbackRate": self.stop_loss_rate},
            )
            await self._place_order(
                side="buy", price=buy_price, amount=self.trade_amount_per_game
            )

        else:
            raise TtaDakException(f"Entered invalid position({game_type}).")

        logger.info(f"buy price: {buy_price}, amount: {self.trade_amount_per_game}")
        logger.info(f"sell price: {sell_price}, amount: {self.trade_amount_per_game}")
        logger.info("Entered ttadak position successfully.")

    async def _place_order(
        self, side: str, price: float, amount: float, params=None
    ) -> None:
        if params is None:
            params = {}
        order = await self.exchange.create_order(
            self.symbol, "limit", side, amount, price, params=params
        )
        logger.info(f"Placed order: {order}")

    async def _adjust_position_mode(self) -> None:
        logger.info("Adjusting your current position mode (One-way or Hedge Mode):")
        response = await self.exchange.fapiPrivate_get_positionside_dual()
        if response["dualSidePosition"]:
            logger.info("You are in Hedge Mode")
            # adjust mode
            response = await self.exchange.fapiPrivate_post_positionside_dual(
                {
                    "dualSidePosition": self.DUAL_SIDE_POSITION,
                }
            )
            logger.info(response)
            return
        logger.info("You are already in One-way Mode. No need to change.")

    async def _adjust_margin_mode(self) -> None:
        logger.info(
            f"Adjusting your {self.symbol} position margin mode to {self.MARGIN_TYPE}"
        )
        try:
            response = await self.exchange.fapiPrivate_post_margintype(
                {
                    "symbol": self.market["id"],
                    "marginType": self.MARGIN_TYPE,
                }
            )
            logger.info(response)
        except ExchangeError:
            logger.info(
                f"You are already in {self.MARGIN_TYPE} Mode. No need to change."
            )

    async def _adjust_leverage_level(self) -> None:
        logger.info(f"Changing your leverage level to x{self.leverage_level}")
        await self.exchange.fapiPrivate_post_leverage(
            {
                "symbol": self.market["id"],
                "leverage": self.leverage_level,
            }
        )

    async def _get_all_positions(self) -> None:
        logger.info("Getting your positions:")
        # response = await self.exchange.fapiPrivateV2_get_positionrisk()

    def _update_setting(self, new_config: Dict[str, Any]):
        self.symbol = new_config.get("symbol", default=self.symbol)
        self.leverage_level = new_config.get(
            "leverage_level", default=self.leverage_level
        )
        self.trade_amount_per_game = new_config.get(
            "trade_amount_per_game", default=self.trade_amount_per_game
        )
        self.target_profit_per_game = new_config.get(
            "target_profit_per_game", default=self.target_profit_per_game
        )

    @staticmethod
    def _calculate_bep_price(
        game_type: GameType, P: float, R: float, F: float, L: int
    ) -> float:
        """
        Calculator that considers final price of the exit(close) position
        considering Leverage level, fees and target return set by Ttadak bot user.
        The returned value should be used for placing actual order per Ttadak Game.
        :param P:
            Enter Price (진입 포지션 가격)
            if game_type==GameType.BUY, then it is price of long position
            if game_type==GameType.SELL, then it is price of short position
        :param R:
            Target return in bp
            R=0.02 means 2%
        :param F:
            Fee in bp
            F=0.0002 means fee is 0.02%
        :param L:
            Leverage level
            For Binance, 1 <= L <= 125
        :param game_type:
            Game type of TtadakBot
            If it is BUY game, trade will be [long -> short]
                : Price(long) < Price(short)
            If it is SELL game, trade will be [short -> long]
                : Price(long) > Price(short)
        :return: Close Price (청산 포지션 가격)
        """
        # We should get PC: close price (청산 포지션 가격)
        if game_type == GameType.BUY:
            # PC for BUY Game
            return (L * P * (1 + F) + P * R) / (L * (1 - F))

        if game_type == GameType.SELL:
            # PC for SELL Game
            return (L * P * (1 - F) - P * R) / (L * (1 + F))

        raise RuntimeError(f"Invalid game_type {game_type.name}")
