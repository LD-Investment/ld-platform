import logging
from typing import Any

from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ld_platform.bots.models import Bot

from .serializers import BotControlCommandSerializer, BotSerializer

logger = logging.getLogger(__name__)


###############################
# Bot Administration ViewSets #
###############################


class BotViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = BotSerializer
    queryset = Bot.objects.all()
    lookup_field = "bot_id"

    def get_queryset(self, *args, **kwargs):
        # TODO
        return


########################
# Bot Control ViewSets #
########################


class BotControlCommandViewSet(GenericViewSet):
    serializer_class = BotControlCommandSerializer

    def command(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise PermissionError

        logger.info("data: ", serializer.data)
        logger.info("hihi")
        return Response(data="success", status=status.HTTP_200_OK)


class BotControlSettingViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    def get_setting(self):
        pass

    def update_setting(self):
        pass
