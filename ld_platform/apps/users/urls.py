from django.urls import path

from ld_platform.apps.users.api.views import UserProfileViewSet

app_name = "users"

user_profile_detail = UserProfileViewSet.as_view({"get": "retrieve"})

urlpatterns = [path("profile/", user_profile_detail, name="user-profile-detail")]
