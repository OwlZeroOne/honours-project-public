import random as rnd

from chromosome import *

class Mutation:
    """
    This genetic operator class mutates an individual (genotype). It uses the `Config` instance to apply certain
    restrictions or constraints on mutation parameters, such as mutation rates or value ranges. Mutation constructor
    takes two parameters:

    :param individual: 'Individual' - The genotype object passed for mutation.
    :param config: `Config` - The configuration instance used to provide mutation parameters.
    """
    def __init__(self, individual: Individual,mutation_rate: float, config:Config) -> None:
        self._individual: Individual = individual
        self._config: Config = config
        # self._gene: Gene = gene
        self._data: ExerciseRepository = config.get_compendium()

        # TODO: Move mutation rates to `Config`
        self._mutation_rate: float = mutation_rate
        self._alt_rate = 0.7
        self._add_rate = 0.2
        self._rem_rate = 0.1

        if not self._valid_rate(self._mutation_rate):
            raise ValueError(f"Base mutation rate out of bounds! Got {self._mutation_rate}")

    # TODO: Encapsulate the method within the instance (remove staticmethod)
    @staticmethod
    def _valid_rate(rate: float) -> bool:
        """
        Ensures that mutation rates are between 0 and 1.
        :return: `True` if the mutation rate is valid, `False` otherwise.
        """
        return 0 <= rate < 1

    # TODO: Replace __call__() with run()
    def __call__(self) -> Individual:
        self._mutate(self._alt_rate, self._add_rate, self._rem_rate)
        return self._individual

    def _mutate(self, alt_rate: float, add_rate: float, rem_rate: float) -> None:
        """
        Conduct mutation operation, involving three different mutation types: gene alteration, gene addition, gene
        deletion.
        :param alt_rate: Mutation rate for gene alteration.
        :param add_rate: Mutation rate for gene addition.
        :param rem_rate: Mutation rate for gene removal.
        :return:
        """
        alt, add, rem = int(alt_rate * 100), int(add_rate * 100), int(rem_rate * 100)
        # print(alt, add, rem)
        if alt + add + rem != 100:
            raise ValueError(f"Concrete mutation rates must sum up to 1. Got {alt + add + rem / 100}")

        if not (self._valid_rate(alt_rate)
                and self._valid_rate(add_rate)
                and self._valid_rate(rem_rate)):
            raise ValueError("A rate must be a real number between 0 and 1.")

        probability_pool = [1] * alt + [2] * add + [3] * rem
        choice = rnd.choice(probability_pool)

        if choice == 1:
            self._alter()
        elif choice == 2:
            self._add()
        elif choice == 3:
            self._delete()
        else:
            raise ValueError(f"Invalid mutation choice. Got {choice} where element of {set(probability_pool)} was expected")

    def _alter(self) -> None:
        """
        Gene alteration mutation - invokes the gene's alteration method via the individual's alteration method that
        takes the gene's indexes, and alters the gene at those indexes.
        """
        individual_lst: list[list[int]] = self._individual.to_list('deep')
        i = rnd.randrange(0, len(individual_lst))
        j = rnd.randrange(0, len(individual_lst[i]))
        self._individual.alter(i,j)

    def _add(self) -> None:
        """
        Gene addition mutation - invokes the individual's addition method and adds a random gene to the genotype.
        """
        self._individual.add()

    def _delete(self) -> None:
        """
        Gene deletion mutation - invokes the individual's deletion method and removes a random gene from the genotype.
        """
        size = len(self._individual.to_list())
        self._individual.remove(rnd.choice(range(size)))