"""Module to that provides utility functions for EMA survey sms messaging.
"""
import PhoneNumber

from django.utils import timezone
from datetime import datetime
from .models import EMASession

# TODO: def start_survey():
# Needs to include randomly choosing the first question


def survey_active(limit: int) -> bool:
    """Decides whether the latest survey session is currently active by calculating
    whether the current time is within the limit of the session length. 

    Parameters
    ----------
    limit : int
        Desired session length in minutes

    Returns
    -------
    bool
        True if the current time is still within the limit, and False otherwise.
    """

    # From the EMASession table, get the start time of the most recent session
    time_diff = timezone.now() - EMASession.objects.latest("start_time").start_time
    # Get the number of minutes elapsed by using the modulo operator. Only want the first part, hence [0]
    minutes_since = divmod(time_diff.seconds, 60)[0]

    if minutes_since >= limit:
        return False
    else:
        return True


def save_and_reply(number: str, text: str, recieved: datetime) -> str:
    return
