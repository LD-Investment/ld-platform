from django.db import models
from django.utils.translation import gettext_lazy as _

from ld_platform.apps.users.models import User


class Bot(models.Model):
    class NameChoices(models.TextChoices):
        # Add field every time new bots are created
        TTADAK = "TTDK", _("Ttadak Bot")

    class TypeChoices(models.TextChoices):
        AUTOMATED = "AUTO", _("Automated Bot")
        MANUAL = "MANU", _("Manual Bot")
        INDICATOR = "INDI", _("Indicator Bot")

    name = models.CharField(
        max_length=4, choices=NameChoices.choices, null=False, blank=False
    )
    type = models.CharField(
        max_length=4, choices=TypeChoices.choices, default=TypeChoices.AUTOMATED
    )
    version = models.CharField(max_length=32, null=True, blank=True)
    default_setting = models.JSONField(null=True, blank=True, default=dict)

    class Meta:
        # Bot (Name, Type) should be unique
        unique_together = (
            "name",
            "type",
        )


class UserSubscribedBot(models.Model):
    class CommandChoices(models.TextChoices):
        START = "start", _("Start the bot")
        STOP = "stop", _("Stop the bot")

    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTV", _("Active")
        INACTIVE = "INAC", _("Inactive")

    class RunTypeChoices(models.TextChoices):
        BACK_TEST = "BACK", _("Back-testing Mode")
        SIMULATION = "SIML", _("Simulation Mode")
        DRY_RUN = "DRYR", _("Dry-run Mode")
        LIVE_RUN = "LIVR", _("Live-run Mode")

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    bot = models.ForeignKey(Bot, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=4, choices=StatusChoices.choices, default=StatusChoices.INACTIVE
    )
    run_type = models.CharField(
        max_length=4, choices=RunTypeChoices.choices, default=RunTypeChoices.LIVE_RUN
    )
    user_bot_settings = models.JSONField(default=dict)
    # TODO: for now, just leave it as null
    subscribe_start_date = models.DateTimeField(null=True)
    subscribe_end_date = models.DateTimeField(null=True)
