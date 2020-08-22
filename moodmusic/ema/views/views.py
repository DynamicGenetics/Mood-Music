import os
import random

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from .decorators import validate_twilio_request
from moodmusic.ema.services import manage_response
from moodmusic.ema.models import EMASession, SessionState, EMAQuestions


@csrf_exempt
@validate_twilio_request
def respond_to_incoming_message(request):
    """Responds to a text message to the Twilio number with a predefined message"""

    # Get message content
    number = request.POST.get("From")
    text = request.POST.get("Body")
    receieved = timezone.now()

    if get_user_model().objects.filter(phone_number=number).exists():
        # Pass to function to decide on appropriate action
        reply = manage_response(number, text, receieved)
    else:
        # Work out how to tell Twilio we don't want to reply
        reply = "User not recognised"

    # Start response
    resp = MessagingResponse()
    # Add a text message to the response
    resp.message(reply)

    return HttpResponse(str(resp))


def start_survey_session(request):

    # Get a random question to start with
    question = random.choice(EMAQuestions.objects.all())

    # Start an EMA Session that will record an id and start_time
    session = EMASession.objects.create(first_question=question)

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
            to=user.phone_number, from_=os.environ["TWILIO_NUMBER"], body=message
        )
        # Initialise the user's state for this new session
        SessionState.objects.create(
            user=user, session=session, state=0, last_question=question
        )

    return HttpResponse("Messages successfully sent!", 200)

