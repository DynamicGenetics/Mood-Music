from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from twilio.twiml.messaging_response import MessagingResponse


@csrf_exempt
def respond_to_incoming_message(request):
    """Responds to a text message to the Twilio number with a predefined message"""
    # Start response
    resp = MessagingResponse()

    # Add a text message to the response
    resp.message("Check out this cute owl! https://bit.ly/3i3ru4p")

    return HttpResponse(str(resp))
