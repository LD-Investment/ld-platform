from django.urls import path

from ld_platform.bots.api.views import BotViewSet

app_name = "bots"

bot_list = BotViewSet.as_view({"get": "list"})
bot_detail = BotViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("", bot_list, name="bot-list"),
    path("<int:bot_id>/", bot_detail, name="bot-detail"),
]
