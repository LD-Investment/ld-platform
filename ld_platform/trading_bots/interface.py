"""
Flow:

1. User가 UI에서 본인이 subscribe 된 정보를 클릭
  * 해당 Subscription 내 Bot list를 보고 특정 bot control 클릭
  * 토큰이 발급된다.

2. 선택한 bot을 start한다 (토큰 인증).
  * bot_id를 통해 Bot 정보를 SQL에서 받아서
  * name을 통해 실제 Bot instance를 resolve한다.
  * 유저가 설정한 setting 확인한다
  * 유저가 설정한 bot setting을 통해 bot을 initiate한다.
    * 여기서 부터는 각 Bot의 플로우대로
"""
import logging
from abc import ABC, abstractmethod

from ld_platform.apps.bots.models import Bot
from ld_platform.apps.users.models import UserExchangeSetting
from ld_platform.mixins.logging_mixins import LoggingMixin


class IBot(ABC, LoggingMixin):
    """
    필요기능:
      * 유저의 CCXT Exchange 인스턴스 stop 때까지 연결 지속
      * dynamic setting 설정
      *

    """

    NAME: str
    TYPE: Bot.TypeChoices

    def __init__(self, setting: UserExchangeSetting, logger: logging.Logger):
        self._setting = setting
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
