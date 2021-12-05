from django.urls import path

from ld_platform.bots.api.views import (
    BotControlCommandViewSet,
    BotControlSettingViewSet,
    BotViewSet,
)

app_name = "bots"

# Bot Administration
bot_list = BotViewSet.as_view({"get": "list"})
bot_detail = BotViewSet.as_view({"get": "retrieve"})

# Bot Authentication
# TODO: Check if subscription is valid, bot setting etc.
#  should give token to control bot

# Bot Control
bot_command = BotControlCommandViewSet.as_view({"post": "command"})
bot_setting = BotControlSettingViewSet.as_view(
    {"get": "get_setting", "put": "update_setting"}
)

urlpatterns = [
    # Bot Administration
    path("", bot_list, name="bot-list"),
    path("<int:pk>/", bot_detail, name="bot-detail"),
    # Bot Control
    path("control/bot/<int:pk>/command", bot_command, name="bot-control-command"),
    path("control/bot/<int:pk>/setting", bot_setting, name="bot-control-setting"),
]
