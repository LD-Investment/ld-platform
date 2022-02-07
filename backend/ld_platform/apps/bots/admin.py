from django.contrib import admin

from ld_platform.apps.bots.models import Bot, CoinnessNewsData, SubscribedBot


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "type", "default_setting", "version"]
    search_fields = ["id", "name", "type", "version"]


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


@admin.register(CoinnessNewsData)
class CoinnessNewsDataAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "article_num",
        "date",
        "title",
        "content",
        # "bull_count",
        # "bear_count",
    ]
    search_fields = [
        "id",
        "article_num",
        "date",
        "title",
        "content",
        # "bull_count",
        # "bear_count",
    ]
