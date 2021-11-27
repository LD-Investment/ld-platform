from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BotControlsConfig(AppConfig):
    name = "ld_platform.bot_controls"
    verbose_name = _("Bot Controls")
