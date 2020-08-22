"""
Module to that provides utility and routing functions for EMA survey sms messaging.
"""
from django.contrib.auth import get_user_model
from datetime import datetime

from .models import EMASession, EMAResponse, SessionState, QuestionHistory


AUTO_MESSAGE = {
    "no_active_session": """There is not a survey running at the moment.
    We will message you the next time that we have questions for you.""",
    "message_invalid": """Sorry, we can only recieve messages that contains a number
    from 0 to 10 with no punctuation. Please send your response again. """,
    "thanks": """Thank you! You have completed the survey and there are no
    more questions for you to answer.""",
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
        return AUTO_MESSAGE["no_active_session"]

    # Find out if a session is active by seeing if one was started in the last hour
    if latest_session.is_active:
        state = SessionState.objects.get(user=user, session=latest_session)
    else:
        return AUTO_MESSAGE["no_active_session"]

    # Strip any spaces or punctuation from the message and see if there are any more
    # questions
    text = "".join(e for e in text if e.isalnum())
    next_message = state.get_next_question()

    # Main reply logic sequence
    if next_message is None:
        # There is no next message, so just say thanks
        return AUTO_MESSAGE["thanks"]
    elif (next_message is not None) and (is_valid(text) is False):
        # There is a next message, but the text is invalid, so ask again
        return AUTO_MESSAGE["message_invalid"]
    else:
        # Assuming this means the response is valid...
        # Save the response to the db
        save_response(text, state)
        # Update the state and record the last question asked
        state.update(next_message)
        # Return the string of text for the next question
        return next_message.body


def is_valid(text: str):
    """Ensures the text only contains a number between 0 and 10
    """
    accepted_responses = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

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
