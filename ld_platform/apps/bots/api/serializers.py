from rest_framework import serializers

from ld_platform.apps.bots.models import Bot, SubscribedBot


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ["name"]


class BotControlGeneralCommandSerializer(serializers.Serializer):
    command = serializers.ChoiceField(SubscribedBot.CommandChoices)


class BotControlManualCommandSerializer(serializers.Serializer):
    # TODO: Custom Validator according to Bot
    command = serializers.ChoiceField(SubscribedBot.CommandChoices)
