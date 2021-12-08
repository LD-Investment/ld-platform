import logging

from ld_platform.bots.bots.base import BaseBot
from ld_platform.bots.models import Bot

logger = logging.getLogger(__name__)


class TtadakBot(BaseBot):
    NAME = "TTADAK"
    TYPE = Bot.TypeChoices.MANUAL

    def __init__(self, setting):
        super(TtadakBot, self).__init__(setting, logger)

    def run(self):
        # validate exchange setting
        pass

    def stop(self):
        pass

    def _change_setting(self, new_setting):
        self._setting = new_setting
        pass
