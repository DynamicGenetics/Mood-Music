from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


User = get_user_model()


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=30, label="Full Name")
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget, label=_("Phone number"), required=True,
    )

    def signup(self, request, user):
        user.name = self.cleaned_data["name"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.email = self.clean_email()
        user.save()
        return user
