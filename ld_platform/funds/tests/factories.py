from factory import Faker
from factory.django import DjangoModelFactory

from ld_platform.funds.models import Fund


class FundFactory(DjangoModelFactory):
    name = Faker("sentence", nb_words=4)

    class Meta:
        model = Fund
