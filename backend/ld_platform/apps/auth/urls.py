from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from django.urls import include, path, re_path

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    # path('signup/', include('dj_rest_auth.registration.urls')),
    path("signup/", RegisterView.as_view()),
    path(
        "account_confirm_email/", RegisterView.as_view(), name="account_confirm_email"
    ),
    path("verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path(
        "account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    # path(r'signup/^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(),
    # name='account_confirm_email'),
]
