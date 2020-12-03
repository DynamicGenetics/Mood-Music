"""
Module that provides utility and routing functions for EMA survey sms messaging.
"""
import logging

from django.contrib.auth import get_user_model
from datetime import datetime

from moodmusic.ema.models import (
    EMASession,
    EMAResponse,
    EMAQuestion,
    SessionState,
    QuestionHistory,
)

logger = logging.getLogger(__name__)

AUTO_MESSAGE = {
    "no_active_session": (
        "There is not a survey running at the moment."
        + " We will message you the next time that we have questions for you."
    ),
    "message_invalid": (
        "Sorry, we can only recieve messages that contain a"
        + " whole number from 1 to 10. Please send your response again."
    ),
    "thanks": (
        "Thank you! You have completed the survey and there are no"
        + " more questions for you to answer."
    ),
}


def manage_response(user: get_user_model(), text: str, recieved: datetime) -> str:
    """Function to manage routing for incoming text messages by providing the
    correct response for the user and saving their response if it is accepted.

    Parameters
    ----------
    user: User Model
        User that matched the phone number
    text: str
        Body of the recieved message.
    recieved: datetime
        Time that the message was recieved.

    Returns
    -------
    str
        An appropriate response message to the User
    """
    try:
        latest_session = EMASession.objects.latest("start_time")
    except EMASession.DoesNotExist:
        logger.info("No active session returned (none set).")
        return AUTO_MESSAGE["no_active_session"]

    # Find out if a session is active by seeing if one was started in the last hour
    if latest_session.is_active:
        state = SessionState.objects.get(user=user, session=latest_session)
    else:
        logger.info("No active session returned (non active).")
        return AUTO_MESSAGE["no_active_session"]

    # Strip any spaces or punctuation from the message and see if there are any more
    # questions
    text = "".join(e for e in text if e.isalnum())
    answer_expected = (
        EMAResponse.objects.filter(state=state).count()
        < EMAQuestion.objects.all().count()
    )

    # Main reply logic sequence
    if answer_expected:
        if is_valid(text):
            save_response(text, state)
            next_message = state.get_next_question()
            print(next_message)
            if next_message is None:
                return AUTO_MESSAGE["thanks"]
            else:
                state.update(next_message)
                return next_message.body
        else:
            return AUTO_MESSAGE["message_invalid"]
    else:
        return AUTO_MESSAGE["thanks"]


def is_valid(text: str):
    """Ensures the text only contains a number between 1 and 10
    """
    accepted_responses = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    if text in accepted_responses:
        return True
    else:
        return False


def save_response(text: str, state: SessionState):
    """Given some text will save it as the response to the
    last question asked as an EMARepsonse instance.
    """
    # Save response to database
    EMAResponse.objects.create(
        state=state, question=QuestionHistory.last_question(state), response=int(text),
    )
