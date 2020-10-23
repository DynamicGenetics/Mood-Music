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
from moodmusic.ema.models import EMASession, SessionState, EMAQuestion

# Retieve or create a logger instance
logger = logging.getLogger(__name__)


@csrf_exempt
@validate_twilio_request
def respond_to_incoming_message(request):
    """Responds to an incoming text message with an appropriate message"""

    # Get message content
    number = request.POST.get("From")
    text = request.POST.get("Body")
    receieved = timezone.now()
    logger.info(
        "Message receieved. Number: {}, Message: {}, Time: {}".format(
            number, text, receieved
        )
    )

    # Set up the Twilio messaging object
    resp = MessagingResponse()

    # If a user can be associated with this number then...
    try:
        user = get_user_model().objects.filter(phone_number=number)[0]
        # Pass to function to decide on appropriate action

        if user.phone_verified is False:
            resp.message(
                """Please verify your phonenumber through your online dashboard."""  # noqa
            )
        else:
            reply = manage_response(user, text, receieved)
            # Add the return message to the response
            resp.message(reply)

        # Return this response with a success code
        return HttpResponse(str(resp))

    except get_user_model().DoesNotExist:

        logger.info(
            "Message from unrecognised number. Number: {}, Message: {}, Time: {}".format(
                number, text, receieved
            )
        )
        reply = "Sorry, we don't know this number. Get in touch if you think that we should."
        resp.message(reply)
        # Return with a 401 'Unauthorised' code - client must authenticate to get correct response.
        return HttpResponse(str(resp))


def start_survey_session(request):

    # Get a random question to start with
    question = random.choice(EMAQuestion.objects.all())

    # Start an EMA Session that will record an id and start_time
    session = EMASession.objects.create()

    message = (
        "Hi, it's time for a survey - please reply within 1 hour. Rate your"
        + " agreement with the following statements, where 1=not at all and 10=completely:\n"
        + question.body
    )

    # Set up the Twilio client to send messages
    client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

    # Get all the users whose phone numbers are verified.
    users = get_user_model().objects.filter(phone_verified=True)

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
