from django.contrib import admin

from ld_platform.bots.models import Bot


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
