from django.urls import path

from ld_platform.apps.bots.api.views import (
    BotControlGeneralCommandViewSet,
    BotControlManualCommandViewSet,
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
bot_general_command = BotControlGeneralCommandViewSet.as_view(
    {"post": "command"}
)  # Command to all bot types
bot_manual_command = BotControlManualCommandViewSet.as_view(
    {"post": "command"}
)  # Command to manual bot only
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
        "control/subscribed_bot/<int:pk>/general/command",
        bot_general_command,
        name="bot-control-general-command",
    ),
    path(
        "control/subscribed_bot/<int:pk>/manual/command",
        bot_manual_command,
        name="bot-control-manual-command",
    ),
    path(
        "control/subscribed_bot/<int:pk>/setting",
        bot_setting,
        name="bot-control-setting",
    ),
]
