from django.contrib import admin

from ld_platform.apps.dataset.models import CoinnessNewsData, LongShortRatioData


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


@admin.register(LongShortRatioData)
class LongShortRatioDataAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "exchange_name",
        "symbol",
        "long_ratio",
        "short_ratio",
        "timestamp",
    ]
    search_fields = [
        "id",
        "exchange_name",
        "symbol",
        "long_ratio",
        "short_ratio",
        "timestamp",
    ]
