import datetime

from hypothesis import assume
from hypothesis import strategies as st

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
