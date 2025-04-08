class Defaults:
    MAX_EXERCISES_PER_SCHEDULE = 10
    """Maximum number of exercise types per schedule."""
    MAX_EXERCISE_DURATION = 12 * 60
    """Maximum duration of an exercise in minutes."""
    MAX_DAILY_DURATION = 8 * 60
    """Maximum duration of the daily workout in minutes."""
    MAX_BASE_10_SCHEDULE = 2 ** 7 - 1
    """Maximum base 10 binary representation of a weekly schedule."""
    MAX_DAILY_EXERCISE_COUNT = 10
    """Maximum number of exercises in a day."""


    LARGE_COMPENDIUM_PATH = "./../data/compendium_large.csv"
    """Path to the large Compendium of Physical Activities csv file (522 rows)."""
    MEDIUM_COMPENDIUM_PATH = "./../data/compendium_medium.csv"
    """Path to the large Compendium of Physical Activities csv file (260 rows)."""
    SMALL_COMPENDIUM_PATH = "./../data/compendium_small.csv"
    """Path to the large Compendium of Physical Activities csv file (65 rows)."""


    MAP_BINS = 20
    """Number of bins in a single dimension for the map of elites."""
    WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    """List of names of days of the week."""


    MIN_DAILY_EXERCISE_COUNT = 0
    """Minimum number of exercises in a day."""
    MIN_EXERCISE_DURATION = 15
    """Minimum duration of an exercise in minutes."""
    MIN_DAILY_DURATION = 0
    """Minimum duration of the daily workout in minutes."""
    MIN_BASE_10_SCHEDULE = 1
    """Minimum base 10 binary representation of a weekly schedule."""

    @staticmethod
    def exercise_duration_range() -> range:
        """
        :return: `range` - The default range of minutes for a single exercise's duration.
        """
        return range(15, Defaults.MAX_EXERCISE_DURATION + 1, 15)

    @staticmethod
    def daily_duration_range() -> range:
        """
        :return: `range` - The default range of minutes for a single day of workout.
        """
        return range(Defaults.MIN_DAILY_DURATION, Defaults.MAX_DAILY_DURATION + 1)

    @staticmethod
    def base10_schedule_range() -> range:
        """
        :return: `range` - The default range of base 10 binary values for determination of a weekly schedule.
        """
        return range(Defaults.MIN_BASE_10_SCHEDULE, Defaults.MAX_BASE_10_SCHEDULE + 1)

    @staticmethod
    def daily_exercise_count_range():
        """
        :return: `range` - The default range of numbers of exercises in a single day.
        """
        return range(Defaults.MAX_DAILY_EXERCISE_COUNT, Defaults.MAX_DAILY_EXERCISE_COUNT + 1)