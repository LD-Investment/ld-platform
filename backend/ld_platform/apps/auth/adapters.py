from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import build_absolute_uri
from django.http import HttpResponseRedirect
from django.urls import reverse


class EmailAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        url = reverse("api:auth:account_confirm_email", args=[emailconfirmation.key])
        ret = build_absolute_uri(request, url)
        return ret

    def respond_email_verification_sent(self, request, user):
        return HttpResponseRedirect(reverse("api:auth:account_email_verification_sent"))
