from rest_framework import serializers

from ld_platform.apps.bots.models import Bot, SubscribedBot


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ["type", "name", "version", "default_setting"]


class BotDefaultSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ["default_setting"]


class BotControlCommandSerializer(serializers.Serializer):
    command = serializers.ChoiceField(SubscribedBot.CommandChoices)
