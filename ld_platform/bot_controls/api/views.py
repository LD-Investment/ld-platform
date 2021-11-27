from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from ld_platform.bots.models import Bot

from .serializers import BotControlSerializer


class BotControlViewSet(
    RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet
):
    serializer_class = BotControlSerializer
    queryset = Bot.objects.all()

    def get_queryset(self, *args, **kwargs):
        # TODO
        return
