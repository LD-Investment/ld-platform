import pytest
from django.test import RequestFactory

from ld_platform.bot_controls.api.views import BotControlViewSet
from ld_platform.bots.models import Bot

pytestmark = pytest.mark.django_db


class TestBotControlViewSet:
    def test_get_queryset(self, bot: Bot, rf: RequestFactory):
        view = BotControlViewSet()
        request = rf.get("/fake-url/")
        view.request = request
        pass
