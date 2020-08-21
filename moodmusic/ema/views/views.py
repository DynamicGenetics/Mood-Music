from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse

from .decorators import validate_twilio_request
from ..services import save_and_reply


@csrf_exempt
@validate_twilio_request
def respond_to_incoming_message(request):
    """Responds to a text message to the Twilio number with a predefined message"""

    # Get message content
    number = request.POST.get("From")
    text = request.POST.get("Body")
    receieved = timezone.now()

    # Pass to function to decide on appropriate action
    reply = save_and_reply(number, text, receieved)

    # Start response
    resp = MessagingResponse()
    # Add a text message to the response
    resp.message(reply)

    return HttpResponse(str(resp))

