import logging
from datetime import datetime, timedelta
from typing import Any

from django.db.models import Q, QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ld_platform.apps.bots.models import Bot, SubscribedBot
from ld_platform.apps.dataset.models import CoinnessNewsData

from .permissions import (
    IsBotActive,
    IsNewsTrackerBot,
    IsSubscriptionValid,
    IsUserBotOwner,
)
from .serializers import (
    BotSerializer,
    BotSubscribeSerializer,
    IBNewsTrackerAiModelCalculateSerializer,
    IBNewsTrackerAiModelListSerializer,
    IBNewsTrackerAiModelRetrieveSerializer,
)

logger = logging.getLogger(__name__)


###############################
# Bot Administration ViewSets #
###############################


class BotViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = BotSerializer
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
        if getattr(self, "swagger_fake_view", False):
            return context
        context["user"] = self.request.user
        context["bot"] = Bot.objects.get(id=self.kwargs["id"])
        return context


#####################################
# Indicator - News Tracker ViewSets #
#####################################

#  Note: IB will be prefixed to every ViewSet classes that represent Indicator Bot.


class IBNewsTrackerAiModelViewSet(viewsets.ModelViewSet):
    serializer_class = IBNewsTrackerAiModelListSerializer
    permission_classes = [
        IsAuthenticated
        & IsBotActive
        & IsUserBotOwner
        & IsSubscriptionValid
        & IsNewsTrackerBot
    ]

    def get_object(self) -> SubscribedBot:
        qs = self.get_queryset()
        if not qs.exists():
            raise NotFound(detail="User is not subscribed to News Tracker")
        return qs.first()

    def get_queryset(self) -> QuerySet:
        return SubscribedBot.objects.filter(
            Q(bot__name=Bot.NameChoices.NEWS_TRACKER)
            & Q(bot__type=Bot.TypeChoices.INDICATOR)
            & Q(user=self.request.user)
        )

    def get_serializer_class(self):
        if self.action == "list":
            return IBNewsTrackerAiModelListSerializer
        if self.action == "retrieve":
            return IBNewsTrackerAiModelRetrieveSerializer
        if self.action == "calculate":
            return IBNewsTrackerAiModelCalculateSerializer
        return self.serializer_class

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Detail information about AI model registered to News Tracker service
        """
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        serializer = self.get_serializer(
            obj, context={"model_name": self.kwargs["model_name"]}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        List AI models registered to News Tracker service
        """
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def calculate(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Get News Tracker score calculated by selected AI model.
        """
        # TODO: Impl query param for date selection.
        #  refer https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
        obj = self.get_object()
        self.check_object_permissions(request, obj)

        # Serialize
        sd = datetime.strptime(self.request.data["start_date"], "%Y-%m-%d").date()
        ed = datetime.strptime(
            self.request.data["end_date"], "%Y-%m-%d"
        ).date() + timedelta(days=1)

        qs = CoinnessNewsData.objects.filter(
            date__gte=sd,
            date__lte=ed,
        ).order_by("article_num")
        models = Bot.indicator_bot_objects.load_ai_models(bot=obj.bot)
        for m in models:
            if m.name == self.kwargs["model_name"]:
                serializer = self.get_serializer(qs, many=True, context={"model": m})
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
