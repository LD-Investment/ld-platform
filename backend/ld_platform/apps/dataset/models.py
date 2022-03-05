from django.db import models
from django.utils.translation import gettext_lazy as _

from ld_platform.apps.dataset.managers import CoinnessNewsDataManager
from ld_platform.shared.choices import CryptoExchangeChoices


class CoinnessNewsData(models.Model):
    article_num = models.IntegerField(unique=True)
    date = models.DateTimeField(null=True)
    title = models.TextField(null=True, blank=True, default="")
    content = models.TextField(null=True, blank=True, default="")

    objects = CoinnessNewsDataManager()


class LongShortRatioData(models.Model):
    class BinanceSymbolChoices(models.TextChoices):
        # Binance
        BINANCE_BTC_USDT = "BTCUSDT", _("BTC/USDT")
        BINANCE_ETH_USDT = "ETHUSDT", _("ETH/USDT")
        BINANCE_XRP_USDT = "XRPUSDT", _("XRP/USDT")
        BINANCE_BCH_USDT = "BCHUSDT", _("BCH/USDT")

    class BybitSymbolChoices(models.TextChoices):
        # Bybit
        BYBIT_BTC_USD = "BTCUSD", _("BTC/USD")
        BYBIT_ETH_USD = "ETHUSD", _("ETH/USD")
        BYBIT_XRP_USD = "XRPUSD", _("XRP/USD")

    exchange_name = models.CharField(
        max_length=32, choices=CryptoExchangeChoices.choices, null=False, blank=False
    )
    symbol = models.CharField(
        max_length=32,
        choices=(BinanceSymbolChoices.choices + BybitSymbolChoices.choices),
        null=False,
        blank=False,
    )
    long_ratio = models.FloatField(null=False, blank=False)
    short_ratio = models.FloatField(null=False, blank=False)
    timestamp = models.IntegerField(null=False, blank=False)  # epoch, 10 digits
