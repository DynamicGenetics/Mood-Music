"""Decorator for the Twilio webhook that validates incoming requests.

Validation is done by comparing the signature from Twilio recieved in the payload
with the known authorisation token for the Twilio account being used.
This will ensure the application will only respond to genuine requests we can be
sure came from Twilio. 
"""

from django.conf import settings
from django.http import HttpResponseForbidden
from functools import wraps
from twilio.request_validator import RequestValidator

import os


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""

    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(os.environ.get("TWILIO_AUTH_TOKEN"))

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.build_absolute_uri(),
            request.POST,
            request.META.get("HTTP_X_TWILIO_SIGNATURE", ""),
        )

        # Continue processing the request if it's valid (or if DEBUG is True)
        # and return a 403 error if it's not
        if request_valid or settings.DEBUG:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    return decorated_function
