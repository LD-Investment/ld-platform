from django.db import models
from django.utils.translation import gettext_lazy as _


class CryptoExchangeChoices(models.TextChoices):
    BINANCE = "binance", _("Binance")
    UPBIT = "upbit", _("Upbit")


class BotCommandsChoices:
    class General(models.TextChoices):
        """
        Commands that apply to All Bots,
        regardless of its type (automated, manual, indicator)
        """

        START = "start", _("Start the bot")
        STOP = "stop", _("Stop the bot")

    class Automated(models.TextChoices):
        """
        Commands that specifically apply to Automated Bots.
        """

        pass

    class Manual(models.TextChoices):
        """
        Commands that specifically apply to Manual Bots.
        """

        # TODO: Currently, Ttadak bot is the only manual bot.
        #  If there comes more manual bot, we need to divide commands
        #  for each bots.
        # Ttadak Bot (Manual) specific commands
        BUY_GAME = "buy_game", _("Buy game")
        SELL_GAME = "sell_game", _("Sell game")

    class Indicator(models.TextChoices):
        """
        Commands that specifically apply to Indicator Bots.
        """
