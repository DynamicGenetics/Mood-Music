import logging

from django.db.models.signals import post_save
from django.core import management
from django.dispatch import receiver

from .models import StudyMeta
from .services.generate_schedule import EMASchedule

logger = logging.getLogger(__name__)


@receiver(post_save, sender=StudyMeta)
def schedule_study(sender, instance, **kwargs):
    """A post-save instruction when generating the StudyMeta to start the scheduler
    if the user has indicated start_scheduler as 'true'.
    """

    if instance.start_scheduler:

        # First, delete any pre-existing ema times for this study meta
        if instance.session_times:
            existing_ema = instance.session_times.all()
            qs_size = existing_ema.count()
            existing_ema.delete()
            logger.info("{} existing EMA session times deleted.".format(qs_size))

        # (Re)generate the schedule and save it to the database.
        EMASchedule(instance).schedule
        # Log
        logger.info("Schedule generated")
        # !! Start scheduler !!
        management.call_command("start_scheduler")
        logger.info(
            "Study scheduler started for StudyMeta labelled {}".format(instance.label)
        )
