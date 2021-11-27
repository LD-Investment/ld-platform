from django.urls import path

from ld_platform.bot_controls.api.views import BotControlViewSet

app_name = "bot_controls"

bot_control_list = BotControlViewSet.as_view({"get": "list"})
bot_control_detail = BotControlViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("", bot_control_list, name="bot-control-list"),
]
