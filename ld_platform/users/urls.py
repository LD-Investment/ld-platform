from django.urls import path

from ld_platform.users.api.views import UserViewSet

app_name = "users"

user_list = UserViewSet.as_view({"get": "list"})
user_detail = UserViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("", user_list, name="user-list"),
    path("<int:user_id>/", user_detail, name="user-detail"),
]
