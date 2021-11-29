from django.urls import path

from ld_platform.funds.api.views import FundViewSet

app_name = "funds"

fund_list = FundViewSet.as_view({"get": "list"})
fund_detail = FundViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("", fund_list, name="fund-list"),
    path("<int:fund_id>/", fund_detail, name="fund-detail"),
]
