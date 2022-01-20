from django.db.models.query import QuerySet
from django.utils import timezone
from rest_framework import serializers

from ld_platform.apps.bots.models import Bot, SubscribedBot
from ld_platform.apps.users.models import User
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


class BotSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribedBot
        fields = ["status", "run_type", "user_bot_settings"]

    def create(self, validated_data):
        user: User = self.context["user"]
        bot: Bot = self.context["bot"]

        # check if user already subscribed to same bot
        if self.check_bot_subscription(user, bot):
            raise serializers.ValidationError("User already subscribed to the bot")

        # TODO: set subscription start/end date as default
        validated_data["subscribe_end_date"] = timezone.now() + timezone.timedelta(
            days=100
        )

        subscribed_bot: SubscribedBot = SubscribedBot(
            user=user,
            bot=bot,
            **validated_data,
        )
        subscribed_bot.save()
        return subscribed_bot

    @staticmethod
    def check_bot_subscription(user: User, bot: Bot):
        """
        Check whether the user subscribed to the Bot or not.
        """
        qs: QuerySet = SubscribedBot.objects.filter(bot=bot, user=user)
        return qs.exists()


class BotDefaultSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ["default_setting"]


class BotControlGeneralCommandSerializer(serializers.Serializer):
    command = serializers.ChoiceField(BotCommandsChoices.General)


class BotControlManualCommandSerializer(serializers.Serializer):
    # TODO: Custom Validator according to Bot
    command = serializers.ChoiceField(BotCommandsChoices.Manual)
