from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


# Set up a varb for the user model
User = get_user_model()


class TokenForm(forms.Form):
    """Form used to input the verification token from Twilio phone number verify API.
    """

    token = forms.CharField(label="Verification Token")


class UploadListeningHistoryForm(forms.Form):
    file_field = forms.FileField(
        label="Listening History File/s",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )
