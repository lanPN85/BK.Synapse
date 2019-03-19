#!/usr/bin/env python3

import os

from argparse import ArgumentParser

from bkdnode import utils


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-c', '--config', action='append', default=['configs/config.json'])

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    configs = utils.load_configs(args.config)
