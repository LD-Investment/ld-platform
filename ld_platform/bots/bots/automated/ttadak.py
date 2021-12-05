from ld_platform.bots.bots.base import BaseBot
from ld_platform.bots.models import Bot


class TtadakBot(BaseBot):
    NAME = "TTADAK"
    TYPE = Bot.TypeChoices.AUTOMATED

    def __init__(self, setting):
        super(TtadakBot, self).__init__(setting=setting)

    def run(self):
        pass

    def stop(self):
        pass

    def _change_setting(self):
        pass
