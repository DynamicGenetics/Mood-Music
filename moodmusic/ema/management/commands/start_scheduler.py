# https://github.com/jarekwg/django-apscheduler

import logging
import pytz
from datetime import time, datetime

from django.conf import settings
from django.core import management

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from moodmusic.ema.models import StudyMeta, SessionTime

logger = logging.getLogger(__name__)


def send_eve_text_job():
    """Calls management command "send_evening_text"."""
    management.call_command("send_evening_text")


def get_spotify_history_job():
    """Calls management command "get_recent_history"."""
    management.call_command("get_recent_history")


def send_ema_job():
    """Calls management command "send_ema"."""
    management.call_command("send_ema")


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def add_ema_jobs(scheduler):
    """
    Function to add all the EMA SessionTime objects (generated by the generate_schedule.py
    management command) as jobs to the Django JobStore.
    Jobs are named with convention "ema-day-{day number}-beep-{beep number}".

    Parameters
    ----------
    scheduler : APScheduler object
        The APS Scheduler that jobs should be passed to.
    """
    # Get all of the saved sessiontime objects
    jobs = SessionTime.objects.all()

    # Iterate over the jobs and add them to the scheduler.
    # Use the iterator in case there are a large number of jobs.
    for job in jobs.iterator():
        scheduler.add_job(
            send_ema_job,
            trigger=DateTrigger(run_date=job.datetime),
            id="ema-day-{}-beep-{}".format(job.day, job.beep),
            max_instances=1,
            replace_existing=True,
        )


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE, id="main")
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Get the start and end dates from StudyMeta - assumes there is only one StudyMeta object.
        meta = StudyMeta.objects.all().first()
        # Make these datetimes, starting at beginning/end of the bookend days, UTC timezone aware.
        study_start = datetime.combine(meta.start_date, time(0, 1)).replace(
            tzinfo=pytz.UTC
        )
        study_end = datetime.combine(meta.end_date, time(23, 59)).replace(
            tzinfo=pytz.UTC
        )

        # EMA TEXT MESSAGES
        add_ema_jobs(scheduler)
        logger.info("Added all EMA jobs.")

        # EVENING TEXT MESSAGES
        scheduler.add_job(
            send_eve_text_job,
            trigger=CronTrigger(hour="20", minute="30"),  # 20:30 every evening
            id="evening_texts",
            max_instances=1,
            replace_existing=True,
            start_date=study_start,
            end_date=study_end,
        )
        logger.info("Added daily job: end of day text.")

        # SPOTIFY API COLLECTOR
        scheduler.add_job(
            get_spotify_history_job,
            trigger=CronTrigger(minute="*/25"),  # Every 25 minutes
            id="spotify_history",
            max_instances=1,
            replace_existing=True,
            start_date=study_start,
            end_date=study_end,
        )
        logger.info("Added every 25 minutes job: 'spotify_history'.")

        # DELETE OLD JOBS FROM DATABASE
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon",
                hour="00",
                minute="00",
                start_date=study_start,
                end_date=study_end,
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
