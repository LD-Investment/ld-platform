from django.db import models
from django.utils.translation import gettext_lazy as _

from ld_platform.apps.users.models import User

from .managers import IndicatorBotManager


class Bot(models.Model):
    class NameChoices(models.TextChoices):
        # Add field every time new bots are created
        NEWS_TRACKER = "news-tracker", _("News Tracker")

    class TypeChoices(models.TextChoices):
        AUTOMATED = "automated-bot", _("Automated Bot")
        MANUAL = "manual-bot", _("Manual Bot")
        INDICATOR = "indicator-bot", _("Indicator Bot")

    name = models.CharField(
        max_length=256, choices=NameChoices.choices, null=False, blank=False
    )
    type = models.CharField(
        max_length=256, choices=TypeChoices.choices, default=TypeChoices.AUTOMATED
    )
    default_setting = models.JSONField(null=True, blank=True, default=dict)

    class Meta:
        # Bot (Name, Type) should be unique
        unique_together = (
            "name",
            "type",
        )

    # Managers for each type of bots
    objects = models.Manager()
    indicator_bot_objects = IndicatorBotManager()


class SubscribedBot(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "active", _("Active")
        INACTIVE = "inactive", _("Inactive")

    class RunTypeChoices(models.TextChoices):
        BACK_TEST = "back-test", _("Back-testing Mode")
        SIMULATION = "simulation", _("Simulation Mode")
        DRY_RUN = "dry-run", _("Dry-run Mode")
        LIVE_RUN = "live-run", _("Live-run Mode")

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    bot = models.ForeignKey(Bot, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=256, choices=StatusChoices.choices, default=StatusChoices.INACTIVE
    )
    run_type = models.CharField(
        max_length=256, choices=RunTypeChoices.choices, default=RunTypeChoices.LIVE_RUN
    )
    user_bot_settings = models.JSONField(default=dict, null=True, blank=True)
    # TODO: for now, just leave it as null
    subscribe_start_date = models.DateTimeField(null=True, auto_now_add=True)
    subscribe_end_date = models.DateTimeField(null=True)
