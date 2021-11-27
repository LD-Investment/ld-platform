from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _


class Bot(models.Model):
    name = CharField(_("Name of Bot"), blank=True, max_length=255)
