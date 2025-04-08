from errs import *

class Validation:
    @staticmethod
    def range_validation(x, hi, lo) -> None:
        """
        Tests variable's value against its range.
        :param x: Actual value
        :param hi: Upper bound
        :param lo: Lower bound
        :exception ParameterRangeError: If `x` is found out of bounds
        """
        if not lo <= x <= hi:
            raise ParameterRangeError(x, hi, lo)

    @staticmethod
    def value_validation(x, expected) -> None:
        """
        Tests a variable for a specific value.
        :param x: Actual value
        :param expected: Expected value
        :exception UnexpectedValueError: If `x` is not of the expected value.
        """
        if not x == expected:
            raise UnexpectedValueError(x, expected)

    @staticmethod
    def type_validation(x, expected) -> None:
        """
        Tests a variable's actual type against an expected type.
        :param x: The variable to be tested
        :param expected: Expected type
        :exception UnexpectedTypeError: If `x` is not of the expected type.
        """
        if not isinstance(x, expected):
            raise UnexpectedTypeError(type(x), expected)