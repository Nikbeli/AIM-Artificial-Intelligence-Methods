import numpy as np
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m.%d.%Y %I:%M:%S %p', level=logging.DEBUG)


class Chromosome:
    def __init__(self, size):
        self._gene_length = size
        self._fitnes = None
        self._genes = np.empty(size, dtype=int)

    @property
    def fitness(self):
        ftns = self._genes[self._genes == 1].sum()
        logging.debug(f"Fitness : {ftns}, Genes : {self._genes}")
        return ftns
    
    def generate_genes(self):
        self._genes = np.random.randint(2, size=self._gene_length)

def create():
    """Фабрика по производству хромоссом"""
    logging.debug("Creating Chromosomes")
    entity = Chromosome(10)
    entity.generate_genes()
    return entity
