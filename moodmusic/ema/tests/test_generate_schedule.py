from moodmusic.ema.services.generate_schedule import EMASchedule
from moodmusic.ema.models import StudyMeta

import hypothesis.strategies as st
from hypothesis import given
from hypothesis.extra.django import TestCase


class TestEMASchedule(TestCase):
    def test_intervals(self):
        StudyMeta()
