from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.http import HttpRequest
from django.forms import ValidationError


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def clean_email(self, email):
        # Check that the email address is a bristol university one.
        provider = email.split("@")[1]
        provider = provider.lower()

        if provider != "bristol.ac.uk":
            raise ValidationError(
                """You can only sign up with your university email address
                ending in `@bristol.ac.uk`. Please try again."""
            )
        return email
