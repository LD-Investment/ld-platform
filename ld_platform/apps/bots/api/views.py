import logging
from typing import Any, Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ld_platform.apps.bots.models import Bot, SubscribedBot
from ld_platform.apps.users.models import UserExchangeSetting
from ld_platform.shared.resolvers import BotResolver, BotSettingResolver
from ld_platform.trading_bots.interface import IBot

from .serializers import (
    BotControlGeneralCommandSerializer,
    BotControlManualCommandSerializer,
    BotSerializer,
)

logger = logging.getLogger(__name__)

RUNNING_BOTS: Dict[int, IBot] = {}  # Dict(user_id, Bot instance)


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


class BotControlGeneralCommandViewSet(viewsets.GenericViewSet):
    queryset = SubscribedBot.objects.all()
    serializer_class = BotControlGeneralCommandSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        responses={
            200: "success",
            403: "Bot is active/inactive",
            406: "invalid payload",
        }
    )
    def command(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        subscribed_bot: SubscribedBot = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={"detail": f"invalid payload: {request.data}"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        # parse and execute command
        command = serializer.data["command"]
        if command == SubscribedBot.CommandChoices.START:
            # if bot active,
            if subscribed_bot.status == SubscribedBot.StatusChoices.ACTIVE:
                return Response(
                    data={"detail": "Cannot run bot that is active. Stop first."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            # if bot inactive, start
            # get bot instance
            user = subscribed_bot.user
            exchange_setting = UserExchangeSetting.objects.get(user=user)
            compiled_setting = BotSettingResolver.compile_setting(
                exchange_setting, subscribed_bot
            )
            bot = BotResolver.model_to_instance(subscribed_bot, compiled_setting)
            # initiate bot and save
            bot.run()
            # change status
            subscribed_bot.status = SubscribedBot.StatusChoices.ACTIVE
            subscribed_bot.save()

            # TODO: To handle a case where server needs to be restarted, storing
            #  running bots in memory as dict is dangerous. User bot will be gone and
            #  there is no way to handle them after server is up again. Data is just lost.
            #  Maybe we should use "pickle" to handle serialization/deserialization of bot objects.
            RUNNING_BOTS[user.id] = bot

        if command == SubscribedBot.CommandChoices.STOP:
            # if bot inactive,
            if subscribed_bot.status == SubscribedBot.StatusChoices.INACTIVE:
                return Response(
                    data={"detail": "Bot is already inactive. Cannot stop."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            # TODO: Get bot instance and stop
            # change status
            subscribed_bot.status = SubscribedBot.StatusChoices.INACTIVE
            subscribed_bot.save()

        return Response(status=status.HTTP_200_OK)

    def check_object_permissions(self, request: Request, obj: Any) -> None:
        """
        Object level permissions are run by REST framework's generic
        views when .get_object() is called
        """
        # TODO(1): check if user is owner of the bot
        # TODO(2): check if subscription is valid
        pass


class BotControlManualCommandViewSet(viewsets.GenericViewSet):
    queryset = SubscribedBot.objects.all()
    serializer_class = BotControlManualCommandSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        responses={
            200: "success",
        }
    )
    def command(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        # subscribed_manual_bot: Bot = self.get_object()
        return

    def get_object(self) -> Bot:
        # queryset = self.get_queryset()
        return
        # return queryset.filter(bot=)

    def check_object_permissions(self, request: Request, obj: Any) -> None:
        """
        Object level permissions are run by REST framework's generic
        views when .get_object() is called
        """
        # TODO(1): check if user is owner of the bot
        # TODO(2): check if subscription is valid
        # TODO(3): check if bot is manual bot


class BotControlSettingViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = SubscribedBot.objects.all()
    serializer_class = BotControlGeneralCommandSerializer

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pass

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pass
