from rest_framework import serializers

from ld_platform.apps.bots.models import Bot, UserSubscribedBot


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ["name"]


class BotControlCommandSerializer(serializers.Serializer):
    command = serializers.ChoiceField(UserSubscribedBot.CommandChoices)
