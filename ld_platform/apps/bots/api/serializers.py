from rest_framework import serializers

from ld_platform.apps.bots.models import Bot
from ld_platform.shared.choices import BotCommandsChoices


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ["name"]


class BotControlGeneralCommandSerializer(serializers.Serializer):
    command = serializers.ChoiceField(BotCommandsChoices.General)


class BotControlManualCommandSerializer(serializers.Serializer):
    # TODO: Custom Validator according to Bot
    command = serializers.ChoiceField(BotCommandsChoices.Manual)
