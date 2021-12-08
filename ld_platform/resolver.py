from dataclasses import dataclass

from ld_platform.apps.bots.models import Bot, SubscribedBot
from ld_platform.apps.users.models import UserExchangeSetting

#####################
# Setting Resolvers #
#####################


class BotSettingResolver:
    @staticmethod
    def compile_setting(
        user_exchange_setting: UserExchangeSetting,
        subscribed_bot: SubscribedBot,
    ):
        """
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
                from ld_platform.trading_bots.automated.ttadak import TtadakBot

                return TtadakBot(compiled_setting)
            else:
                raise RuntimeError(f"Failed to resolve bot_name({bot_name})")

        if bot_type == Bot.TypeChoices.MANUAL:
            if bot_name == Bot.NameChoices.TTADAK:
                from ld_platform.trading_bots.manual.ttadak import TtadakBot

                return TtadakBot(compiled_setting)
            else:
                raise RuntimeError(f"Failed to resolve bot_name({bot_name})")

        if bot_type == Bot.TypeChoices.INDICATOR:
            pass

        raise RuntimeError(f"Failed to resolve bot_type({bot_type})")
