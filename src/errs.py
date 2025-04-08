import datetime as dt


class Base(Exception):
    def __init__(self, msg: str, err_code: int):
        self.dt = self._get_date_time()
        self.msg: str = msg
        self.err_code: int = err_code
        super().__init__(self.msg)

    def __str__(self):
        return f"[{self.dt['date']} {self.dt['time']}] ERR{self.err_code}-{self.msg}"



    @staticmethod
    def _get_date_time() -> dict:
        now = dt.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        return {"date": date, "time": time}



class AlgorithmParamsError(Base):
    def __init__(self, params_obj):
        super().__init__(
            f"The algorithm expects a `Parameters` object. The type of the parameter is {type(params_obj).__name__}.",
            1001
        )


class ParameterRangeError(Base):
    def __init__(self, value, hi, lo):
        super().__init__(
            f"Invalid parameter range. Expected between {lo} and {hi}. Got {value}.",
            1002
        )

    def __str__(self) -> str:
        return super().__str__()


class UnexpectedValueError(Base):
    def __init__(self, value, expected):
        super().__init__(
            f"Unexpected value. Expected {expected}. Got {value}.",
            1003
        )

class UnexpectedTypeError(Base):
    def __init__(self, actual_type, expected_type):
        super().__init__(
            f"Unexpected type. Expected {expected_type.__name__}. Got {actual_type.__name__}.",
            1004
        )