import os
import time
import random
import logging
import traceback

from twilio.rest import Client
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from moodmusic.ema.models import EMASession, SessionState, EMAQuestion

# Retrieve or start logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Start an EMA instance and text the starting question to all users."

    def handle(self, *args, **options):
        # Init some logging information
        start = time.time()
        logger.info("Command receieved to send EMA at {}".format(start))

        # Get a random question to start with
        question = random.choice(EMAQuestion.objects.all())

        # Start an EMA Session that will record an id and start_time
        session = EMASession.objects.create()

        message = (
            "Hi, it's time for a survey - please reply within 1 hour. Rate your"
            + " agreement with the following statements, where 1=Not At All and 10=Completely:\n"
            + question.body
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
                # Initialise the user's state for this new session
                s = SessionState.objects.create(user=user, session=session)
                s.update(question)
                # Update the logging counter
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
            "Messages have been dispatched to {} of {} users.".format(n, users.count())
        )
        logger.info("Seconds taken: {}".format(total_time))
