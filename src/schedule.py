import numpy as np

from chromosome import *
from exercise import *
from configurations import *
from weight_loss_difference import WeightLossDifference


class Schedule(Chromosome):
    """
    The phenotypic representation of a chromosome. An object of this class will hold information regarding all the exercises contained within the schedule.
    :var: _config: `Config` - The configurations object that holds necessary settings.
    :var _exercises: `list[Exercise]` - The unordered list of exercises with no multiplicity.
    :var _schedule_as_list: `list` - The list of exercise occurrences in chronological order.
    :var _base2_schedule: `str` - The binary representation of a weekly schedule.
    :var _fitness: `float` - The fitness value of the schedule.
    """

    def __init__(self, chromosome: Chromosome, config: Config) -> None:
        """
        he phenotypic representation of a chromosome. An object of this class will hold information regarding all the exercises contained within the schedule.
        :param chromosome: `Chromosome` - The chromosome object to be inherited from.
        :param config: `Config` - The configuration object that holds necessary settings.
        """
        super().__init__(config, other=chromosome)
        self._schedule_as_list: list = []
        self._base2_schedule: str = '0000000'
        self._exercises: list = []
        self._fitness = float('INF')
        self._valid = False

        self._update()

    # String overload
    def __str__(self) -> str:
        week = Defaults.WEEK
        s = ""
        for i in range(len(self._schedule_as_list)):
            day = self._schedule_as_list[i]
            s += f"{(week[i][:3]).upper()}: ["
            for j in range(len(day)):
                e: Exercise = day[j]
                s += f'({e.exercise_index()},{e.duration()}),'
            s += f"{']' if s[-1] == '[' else '\b]'}\n"
        return s

    # ==================================================================================================================
    #       PRIVATE METHODS
    # ==================================================================================================================
    def _update(self) -> None:
        """
        Update the schedule based on the chromosome provided.
        """
        self._decode()
        self._make_schedule()
        self._merge_binary_schedules()
        self._evaluate()

    def _decode(self) -> None:
        """
        Decode the schedule to produce a list of phenotypic exercises.
        :return:
        """
        exercises = []
        for gene in self.genotype_to_list('shallow'):
            # print(gene)
            e = Exercise(gene, self._config)
            # print(e)
            # if e.is_valid():
            exercises.append(e)
        self._exercises = exercises

    def _make_schedule(self) -> None:
        """
        Reads exercise data to form the ordered schedule as a list of days with exercises.
        """
        week = [[], [], [], [], [], [], []]
        for exercise in self._exercises:
            schedule = exercise.schedule_to_base(2)
            for i in range(7):
                day = int(schedule[i])
                if day == 1:
                    week[i].append(exercise)
                elif day != 0:
                    raise ValueError(f"Unexpected value for weekly binary exercise schedule. Got {schedule[i]}.")
        self._schedule_as_list = week

    def _evaluate(self) -> None:
        """
        Calculates the schedule's fitness value.
        """
        wld: float = WeightLossDifference(self._config, self._schedule_as_list).run()
        self._fitness = wld

    def _merge_binary_schedules(self) -> None:
        """
        Merge exercise binary schedules into one.
        """
        b2_total: list[str] = ['0'] * 7
        b10_exercise_schedules: list[int] = [E.schedule_to_base(10) for E in self._exercises]
        for b10 in b10_exercise_schedules:
            b2: str = format(b10, '0{}b'.format(7))
            for i in range(7):
                if b2[i] == '1':
                    b2_total[i] = '1'
        self._base2_schedule = ''.join(b2_total)

    @staticmethod
    def _fill_and_return_matrix(lst: list[list], filler=0) -> np.ndarray:
        """
        Generate an uneven 2D list to a complete Numpy 2D matrix by filling in blanks with a filler value.
        :param lst: `list[list` - The list to be filled.
        :param filler: `int` - The filler value to fill the blanks with.
        :return: `np.ndarray` - A Numpy 2D matrix.
        """
        max_row_length = max(len(l) for l in lst)
        for i in range(len(lst)):
            row_length = len(lst[i])
            if row_length < max_row_length:
                for _ in range(max_row_length - row_length):
                    lst[i].append(filler)
        return np.array(lst)

    # ==================================================================================================================
    #       PUBLIC METHODS
    # ==================================================================================================================
    def prettify(self) -> None:
        """
        Pretty-print the schedule, illustrating exercises for each day of the week.
        """
        ds = Defaults.WEEK
        s = "=================================================\n"
        s += "   PRETTY SCHEDULE\n"
        s += "=================================================\n\n"

        for i in range(7):
            sch = self._schedule_as_list[i]
            s += f" {ds[i]} ({f"{len(sch)} exercises" if len(sch) > 0 else "REST"}):\n"
            for e in sch:
                s += f"    Activity:  {e.name()}\n"
                s += f"    Duration:  {e.duration()} minutes\n\n"

            s += "-------------------------------------------------\n"
        print(s)

    def is_valid(self) -> bool:
        return self._valid

    def schedule_to_base(self, base: int) -> str | int:
        """
        :param base: `int` - The base to which return the schedule: 2 - binary; 10 - decimal.
        :return: The weekly exercise schedule as either a binary (base-2) number string, or decimal (base-10) number integer.
        """
        if base == 10:
            return format(self._base2_schedule, '0{}b'.format(7))
        elif base == 2:
            return self._base2_schedule
        else:
            raise ValueError(f"Unexpected number base! Expecting 2 for binary or 10 for decimal. Got {base}.")

    def phenotype_to_list(self, depth: str = 'shallow') -> list[list[Exercise]] | list[list[list[int]]]:
        """
        Convert the schedule to a 2D list of exercise objects, or a 3D list where the third dimension is the list of exercise details: index, duration, MET Value.
        :param depth: `string` - Specifies the depth of the output list. Can be 'shallow' or 'deep'.
        :return: The 2D or 3D list of exercises.
        """
        if depth == 'shallow':
            return self._schedule_as_list
        elif depth == 'deep':
            l = [[], [], [], [], [], [], []]
            for i in range(len(self._schedule_as_list)):
                day = self._schedule_as_list[i]
                for j in range(len(day)):
                    e: Exercise = day[j]
                    l[i].append([e.exercise_index(), e.duration(), e.met()])
            return l
        else:
            raise ValueError(f"Unexpected depth! Expecting 'shallow' or 'deep'. Got {depth}.")

    # ===== MEASURABLES ================================================================================================
    def mets(self) -> np.ndarray:
        """
        Gets MET values of all exercises within the schedule, organised into their respective days of the week.
        :return: `2darray` - All MET value occurrences.
        """
        arr = []
        schedule = self._schedule_as_list
        for i in range(7):
            day = schedule[i]
            arr.append([])
            for exercise in day:
                arr[i].append(exercise.met())
        return self._fill_and_return_matrix(arr)

    def durations(self) -> np.ndarray:
        """
        Get durations of all exercises within the schedule and organise them into a computable `numpy` matrix.
        :return: `ndarray` - All exercise durations.
        """
        arr = []
        schedule = self._schedule_as_list
        for i in range(7):
            day = schedule[i]
            arr.append([])
            for exercise in day:
                arr[i].append(exercise.duration())
        return self._fill_and_return_matrix(arr)

    def frequencies(self) -> np.ndarray:
        # pass
        """
        Get frequencies of all exercises within the schedule and organise them into a computable `numpy` matrix.
        :return: `ndarray` - All exercise frequencies.
        """
        arr = []
        exercises = self._exercises
        for E in exercises:
            arr.append(E.frequency())
        return np.array(arr)

    def exercise_counts(self) -> np.ndarray:
        """
        Counts the number of exercises for each day of the week.
        :return: `ndarray` - Exercise counts.
        """
        arr = np.array([0] * 7)
        schedule = self._schedule_as_list
        for i in range(7):
            day = schedule[i]
            arr[i] = len(day)
        return arr

    # ===== MEASURABLES ================================================================================================

    def features(self) -> tuple:
        """
        Describe the schedule's features by calculating the mean MET value, mean exercise durations, and mean frequencies to a tuple.
        :return: The tuple of respective descriptor values.
        """
        mean_mets: float = np.mean(self.mets())
        mean_durations: float = np.mean(self.durations())
        mean_frequencies: int = np.mean(self.frequencies())
        return mean_mets, mean_durations, mean_frequencies

    def fitness(self) -> float:
        """
        :return: The schedule's fitness score.
        """
        return self._fitness

    def exercises(self) -> list[Exercise]:
        """
        :return: The list of exercise phenotypes.
        """
        return self._exercises