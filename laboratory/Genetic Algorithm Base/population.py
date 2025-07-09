import numpy as np
import logging

import chromosome

class Population:
    def __init__(self, size):
        self._data = np.array([chromosome.create() for _ in range(size)])

    def __repr__(self):
        return [e.fitnesss for e in self._data]
    
    @property
    def fitness(self):
        pop_ftns = np.sum([e.fitness for e in self._data])
        logging.debug(f"Fitness of the population : {pop_ftns}")
        return pop_ftns
    