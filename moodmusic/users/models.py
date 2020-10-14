from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField, EmailField, CharField
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
        return reverse("users:detail", kwargs={"name": self.name})
