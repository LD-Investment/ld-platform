from django.contrib import admin

from ld_platform.apps.bots.models import Bot, SubscribedBot


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "default_setting", "version"]
    search_fields = ["id", "name", "version"]


@admin.register(SubscribedBot)
class SubscribedBotAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "bot",
        "status",
        "run_type",
        "user_bot_settings",
        "subscribe_start_date",
        "subscribe_end_date",
    ]
    search_fields = [
        "id",
        "user",
        "bot",
        "status",
        "run_type",
        "user_bot_settings",
        "subscribe_start_date",
        "subscribe_end_date",
    ]
