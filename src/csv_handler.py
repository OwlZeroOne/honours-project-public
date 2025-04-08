import csv
import os

class CsvHandler:
    """
    This class handles CSV I/O operations. A single class instance represents a single CSV file, provided its directory,
    name, and column names.
    :var _path: `str` - The path to the directory that should hold the CSV file.
    """

    def __init__(self, dest_dir: str, filename: str, cols: list) -> None:
        """
        This class handles CSV I/O operations. A single class instance represents a single CSV file, provided its directory,
        name, and column names.
        :param dest_dir: `str` - Destination directory where the CSV file should reside. The provided directory will be created if it does not exist.
        :param filename: `str` -  Name of the CSV file, including the `.csv` extension.
        :param cols: `list` - The list of column names for the CSV file.
        """
        self._path = dest_dir
        self._check_directory()
        self._path += filename

        if self._csv_empty():
            with open(self._path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(cols)

    def _check_directory(self) -> None:
        """
        Checks if provided directory exists. If not, the directory is created.
        """
        if not os.path.exists(self._path):
            os.makedirs(self._path)

    def _csv_empty(self) -> bool:
        """
        Checks if provided CSV file is empty.

        :return: `True` if CSV file is empty, `False` otherwise.
        :exception FileNotFoundError: If CSV file does not exist.
        """
        try:
            with open(self._path, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                cols = next(reader, None)
                if cols is None:
                    return True
                first_row = next(reader, None)
                return first_row is None

        except FileNotFoundError:
            print("File not found.")
            return True

    def append(self, vals: list) -> None:
        """
        Adds a new row to the CSV file, provided a list of values.
        :param vals: The list of row values to be added to the CSV file.
        :type vals: List of values to fill a row.
        :exception ValueError: When an unexpected value is provided for `vals`.
        """
        if vals is None or not isinstance(vals, list):
            raise ValueError("List of values must be provided in order to write.")
        if not isinstance(vals, list):
            raise ValueError(f"Input parameter must be a list. Got {type(vals)}.")

        with open(self._path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(vals)