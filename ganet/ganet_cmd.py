import argparse
import logging
import warnings

warnings.filterwarnings("ignore")

from ganet import group_detector
from ganet import network as ga_network


parser = argparse.ArgumentParser(
    description='Network detection tool, based on Pizzuti`s GA-Net algorithm.')
parser.add_argument('--path', required=True,
                    help='The network definition file path. It is expected to '
                         'contain one vertex per line, as a tuple containing '
                         'exactly two numbers, separated by a whitespace.')
parser.add_argument('--debug', action='store_true',
                    help='Print debug messages.')


def configure_logging(debug=False):
    log_level = logging.DEBUG if debug else logging.INFO

    handler = logging.StreamHandler()
    handler.setLevel(log_level)

    log_fmt = '[%(asctime)s] %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_fmt)
    handler.setFormatter(formatter)

    LOG = logging.getLogger()
    LOG.addHandler(handler)
    LOG.setLevel(log_level)


if __name__ == '__main__':
    args = parser.parse_args()

    configure_logging(args.debug)

    network = ga_network.Network()
    network.load_from_file(args.path)

    solver = group_detector.GroupDetector(network)
    solver.initialize()

    solution = solver.get_solution()
    solution.draw()
