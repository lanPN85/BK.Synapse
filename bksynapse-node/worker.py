#!/usr/bin/env python3

import os

from logzero import logger
from argparse import ArgumentParser
from bksyn.nodes import NodeDbClient, Node


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-d', '--debug', action='store_true')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

