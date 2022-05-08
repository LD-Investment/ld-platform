from dj_rest_auth.registration.views import ConfirmEmailView, VerifyEmailView
from django.urls import include, path, re_path

app_name = "auth"

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("signup/", include("dj_rest_auth.registration.urls")),
    path("verify/", VerifyEmailView.as_view(), name="account_email_verification_sent"),
    re_path(
        r"^confirm/(?P<key>.+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
]
