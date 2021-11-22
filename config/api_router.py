from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from ld_platform.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls

# Your custom urls for API go here
urlpatterns += [
    # User management
    # TODO: below is just example.
    path("users/", include("ld_platform.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
]
