import logging
from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ld_platform.apps.bots.models import Bot, SubscribedBot
from ld_platform.apps.users.models import UserExchangeSetting
from ld_platform.resolver import BotResolver, BotSettingResolver

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
    queryset = SubscribedBot.objects.all()
    serializer_class = BotControlCommandSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(responses={200: "success", 406: "invalid payload"})
    def command(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        subscribed_bot: SubscribedBot = self.get_object()
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
        if command == SubscribedBot.CommandChoices.START:
            # resolve settings and bot instance
            exchange_setting = UserExchangeSetting.objects.get(user=subscribed_bot.user)
            compiled_setting = BotSettingResolver.compile_setting(
                exchange_setting, subscribed_bot
            )
            bot = BotResolver.model_to_instance(subscribed_bot, compiled_setting)
            print(bot)

        if command == SubscribedBot.CommandChoices.STOP:
            pass

        return Response(
            data={
                "code": 200,
                "detail": "success",
            },
            status=status.HTTP_200_OK,
        )

    def check_object_permissions(self, request: Request, obj: Any) -> None:
        """
        Object level permissions are run by REST framework's generic
        views when .get_object() is called
        """
        # TODO(1): check if user is owner of the bot
        # TODO(2): check if subscription is valid
        pass


class BotControlSettingViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = SubscribedBot.objects.all()
    serializer_class = BotControlCommandSerializer

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pass

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pass
