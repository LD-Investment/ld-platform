from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


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
