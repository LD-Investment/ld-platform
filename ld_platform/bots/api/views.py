import logging
from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
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


class BotControlCommandViewSet(viewsets.GenericViewSet):
    queryset = Bot.objects.all()
    serializer_class = BotControlCommandSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(responses={200: "success", 406: "invalid payload"})
    def command(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        # bot = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    "code": 406,
                    "detail": f"invalid payload: {request.data}",
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        # parse and execute command
        command = serializer.data["command"]
        if command == Bot.CommandChoices.START:
            # TODO(@jin)
            #  Bot instance should be initiated and saved into memory. Whenever user sends command, should
            #  be able to react in quick manner.
            print("hi")

        elif command == Bot.CommandChoices.STOP:
            # TODO(@jin)
            print("bye")

        return Response(
            data={
                "code": 200,
                "detail": "success",
            },
            status=status.HTTP_200_OK,
        )


class BotControlSettingViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = BotControlCommandSerializer

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pass

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pass
