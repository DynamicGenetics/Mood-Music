import pytest

from django.contrib.auth import get_user_model
from django.test import TestCase

from moodmusic.ema.services import (
    manage_response,
    is_valid,
    save_response,
    AUTO_MESSAGE,
)
from moodmusic.ema.models import EMASession, SessionState, EMAQuestions
from moodmusic.ema.tests.test_models import create_EMASession


@pytest.mark.parametrize("input,expected", [("hello", False), ("", False), ("9", True)])
def test_is_valid(input, expected):
    assert is_valid(input) is expected


class TestManageResponse(TestCase):
    def setUp(self):
        # Add two questions
        EMAQuestions.objects.create(short_name="name1", body="Some text")
        EMAQuestions.objects.create(short_name="name2", body="Some more text")

    def test_no_sessions_exist(self):
        """For when there are no sessions in the database.
        """
        user = get_user_model().objects.create()
        # Create an expired sessions
        reply = manage_response(user, "message", "")
        assert reply == AUTO_MESSAGE["no_active_session"]

    def test_no_active_sessions(self):
        """For when there is no active session.
        """
        create_EMASession(100)
        user = get_user_model().objects.create()
        reply = manage_response(user, "message", "")
        assert reply == AUTO_MESSAGE["no_active_session"]

    def test_invalid_response(self):
        """For when a response is invalid.
        """
        session = create_EMASession(5)
        user = get_user_model().objects.create(phone_number="549")
        SessionState.objects.create(user=user, session=session)
        reply = manage_response(user, "invalid", "")
        assert reply == AUTO_MESSAGE["message_invalid"]

    # def test_answer_not_expected(self):
    #     """For when the user has answered all the questions.
    #     """
    #     session = create_EMASession(5)
    #     user = get_user_model().objects.create(phone_number="549")
    #     state = SessionState.objects.create(user=user, session=session)

    #     save_response("10", state)
    #     save_response("6", state)

