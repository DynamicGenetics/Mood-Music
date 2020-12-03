from django.urls import reverse
from django.test import TestCase

# from moodmusic.ema.views.views import respond_to_incoming_message

# https://www.twilio.com/docs/iam/test-credentials

# def test_validate_twilio_decorator(self):
#     # check if response actually comes from twilio - mock it?
#     return


class TestRespondToMessage(TestCase):
    def test_validate_twilio_decorator(self):
        response = self.client.get(
            reverse("ema"), {"Body": "", "From": "+445670123456"}
        )
        assert response.status_code == 403

    # def test_responds_to_expected_message(self):
    #     pass

    # def test_responds_user_not_recognised(self):
    #     """Attempt to induce a 401 user not recognised error"""
    #     # TODO: Mock around the decorator to get just the function
    #     response = self.client.get(
    #         reverse("ema"), {"Body": "", "From": "+445670123456"}
    #     )
    #     assert response.status_code == 401
