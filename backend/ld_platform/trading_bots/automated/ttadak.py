import logging

from ld_platform.apps.bots.models import Bot
from ld_platform.trading_bots.interface import IBot

logger = logging.getLogger(__name__)


class TtadakBot(IBot):
    NAME = Bot.NameChoices.TTADAK
    TYPE = Bot.TypeChoices.AUTOMATED

    def __init__(self, setting):
        super(TtadakBot, self).__init__(setting, logger)

    def run(self):
        pass

    def stop(self):
        pass

    def _change_setting(self):
        pass
