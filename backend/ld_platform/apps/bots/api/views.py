import logging
from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ld_platform.apps.bots.models import Bot, SubscribedBot

from .serializers import (
    BotDefaultSettingSerializer,
    BotSerializer,
    BotSubscribeSerializer,
)

logger = logging.getLogger(__name__)


###############################
# Bot Administration ViewSets #
###############################


class BotViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = BotSerializer
    queryset = Bot.objects.all()
    lookup_field = "id"


class BotDefaultSettingViewSet(UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = BotDefaultSettingSerializer
    queryset = Bot.objects.all()
    lookup_field = "id"


#############################
# Bot Subscription ViewSets #
#############################


class BotSubscribeViewSet(viewsets.GenericViewSet):
    queryset = Bot.objects.all()
    serializer_class = BotSubscribeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    @swagger_auto_schema(
        responses={200: "success", 401: "unauthorized", 404: "not found"}
    )
    def subscribe(self, request: Request, *args: Any, **kwargs: Any):
        # TODO: Since FE is not ready, replace fields like
        #  `status` and `run_type` with default values
        request.data["status"] = SubscribedBot.StatusChoices.ACTIVE
        request.data["run_type"] = SubscribedBot.RunTypeChoices.LIVE_RUN

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={"detail": f"invalid payload: {request.data}"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        # subscribe to bot
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        context["bot"] = Bot.objects.get(id=self.kwargs["id"])
        return context
