import pytest
import time

from hypothesis.extra.django import TestCase
from apscheduler.datastores.memory import MemoryScheduleStore

from .factories import meta


class TestScheduleSignal(TestCase):
    def setUp(self):
        self.store = MemoryScheduleStore()

    @pytest.mark.django_db
    def test_signal_triggers_scheduler(self):
        studymeta = meta().example()
        studymeta.save()
        time.sleep(10)

        # Get scheduler
        self.store.get_schedules({"main"})
