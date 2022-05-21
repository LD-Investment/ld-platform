from typing import List

from django.contrib.auth import get_user_model
from django.db import models

from ld_platform.ai.indicator.news_tracker import CryptoDeberta

User = get_user_model()
crypto_deberta = CryptoDeberta()


class IndicatorBotManager(models.Manager):
    @staticmethod
    def load_ai_models(bot) -> List[CryptoDeberta]:
        from ld_platform.apps.bots.models import Bot

        if bot.type != Bot.TypeChoices.INDICATOR:
            raise RuntimeError(f"Bot type should be {Bot.TypeChoices.INDICATOR}.")

        avail_models = []
        if bot.name == Bot.NameChoices.NEWS_TRACKER:
            # TODO: import from ld_platform.ai ... and return the Class object
            avail_models.append(crypto_deberta)
        return avail_models
