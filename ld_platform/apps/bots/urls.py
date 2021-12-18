from django.urls import path

from ld_platform.apps.bots.api.views import (
    BotControlCommandViewSet,
    BotControlSettingViewSet,
    BotDefaultSettingViewSet,
    BotViewSet,
)

app_name = "bots"

# Bot Administration
bot_list = BotViewSet.as_view({"get": "list", "post": "create"})
bot_detail = BotViewSet.as_view({"get": "retrieve", "delete": "destroy"})
bot_default_setting = BotDefaultSettingViewSet.as_view(
    {"get": "retrieve", "put": "update"}
)

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
    path("<int:id>/", bot_detail, name="bot-detail"),
    path(
        "<int:id>/administration/setting",
        bot_default_setting,
        name="bot-default-setting",
    ),
    # Bot Control
    path(
        "control/subscribed_bot/<int:pk>/command",
        bot_command,
        name="bot-control-command",
    ),
    path(
        "control/subscribed_bot/<int:pk>/setting",
        bot_setting,
        name="bot-control-setting",
    ),
]
