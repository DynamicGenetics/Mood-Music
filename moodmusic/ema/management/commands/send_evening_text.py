import os
import time
import logging
import traceback

from twilio.rest import Client
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

# Retrieve or start logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Send a text message to all users thanking them for their participation."

    def handle(self, *args, **options):
        # Init some logging information
        start = time.time()

        message = (
            "A big thank you for your participation today. Remember that if you need support you can"
            + " get in touch with the University's Wellbeing Service https://bit.ly/2VmHiWu"
        )

        # Set up the Twilio client to send messages
        client = Client(
            os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"]
        )

        # Get all the users whose phone numbers are verified.
        users = get_user_model().objects.filter(phone_verified=True)
        # Init a counter for logging
        n = 0

        for user in users:
            # Send message
            try:
                client.messages.create(
                    to=user.phone_number.as_e164,
                    from_=os.environ["TWILIO_NUMBER"],
                    body=message,
                )
                n += 1
            except Exception:
                logger.error(
                    """A problem occured when trying to send a message to user: {}.
                    The error was {}.""".format(
                        user.id, traceback.format_exc()
                    )
                )
                pass

        # Record logging information
        end = time.time()
        total_time = end - start

        # Record actions in logger
        logger.info(
            "Evening messages have been dispatched to {} of {} users.".format(
                n, users.count()
            )
        )
        logger.info("Seconds taken: {}".format(total_time))
