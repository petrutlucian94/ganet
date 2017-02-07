import copy
import random

import networkx as nx
import numpy

from ganet import conf
from ganet import network as ga_network


class Chromosome(object):
    def __init__(self, base_network):
        self._base_network = base_network
        self._network = None
        self._genes = []
        self._cached_score = None

        self._score_mean_order = conf.CONF['community_score_mean_order']
        self._mutation_rate = conf.CONF['mutation_rate']

        self.size = len(self._base_network.nodes())

    def set_genes(self, genes):
        assert len(genes) == self.size
        self._genes = copy.copy(genes)

        self._refresh()

    def _refresh(self):
        self._cached_score = None
        self._network = ga_network.Network()
        self._network.add_edges_from(enumerate(self._genes))

    def get_genes(self):
        return copy.copy(self._genes)

    def generate(self):
        genes = []

        for idx in range(self.size):
            gene = self._generate_gene(idx)
            genes.append(gene)

        self._genes = genes
        self._refresh()

    def _generate_gene(self, idx):
        neighbors = self._base_network.neighbors(idx)
        neighbor_idx = random.randint(0, len(neighbors) - 1)
        return neighbors[neighbor_idx]

    def mutate(self):
        mutated = False

        for idx in range(self.size):
            should_mutate = random.random() < self._mutation_rate
            if should_mutate:
                mutated_gene = self._generate_gene(idx)
                self._genes[idx] = mutated_gene
                mutated = True

        if mutated:
            self._refresh()

    def get_score(self):
        # TODO(fetch r from a conf obj)
        if self._cached_score is None:
            self._cached_score = self._get_score()
        return self._cached_score

    def _get_score(self):
        score = 0

        for subgraph_nodes in nx.connected_components(self._network):
            subgraph = self._base_network.subgraph(subgraph_nodes)
            adj_matrix = nx.to_numpy_matrix(subgraph)
            power_mean = 0

            for line in adj_matrix:
                mean = numpy.mean(line)
                power_mean += pow(mean, self._score_mean_order)

            power_mean /= len(adj_matrix)

            score += power_mean
        return score
