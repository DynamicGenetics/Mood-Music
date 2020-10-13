from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField, EmailField, CharField, ForeignKey
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class User(AbstractUser):

    # Remove the username and names fields
    username = None

    name = CharField(_("Name of User"), blank=True, max_length=255)
    # Add email as the replacement unique id field
    email = EmailField(_("email address"), unique=True)
    USERNAME_FIELD = "email"

    # Add other required flags
    phone_number = PhoneNumberField()
    consent_granted = BooleanField(default=False)
    phone_verified = BooleanField(default=False)

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.email})


class Consent(models.Model):
    """Model to record that a user consented to the study.
    """

    user = ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="consent"
    )
    seen_information = BooleanField(default=False)
    voluntary_participation = BooleanField(default=False)
    data_unwithdrawable = BooleanField(default=False)
    data_collected = BooleanField(default=False)
    confidentiality = BooleanField(default=False)
    data_access = BooleanField(default=False)
    data_stored_longterm = BooleanField(default=False)
    could_be_reused = BooleanField(default=False)
    breaking_confidentiality = BooleanField(default=False)
    full_consent = BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
