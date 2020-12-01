from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudyMeta
from .services.generate_schedule import EMASchedule
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=StudyMeta)
def schedule_study(sender, instance, **kwargs):
    # First, delete any pre-existing ema times for this study meta
    if instance.session_times:
        existing_ema = instance.session_times.all()
        qs_size = existing_ema.count()
        existing_ema.delete()
        logger.info("{} existing EMA session times deleted.".format(qs_size))

    # Regenerate the schedule and save it to the database.
    EMASchedule(instance).schedule
    # Log
    logger.info("Schedule generated")
