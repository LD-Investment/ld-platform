from rest_framework import serializers

from ld_platform.bots.models import Bot


class BotControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ["name"]
