from typing import List, Union

from django.db.models.query import QuerySet
from django.utils import timezone
from rest_framework import serializers

from ld_platform.ai.indicator.news_tracker import CryptoDeberta
from ld_platform.apps.bots.models import Bot, SubscribedBot
from ld_platform.apps.dataset.models import CoinnessNewsData
from ld_platform.apps.users.models import User

#################################
# Bot Administration Serializer #
#################################


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
            "default_setting",
        ]


###############################
# Bot Subscription Serializer #
###############################


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


#######################################
# Indicator - News Tracker Serializer #
#######################################


class IBNewsTrackerAiModelListSerializer(serializers.Serializer):
    models = serializers.SerializerMethodField()

    def get_models(self, obj: SubscribedBot):
        models = Bot.indicator_bot_objects.load_ai_models(bot=obj.bot)
        return [{"name": m.name, "detail": m.detail} for m in models]


class IBNewsTrackerAiModelRetrieveSerializer(serializers.Serializer):
    model = serializers.SerializerMethodField()

    def get_model(self, obj: SubscribedBot):
        models = Bot.indicator_bot_objects.load_ai_models(bot=obj.bot)
        for m in models:
            if m.name == self.context["model_name"]:
                return {"name": m.name, "detail": m.detail}
        return {}


class IBNewsTrackerAiModelCalculateSerializer(serializers.Serializer):
    result = serializers.SerializerMethodField(method_name="calculate_score")

    def calculate_score(self, obj: SubscribedBot):
        models = Bot.indicator_bot_objects.load_ai_models(bot=obj.bot)
        for m in models:
            if m.name == self.context["model_name"]:
                return self._extract_and_get_avg_scores(
                    news=self.context["news"], model=m
                )
        raise serializers.ValidationError("AI Model not found.")

    @staticmethod
    def _extract_and_get_avg_scores(
        news: List[CoinnessNewsData], model: Union[CryptoDeberta]
    ):
        import statistics

        bull_scores = []
        bear_scores = []
        neutral_scores = []
        for n in news:
            score = model.calculate(n.title, n.content)
            bull_scores.append(score[0])
            neutral_scores.append(score[1])
            bear_scores.append(score[2])

        avg_bull_score = statistics.mean(bull_scores)
        avg_neutral_score = statistics.mean(neutral_scores)
        avg_bear_score = statistics.mean(bear_scores)
        return avg_bull_score, avg_neutral_score, avg_bear_score
