import os

from setuptools import setup

setup(
    name = "ganet",
    version = "0.0.1",
    author = "Lucian Petrut",
    author_email = "petrutlucian94@gmail.com",
    description = ("Network detection tool, based on "
                   "Pizzuti`s GA-Net algorithm. "),
    packages=['ganet'],
    install_requires=['networkx']
)
