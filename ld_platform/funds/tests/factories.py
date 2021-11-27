from factory import Faker
from factory.django import DjangoModelFactory

from ld_platform.funds.models import Fund


class FundFactory(DjangoModelFactory):
    name = Faker("fund_name")

    class Meta:
        model = Fund
