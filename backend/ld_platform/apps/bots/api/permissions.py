from django.utils import timezone
from rest_framework import exceptions, permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from ld_platform.apps.bots.models import Bot, SubscribedBot


class IsUserBotOwner(permissions.BasePermission):
    message = "Permission denied. User is not an owner of the bot."

    def has_object_permission(
        self, request: Request, view: APIView, obj: SubscribedBot
    ) -> bool:
        if request.user != obj.user:
            raise exceptions.PermissionDenied(detail=self.message)
        return True


class IsSubscriptionValid(permissions.BasePermission):
    message = "Permission denied. Subscription expired."

    def has_object_permission(
        self, request: Request, view: APIView, obj: SubscribedBot
    ) -> bool:
        if timezone.now() > obj.subscribe_end_date:
            raise exceptions.PermissionDenied(detail=self.message)
        return True


class IsBotActive(permissions.BasePermission):
    message = "Permission denied. Bot is not active."

    def has_object_permission(
        self, request: Request, view: APIView, obj: SubscribedBot
    ) -> bool:
        if obj.status != SubscribedBot.StatusChoices.ACTIVE:
            raise exceptions.PermissionDenied(detail=self.message)
        return True


class IsNewsTrackerBot(permissions.BasePermission):
    message = "The bot is not News Tracker Bot."

    def has_object_permission(
        self, request: Request, view: APIView, obj: SubscribedBot
    ) -> bool:
        if not (
            obj.bot.name == Bot.NameChoices.NEWS_TRACKER
            and obj.bot.type == Bot.TypeChoices.INDICATOR
        ):
            raise exceptions.PermissionDenied(detail=self.message)
        return True
