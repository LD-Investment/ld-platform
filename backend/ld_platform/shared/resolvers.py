from dataclasses import dataclass
from typing import Any, Callable

from ld_platform.apps.bots.models import Bot, SubscribedBot
from ld_platform.apps.users.models import UserExchangeSetting

#####################
# Setting Resolvers #
#####################


class BotSettingResolver:
    """
    BotSettingResolver comprises of methods that are needed for
    handling different settings needed in various bots.

    Since there are many types of bots, each having different structure
    of setting, this resolver can act as an interface for sustaining and
    conversion of settings.
    """

    @staticmethod
    def compile_setting(
        user_exchange_setting: UserExchangeSetting,
        subscribed_bot: SubscribedBot,
    ):
        """
        Compile UserExchangeSetting and Bot specific setting so that
        Bot instance can make use of.

        Args:
            subscribed_bot: UserExchangeSetting django model instance.
            user_exchange_setting: UserSubscribedBot django model instance.
        """
        return CompiledBotSetting(user_exchange_setting, subscribed_bot)


@dataclass
class CompiledBotSetting:
    """
    Accepts 'UserExchangeSetting' and 'UserSubscribedBot' models
    and combines them into one compiled setting for 'Bot' to run.

    >>> from ld_platform.trading_bots.manual.ttadak import TtadakBot
    >>>
    >>> setting = CompiledBotSetting(...)
    >>> TtadakBot(setting=setting)
    """

    exchange_name: str
    exchange_api_key: str
    exchange_api_secret: str
    bot_run_type: str
    user_bot_setting: dict

    def __init__(
        self,
        user_exchange_setting: UserExchangeSetting,
        subscribed_bot: SubscribedBot,
    ):
        # Exchange specific info
        self.exchange_name = user_exchange_setting.exchange_name
        self.exchange_api_key = user_exchange_setting.api_key
        self.exchange_api_secret = user_exchange_setting.api_secret
        # Bot specific info
        self.bot_run_type = subscribed_bot.run_type
        self.user_bot_setting = subscribed_bot.user_bot_settings


#########################
# Trading Bot Resolvers #
#########################


class BotResolver:
    @staticmethod
    def model_to_instance(
        subscribed_bot: SubscribedBot, compiled_setting: CompiledBotSetting
    ):
        """
        Resolver that returns Trading bot instance by
        accepting 'UserSubscribedBot' model's attributes.

        Args:
            subscribed_bot: UserSubscribedBot django model.
            compiled_setting: Compiled setting resolved from BotSettingResolver.compile_setting(..)

        Return:
            IBot inherited instance
        """
        bot_name = subscribed_bot.bot.name
        bot_type = subscribed_bot.bot.type

        if bot_type == Bot.TypeChoices.AUTOMATED:
            if bot_name == Bot.NameChoices.TTADAK:
                from ld_platform.ai.automated.ttadak import TtadakBot

                return TtadakBot(compiled_setting)
            else:
                raise RuntimeError(f"Failed to resolve bot_name({bot_name})")

        if bot_type == Bot.TypeChoices.MANUAL:
            if bot_name == Bot.NameChoices.TTADAK:
                from ld_platform.ai.manual.ttadak import TtadakBot

                return TtadakBot(compiled_setting)
            else:
                raise RuntimeError(f"Failed to resolve bot_name({bot_name})")

        if bot_type == Bot.TypeChoices.INDICATOR:
            pass

        raise RuntimeError(f"Failed to resolve bot_type({bot_type})")

    @staticmethod
    def command_to_method(command: str, bot_obj: Any) -> Callable:
        """
        Resolves commands from client to bot methods.
        """
        if hasattr(bot_obj, command):
            return getattr(bot_obj, command)
        raise RuntimeError(
            f"Failed to resolve command(={command}) to bot(={bot_obj})'s methods"
        )
