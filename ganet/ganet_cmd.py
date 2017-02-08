import warnings
warnings.filterwarnings("ignore")

import argparse

from ganet import conf
from ganet import network as ga_network
from ganet import population as ga_population

parser = argparse.ArgumentParser(
    description='Network detection tool, based on Pizzuti`s GA-Net algorithm.')
parser.add_argument('--path', required=True,
                    help='The network definition file path. It is expected to '
                         'contain one vertex per line, as a tuple containing '
                         'exactly two numbers, separated by a whitespace.')


if __name__ == '__main__':
    args = parser.parse_args()

    network = ga_network.Network()
    network.load_from_file(args.path)

    population = ga_population.Population(network)
    population.initialize()

    generation_count = conf.CONF['generation_count']

    for generation in range(generation_count):
        population.step()
        if not (generation % 20) or generation == (generation_count - 1):
            print("Processed generation step: %s" % generation)
            print('Fittest element info: %s' %
                  population.get_fittest().get_info())

    fittest = population.get_fittest()
    fittest.draw()
