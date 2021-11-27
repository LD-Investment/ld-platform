from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FundsConfig(AppConfig):
    name = "ld_platform.funds"
    verbose_name = _("Funds")
