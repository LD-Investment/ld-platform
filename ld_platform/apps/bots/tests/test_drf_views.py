import pytest
from django.test import RequestFactory

from ld_platform.apps.bots.api.views import BotViewSet
from ld_platform.apps.bots.models import Bot

pytestmark = pytest.mark.django_db


class TestBotViewSet:
    def test_get_queryset(self, bot: Bot, rf: RequestFactory):
        view = BotViewSet()
        request = rf.get("/fake-url/")
        view.request = request
        pass
