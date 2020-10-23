from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudyMeta
from .services.generate_schedule import EMASchedule
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=StudyMeta)
def schedule_study(sender, instance, **kwargs):
    schedule = EMASchedule(
        instance.start_time,
        instance.end_time,
        instance.beeps_per_day,
        instance.start_date,
        instance.end_date,
    )
    # Holder action, need to work this part out
    logger.info("Schedule generated")
