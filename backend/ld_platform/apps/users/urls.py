from django.urls import path

from ld_platform.apps.users.api.views import (
    UserProfileViewSet,
    UserSubscribedBotViewSet,
)

app_name = "users"

user_profile_detail = UserProfileViewSet.as_view()
user_subscribed_bot_list = UserSubscribedBotViewSet.as_view()

urlpatterns = [
    path("profile/", user_profile_detail, name="user-profile-detail"),
    path(
        "subscribed-bots/", user_subscribed_bot_list, name="user-subscribed-bots-list"
    ),
]
