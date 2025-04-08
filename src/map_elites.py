# import numpy as np
# import random as rnd
#
# from configurations import *
# from chromosome import *
# from parameters import *
from results import Results
from schedule import *


class MapElites:
    """
    Illumination algorithm that *illuminates* the schedule's feature space in 3 dimensions: average MET value, average
    exercise durations, and base-10 representation for days of the week of each schedule. The algorithm initialises the
    first set of solutions of a predefined size. After that, the algorithm uses mutation and random selection to evolve
    existing solutions until the predefined number of total evaluations has been reached. In both scenarios, a map of
    best-performing solutions is filled, along with a map of their respective performances, where solutions with the
    smallest fitness values are favoured more.
    :var _config: `Config` - Configurations object with all necessary settings.
    :var _repo: `ExerciseRepository` - The local database container for all exercises.
    :var _bins: `int` - The number of bins/boxes in each dimension of the map of elites.
    :var _map_X: `numpy.ndarray` - The 3-dimensional array of solutions.
    :var _map_P: `numpy.ndarray` - The 3-dimensional array of performances.
    :var _data_points: `list` - The list of schedule datapoints of schedules with respect to where they are found on the maps.
    """

    def __init__(self, config: Config) -> None:
        """
        Illumination algorithm that *illuminates* the schedule's feature space in 3 dimensions: average MET value, average
        exercise durations, and base-10 representation for days of the week of each schedule. The algorithm initialises the
        first set of solutions of a predefined size. After that, the algorithm uses mutation and random selection to evolve
        existing solutions until the predefined number of total evaluations has been reached. In both scenarios, a map of
        best-performing solutions is filled, along with a map of their respective performances, where solutions with the
        smallest fitness values are favoured more.
        :param config:
        """
        self._config: Config = config
        self._repo: ExerciseRepository = self._config.repository()
        self._bins: int = self._config.bins()
        self._map_X: np.ndarray = np.array([[[None] * self._bins] * self._bins] * self._bins)
        self._map_P: np.ndarray = np.array([[[float(-1)] * self._bins] * self._bins] * self._bins)
        self._data_points: list = []

    def _scale_features(self, raw_features: tuple) -> tuple:
        """
        Scale raw solution features to the number of bins in the map of elites in each dimension.
        :param raw_features: `tuple` - A schedule's feature vector.
        :return: A new feature vector of scaled integers.
        """
        # TODO: Write as addition in implementation
        ranges = [self._repo.met_range(), self._config.daily_duration_range(), range(0, 8)]
        b = self._bins
        scaled_features = [0] * len(raw_features)

        for i in range(len(raw_features)):
            rng: range = ranges[i]
            r = raw_features[i]
            r_min = rng.start
            r_max = rng.stop

            delta = (r_max + 1) - r_min
            c = delta / b
            s = int((r - r_min) / c) + 1

            scaled_features[i] = s

        return tuple(scaled_features)

    def _select_random(self) -> Chromosome:
        """
        Selects a random individual by selecting a random data point from an existing list of data points.
        :return: `Individual` - A solution object.
        """
        # TODO: Write as addition in implementation
        dps = self._data_points
        assert len(dps) > 0, "Attempting to select from an empty map!"
        index = rnd.randint(0, len(dps) - 1)
        x, y, z = dps[index]
        result: Chromosome = self._map_X[x][y][z]
        return result

    def run(self, init_times: int, total_evals: int) -> Results:
        """
        Execute the MAP-Elites algorithm with provided parameters.
        :param init_times: `int` - number of random solutions to be initialised before evolving.
        :param total_evals: `int` - Total number of iterations, including both initialisation and evolution.
        :return: `Results` - Object which collects the results from this MAP-Elites instance.
        """
        elements_skipped = 0
        for i in range(total_evals):
            print(f"\rIteration: {i + 1} / {total_evals}", end="")
            if i < init_times:
                individual = Chromosome(self._config)
                x = Schedule(individual, self._config)
            else:
                parent = self._select_random()
                parent.mutate()
                x = Schedule(parent, self._config)
            if True:
                raw_descriptor: tuple[float, float, int] = x.features()
                dp = j, k, l = self._scale_features(raw_descriptor)
                try:
                    p = x.fitness()
                    curr_x = self._map_P[j][k][l]
                    if curr_x < 0 or curr_x > p:
                        self._data_points.append(dp)
                        self._map_P[j][k][l] = p
                        self._map_X[j][k][l] = x
                except IndexError:
                    elements_skipped += 1
        print(f'\nSuccessfully executed MAP-Elites over {total_evals} iterations.')
        print(f'Elements skipped: {elements_skipped}')
        return Results(self)

    def solutions(self) -> list[Schedule]:
        """
        :return: The list of all best-performing solutions.
        """
        return [s for s in list(self._map_X.flatten()) if s is not None]

    def performances(self, scale: bool = False) -> np.ndarray:
        """
        Format and return performances as an analysis-friendly matrix by setting unfeasible solutions to the highest performance + 1,
        making them thw "worst-case" solutions and hence, unfavourable. For particular purposes, like displaying heatmaps, the matrix
        can be scaled to values between 0 and 1.
        :param scale: `bool` - If `True`, scale the performances to fractions from 0 to 1. Otherwise, omit scaling.
        :return: The N-dimensional array of formatted and either scaled or unscaled performances.
        """
        map_P = self._map_P.copy()
        max_P = np.max(map_P)
        b = self._bins
        for x in range(b):
            for y in range(b):
                for z in range(b):
                    val = map_P[x][y][z]
                    if scale:
                        map_P[x][y][z] = (val / max_P) if val > 0 else 1
                    else:
                        if val < 0:
                            map_P[x][y][z] = int(max_P + 1)
        return map_P

    def data_points(self, remove_duplicates: bool = True) -> list[tuple]:
        """
        :param remove_duplicates: `bool` - If `True`, removes any duplicate data points.
        :return: Data points of best-performing solutions with respect to their position in the map of elites.
        """
        if remove_duplicates:
            return list(set(self._data_points))
        return self._data_points