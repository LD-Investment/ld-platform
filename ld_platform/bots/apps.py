from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BotsConfig(AppConfig):
    name = "ld_platform.bots"
    verbose_name = _("Bots")
