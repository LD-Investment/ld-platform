from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _


class Fund(models.Model):
    name = CharField(_("Name of Fund"), blank=True, max_length=255)
