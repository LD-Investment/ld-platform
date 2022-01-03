import logging
from typing import Any, Dict

from django.db.utils import ProgrammingError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ld_platform.apps.bots.models import Bot, SubscribedBot
from ld_platform.apps.users.models import UserExchangeSetting
from ld_platform.shared.choices import BotCommandsChoices
from ld_platform.shared.resolvers import BotResolver, BotSettingResolver
from ld_platform.trading_bots.interface import IBot

from .permissions import IsBotActive, IsManualBot, IsSubscriptionValid, IsUserBotOwner
from .serializers import (
    BotControlGeneralCommandSerializer,
    BotControlManualCommandSerializer,
    BotDefaultSettingSerializer,
    BotSerializer,
)

logger = logging.getLogger(__name__)

T_USER_ID = int
T_SUBSCRIBED_BOT_ID = int


# FIXME
#  ** WARNING **
#  Since django is multi-process level web server, not multi-threaded in production
#  level, below instance will be not shared per views, meaning no matter how you
#  design in code-level (like singleton), you will not achieve what you want.
#  Django is not Java where there is shared singleton bean injector.
#  -
#  ** PLEASE CONSIDER **
#  1) Make an external single-processed asynchronous server that runs in different port.
#  Use that server as a single place for holding actual bots.
#  2) Or spawn new process per bot request
#  -
#  ** For now **
#  Before designing architecture, just make this server a single process. Then it will resolve.
class RunningBotObjStores:
    """
    A Class that stores running bot instance.
    Maps with user_id and subscribed_bot_id so that viewset can
    access/handle actual running bot instance.
    """

    # TODO: This should be restored back when server is restarted
    #  by fetching active bots and resolving them as bot object again.
    def __init__(self):
        self._bot_stores: Dict[T_USER_ID, Dict[T_SUBSCRIBED_BOT_ID, IBot]] = {}

        # restore active bots
        try:
            subscribed_bots = SubscribedBot.objects.all().filter(
                status=SubscribedBot.StatusChoices.ACTIVE
            )
            for subscribed_bot in subscribed_bots:
                user = subscribed_bot.user
                exchange_setting = UserExchangeSetting.objects.get(user=user)
                compiled_setting = BotSettingResolver.compile_setting(
                    exchange_setting, subscribed_bot
                )
                bot: IBot = BotResolver.model_to_instance(
                    subscribed_bot, compiled_setting
                )
                # initiate bot and save instance
                bot.run()
                self.set_bot_instance(user.id, subscribed_bot.id, bot)

        # skip if db not yet setup
        except (RuntimeError, ProgrammingError):
            return

        logger.info(
            f"Successfully initiated BotObjStores. {len(subscribed_bots)} active bots restored."
        )

    def set_bot_instance(
        self, user_id: T_USER_ID, subscribed_bot_id: T_SUBSCRIBED_BOT_ID, bot_obj: IBot
    ) -> None:

        self._bot_stores[user_id] = {subscribed_bot_id: bot_obj}

    def get_bot_instance(
        self, user_id: T_USER_ID, subscribed_bot_id: T_SUBSCRIBED_BOT_ID
    ) -> IBot:
        try:
            return self._bot_stores[user_id][subscribed_bot_id]
        except KeyError:
            raise RuntimeError(
                f"There is no bot(id={subscribed_bot_id}) running for user(id={user_id})"
            )

    def del_bot_instance(
        self, user_id: T_USER_ID, subscribed_bot_id: T_SUBSCRIBED_BOT_ID
    ) -> None:
        del self._bot_stores[user_id][subscribed_bot_id]


# store = RunningBotObjStores()


###############################
# Bot Administration ViewSets #
###############################


class BotViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = BotSerializer
    queryset = Bot.objects.all()
    lookup_field = "id"


class BotDefaultSettingViewSet(UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = BotDefaultSettingSerializer
    queryset = Bot.objects.all()
    lookup_field = "id"


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
        if command == BotCommandsChoices.General.START:
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
            # store.set_bot_instance(user.id, subscribed_bot.id, bot)
            # change status
            subscribed_bot.status = SubscribedBot.StatusChoices.ACTIVE
            subscribed_bot.save()

        if command == BotCommandsChoices.General.STOP:
            # if bot inactive,
            if subscribed_bot.status == SubscribedBot.StatusChoices.INACTIVE:
                return Response(
                    data={"detail": "Bot is already inactive. Cannot stop."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # get bot instance and stop
            # delete instance
            user = subscribed_bot.user
            # bot = store.get_bot_instance(user.id, subscribed_bot.id)
            # bot.stop()
            # store.del_bot_instance(user.id, subscribed_bot.id)
            # change status
            subscribed_bot.status = SubscribedBot.StatusChoices.INACTIVE
            subscribed_bot.save()

        return Response(status=status.HTTP_200_OK)


class BotControlManualCommandViewSet(viewsets.GenericViewSet):
    queryset = SubscribedBot.objects.all()
    serializer_class = BotControlManualCommandSerializer
    permission_classes = [
        IsUserBotOwner & IsSubscriptionValid & IsManualBot & IsBotActive
    ]

    @swagger_auto_schema(
        responses={
            200: "success",
            403: "permission denied",
            406: "invalid payload",
        }
    )
    def command(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        # subscribed_bot: SubscribedBot = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={"detail": f"invalid payload: {request.data}"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        # resolve command to bot methods
        # command = serializer.data["command"]
        # bot: IBot = store.get_bot_instance(subscribed_bot.user.id, subscribed_bot.id)
        # method = BotResolver.command_to_method(command, bot)
        # run
        # method()
        return Response(status=status.HTTP_200_OK)


class BotControlSettingViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = SubscribedBot.objects.all()
    serializer_class = BotControlGeneralCommandSerializer

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pass

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pass
