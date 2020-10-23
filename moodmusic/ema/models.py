import random
import logging

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


logger = logging.getLogger(__name__)


class EMAQuestion(models.Model):
    short_name = models.CharField(max_length=50)
    body = models.CharField(max_length=160)  # 160 is number of allowed chars in an SMS


class EMASession(models.Model):
    """Data about the EMA session.

    start_time: datetime
        The time and date that this session was initiated
    """

    start_time = models.DateTimeField(auto_now_add=True)

    @property
    def is_active(self):
        """Returns bool of whether 60mins have passed since the session started
        """
        diff = timezone.now() - self.start_time
        day2min = diff.days * 1440  # Days * Minutes in a Day
        sec2min = divmod(diff.seconds, 60)[0]
        mins_elapsed = day2min + sec2min

        if mins_elapsed >= 60:
            return False
        else:
            return True


class SessionState(models.Model):
    """Data about the user's current state in the EMA survey session. There is
    one instance per user per survey session which is updated as they reply.

    questions_asked: EMAQuestion
        The questions the user has been sent.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    session = models.ForeignKey(EMASession, on_delete=models.CASCADE)
    questions_asked = models.ManyToManyField(EMAQuestion, through="QuestionHistory")

    def get_next_question(self):
        # If they have answered less than than number of questions available
        all_qs = EMAQuestion.objects.all()
        answered_qs = self.questions_asked.all()
        # Get the remaining available questions and choose one.
        remaining = all_qs.difference(answered_qs)
        if remaining.count() == 1:
            return remaining.first()
        else:
            try:
                return random.choice(remaining)
            except IndexError:
                logger.info("Index Error Raised - No more questions to ask")
                return None

    def update(self, next_message):
        self.questions_asked.add(
            next_message, through_defaults={"state": self, "time_asked": timezone.now()}
        )


class QuestionHistory(models.Model):
    """Intermediate model that records the questions that have been asked to a
    user in a given session with the time that they were asked.

    Includes a method to find the last question asked in a user session, and to
    find out how many questions have been asked in a user session.
    """

    state = models.ForeignKey(SessionState, on_delete=models.CASCADE)
    question = models.ForeignKey(EMAQuestion, on_delete=models.CASCADE)
    time_asked = models.DateTimeField(auto_now_add=True)

    @classmethod
    def last_question(cls, state):
        last_asked = cls.objects.filter(state=state).latest("time_asked")
        return last_asked.question

    @classmethod
    def questions_asked(cls, state):
        return cls.objects.filter(state=state).count()


class EMAResponse(models.Model):
    # Note that the session state model contains both user and session details
    state = models.ForeignKey(
        SessionState, on_delete=models.CASCADE, related_name="ema_responses"
    )
    question = models.ForeignKey(
        EMAQuestion, on_delete=models.CASCADE, related_name="ema_responses"
    )
    response = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class StudyMeta(models.Model):
    """Information about the EMA study used to generate a schedule."""

    start_time = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(24)]
    )
    end_time = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(24)]
    )
    beeps_per_day = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    @property
    def survey_time(self):
        return self.end_time - self.start_time
