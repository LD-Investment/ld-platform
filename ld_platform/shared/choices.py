from django.db import models
from django.utils.translation import gettext_lazy as _


class CryptoExchangeChoices(models.TextChoices):
    BINANCE = "binance", _("Binance")
    UPBIT = "upbit", _("Upbit")
