from django.core import management
from django.core.management.base import BaseCommand

from ld_platform.apps.users.models import User, UserExchangeSetting
from ld_platform.shared.choices import CryptoExchangeChoices

"""
Note that Custom Commands are only available in LOCAL environment.
See config/settings/local.py
"""


class Command(BaseCommand):
    help = "Command for initial data setup in devel environment"

    def handle(self, *args, **options):
        """Rest DB and migrate"""
        management.call_command("reset_db", "--noinput")
        management.call_command("migrate", "--noinput")

        """ User setup """
        User.objects.create_superuser(
            email="admin@ld-invest.com",
            first_name="LD",
            last_name="Admin",
            password="333",
        )
        user1 = User.objects.create_user(
            email="chungjin93@gmail.com",
            first_name="David",
            last_name="Jeong",
            password="1234",
        )

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

        """ Bot Setup """

        # self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
