import math
import pandas as pd


class ExerciseRepository:
    """
    A local repository of loaded exercises, where information necessary for
    computation are stored, such as activities' MET (Metabolic Equivalent) values.
    :var _data_df: `pandas.DataFrame` - Stores the loaded database of exercises with names, MET Values, categories, and indexes.
    """

    def __init__(self, path: str) -> None:
        """
        A repository instance is created by loading raw data from a source. Raw data is placed into an accessible
        list, of which size is also monitored.\n
        Raw data is currently loaded from CSV file using a CSV reader, which returns the content as a dictionary for
        each CSV row. Each dictionary is stored in a list.
        """
        self._data_df: pd.DataFrame | None = None
        self._load(path)

    def __str__(self) -> str:
        met_rng: range = self.met_range()

        s = "EXERCISE REPOSITORY:\n"
        s += f"         Size: {self.size()}\n"
        s += f"    MET Range: {met_rng.start} - {met_rng.stop}\n"
        s += f"      Columns: {list(self._data_df.columns)}\n"

        return s

    def get(self):
        return self._data_df

    def show(self) -> None:
        """
        Prints the dictionaries within the list of raw data.
        """
        print(self._data_df)

    def size(self) -> int:
        """
        :return: The size of the Compendium.
        """
        return len(self._data_df)

    def item_at(self, index: int) -> pd.Series:
        """
        :param index: Item index within the repository.
        :return: The item at the specified index.
        """
        return self._data_df.iloc[index]

    def met_range(self) -> range:
        """
        Calculates the highest and lowest values of MET values by placing them in a list and applying `max()` and
        `min()` functions on the list to obtain upper and lower bounds for the range. The upper bound is rounded to
        greatest integer, while the lower bound is rounded to lowest integer.
        :return: A range from the lower bound to the upper bound, minus 1.
        """
        mets = list(self._data_df.T.loc['met'])
        return range(math.floor(min(mets)), math.ceil(max(mets)))

    def _load(self, path: str) -> None:
        """
        Read data from a CSV file and store as a dataframe.
        :param path: `str` - Path to the CSV file.
        """
        self._data_df = pd.read_csv(path)