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
urlpatterns = [
    path("accounts/", include("allauth.urls")),
]
urlpatterns += router.urls
