from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudyMeta
from .services.generate_schedule import EMASchedule
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=StudyMeta)
def schedule_study(sender, instance, **kwargs):
    # Generate a schedule and save it to the database.
    EMASchedule(instance).schedule
    # Holder action, need to work this part out
    logger.info("Schedule generated")
