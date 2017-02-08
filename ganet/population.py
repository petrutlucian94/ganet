import math
import random

from ganet import chromosome as ga_chromo
from ganet import conf
from ganet import crossover as ga_crossover


class Population(object):
    def __init__(self, base_network):
        self._base_network = base_network
        self._chromosomes = []

        self._size = conf.CONF['population_size']
        self._crossover_rate = conf.CONF['crossover_rate']
        self._elite_rate = conf.CONF['elite_reproduction_rate']

        self._elite_count = int(math.ceil(self._elite_rate * self._size))

    def initialize(self):
        for idx in range(self._size):
            chromosome = ga_chromo.Chromosome(self._base_network)
            chromosome.generate()
            self._chromosomes.append(chromosome)

    def sort(self):
        key = lambda x: -x.get_score()
        self._chromosomes.sort(key=key)

    def step(self):
        self.sort()

        if self._elite_count:
            elites = self._chromosomes[:self._elite_count]
        else:
            elites = []

        children = []

        pair = None
        for chromosome in self._chromosomes:
            if chromosome not in elites:
                chromosome.mutate()

            should_crossover = random.random() < self._crossover_rate
            if should_crossover:
                if pair:
                    crossover = ga_crossover.UniformCrossOver(pair, chromosome)
                    child = crossover.get_child()
                    children.append(child)
                else:
                    pair = chromosome

        self._chromosomes += children
        self.sort()
        self._chromosomes = self._chromosomes[:self._size]

    def get_fittest(self):
        self.sort()
        return self._chromosomes[0]
