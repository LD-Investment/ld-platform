from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from ld_platform.apps.bots.models import Bot

BOT_NAME_CHOICES = [x[0] for x in Bot.NameChoices]


class BotFactory(DjangoModelFactory):
    name = FuzzyChoice(BOT_NAME_CHOICES)

    class Meta:
        model = Bot
