import abc
import random
import six

from ganet import chromosome as ga_chromo


@six.add_metaclass(abc.ABCMeta)
class CrossOver(object):
    def __init__(self, chromosome_a, chromosome_b, ratio=0.5):
        self._chromosome_a = chromosome_a
        self._chromosome_b = chromosome_b

        assert self._chromosome_a.size == self._chromosome_b.size
        assert (self._chromosome_a._base_network is
                self._chromosome_b._base_network)

        self._size = self._chromosome_a.size
        self._ratio = ratio

    def get_child(self):
        child_genes = self._get_child_genes()
        child = ga_chromo.Chromosome(self._chromosome_a._base_network)
        child.set_genes(child_genes)
        return child

    def _get_child_genes(self):
        genes = []
        crossover_mask = self._get_crossover_mask()

        genes_a = self._chromosome_a.get_genes()
        genes_b = self._chromosome_b.get_genes()

        for idx in range(self._size):
            if crossover_mask[idx]:
                gene = genes_a[idx]
            else:
                gene = genes_b[idx]
            genes.append(gene)

        return genes

    @abc.abstractmethod
    def _get_crossover_mask(self):
        pass


class UniformCrossOver(CrossOver):
    def _get_crossover_mask(self):
        # This may be highly inefficient. Bit ops should be used.
        t_pos = []
        remaining_pos = range(self._size)

        while len(t_pos) / float(self._size) < self._ratio:
            idx = random.randint(0, len(remaining_pos) - 1)

            pos = remaining_pos[idx]
            t_pos.append(pos)
            remaining_pos.remove(pos)

        mask = []
        for idx in range(self._size):
            mask.append(1 if idx in t_pos else 0)

        return mask
