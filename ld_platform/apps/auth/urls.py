from django.urls import include, path

urlpatterns = [
    path("", include("rest_auth.urls")),
    path("signup/", include("rest_auth.registration.urls")),
]
