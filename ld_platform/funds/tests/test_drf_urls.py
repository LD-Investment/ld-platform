import pytest

from ld_platform.funds.models import Fund

pytestmark = pytest.mark.django_db


def test_fund_detail(fund: Fund):
    pass


def test_fund_list():
    pass
