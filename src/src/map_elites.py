from copy import deepcopy

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
        self._bins: int = self._config.bins()
        self._map_X: np.ndarray = np.array([[[None] * self._bins] * self._bins] * self._bins)
        self._map_P: np.ndarray = np.array([[[float(-1)] * self._bins] * self._bins] * self._bins)
        self._data_points: list = []

    def _select_random(self) -> Schedule:
        """
        Selects a random individual by selecting a random data point from an existing list of data points.
        :return: `Individual` - A solution object.
        """
        data_points = self._data_points
        index = rnd.randint(0, len(data_points) - 1)
        x, y, z = data_points[index]
        result: Schedule = self._map_X[x][y][z]
        return result

    def run(self) -> None:
        """
        Execute the MAP-Elites algorithm with provided parameters.
        :param k_init: `int` - number of random solutions to be initialised before evolving.
        :param k_evals: `int` - Total number of iterations, including both initialisation and evolution.
        :return: `Results` - Object which collects the results from this MAP-Elites instance.
        """
        k_init = self._config.total_initialisations()
        k_evals = self._config.total_evaluations()

        print("Executing MAP-Elites for:")
        print(f"Initial Weight:     {self._config.initial_weight()} kg")
        print(f"Target Weight:      {self._config.target_weight()} kg")
        print(f"Period:             {self._config.period()} weeks")
        print(f"Initialisations:    {k_init}")
        print(f"Evaluations:        {k_evals}")
        print("----------------------------------------")

        elements_skipped = 0
        for i in range(k_evals):
            print(f"\rIteration: {i + 1} / {k_evals}", end="")
            if i < k_init:
                x = Schedule(Chromosome(self._config), self._config)
            else:
                x = deepcopy(self._select_random())
                x.mutate()
            j, k, l = x.features()
            p = x.fitness()
            try:
                other_p = self._map_P[j][k][l]
                if other_p < 0 or other_p > p:
                    if not (j,k,l) in self._data_points:
                        self._data_points.append((j, k, l))
                    self._map_P[j][k][l] = p
                    self._map_X[j][k][l] = x
            except IndexError:
                elements_skipped += 1

        print(f'\nSuccessfully executed MAP-Elites over {k_evals} iterations.')
        print(f'Elements skipped: {elements_skipped}')

    def solutions(self) -> list[Schedule]:
        """
        :return: The list of all best-performing solutions.
        """
        return [self._map_X[x][y][z] for x, y, z in self._data_points]

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

    def data_points(self) -> list[tuple]:
        """
        :return: Data points of best-performing solutions with respect to their position in the map of elites.
        """
        return self._data_points