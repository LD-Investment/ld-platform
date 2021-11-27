from django.contrib import admin

from ld_platform.funds.models import Fund


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
