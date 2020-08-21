from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class EMAQuestions(models.Model):
    short_name = models.CharField(max_length=50)
    body = models.CharField(max_length=160)  # 160 is number of allowed chars in an SMS


class EMASession(models.Model):
    """Data about the EMA session.

    session_id: int
        Cumulative session number since study start
    start_time: datetime
        The time and date that this session was initiated
    """

    start_time = models.DateTimeField(auto_now_add=True)
    first_question = models.ForeignKey(EMAQuestions, on_delete=models.CASCADE)

    @property
    def is_active(self):
        """Returns bool of whether 60mins have passed since the session started
        """
        diff = timezone.now() - self.start_time
        mins_elapsed = divmod(diff.seconds, 60)[0]

        if mins_elapsed > 60:
            return False
        else:
            return True


class SessionState(models.Model):
    """Data about the user's current state in the EMA survey session. There is
    one instance per user per survey session which is updated as they reply.

    questions_answered: int
        The number of questions the user has successfully answered, starting from 0
        from point of first question being sent.
    questions_sent: int
        The number of questions the user has been sent, starting from 1 at the point
        the first message is sent.
    last_updated: datetime
        The date and time that this state was last changed.
    last_question_sent: EMAQuestions
        The last question that is recording as having been sent to the user.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    session = models.ForeignKey(EMASession, on_delete=models.CASCADE)
    messages_sent = models.PositiveSmallIntegerField(default=1)
    questions_answered = models.PositiveSmallIntegerField(default=0)
    last_question_sent = models.ForeignKey(EMAQuestions, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

    def get_next_message(self):
        if self.messages_sent > EMAQuestions.objects.count():

            return


class EMAResponse(models.Model):
    session = models.ForeignKey(
        EMASession, on_delete=models.CASCADE, related_name="ema_responses"
    )
    question = models.ManyToManyField(EMAQuestions, related_name="ema_responses")
    response = models.PositiveSmallIntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
