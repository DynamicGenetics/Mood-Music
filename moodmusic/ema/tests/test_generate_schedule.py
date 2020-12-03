from hypothesis import given, settings
from hypothesis.extra.django import TestCase

from moodmusic.ema.services.generate_schedule import EMASchedule

from .factories import meta


class TestEMASchedule(TestCase):
    @given(meta())
    @settings(deadline=None)
    def test_intervals(self, meta):
        """Test that schedules can be generated.
        """
        meta.save()
        EMASchedule(meta).schedule

    # def test_time_limits(self):
    #     ##Use hypothesis to generate a range of
    #     # EMA schedules.
    #     # Make sure none of them are scheduled outside
    #     # of the limits defined.
    #     EMASchedule(instance).schedule


#    def test_time_dist(self):
#        # Hypothesis
#        # Test that distance between times is minimum
#        # the distance they are seperated by in the algorithm.

#     def test_dates(self):
#         # Test that the dates put in are the dates that are generated.

#     def test_save(self):
#         # Test that the place these are saved is where they are saved.

#     def test_objects(self):
#         # Test that the right number of objects were entered into the database
