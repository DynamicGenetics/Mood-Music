import pytest

from django.core.exceptions import PermissionDenied
from moodmusic.users.tests.factories import UserFactory
from django.conf import settings

pytestmark = pytest.mark.django_db


def test_max_users_signal():
    """Assert that permission is denied when making more than the maximum
    number of users defined in settings.
    """
    for n in range(settings.MAX_USERS):
        UserFactory()  # Save a fake user

    with pytest.raises(PermissionDenied):
        UserFactory()
