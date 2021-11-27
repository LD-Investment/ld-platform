import pytest
from django.test import RequestFactory

from ld_platform.funds.api.views import FundViewSet
from ld_platform.funds.models import Fund

pytestmark = pytest.mark.django_db


class TestFundViewSet:
    def test_get_queryset(self, fund: Fund, rf: RequestFactory):
        view = FundViewSet()
        request = rf.get("/fake-url/")
        view.request = request
        pass
