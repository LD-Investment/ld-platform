import logging

from ld_platform.apps.bots.models import Bot
from ld_platform.trading_bots.interface import IBot

logger = logging.getLogger(__name__)


class TtadakBot(IBot):
    NAME = Bot.NameChoices.TTADAK
    TYPE = Bot.TypeChoices.MANUAL

    def __init__(self, bot_setting):
        super(TtadakBot, self).__init__(bot_setting, logger)

    def run(self):
        # validate exchange setting
        pass

    def stop(self):
        pass

    def _change_setting(self, new_setting):
        self._setting = new_setting
        pass
