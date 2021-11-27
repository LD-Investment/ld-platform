from rest_framework import serializers

from ld_platform.bots.models import Bot


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ["name"]
