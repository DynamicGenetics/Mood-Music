"""
Module to that provides utility and routing functions for EMA survey sms messaging.
"""

import PhoneNumber
from django.utils import timezone
from datetime import datetime, timedelta

from .models import EMASession


AUTO_MESSAGE = {
    no_active_session: """Sorry, the last survey period has now expired.
    We'll message you the next time we have questions for you to complete.""",
    message_invalid: """Sorry, we can only recieve messages that contains a number
    from 0 to 10 with no punctuation. Please send your response again. """,
    thanks: """Thank you! You have completed the survey."""
}


def manage_response(number: str, text: str, recieved: datetime) -> str:
    """Function to manage routing for incoming text messages by providing the
    correct response for the user and saving their response if it is accepted.

    Parameters
    ----------
    number: str
        User's phone number
    text: str
        Body of the recieved message.
    recieved: datetime
        Time that the message was recieved.

    Returns
    -------
    str
        An appropriate response message to the User
    """

    user = get_user_model().objects.filter(phone_number=number)

    # Find out if a session is active by seeing if one was started in the last hour
    now = timezone.now()
    one_hour_ago = now - timedelta(minutes=60)
    try:
        session = EMASession.objects.filter(start_time__range=[now, one_hour_ago]).latest('start_time')
        state = SessionState.objects.filter(user=user, session=session)
    except EMASession.DoesNotExist:
        return AUTO_MESSAGE['no_active_session']

    # Assuming the above was successful, save the response and get the next message unless invalid
    if is_valid(text):
        save_response(state)
        return next_message(state)
    else:
        return AUTO_MESSAGE['message_invalid']


def is_valid(text: str):
    """Ensures the text only contains a number between 0 and 10

    Parameters
    ----------
    text: str
        Recieved message text body

    Returns
    -------
    bool
        True if message is valid, False otherwise
    """
    message = text.strip()
    accepted_responses = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    if message in accepted_responses:
        return True
    else:
        return False


def save_response(text: str, state: SessionState):

    # Save response
    new_emaresponse = EMAResponse.create(
        session_no=state.session,
        question=state.last_question_sent,
        user=state.user,
        response=int((text.strip()),
    )

    # Update questions answered in the user's session state
    state.questions_answered =+ 1


def next_message(state: SessionState):
    """Given the state of a 

    Parameters
    ----------
    state : SessionState
        [description]
    """



    # If they have answered as many questions as are in the database...
    if state.messages_sent > EMAQuestions.objects.count()

    if (state.questions_answered == EMAQuestions.objects.count()) :
        
    elif state.questions_answered  .count():

    #If the state.questions answered == number of quesiotns in EMAQuestions then send 'thank you'
        # If the state.messages_sent
    # Get the questions that have been answered in this session from EMAResponses
    # Get the available questions in EMAQuestions
    # Randomly pick a question from the remaining questions

    