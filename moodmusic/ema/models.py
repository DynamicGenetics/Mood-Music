from django.db import models
from django.contrib.auth import get_user_model


class EMAQuestions(models.Model):
    unique_id = models.IntegerField(primary_key=True)
    short_name = models.CharField(max_length=50)
    question = models.CharField(
        max_length=160
    )  # 160 is number of allowed chars in an SMS


class EMASession(models.Model):
    """Data about the EMA session.

    session_id: int
        Cumulative session number since study start
    start_time: datetime
        The time and date that this session was initiated
    """

    session_id = models.IntegerField()
    start_time = models.DateTimeField()

    @property
    def day_of_study():
        """Works out which day and session of the study an
        EMA session is.
        """
        # TODO Work out how to figure this out.
        return


class SessionState(models.Model):
    """Data about the user's current state in the EMA survey session.

    state: int
        Indicates how many accepted replies have been recieved, starting from 0
        from point of first message being sent.
    started_at: datetime
        The date and time that this state was reached by the user.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    session_no = models.ForeignKey(EMASession, on_delete=models.CASCADE)
    state = models.PositiveSmallIntegerField()
    started_at = models.DateTimeField()

    def get_current_state():
        """Find and return a user's current state.
        """


class EMAResponse(models.Model):
    session_no = models.ForeignKey(
        EMASession, on_delete=models.CASCADE, related_name="ema_responses"
    )
    question = models.ManyToManyField(EMAQuestions, related_name="ema_responses")
    response = models.PositiveSmallIntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
