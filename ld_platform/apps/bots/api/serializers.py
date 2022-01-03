from rest_framework import serializers

from ld_platform.apps.bots.models import Bot
from ld_platform.shared.choices import BotCommandsChoices


class BotSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_type_display")
    name_display = serializers.CharField(source="get_name_display")

    class Meta:
        model = Bot
        fields = [
            "id",
            "type",
            "type_display",
            "name",
            "name_display",
            "version",
            "default_setting",
        ]


class BotDefaultSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ["default_setting"]


class BotControlGeneralCommandSerializer(serializers.Serializer):
    command = serializers.ChoiceField(BotCommandsChoices.General)


class BotControlManualCommandSerializer(serializers.Serializer):
    # TODO: Custom Validator according to Bot
    command = serializers.ChoiceField(BotCommandsChoices.Manual)
