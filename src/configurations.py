from defaults import *
from exercise_repository import *

class Config:
    """
    Algorithm configurations class, sets dependencies for the algorithm, pre-determined by the user and administrator.
    The functionality of this class consists of getters and setters that alter instance variables that define the
    algorithm's configuration settings.
    """
    def __init__(self, init_weight: float, target_weight: float, period: int) -> None:
        # Assign
        self._total_evals: int = Defaults.EVAL_TIMES
        self._init_times: int = Defaults.INIT_TIMES
        self._bins: int = Defaults.MAP_BINS
        self._repo: ExerciseRepository = ExerciseRepository(Defaults.SMALL_COMPENDIUM_PATH)

        # User Parameters
        self._init_weight: float = init_weight
        self._target_weight: float = target_weight
        self._period: int = period

        # Initialise ranges
        self._exercise_index_range: range = range(0, self._repo.size())
        self._exercise_duration_range: range = Defaults.exercise_duration_range()
        self._daily_exercise_count_range: list = Defaults.daily_exercise_count_range()
        self._daily_duration_range: range = Defaults.daily_duration_range()
        self._tolerable_days: str = Defaults.TOLERABLE_SCHEDULE

        # Mutation Rates
        self._mutation_rate: float = 0.7
        self._alter_rate: float = 0.6
        self._add_rate: float = 0.2
        self._delete_rate: float = 0.2

    def __str__(self) -> str:
        s = 'CONFIGURATIONS:\n'
        s += f'Number of Initialisations: {self._init_times}\n'
        s += f'Number of Evaluations: {self._total_evals}\n'
        s += f'Number of Map Bins: {self._bins}\n'
        s += f'{self._repo}\n'
        s += f'Initial Weight: {self._init_weight}\n'
        s += f'Target Weight: {self._target_weight}\n'
        s += f'Period: {self._period}\n'
        s += f'Exercise Index Range: {self._exercise_index_range}\n'
        s += f'Exercise Duration Range: {self._exercise_duration_range}\n'
        s += f'Daily Duration Range: {self._daily_duration_range}\n'
        s += f'Daily Exercise Count Range: {self._daily_exercise_count_range}\n'
        s += f"Tolerable Days: {self._tolerable_days}\n"
        return s

    @staticmethod
    def _range_check(lo: int, hi: int, step: int) -> None:
        """
        Conducts validation on input ranges.
        :param lo: Lower range bound (inclusive)
        :param hi: Upper range bound (inclusive)
        :param step: Steps between each element in the range.
        :return: `True` if valid range is provided. `False` if no ranges are provided.
        :raise ValueError:
        """
        # Type check
        if not (type(hi) is int and type(lo) is int and type(step) is int):
            raise ValueError(f'Upper and lower bounds and steps, `lo`, `hi`, `step`, must be integers. Got {type(lo)}, {type(hi)}, and {type(step)}.')

        # Inequality check
        if hi <= lo:
            raise ValueError(f'Upper bound, `hi`, must be greater than than the lower bound, `lo`.')

        # Step check
        if lo % step != 0 or hi % step != 0:
            raise ValueError(f'Input bounds must be divisible by {step}.')

    # ==================================================================================================================
    #       SETTERS
    # ==================================================================================================================

    def set_tolerable_days(self, tolerable_days: str) -> None:
        """
        Sets the days of the week that will be accepted by the algorithm for schedule construction.
        :param tolerable_days: `str` - Base-2 representation of tolerable days of the week.
        """
        # Type check
        if not isinstance(tolerable_days, str):
            raise TypeError(f'`tolerable_days` must be a string, not {type(tolerable_days).__name__}.')

        # Character check
        l = [d in '01' for d in tolerable_days]
        if not all(l):
            raise ValueError(f"Tolerable days must be represented by a binary number string; characters must be either '1' or '0'")

        # Length check
        if len(tolerable_days) != 7:
            raise ValueError(f'Input string must be 7 characters long! Got {len(tolerable_days)}.')

        self._tolerable_days = tolerable_days

    def set_exercise_duration_range(self, lo:int, hi: int) -> None:
        """
        Sets the range of exercise durations that will be allowed for the algorithmic process. An exercise has an
        absolute minimum duration of 15 minutes, and any other duration is a multiple of 15.
        """
        self._range_check(lo, hi, 15)
        rng = range(lo, hi + 1, 15)
        self._exercise_duration_range = rng

    def set_daily_duration_range(self, lo:int, hi: int) -> None:
        """
        Sets the range of daily durations that will be allowed for the algorithmic process.
        :param hi: The upper bound for the range, inclusive of `hi`.
        :param lo: The lower bound for the range, inclusive of `lo`.
        :raise ValueError: If only one bound is provided, or when either of the bounds is not an integer.
        """
        self._range_check(lo, hi, 15)
        rng = range(lo, hi + 1, 15)
        self._daily_duration_range = rng

    def set_daily_exercise_count_range(self, lo:int, hi: int, breaks: bool = True) -> None:
        """
        Sets the range of daily exercise counts that will be allowed for the algorithmic process.
        :param hi: The upper bound for the range, inclusive of `hi`.
        :param lo: The lower bound for the range, inclusive of `lo`.
        :param breaks: Whether the schedule includes day breaks.
        """
        self._range_check(lo, hi, 1)
        rng = ([0] if breaks else []) + list(range(lo, hi + 1))
        self._daily_exercise_count_range = rng

    def set_total_evaluations(self, total_evals: int) -> None:
        """
        Sets the total number of evaluations for the algorithm to iterate over.
        :param total_evals: `int` - The positive number of evaluations.
        """
        if not isinstance(total_evals, int):
            raise TypeError("`total_evals` must be an integer.")

        if total_evals <= 0:
            raise ValueError(f'`total_evals` must be greater than 0. Got {total_evals}.')

        self._total_evals = total_evals

    def set_total_initialisations(self, init_times: int) -> None:
        """
        Sets the number of initialisation times before the algorithm begins mutating solutions.
        :param init_times: `int` - The new number of initialisations.
        """
        if not isinstance(init_times, int):
            raise TypeError("`init_times` must be an integer.")

        if init_times <= 0:
            raise ValueError(f'`init_times` must be greater than 0. Got {init_times}.')

        self._init_times = init_times

    # ==================================================================================================================
    #       GETTERS
    # ==================================================================================================================

    def total_initialisations(self) -> int:
        """
        :return: The number of initialisation times before the algorithm begins mutating solutions.
        """
        return self._init_times

    def total_evaluations(self) -> int:
        """
        :return: The total number of evaluations for the algorithm to iterate over.
        """
        return self._total_evals

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