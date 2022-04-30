from django.urls import include, path, re_path
from rest_auth.registration.views import ConfirmEmailView, VerifyEmailView

urlpatterns = [
    path("", include("allauth.urls")),
    path("signup/", include("rest_auth.registration.urls"), name="account_signup"),
    re_path(
        r"^account-confirm-email/$",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
]
