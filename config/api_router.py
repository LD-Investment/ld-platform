from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"
urlpatterns = [
    path("auth/", include("allauth.urls")),
    path("users/", include("ld_platform.users.urls")),
    path("funds/", include("ld_platform.funds.urls")),
    path("bots/", include("ld_platform.bots.urls")),
]
urlpatterns += router.urls
