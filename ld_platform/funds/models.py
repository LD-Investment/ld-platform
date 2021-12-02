from django.db import models
from django.utils.translation import gettext_lazy as _


class Fund(models.Model):
    name = models.CharField(_("Name of Fund"), blank=False, max_length=255)
    is_private = models.BooleanField(default=False)
