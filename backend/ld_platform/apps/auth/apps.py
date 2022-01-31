from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthConfig(AppConfig):
    name = "ld_platform.apps.auth"
    verbose_name = _("Authentication")
