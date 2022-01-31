import pytest

from ld_platform.apps.bots.models import Bot
from ld_platform.apps.bots.tests.factories import BotFactory
from ld_platform.apps.users.models import User
from ld_platform.apps.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def bot() -> Bot:
    return BotFactory()
