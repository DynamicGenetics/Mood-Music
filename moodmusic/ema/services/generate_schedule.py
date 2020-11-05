import random as rnd
from datetime import time, datetime, timedelta


class EMASchedule:
    def __init__(
        self,
        start_time: float,
        end_time: float,
        beeps_per_day: int,
        start_date: datetime.date,
        end_date: datetime.date,
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.beeps_per_day = beeps_per_day
        self.start_date = start_date
        self.end_date = end_date
        self._survey_time = end_time - start_time

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
        rand_offset = rnd.randrange(0, interval_len * 100) / 100

        # Make a list of scheduled beeps
        for interval in self._intervals():
            # Get a random beep time in the interval
            # Randrange only works with ints, so *100 first
            beep_time = rnd.randrange(interval[0] * 100, interval[1] * 100)
            # Now add the random offset, and use modulo to make sure we wrap
            # back to beginning of survey window if it goes outside.
            beep_time = ((beep_time / 100) + rand_offset) % (self._survey_time)
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
        schedule = []
        date = self.start_date

        # For each date in the range, create a daily schedule dict and add it to list
        while date <= self.end_date:
            schedule.append(self._daily_schedule(date))
            date += one_day

        return schedule
