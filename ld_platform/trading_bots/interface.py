import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ld_platform.apps.bots.models import Bot
from ld_platform.mixins.logging_mixins import LoggingMixin
from ld_platform.shared.resolvers import CompiledBotSetting


@dataclass
class IBotDefaultSetting:
    """
    Interface for Bot Default Setting.
    Method that converts to dictionary is a must-have.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @abstractmethod
    def to_dict(self):
        return self.__dict__


class IBot(ABC, LoggingMixin):
    """
    Interface for Bots. Any bots, regardless of its type (automated, manual,
    indicator) should inherit this class and implement abstract methods.
    """

    NAME: str
    TYPE: Bot.TypeChoices
    DEFAULT_SETTING: IBotDefaultSetting

    def __init__(self, bot_setting: CompiledBotSetting, logger: logging.Logger):
        self._bot_setting = bot_setting
        LoggingMixin.__init__(self, logger)

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def _change_setting(self, new_setting):
        pass
