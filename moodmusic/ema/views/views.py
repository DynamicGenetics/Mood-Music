from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from twilio.twiml.messaging_response import MessagingResponse

from .decorators import validate_twilio_request


@csrf_exempt
@validate_twilio_request
def respond_to_incoming_message(request):
    """Responds to a text message to the Twilio number with a predefined message"""

    # Get message content
    text = request.POST.get("Body")
    print(text)
    # Start response
    resp = MessagingResponse()

    # Add a text message to the response
    resp.message("You just said this: " + text)

    return HttpResponse(str(resp))
