import time as t


class Timer:
    """
    Used to measure execution time using Python's library, `time`.
    :var _start: Start time.
    :var _end: End time.
    """
    def __init__(self) -> None:
        self._start = 0
        self._end = 0

    def start(self) -> None:
        """
        Starts the timer.
        """
        self._start =  t.time()

    def stop(self) -> None:
        """
        Stops the timer and return the elapsed time.
        """
        self._end = t.time()

    def result(self) -> float:
        """
        :return: elapsed time, rounded float to 2 decimal places.
        """
        return round(self._end - self._start, 2)