from twilio.rest import Client
import os

client = Client(os.environ["TWILIO_VERIFY_SID"], os.environ["TWILIO_AUTH_TOKEN"])


def verifications(phone_number, via):
    return client.verify.services(os.environ["TWILIO_VERIFY_SID"]).verifications.create(
        to=phone_number, channel=via
    )


def verification_checks(phone_number, token):
    return client.verify.services(
        os.environ["TWILIO_AUTH_TOKEN"]
    ).verification_checks.create(to=phone_number, code=token)
