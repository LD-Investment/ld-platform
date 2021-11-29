from factory import Faker
from factory.django import DjangoModelFactory

from ld_platform.bots.models import Bot


class BotFactory(DjangoModelFactory):
    name = Faker("sentence", nb_words=4)

    class Meta:
        model = Bot
