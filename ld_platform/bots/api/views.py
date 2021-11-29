from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from ld_platform.bots.models import Bot

from .serializers import BotSerializer


class BotViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = BotSerializer
    queryset = Bot.objects.all()
    lookup_field = "bot_id"

    def get_queryset(self, *args, **kwargs):
        # TODO
        return
