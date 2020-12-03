import random
import pytest

import hypothesis.strategies as st
from hypothesis import given
from hypothesis.extra.django import TestCase

from django.db.models import signals
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

from datetime import timedelta, date
from freezegun import freeze_time

from moodmusic.ema.models import (
    EMAQuestion,
    EMASession,
    SessionState,
    QuestionHistory,
    StudyMeta,
)


def create_EMASession(mins_ago: int):
    """Creates an EMA session instance.
    minsoff is how many minutes ago the instance should
    have been 'created'.
    """
    # Mock the start time of the session (auto-added on creation)
    start_time = timezone.now() - timedelta(minutes=mins_ago)
    with freeze_time(start_time):
        session = EMASession.objects.create()
        return session


class TestEMASession(TestCase):
    @given(st.integers(min_value=0, max_value=59))
    def test_is_active(self, mins_ago):
        session = create_EMASession(mins_ago)
        assert session.is_active is True

    # 1576800 is 3 years in minutes
    @given(st.integers(min_value=60, max_value=1576800))
    def test_is_not_active(self, mins_ago):
        session = create_EMASession(mins_ago)
        assert session.is_active is False


class TestSessionState(TestCase):
    def setUp(self):
        # Add two sample questions
        EMAQuestion.objects.create(short_name="name1", body="Some text")
        EMAQuestion.objects.create(short_name="name2", body="Some more text")
        # Add a pretend person
        user = get_user_model().objects.create()
        # Add a session
        session = EMASession.objects.create()
        # Start a session state and add the first question
        SessionState.objects.create(user=user, session=session)

    def test_update(self):
        # Get the state we set up
        state = SessionState.objects.all()[0]
        # Get a random choice of EMA question
        question = random.choice(EMAQuestion.objects.all())
        # Add the question to the state
        state.update(question)
        # Get the QuerySet of questions asked in that state, then
        # check that the question we just added is in there.
        assert state.questions_asked.filter(id=question.id).exists()

    def test_get_next_question(self):
        """For when there are more questions to ask
        """
        state = SessionState.objects.all()[0]

        # Add a random next question to the state
        question = random.choice(EMAQuestion.objects.all())
        state.update(question)
        # Get the next question
        next_question = state.get_next_question()
        # Make sure next question is not in the set of already asked questions
        assert state.questions_asked.filter(id=next_question.id).exists() is False
        assert next_question is not None

    def test_get_next_question_none(self):
        """For when there are no more questions to ask
        """
        state = SessionState.objects.all()[0]

        # Add all the questions to the state
        for question in EMAQuestion.objects.all():
            state.update(question)

        assert state.get_next_question() is None

    def tearDown(self):
        pass


class TestQuestionHistory(TestCase):
    def setUp(self):
        # Add two sample questions
        EMAQuestion.objects.create(short_name="name1", body="Some text")
        EMAQuestion.objects.create(short_name="name2", body="Some more text")
        # Add a pretend person
        user = get_user_model().objects.create()
        # Add a session
        session = EMASession.objects.create()
        # Start a session state and add the first question
        SessionState.objects.create(user=user, session=session, id=1)

    def test_last_question(self):
        state = SessionState.objects.get(id=1)
        question = EMAQuestion.objects.get(short_name="name2")
        state.update(question)
        last_q = QuestionHistory.last_question(state)

        assert last_q == question

    def test_questions_asked(self):
        state = SessionState.objects.get(id=1)
        for question in EMAQuestion.objects.all():
            state.update(question)

        assert (
            QuestionHistory.questions_asked(state) == EMAQuestion.objects.all().count()
        )


class TestStudyMeta(TestCase):
    def setUp(self):
        # Make sure we don't trigger the scheduler
        signals.post_save.disconnect(StudyMeta)

    def test_dates(self):
        """Check save method prevents dates in wrong order"""
        # Start date cannot be in the past
        with pytest.raises(ValidationError):
            StudyMeta.objects.create(
                start_date=date.today() - timedelta(days=1),
                end_date=date.today() + timedelta(days=1),
            )

        # Start date must not be before end date
        with pytest.raises(ValidationError):
            StudyMeta.objects.create(
                start_date=date.today() + timedelta(days=10),
                end_date=date.today() + timedelta(days=9),
            )

    def test_times(self):
        """Check save methods prevents times in wrong order"""
        # Start time cannot be before the end time
        with pytest.raises(ValidationError):
            StudyMeta.objects.create(
                start_date=date.today(),
                end_date=date.today() + timedelta(days=5),
                start_time=6,
                end_time=5,
            )
