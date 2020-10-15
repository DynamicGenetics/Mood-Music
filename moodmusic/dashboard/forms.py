from django import forms
from django.contrib.auth import get_user_model

# Set up a varb for the user model
User = get_user_model()


class TokenForm(forms.Form):
    """Form used to input the verification token from Twilio phone number verify API.
    """

    token = forms.CharField(label="Verification Token")
