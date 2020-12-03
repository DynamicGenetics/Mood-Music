from django.core.exceptions import PermissionDenied
from django.db.models.signals import pre_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# Get the generic user model
User = get_user_model()


@receiver(pre_save, sender=User)
def check_limits(sender, **kwargs):
    """Ensures that the maximum number of users does not exceed
    the number specified by MAX_USERS in settings.

    Raises
    ------
    PermissionDenied
        If max number of users is reached, this error will be raised.
    """
    if sender.objects.count() > settings.MAX_USERS:
        raise PermissionDenied
