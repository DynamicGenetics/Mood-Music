import uuid
from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField, EmailField, CharField, signals
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


# Set a random username for each user.
def random_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = uuid.uuid4().hex[:30]


class User(AbstractUser):
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
        return reverse("users:detail", kwargs={"name": self.username})


signals.pre_save.connect(random_username, sender=User)
