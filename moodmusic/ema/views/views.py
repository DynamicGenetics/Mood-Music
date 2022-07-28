import logging

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from twilio.twiml.messaging_response import MessagingResponse
from .decorators import validate_twilio_request
from moodmusic.ema.services.ema_response import manage_response

# Retrieve or create a logger instance
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
