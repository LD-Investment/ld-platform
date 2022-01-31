from django.contrib.auth import get_user_model
from rest_framework import serializers

from ld_platform.apps.bots.api.serializers import BotSerializer
from ld_platform.apps.bots.models import SubscribedBot

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class UserSubscribedBotSerializer(serializers.ModelSerializer):
    bot = BotSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display")
    run_type_display = serializers.CharField(source="get_run_type_display")
    # simplify date format
    subscribe_start_date = serializers.DateTimeField(format="%Y-%m-%d")
    subscribe_end_date = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = SubscribedBot
        exclude = ["user"]
