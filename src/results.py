import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from chromosome import *
from map_elites import *
from schedule import Schedule

class Results:
    """
    This class brings together the necessary results from the algorithm to either return to the user, or for statistical analysis.
    :var _schedules: `list[Schedule]` - List of schedule objects.
    :var _performances: `numpy.ndarray` - N-dimensional performance matrix with respect to schedule's position on the map of elites.
    :var _data_points: `list[tuple[int]]` - Data points of schedules with respect to their position on the map of elites.
    """

    def __init__(self, map_of_elites) -> None:
        self._schedules: list[Schedule] = map_of_elites.solutions()
        self._performances: np.ndarray = map_of_elites.performances()
        self._data_points: list[tuple[int]] = map_of_elites.data_points()

    def statistics(self, detailed: bool = False) -> pd.DataFrame:
        """
        Gets all statistics from the algorithm's results as a `pandas` dataframe.
        :param detailed: `bool` - If `True`, statistics for all solutions will be returned. Otherwise, a summary of those statistics will be returned.
        :return: The dataframe of statistics, reflecting the results.
        """

        df = None
        if detailed:
            data_dict: dict = {
                'mean_met': [],
                'std_met': [],
                'mean_duration': [],
                'std_duration': [],
                'week_schedule': [],
                'total_exercises': [],
                'mean_frequency': [],
                'performance': []
            }
            for schedule in self._schedules:
                data_dict['mean_met'].append(np.mean(schedule.mets()))
                data_dict['std_met'].append(np.std(schedule.mets()))
                data_dict['mean_duration'].append(np.mean(schedule.durations()))
                data_dict['std_duration'].append(np.std(schedule.durations()))
                week_schedule = schedule.schedule_to_base(2)
                data_dict['week_schedule'].append(week_schedule)
                data_dict['total_exercises'].append(sum(len(day) for day in schedule.phenotype_to_list()))
                data_dict['mean_frequency'].append(np.mean(schedule.frequencies()))
                data_dict['performance'].append(schedule.fitness())

                df = pd.DataFrame(data_dict)
        else:
            stats_performance = [
                [self.mean_quality(), self.std_quality(), self.worst_quality(), self.best_quality()],
                [self.mean_duration(), self.std_duration(), self.max_duration(), self.min_duration()],
                [self.mean_met(), self.std_met(), self.max_met(), self.min_met()],
                [self.mean_counts(), self.std_counts(), self.max_count(), self.min_count()]
            ]
            df = pd.DataFrame(
                stats_performance,
                columns=["Mean", "Standard Deviation", "Maximum", "Minimum"],
                index=["Performance", "Exercise Duration", "MET Value", "Exercises/Day"])

        return df

    def schedules(self) -> list[Schedule]:
        """
        :return: The list of schedule objects.
        """
        return self._schedules

    # ===== MEAN =======================================================================================================
    def mean_quality(self) -> float:
        """
        :return: The mean quality of all best-performing schedules.
        """
        mean = np.mean(np.array([schedule.fitness() for schedule in self._schedules]))
        return round(mean, 2)

    def mean_duration(self) -> float:
        """
        :return: The mean duration of all best-performing schedules.
        """
        mean = np.mean(np.concatenate([schedule.durations().flatten() for schedule in self._schedules]))
        return round(mean, 2)

    def mean_met(self) -> float:
        """
        :return: The mean MET Value of all best-performing schedules.
        """
        mean = np.mean(np.concatenate([schedule.mets().flatten() for schedule in self._schedules]))
        return round(mean, 2)

    def mean_counts(self) -> float:
        """
        :return: The mean exercise count per day for all best-performing schedules.
        """
        mean = np.mean(np.array([schedule.exercise_counts() for schedule in self._schedules]))
        return round(mean, 2)

    # ===== MEAN =======================================================================================================

    # ===== STANDARD DEVIATION =========================================================================================
    def std_quality(self) -> float:
        """
        :return: The standard deviation of qualities of all best-performing schedules.
        """
        std = np.std(np.array([schedule.fitness() for schedule in self._schedules]))
        return round(std, 2)

    def std_duration(self) -> float:
        """
        :return: The standard deviation of durations of all best-performing schedules.
        """
        std = np.std(np.concatenate([schedule.durations().flatten() for schedule in self._schedules]))
        return round(std, 2)

    def std_met(self) -> float:
        """
        :return: The standard deviation of MET Values of all best-performing schedules.
        """
        std = np.std(np.concatenate([schedule.mets().flatten() for schedule in self._schedules]))
        return round(std, 2)

    def std_counts(self) -> float:
        """
        :return: The standard deviation of exercise counts per day for all best-performing schedules.
        """
        std = np.std(np.array([schedule.exercise_counts() for schedule in self._schedules]))
        return round(std, 2)

    # ===== STANDARD DEVIATION =========================================================================================

    ## ===== MAXIMUM ===================================================================================================
    def worst_quality(self) -> float:
        """
        :return: The worst (maximum) quality of all best-performing schedules.
        """
        hi = np.max(np.array([schedule.fitness() for schedule in self._schedules]))
        return round(hi, 2)

    def max_duration(self) -> float:
        """
        :return: The longest duration of all best-performing schedules.
        """
        hi = np.max(np.concatenate([schedule.durations().flatten() for schedule in self._schedules]))
        return round(hi, 2)

    def max_met(self) -> float:
        """
        :return: The highest MET Value of all best-performing schedules.
        """
        hi = np.max(np.concatenate([schedule.mets().flatten() for schedule in self._schedules]))
        return round(hi, 2)

    def max_count(self) -> float:
        """
        :return: The highest exercise count per day for all best-performing schedules.
        """
        hi = np.max(np.array([max(schedule.exercise_counts()) for schedule in self._schedules]))
        return round(hi, 2)

    ## ===== MAXIMUM ===================================================================================================

    ## ===== MINIMUM ===================================================================================================
    def best_quality(self) -> float:
        """
        :return: The best (minimum) quality of all best-performing schedules.
        """
        lo = np.min(np.array([schedule.fitness() for schedule in self._schedules]))
        return round(lo, 2)

    def min_duration(self) -> float:
        """
        :return: The shortest duration of all best-performing schedules.
        """
        lo = np.min(np.concatenate([schedule.durations().flatten() for schedule in self._schedules]))
        return round(lo, 2)

    def min_met(self):
        """
        :return: The lowest MET Value of all best-performing schedules.
        """
        lo = np.min(np.concatenate([schedule.mets().flatten() for schedule in self._schedules]))
        return round(lo, 2)

    def min_count(self):
        """
        :return: The lowest exercise count per day for all best-performing schedules.
        """
        lo = np.min(np.array([min(schedule.exercise_counts()) for schedule in self._schedules]))
        return round(lo, 2)

    ## ===== MINIMUM ===================================================================================================

    def count_solutions(self) -> int:
        """
        :return: The number of yielded solutions.
        """
        return len(self._schedules)

    def output(self) -> None:
        """
        Output results to a CSV file for further data analysis.
        """
        df: pd.DataFrame = self.statistics(True)
        df.to_csv('output.csv', index=False)