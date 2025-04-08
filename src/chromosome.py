from configurations import Config
from gene import *


class Chromosome:
    """
    A class to represent a single chromosome, which represents a list of exercises
    configured by parameters from Gene super-class. The chromosome also possesses the ability to mutate upon
    invoking the `mutate()` function.
    :var _config: `Config` - The configurations object that holds the necessary settings.
    :var _mutation_rate: `float` - The mutation rate of the chromosome.
    :var _alter_rate: `float` - The alteration sub-mutation rate of the chromosome.
    :var _add_rate: `float` - The addition sub-mutation rate of the chromosome.
    :var _delete_rate: `float` - The deletion sub-mutation rate of the chromosome.
    :var _chromosome: `list[Gene]` - The chromosome as a list of gene objects.
    :var _probability_pool: `list[int]` - A pool of 100 integers of 3 different possibilities, derived by each of the sub-mutation rates.
    """

    def __init__(self, config: Config, other=None) -> None:
        """
        A class to represent a single chromosome, which represents a list of exercises
        configured by parameters from Gene super-class. The chromosome also possesses the ability to mutate upon invoking the `mutate()` function.
        :param config: `Config` - The configurations object that holds the necessary settings.
        :param other: `Chromosome | None` - If provided, this instance will inherit properties of the `other` chromosome instance. Otherwise, new properties are generated.
        """
        if other is not None:
            if not isinstance(other, Chromosome):
                raise TypeError("Improper input parameter type for `other`. Should be `Chromosome`")

        self._config: Config = config

        self._mutation_rate: float = config.mutation_rate()
        self._alter_rate: float = config.alteration_rate()
        self._add_rate: float = config.addition_rate()
        self._delete_rate: float = config.deletion_rate()

        self._chromosome: list[Gene] = self._generate(5) if other is None else other.genotype_to_list('shallow')

        self._probability_pool: list[int] = (
                [0] * int(self._alter_rate * 100)
                + [1] * int(self._add_rate * 100)
                + [2] * int(self._delete_rate * 100)
        )
        self._shuffle_probability_pool(5)

    def __str__(self) -> str:
        """
        :return: The deep representation of the genotype as a string.
        """
        return str(self.genotype_to_list('deep'))

    def _shuffle_probability_pool(self, times: int) -> None:
        """
        Shuffle the probability pool to obtain more randomness.
        :param times: `int` - The amount of times the pool is to be shuffled.
        """
        for i in range(times):
            rnd.shuffle(self._probability_pool)

    def _generate(self, size: int) -> list[Gene]:
        """
        Generate a random list of genes that will be denoted by the chromosome.
        :param size: `int` - The initial chromosome size.
        :return: `list[Gene]` - Random list of genes.
        """
        l = []
        for _ in range(size):
            l.append(Gene(self._config))
        return l

    def _alter(self) -> None:
        """
        Perform an alteration mutation that randomly alters a random gene's trait.
        """
        chromosome: list[list[int]] = self.genotype_to_list('shallow')
        index = rnd.randrange(0, len(chromosome))
        gene = chromosome[index]
        assert isinstance(gene, Gene), f"Improper type for gene. Got {type(gene)}."
        gene.alter()

    def _add(self) -> None:
        """
        Perform an addition mutation that adds a random new gene to the chromosome.
        """
        if self.size() < Defaults.MAX_EXERCISES_PER_SCHEDULE:
            self._chromosome.append(Gene(self._config))

    def _delete(self) -> None:
        """
        Perform a deletion mutation that removes a random gene from the chromosome.
        :return:
        """
        size = self.size()
        gene_index = rnd.choice(range(size))
        gene = self._chromosome[gene_index]
        if size > 1:
            self._chromosome.remove(gene)

    def size(self) -> int:
        """
        :return: The size of the individual in terms of number of genes/exercises.
        """
        return len(self._chromosome)

    def mutate(self) -> None:
        """
        Conducts genetic mutation over the individual based on muation rates specified
        in the configurations.
        """
        chance = rnd.randrange(0, 100) / 100
        if chance <= self._mutation_rate:
            sub_mutation_index = rnd.choice(self._probability_pool)
            if sub_mutation_index == 0:
                self._alter()
            elif sub_mutation_index == 1:
                self._add()
            elif sub_mutation_index == 2:
                self._delete()
            else:
                raise ValueError(
                    f"Invalid mutation choice. Got {sub_mutation_index} where element of {set(self._probability_pool)} was expected")

    def genotype_to_list(self, depth: str = 'shallow') -> list[Gene] | list[list[int]]:
        """
        Creates and returns the individuals as a list of genotypic exercises.
        :param: `depth` - specifies the depth for the list. If `"deep"`, the output list
        will contain sublists representing genes. `"shallow"` returns a list of respective
        `Gene` objects.
        :return: 1-dimensional list of `Gene` objects, or 2-dimensional list of integers.
        """
        if depth == 'shallow':
            return [gene for gene in self._chromosome]
        elif depth == 'deep':
            return [gene.to_list() for gene in self._chromosome]
        else:
            raise ValueError(f"Unexpected depth parameter, '{depth}'. Expecting 'deep or 'shallow'.")
