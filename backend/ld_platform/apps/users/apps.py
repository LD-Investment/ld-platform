from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "ld_platform.apps.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import ld_platform.apps.users.signals  # noqa F401
        except ImportError:
            pass
