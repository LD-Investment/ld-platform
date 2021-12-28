from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from ld_platform.shared.choices import CryptoExchangeChoices

from .managers import UserManager


class User(AbstractUser):
    """Default user for L&D Investment Platform."""

    #: First and last name do not cover name patterns around the globe
    email = models.EmailField(unique=True)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    objects = UserManager()

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("api:users:user-detail", kwargs={"user_id": self.id})


class UserExchangeSetting(models.Model):
    exchange_name = models.CharField(
        max_length=32, choices=CryptoExchangeChoices.choices, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # TODO: Encrypt below fields. Consider using something like this.
    #   https://pypi.org/project/django-encrypted-model-fields/
    api_key = models.TextField(blank=False)
    api_secret = models.TextField(blank=False)
