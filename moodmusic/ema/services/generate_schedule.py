from numpy import random
from datetime import time, datetime, timedelta
from moodmusic.ema.models import StudyMeta, SessionTime


class EMASchedule:
    def __init__(self, StudyMeta: StudyMeta):
        self.StudyMeta = StudyMeta
        self.start_time = StudyMeta.start_time
        self.end_time = StudyMeta.end_time
        self.beeps_per_day = StudyMeta.beeps_per_day
        self.start_date = StudyMeta.start_date
        self.end_date = StudyMeta.end_date
        self._survey_time = self.end_time - self.start_time

    def _intervals(self) -> list:
        """Method that produces a list of tuples where each tuple is an
        interval, with all tuples spanning the number of hours a day a
        beep can be scheduled within, excluding buffer zones."""

        # Calculate the length of each daily interval block
        interval_len = self._survey_time / self.beeps_per_day

        # The buffer on the end of each interval
        buffer = 0.25 * interval_len

        # Set up the list of intervals
        intervals = []

        # Create a list of interval blocks each day should be split into.
        for beep in range(self.beeps_per_day):
            # Earliest beep time
            lower_beep_bound = round(beep * interval_len, 2)
            # Latest beep time, excluding buffer time period
            upper_beep_bound = round(((beep + 1) * interval_len) - buffer, 2)
            # Append the tuple of bounds to the list of intervals
            intervals.append((lower_beep_bound, upper_beep_bound))

        return intervals

    def _generate_beeps(self) -> list:
        """Within the predefined intervals per day, generates a list of beeps which are all
        randomly chosen within the interval range, then offset by a random number.
        Here, beeps are 2dp floats starting at 0, which need to be translated to times."""

        # Set up the list of beeps
        beeps = []

        # Define an offset value that is no larger than the interval length
        interval_len = self._survey_time / self.beeps_per_day
        rand_offset = random.uniform(0, interval_len)

        # Make a list of scheduled beeps
        for interval in self._intervals():
            # Get a random beep time in the interval
            beep_time = random.uniform(interval[0], interval[1])
            # Now add the random offset, and use modulo to make sure we wrap
            # back to beginning of survey window if it goes outside.
            beep_time = (beep_time + rand_offset) % (self._survey_time)
            # Add to the list of beeps, rounded to 2 d.p.
            beeps.append(round(beep_time, 2))

        return beeps

    def _daily_schedule(self, date: datetime.date):
        """Generate a dict of semi-random beeps within the intervals given, for a given date."""

        # The beep schedule needs to be unqiue to each date, so generate it within the daily schedule.
        # We're also sorting, as the last item can sometimes be the smallest due to modulo operations
        beeps = sorted(self._generate_beeps())

        # Get the start time for this date.
        start_datetime = datetime.combine(date, time(hour=self.start_time))

        # Intitialise a new list of times
        beep_times = {}

        # Generate a dictionary of beep times as key value pairs with number of beep in day.
        for num, beep in enumerate(beeps, start=1):
            beep_datetime = start_datetime + timedelta(hours=beep)
            beep_times[num] = beep_datetime

        return beep_times

    @property
    def schedule(self):
        """For the date range in this instance, generate a full schedule of beep times.
        Returned as a list of dicts."""

        # Set up initial variables
        one_day = timedelta(days=1)
        date = self.start_date
        day = 1
        # For each date in the range, create a daily schedule dict and add it to list
        while date <= self.end_date:
            schedule = self._daily_schedule(date)

            for beep in schedule:
                SessionTime(
                    study=self.StudyMeta, datetime=schedule[beep], day=day, beep=beep
                ).create()

            # Increase the day counter
            day += 1
            # Increase the date by one day
            date += one_day

        return schedule
