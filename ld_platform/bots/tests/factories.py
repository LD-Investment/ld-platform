from factory import Faker
from factory.django import DjangoModelFactory

from ld_platform.bots.models import Bot


class BotFactory(DjangoModelFactory):
    name = Faker("bot_name")

    class Meta:
        model = Bot
