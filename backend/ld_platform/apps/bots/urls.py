from django.urls import path

from ld_platform.apps.bots.api.views import (
    BotSubscribeViewSet,
    BotViewSet,
    IBNewsTrackerAiModelViewSet,
)

app_name = "bots"

bot_general_list = BotViewSet.as_view({"get": "list"})
bot_general_detail = BotViewSet.as_view({"get": "retrieve"})
bot_general_subscribe = BotSubscribeViewSet.as_view({"post": "subscribe"})

# Indicator Views
bot_indicator_news_tracker_ai_list = IBNewsTrackerAiModelViewSet.as_view(
    {"get": "list"}
)
bot_indicator_news_tracker_ai_detail = IBNewsTrackerAiModelViewSet.as_view(
    {"get": "retrieve"}
)
bot_indicator_news_tracker_score = IBNewsTrackerAiModelViewSet.as_view(
    {"post": "calculate"}
)

urlpatterns = [
    # Bot General
    # -------------------
    path("", bot_general_list, name="bot-general-list"),
    path("<int:id>/", bot_general_detail, name="bot-general-detail"),
    path("<int:id>/subscribe", bot_general_subscribe, name="bot-general-subscribe"),
    # Indicator Bots
    # -------------------
    # - News Tracker
    path(
        "indicator/news-tracker/ai-model",
        bot_indicator_news_tracker_ai_list,
        name="bot-indicator-news-tracker-ai-list",
    ),
    path(
        "indicator/news-tracker/ai/<str:model_name>",
        bot_indicator_news_tracker_ai_detail,
        name="bot-indicator-news-tracker-ai-detail",
    ),
    path(
        "indicator/news-tracker/ai-model/<str:model_name>/calculate",
        bot_indicator_news_tracker_score,
        name="bot-indicator-news-tracker-score",
    ),
]
