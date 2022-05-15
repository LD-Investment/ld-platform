from django.contrib import admin

from ld_platform.apps.bots.models import Bot, SubscribedBot


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "type",
        "default_setting",
    ]
    search_fields = [
        "id",
        "name",
        "type",
    ]


@admin.register(SubscribedBot)
class SubscribedBotAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "get_bot_name",
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

    def get_bot_name(self, obj):
        return obj.bot.name

    get_bot_name.short_description = "Bot Name"  # Renames column head
