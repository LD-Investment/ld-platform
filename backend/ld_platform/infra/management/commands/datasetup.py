from allauth.account.models import EmailAddress
from django.core import management
from django.core.management.base import BaseCommand
from django.utils import timezone

from ld_platform.apps.bots.models import Bot, SubscribedBot
from ld_platform.apps.users.models import User, UserExchangeSetting
from ld_platform.shared.choices import CryptoExchangeChoices

"""
Note that Custom Commands are only available in LOCAL environment.
See config/settings/local.py
"""


class Command(BaseCommand):
    help = "Command for initial data setup in devel environment"

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            action="store_true",
            help="Bypass input from command",
        )

    def handle(self, *args, **options):
        """Rest DB and migrate"""

        if options["noinput"]:
            management.call_command("flush", "--noinput")
        else:
            management.call_command("flush")
        management.call_command("migrate", "--noinput")

        """ User setup """
        super_user = User.objects.create_superuser(
            email="admin@ld-invest.com",
            username="admin",
            first_name="LD",
            last_name="Admin",
            password="333",
        )
        EmailAddress.objects.create(user=super_user, email="admin@ld-invest.com", verified=True)
        user1 = User.objects.create_user(
            email="chungjin93@gmail.com",
            username="chungjin93",
            first_name="David",
            last_name="Jeong",
            password="1234",
        )
        user2 = User.objects.create_user(
            email="lukekim@gmail.com",
            username="luke",
            first_name="Luke",
            last_name="Kim",
            password="1234",
        )
        user3 = User.objects.create_user(
            email="hanul@gmail.com",
            username="hanul",
            first_name="Hanul",
            last_name="Lee",
            password="1234",
        )
        self.stdout.write(self.style.SUCCESS("Successfully set up data for [User]"))

        """ User Exchange Setting setup """
        # For user1
        UserExchangeSetting.objects.create(
            exchange_name=CryptoExchangeChoices.BINANCE,
            user=user1,
            api_key="user1_api_key_example",
            api_secret="user1_api_secret_example",
        )
        UserExchangeSetting.objects.create(
            exchange_name=CryptoExchangeChoices.UPBIT,
            user=user1,
            api_key="user1_api_key_example",
            api_secret="user1_api_secret_example",
        )
        UserExchangeSetting.objects.create(
            exchange_name=CryptoExchangeChoices.UPBIT,
            user=user2,
            api_key="user2_api_key_example",
            api_secret="user2_api_secret_example",
        )
        UserExchangeSetting.objects.create(
            exchange_name=CryptoExchangeChoices.BINANCE,
            user=user3,
            api_key="user3_api_key_example",
            api_secret="user3_api_secret_example",
        )
        UserExchangeSetting.objects.create(
            exchange_name=CryptoExchangeChoices.UPBIT,
            user=user3,
            api_key="user3_api_key_example",
            api_secret="user3_api_secret_example",
        )
        self.stdout.write(
            self.style.SUCCESS("Successfully set up data for [UserExchangeSetting]")
        )

        """ Bot Setup """
        news_tracker_indi_bot = Bot.objects.create(
            name=Bot.NameChoices.NEWS_TRACKER,
            type=Bot.TypeChoices.INDICATOR,
            default_setting={"option1": 2.0, "option2": "test", "option3": "test2"},
        )
        self.stdout.write(self.style.SUCCESS("Successfully set up data for [Bot]"))

        """ SubscribedBot Setup """
        now = timezone.now()
        SubscribedBot.objects.create(
            user=user1,
            bot=news_tracker_indi_bot,
            status=SubscribedBot.StatusChoices.ACTIVE,
            run_type=SubscribedBot.RunTypeChoices.LIVE_RUN,
            user_bot_settings={"user_setting1": 1234, "user_setting2": "hihi"},
            subscribe_start_date=now,
            subscribe_end_date=now + timezone.timedelta(days=5),
        )
        SubscribedBot.objects.create(
            user=user2,
            bot=news_tracker_indi_bot,
            status=SubscribedBot.StatusChoices.INACTIVE,
            run_type=SubscribedBot.RunTypeChoices.SIMULATION,
            user_bot_settings={"user_setting1": 1234, "user_setting2": "hihi"},
            subscribe_start_date=now,
            subscribe_end_date=now + timezone.timedelta(days=5),
        )
        SubscribedBot.objects.create(
            user=user3,
            bot=news_tracker_indi_bot,
            status=SubscribedBot.StatusChoices.ACTIVE,
            run_type=SubscribedBot.RunTypeChoices.LIVE_RUN,
            user_bot_settings={"user_setting1": 1234, "user_setting2": "hihi"},
            subscribe_start_date=now,
            subscribe_end_date=now + timezone.timedelta(days=45),
        )
        self.stdout.write(
            self.style.SUCCESS("Successfully set up data for [SubscribedBot]")
        )
