from django.db import models
from django.utils.translation import gettext_lazy as _

from ld_platform.funds.models import Fund


class Bot(models.Model):
    class TypeChoices(models.TextChoices):
        AUTOMATED = "AUTO", _("Automated Bot")
        MANUAL = "MANU", _("Manual Bot")
        INDICATOR = "INDI", _("Indicator Bot")

    name = models.CharField(_("Name of Bot"), blank=True, max_length=255)
    fund = models.ForeignKey(
        Fund,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    default_setting = models.JSONField(null=False, blank=False, default=dict)
    type = models.CharField(
        max_length=4, choices=TypeChoices.choices, default=TypeChoices.AUTOMATED
    )
    version = models.CharField(max_length=32, null=True, blank=True)
