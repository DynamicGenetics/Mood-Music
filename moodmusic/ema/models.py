from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

# Largely from by Twilio's sample Appointment Reminders and Automated Survey projects
# https://github.com/TwilioDevEd/automated-survey-django/blob/master/automated_survey/models.py
# https://github.com/TwilioDevEd/appointment-reminders-django/blob/next/reminders/models.py


class Survey(models.model):
    """Survey model that records the title and key information about
    when the surveys will be administered.

    Parameters
    ----------
    title : str
        Title of the survey
    start_date: datetime
        Date that the surveys should start
    end_date: datetime
        Date that the surveys should end
    daily_start: time
        Time of day that the survey window can start
    daily_end: time
        Time of day that the survey window will end
    surveys_perday: int
        Number of surveys to be sent per day
    """

    title = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    daily_start = models.TimeField()
    daily_end = models.TimeField()
    surveys_perday = models.IntegerField(MinValueValidator(1))

    @property
    def responses(self):
        return QuestionResponse.objects.filter(question__survey__id=self.id)

    @property
    def first_question(self):
        return Question.objects.filter(survey__id=self.id).order_by("id").first()

    def __str__(self):
        return "%s" % self.title


class Question(models.model):
    """Stores a survey question.
    """

    # Max length of a SMS message is 160 chars
    body = models.CharField(max_length=160)
    survey = models.ForeignKey(Survey)

    def next(self):
        """Returns the next question in the survey, if there is one"""
        survey = Survey.objects.get(id.self.survey_id)
        next_questions = survey.question_set.order_by("id").filter(id__gt=self.id)

        return next_questions[0] if next_questions else None

    def __str__(self):
        return "%s" % self.body


class QuestionResponse(models.Model):
    """Records the user response to a question"""

    response = models.IntegerField()
    call_sid = models.CharField(max_length=255)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question = models.ForeignKey(Question)

    def __str__(self):
        return "%s" % self.response

    def as_dict(self):
        return {
            "body": self.question.body,
            "response": self.response,
            "user": self.user,
        }
