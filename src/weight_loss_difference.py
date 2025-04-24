from schedule import *


class WeightLossDifference:
    """
    This objective function calculates the difference between target weight, provided by the user, and actual weight
    after completing the generated schedule. This is done by accepting three parameters - initial weight, target
    weight, and time frame in weeks - and performing a simulation run of the schedule, assuming workout consistency
    and no weight gain in parallel, and continuously updating user's weight after each exercise is completed.
    :var _w0: `float` - User's initial weight.
    :var _wt: `float` - User;s target weight.
    :var _P: `float` - Period by which target weight should be achieved.
    :var _schedule: `list` - The ordered schedule as a list.
    """

    def __init__(self, config: Config, schedule: list) -> None:
        """
        This objective function calculates the difference between target weight, provided by the user, and actual weight
        after completing the generated schedule. This is done by accepting three parameters - initial weight, target
        weight, and time frame in weeks - and performing a simulation run of the schedule, assuming workout consistency
        and no weight gain in parallel, and continuously updating user's weight after each exercise is completed.
        :param config: `Config` - The configuration object wit necessary settings.
        :param schedule: `list` - The ordered schedule as a list.
        """
        self._w0: float = config.initial_weight()
        self._wt: float = config.target_weight()
        self._P: int = config.period()
        self._schedule: list = schedule

    def run(self) -> float:
        """
        Run the objective function.
        :return: `float` - The difference between aspired weight and estimated final weight.
        """
        return self._delta()

    def _delta(self) -> float:
        """
        :return: `float` - Absolute value of the difference between aspired weight and final weight.
        """
        final_w = self._final_weight()
        return round(abs(self._wt - final_w), 2)

    def _final_weight(self) -> float:
        """
        Compute final weight by conducting a simulation of the schedule over given number of weeks, `self._P`. The
        user's weight is continuously updated, starting from the provided initial weight, `self._w0`.
        :return: `float` - The final estimated weight.
        """
        current_weight = self._w0
        for i in range(self._P):
            for day in self._schedule:
                for exercise in day:
                    current_weight -= self._weight_loss(exercise, current_weight)
        return current_weight

    @staticmethod
    def _weight_loss(exercise, w: float) -> float:
        """
        Calculates estimated weight loss after completing an exercise with current weight, utilising the MET value of
        the exercise.
        :param exercise: `Exercise` - The exercise that is to be completed.
        :param w: `float` - Weigh at the time of the exercise.
        :return: The estimated weight after exercise completion.
        """
        return (0.00013 * exercise.met() * w * exercise.duration()) / 60