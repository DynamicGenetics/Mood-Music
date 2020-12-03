import datetime

from hypothesis import given, assume, settings
from hypothesis.extra.django import TestCase
from hypothesis import strategies as st

from moodmusic.ema.services.generate_schedule import EMASchedule
from moodmusic.ema.models import StudyMeta


@st.composite
def meta(draw):
    """Custom strategy for StudyMeta objects.
    This is needed so that dates and times are in the correct order.
    """
    # Strategies for the data types needed
    dates = st.dates(min_value=datetime.date.today())
    times = st.floats(min_value=0, max_value=24)
    beeps = st.integers(min_value=1, max_value=10)
    days = st.integers(min_value=1, max_value=200)
    labels = st.text(alphabet=st.characters(blacklist_categories=("Cc", "Cs")))
    # Draw from the strategies
    # Study Dates (start plus no. of days)
    start_date = draw(dates)
    end_date = start_date + datetime.timedelta(days=draw(days))

    # Study Times
    time1 = draw(times)
    time2 = draw(times)
    assume(time1 != time2)
    start_time = min(time1, time2)
    end_time = max(time1, time2)

    return StudyMeta(
        label=draw(labels),
        start_time=start_time,
        end_time=end_time,
        beeps_per_day=draw(beeps),
        start_date=start_date,
        end_date=end_date,
    )


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
