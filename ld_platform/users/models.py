from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ld_platform.bots.models import Bot
from ld_platform.funds.models import Fund


class User(AbstractUser):
    """Default user for L&D Investment Platform."""

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("api:users:user-detail", kwargs={"user_id": self.id})


class UserExchangeSetting(models.Model):
    name = models.CharField(blank=False, max_length=255)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # TODO: Encrypt below fields. Consider using something like this.
    #   https://pypi.org/project/django-encrypted-model-fields/
    api_key = models.TextField(blank=False)
    api_secret = models.TextField(blank=False)


class Subscription(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)


class UserSubscription(models.Model):
    class StatusChoices(models.TextChoices):
        INACTIVE = "INAC", _("Inactive")
        ACTIVE = "ACTV", _("Active")
        PAUSED = "PAUS", _("Paused")
        TERMINATED = "TERM", _("Terminated")

    class RunTypeChoices(models.TextChoices):
        BACK_TEST = "BACK", _("Back-testing Mode")
        SIMULATION = "SIML", _("Simulation Mode")
        DRY_RUN = "DRYR", _("Dry-run Mode")
        LIVE_RUN = "LIVR", _("Live-run Mode")

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=4, choices=StatusChoices.choices, default=StatusChoices.INACTIVE
    )
    run_type = models.CharField(
        max_length=4, choices=RunTypeChoices.choices, default=RunTypeChoices.LIVE_RUN
    )
    settings = models.JSONField(default=dict)
    # TODO: for now, just leave it as null
    subscribe_start_date = models.DateTimeField(null=True)
    subscribe_end_date = models.DateTimeField(null=True)
