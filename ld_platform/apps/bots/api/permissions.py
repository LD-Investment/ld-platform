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


class IsManualBot(permissions.BasePermission):
    message = "Permission denied. Bot is not a manual bot."

    def has_object_permission(self, request: Request, view: APIView, obj: Bot) -> bool:
        if obj.type != Bot.TypeChoices.MANUAL:
            raise exceptions.PermissionDenied(detail=self.message)
        return True
