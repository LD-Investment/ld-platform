from django.db import models
from django.utils.translation import gettext_lazy as _

from ld_platform.funds.models import Fund


class Bot(models.Model):
    class NameChoices(models.TextChoices):
        # Add field every time new bots are created
        TTADAK = "TTDK", _("Ttadak Bot")

    class TypeChoices(models.TextChoices):
        AUTOMATED = "AUTO", _("Automated Bot")
        MANUAL = "MANU", _("Manual Bot")
        INDICATOR = "INDI", _("Indicator Bot")

    class CommandChoices(models.TextChoices):
        START = "start", _("Start the bot")
        STOP = "stop", _("Stop the bot")

    name = models.CharField(
        unique=True, max_length=4, choices=NameChoices.choices, null=False, blank=False
    )
    fund = models.ForeignKey(
        Fund,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    default_setting = models.JSONField(null=True, blank=True, default=dict)
    type = models.CharField(
        max_length=4, choices=TypeChoices.choices, default=TypeChoices.AUTOMATED
    )
    version = models.CharField(max_length=32, null=True, blank=True)
