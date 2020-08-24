import os
import random
import logging

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from .decorators import validate_twilio_request
from moodmusic.ema.services import manage_response
from moodmusic.ema.models import EMASession, SessionState, EMAQuestions

# Retieve or create a logger instance
logger = logging.getLogger(__name__)


@csrf_exempt
@validate_twilio_request
def respond_to_incoming_message(request):
    """Responds to a text message to the Twilio number with a predefined message"""

    # Get message content
    number = request.POST.get("From")
    text = request.POST.get("Body")
    receieved = timezone.now()
    logger.info(
        "Message receieved. Number: {}, Message: {}, Time: {}".format(
            number, text, receieved
        )
    )
    # If a user can be associated with this number then...
    try:
        user = get_user_model().objects.filter(phone_number=number)
        # Pass to function to decide on appropriate action
        reply = manage_response(user, text, receieved)
    except get_user_model().DoesNotExist:
        # Work out how to tell Twilio we don't want to reply
        reply = "User not recognised"
        logger.info(
            "Message from unrecognised number. Number: {}, Message: {}, Time: {}".format(
                number, text, receieved
            )
        )

    # Start response
    resp = MessagingResponse()
    # Add a text message to the response
    resp.message(reply)

    return HttpResponse(str(resp))


def start_survey_session(request):

    # Get a random question to start with
    question = random.choice(EMAQuestions.objects.all())

    # Start an EMA Session that will record an id and start_time
    session = EMASession.objects.create()

    message = (
        "Hi, it's time for a survey - please reply within 1 hour. " + question.body
    )

    # Set up the Twilio client to send messages
    client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

    # Get all the users
    users = get_user_model().objects.all()

    for user in users:
        # Send message

        client.messages.create(
            to=user.phone_number.as_e164,
            from_=os.environ["TWILIO_NUMBER"],
            body=message,
        )
        # Initialise the user's state for this new session
        s = SessionState.objects.create(user=user, session=session)
        s.update(question)

    return HttpResponse("Messages successfully sent!", 200)
