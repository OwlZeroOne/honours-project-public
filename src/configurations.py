from defaults import *
from exercise_repository import *


class Config:
    """
    Algorithm configurations class, sets dependencies for the algorithm, pre-determined by the user and administrator.
    The functionality of this class consists of getters and setters that alter instance variables that define the
    algorithm's configuration settings.

    :param parameters: A `Parameters` instance obtained from the client class that instantiates this class.
    """
    def __init__(self, init_weight: float, target_weight: float, period: int) -> None:
        # Assign
        self._bins: int = Defaults.MAP_BINS
        self._repo: ExerciseRepository = ExerciseRepository(Defaults.LARGE_COMPENDIUM_PATH)

        # User Parameters
        self._init_weight: float = init_weight
        self._target_weight: float = target_weight
        self._period: int = period

        # Initialise ranges
        self._exercise_index_range: range = range(0, self._repo.size())
        self._exercise_duration_range: range = Defaults.exercise_duration_range()
        self._daily_exercise_count_range: list = Defaults.daily_exercise_count_range()
        self._daily_duration_range: range = Defaults.daily_duration_range()
        self._base10_schedule_range: range = Defaults.base10_schedule_range()

        # Mutation Rates
        self._mutation_rate: float = 0.7
        self._alter_rate: float = 0.6
        self._add_rate: float = 0.2
        self._delete_rate: float = 0.2

    def __str__(self) -> str:
        s = 'CONFIGURATIONS:\n'
        s += f'Number of Map Bins: {self._bins}\n'
        s += f'{self._repo}\n'
        s += f'Initial Weight: {self._init_weight}\n'
        s += f'Target Weight: {self._target_weight}\n'
        s += f'Period: {self._period}\n'
        s += f'Exercise Index Range: {self._exercise_index_range}\n'
        s += f'Exercise Duration Range: {self._exercise_duration_range}\n'
        s += f'Daily Duration Range: {self._daily_duration_range}\n'
        s += f'Daily Duration Count Range: {self._daily_exercise_count_range}\n'
        s += f'Base10 Schedule Range: {self._base10_schedule_range}\n'
        return s

    @staticmethod
    def _range_check(lo: int, hi: int, step: int) -> bool:
        """
        Conducts validation on input ranges.
        :param lo: Lower range bound (inclusive)
        :param hi: Upper range bound (inclusive)
        :param step: Steps between each element in the range.
        :return: `True` if valid range is provided. `False` if no ranges are provided.
        :raise ValueError:
        """
        # Input check
        if hi is None and lo is None:
            return True

        if (hi is None) != (lo is None):
            raise ValueError(f'`lo`, `hi`, and `step` must all be provided, or both must be `None` for default.')

        # Type check
        if not (type(hi) is int and type(lo) is int and type(step) is int):
            raise ValueError(f'Upper and lower bounds and steps, `lo`, `hi`, `step`, must be integers. Got {type(lo)}, {type(hi)}, and {type(step)}.')

        # Inequality check
        if hi <= lo:
            raise ValueError(f'Upper bound, `hi`, must be greater than than the lower bound, `lo`.')

        # Step check
        if lo % step != 0 or hi % step != 0:
            raise ValueError(f'Input bounds must be divisible by {step}.')

        return True

    # ==================================================================================================================
    #       SETTERS
    # ==================================================================================================================

    def set_exercise_duration_range(self, hi: None | int = None, lo: None | int = None) -> None:
        """
        Sets the range of exercise durations that will be allowed for the algorithmic process. The result is either a
        range, defined by the user, or a default if the respective parameter is found to be `None`. An exercise has an
        absolute minimum duration of 15 minutes, and any other duration is a multiple of 15.
        """
        parameters_present = self._range_check(lo, hi, 15)
        rng = range(lo, hi + 1, 15) if parameters_present else Defaults.exercise_duration_range()
        self._exercise_duration_range = rng

    def set_base10_schedule_range(self, lo: None | int = None, hi: None | int = None) -> None:
        """
        Sets the range of base10 schedules that will be allowed for the algorithmic process. The result is either a
        base-2 weekly schedule representation, defined by the user, or a default if the respective parameter is found to
        be `None`.
        """
        parameters_present = self._range_check(lo, hi, 1)
        rng = range(lo, hi + 1) if parameters_present else Defaults.base10_schedule_range()
        self._base10_schedule_range = rng

    def set_daily_duration_range(self, lo: None | int = None, hi: None | int = None) -> None:
        """
        Sets the range of daily durations that will be allowed for the algorithmic process. The result is either a
        `range`, or a default if the respective parameter is found to be `None`.
        :param hi: The upper bound for the range, inclusive of `hi`.
        :param lo: The lower bound for the range, inclusive of `lo`.
        :raise ValueError: If only one bound is provided, or when either of the bounds is not an integer.
        """
        parameters_present = self._range_check(lo, hi, 15)
        rng = range(lo, hi + 1, 15) if parameters_present else Defaults.daily_duration_range()
        self._daily_duration_range = rng

    def set_daily_exercise_count_range(self, lo: None | int = None, hi: None | int = None, breaks: bool = True) -> None:
        """
        Sets the range of daily exercise counts that will be allowed for the algorithmic process. The result is either
        a list of possible exercise counts, specified by the user, or a default if the respective parameter is found to
        be `None`.
        :return:
        """
        parameters_present = self._range_check(lo, hi, 1)
        rng = (
                ([0] if breaks else [])
                + list(range(lo, hi + 1) if not parameters_present else Defaults.daily_exercise_count_range())
        )
        self._daily_exercise_count_range = rng

    # ==================================================================================================================
    #       GETTERS
    # ==================================================================================================================

    def repository(self) -> ExerciseRepository:
        """
        :return: The stored `ExerciseRepository` object, containing recorded list of available exercises.
        """
        return self._repo

    def initial_weight(self) -> float:
        """
        :return: The initial weight at the time of schedule creation.
        """
        return self._init_weight

    def target_weight(self) -> float:
        """
        :return: The weight to be achieved by the user.
        """
        return self._target_weight

    def period(self) -> int:
        """
        :return: The period by which target weight is to be achieved.
        """
        return self._period

    def exercise_index_range(self) -> range:
        """
        :return: The range of exercise indexes as defined by the data source, where activities are originally stored.
        """
        return self._exercise_index_range

    def exercise_duration_range(self) -> range:
        """
        :return: The range of allowed durations, defined by the user, for a single exercise.
        """
        return self._exercise_duration_range

    def daily_exercise_count_range(self) -> list:
        """
        :return: The range of numbers of activities, defined by the user, that are allowed to take place in a single day.
        """
        return self._daily_exercise_count_range

    def daily_duration_range(self) -> range:
        """
        :return: The range of combined exercise durations, defined by the user, that are allowed to take place in a single day.
        """
        return self._daily_duration_range

    def base10_schedule_range(self) -> range:
        """
        :return: The range of decimal numbers, represented by a 7-bit, binary number (0-127).
        """
        return self._base10_schedule_range

    def bins(self) -> int:
        """
        :return: The number of bins on the Map of Elites in a single dimension.
        """
        return self._bins

    def mutation_rate(self) -> float:
        """
        :return: The rate of the super-mutation.
        """
        return self._mutation_rate

    def alteration_rate(self) -> float:
        """
        :return: The rate of the alteration sub-mutation.
        """
        return self._alter_rate

    def addition_rate(self) -> float:
        """
        :return: The rate of the addition sub-mutation.
        """
        return self._add_rate

    def deletion_rate(self) -> float:
        """
        :return: The rate of the deletion sub-mutation.
        """
        return self._delete_rate