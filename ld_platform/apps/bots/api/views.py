import logging
from typing import Any, Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ld_platform.apps.bots.models import Bot, SubscribedBot
from ld_platform.apps.users.models import UserExchangeSetting
from ld_platform.shared.resolvers import BotResolver, BotSettingResolver
from ld_platform.trading_bots.interface import IBot

from .permissions import IsManualBot, IsSubscriptionValid, IsUserBotOwner
from .serializers import (
    BotControlGeneralCommandSerializer,
    BotControlManualCommandSerializer,
    BotSerializer,
)

logger = logging.getLogger(__name__)

# Stores Bot instance
# TODO: This should be restored back when server is restarted
#  by fetching active bots and resolving them as bot object again.
_user_id = int
_subscribed_bot_id = int
RUNNING_BOTS: Dict[_user_id, Dict[_subscribed_bot_id, IBot]] = {}


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
    permission_classes = [IsUserBotOwner & IsSubscriptionValid]

    @swagger_auto_schema(
        responses={
            200: "success",
            400: "bot is active/inactive",
            403: "permission denied",
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
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # if bot inactive, start
            user = subscribed_bot.user
            exchange_setting = UserExchangeSetting.objects.get(user=user)
            compiled_setting = BotSettingResolver.compile_setting(
                exchange_setting, subscribed_bot
            )
            bot: IBot = BotResolver.model_to_instance(subscribed_bot, compiled_setting)
            # initiate bot and save instance
            bot.run()
            RUNNING_BOTS[user.id] = {subscribed_bot.id: bot}
            # change status
            subscribed_bot.status = SubscribedBot.StatusChoices.ACTIVE
            subscribed_bot.save()

        if command == SubscribedBot.CommandChoices.STOP:
            # if bot inactive,
            if subscribed_bot.status == SubscribedBot.StatusChoices.INACTIVE:
                return Response(
                    data={"detail": "Bot is already inactive. Cannot stop."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # get bot instance and stop
            # delete instance
            bot: IBot = RUNNING_BOTS[request.user.id][subscribed_bot.id]
            bot.stop()
            del RUNNING_BOTS[request.user.id][subscribed_bot.id]
            # change status
            subscribed_bot.status = SubscribedBot.StatusChoices.INACTIVE
            subscribed_bot.save()

        return Response(status=status.HTTP_200_OK)


class BotControlManualCommandViewSet(viewsets.GenericViewSet):
    queryset = SubscribedBot.objects.all()
    serializer_class = BotControlManualCommandSerializer
    permission_classes = [IsUserBotOwner & IsSubscriptionValid & IsManualBot]

    @swagger_auto_schema(
        responses={
            200: "success",
        }
    )
    def command(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        # subscribed_bot: SubscribedBot = self.get_object()
        return

    def check_object_permissions(self, request: Request, obj: Any) -> None:
        """
        Object level permissions are run by REST framework's generic
        views when .get_object() is called
        """
        if obj.bot.type != Bot.TypeChoices.MANUAL:
            pass


class BotControlSettingViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = SubscribedBot.objects.all()
    serializer_class = BotControlGeneralCommandSerializer

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pass

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pass
