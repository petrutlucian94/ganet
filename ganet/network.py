import re

import matplotlib.pyplot as plt
import networkx as nx


class Network(nx.Graph):
    def load_from_file(self, path):
        pattern = re.compile(r'(\d+)(?:[ ,;]*)(\d+)')
        get_node = lambda x: int(x) - 1

        with open(path, 'r') as f:
            for line in f:
                if not line.strip():
                    continue

                match = pattern.findall(line)
                if len(match) != 1 or len(match[0]) != 2:
                    raise Exception('Invalid vertex in graph '
                                    'definition file: %s' % line)
                node = get_node(match[0][0])
                vertex = (node, get_node(match[0][1]))

                # self.add_node(node)
                self.add_edge(*vertex)

    def draw(self):
        nx.draw(self)
        plt.show()
