from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from ld_platform.funds.models import Fund

from .serializers import FundSerializer


class FundViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = FundSerializer
    queryset = Fund.objects.all()
    lookup_field = "fund_id"

    def get_queryset(self, *args, **kwargs):
        # TODO
        return
