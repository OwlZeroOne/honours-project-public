# from chromosome import *
# from configurations import *
from gene import *

class Exercise(Gene):
    """
    The phenotypic representation of a single gene. Contains concrete information regarding a single exercises.
    :var _name: The exercise name.
    :var _tag: The category of the exercise.
    :var _met: The exercise's MET Value.
    """
    def __init__(self, gene: Gene, config) -> None:
        """
        The phenotypic representation of a single gene. Contains concrete information regarding a single exercises.
        :param gene: `Gene` - The gene instance from which to inherit and translate from.
        :param config: `Config` - The configurations object that stores all necessary settings.
        """
        super().__init__(config, other=gene)
        self._name: str = ''
        self._tag: str = ''
        self._met: float = 0
        self._update_exercise()

    def __str__(self) -> str:
        s =   "EXERCISE PHENOTYPE:\n"
        s += f"          Name: {self._name}\n"
        s += f"      Category: {self._tag}\n"
        s += f"     MET Value: {self._met}\n"
        s += f"      Duration: {self._duration} minutes\n"
        s +=  "        Repeat:"
        for ed in self.exercise_days():
            s += f" {ed[:3]},"
        s += f"\b\n"
        s += f"      Genotype: {self.to_list()}\n"
        s += f"      Schedule: {self.schedule_to_base(2)}\n"
        s += f"     Frequency: {self.frequency()}\n"
        return s

    def _update_exercise(self) -> None:
        """
        Update phenotype based on the current genotype.
        """
        exercise_series = self._config.repository().item_at(self.exercise_index())
        self._name: str = exercise_series['name']
        self._tag: str = exercise_series['tags']
        self._met: float = exercise_series['met']

    def alter(self) -> None:
        """
        Invoke parent `alter()` method and update phenotypic properties.
        """
        super().alter()
        self._update_exercise()

    def name(self) -> str:
        """
        :return: The name of the exercise.
        """
        return self._name

    def tag(self) -> str:
        """
        :return: The category of the exercise.
        """
        return self._tag

    def met(self) -> float:
        """
        :return: The MET Value of the exercise.
        """
        return self._met

    def frequency(self) -> int:
        """
        :return: The weekly frequency of an exercise, calculated by summing bits of its base-2 schedule representation.
        """
        base2_schedule = self.schedule_to_base(2)
        return sum([int(bit) for bit in base2_schedule])