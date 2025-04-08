import random as rnd
from configurations import *


class Gene:
    """
    The `Gene` represents a combination of phenotypic exercise parameters for the genetic algorithm. A new instance
    invokes a random generation of genes, defined in the configurations object.
    :var _config: `Config` - The configurations objects that holds all necessary settings.
    :var _exercise_index: `int` - The index of the exercise.
    :var _duration: `int` - The duration of the exercise in minutes.
    :var _base10_schedule: `int` - Binary schedule representation a decimal value.
    """

    def __init__(self, config: Config, other=None) -> None:
        """
        A new `Gene` instance is created which initialises randomised genotypic traits,that adheres to the settings
        defined in the configurations object. If another gene is passed in the case of creating a new `Exercise`
        object, the other gene's traits are inherited and passed onto the child class object.

        :param config: `Config` - The configuration object from which settings are extracted.
        :param other: `Gene` - The gene object from which traits will be inherited.
        """
        if other is not None:
            if not (isinstance(other, Gene)):
                raise TypeError(f"Improper input parameter type for `other`. Should be `Gene`. Got {type(other)}")

        self._config = config

        # Generate and store random gene attribute values
        self._exercise_index = self._random_index() if other is None else other.exercise_index()
        self._duration = self._random_duration() if other is None else other.duration()
        self._base10_schedule = self._random_schedule() if other is None else other.schedule_to_base(10)

        # Delete the unused instance
        if other is not None:
            del other

    def __str__(self) -> str:
        return str(self.to_list())

    def _random_index(self) -> int:
        """
        :return: A random exercise index within range.
        """
        return rnd.choice(self._config.exercise_index_range())

    def _random_duration(self) -> int:
        """
        :return: A random exercise duration within range.
        """
        return rnd.choice(self._config.exercise_duration_range())

    def _random_schedule(self) -> int:
        """
        :return: A random base-10 schedule within range (1-127).
        """
        return rnd.choice(self._config.base10_schedule_range())

    def _schedule_to_week_days(self):
        base2_schedule = self.schedule_to_base(2)
        week = Defaults.WEEK
        schedule = []
        for i in range(7):
            if base2_schedule[i] == '1':
                schedule.append(week[i])
            elif base2_schedule[i] != '0':
                raise ValueError(f"Invalid binary value, {base2_schedule[i]}.")

        return schedule

    def exercise_index(self) -> int:
        """
        :return: The index of the exercise with respect to the exercise repository.
        """
        return self._exercise_index

    def duration(self) -> int:
        """
        :return: The duration of the exercise.
        """
        return self._duration

    def schedule_to_base(self, base: int) -> str | int:
        """
        :return: The weekly exercise schedule as either a binary (base-2) number string, or decimal (base-10) number integer.
        """
        if base == 2:
            return format(self._base10_schedule, '0{}b'.format(7))
        elif base == 10:
            return self._base10_schedule
        else:
            raise ValueError(f"Unexpected number base! Expecting 2 for binary or 10 for decimal. Got {base}.")

    def exercise_days(self):
        """
        :return: A list of days of the week when the exercise takes place.
        """

        return self._schedule_to_week_days()

    def to_list(self) -> list[int]:
        """
        :return: The gene as a list of phenotypic parameters in the form `[exercise_index, exercise_duration, base10_schedule]`.
        """
        return [self._exercise_index, self._duration, self._base10_schedule]

    def alter(self) -> None:
        """
        Performs an alteration mutation to a random attribute of the gene.
        """
        param_index = rnd.choice(list(range(len(self.to_list()))))

        if param_index == 0:  # Generate random index
            self._exercise_index = self._random_index()
        elif param_index == 1:  # Generate random duration
            self._duration = self._random_duration()
        elif param_index == 2:  # Generate random base-10 schedule
            self._base10_schedule = self._random_schedule()
        else:
            raise ValueError(f"Unexpected value of gene index ({param_index}).")