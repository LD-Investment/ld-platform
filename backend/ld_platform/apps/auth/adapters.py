from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import build_absolute_uri
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework_simplejwt.authentication import JWTAuthentication


class EmailAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        url = reverse("api:auth:account_confirm_email", args=[emailconfirmation.key])
        ret = build_absolute_uri(request, url)
        return ret

    def respond_email_verification_sent(self, request, user):
        return HttpResponseRedirect(reverse("api:auth:account_email_verification_sent"))


# NOTE: Since dj-rest-auth goes along with rest_framework_simplejwt when set REST_USE_JWT=True, but does not support
# httpOnly Cookie, we decided to customize and apply adapter to support httpOnly Cookie for JWT Authentication.
#
# For more information, refer:
#  https://github.com/jazzband/djangorestframework-simplejwt/issues/71
#  https://dj-rest-auth.readthedocs.io/en/latest/configuration.html
class JWTHttpOnlyCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)

        raw_token = None
        if header is None:
            if settings.JWT_AUTH_COOKIE:
                raw_token = request.COOKIES.get(settings.JWT_AUTH_COOKIE)
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token
