#!/usr/bin/env python

import os
import time
import logzero
import traceback
import logging

from pprint import pformat
from logzero import logger
from argparse import ArgumentParser
from bksyn.nodes import Node

UPDATE_INTERVAL_S = 3


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('--id', default=os.environ['BKSYN_NODE_ADDRESS'])

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    logzero.logfile('logs/node-%s.log' % args.id, mode='a')
    if args.debug:
        logzero.loglevel(logging.DEBUG)
    else:
        logzero.loglevel(logging.INFO)

    # Register node
    node = Node.from_env(args.id)
    node.query_status()
    node.save()

    while True:
        try:
            node.query_status()
            logger.info(pformat(node.status, indent=2))
            node.update_status()
            time.sleep(UPDATE_INTERVAL_S)
        except (KeyboardInterrupt, SystemExit):
            break
        except Exception as e:
            logger.error(traceback.format_exc())
            break
