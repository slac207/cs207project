#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following line in the
entry_points section in setup.cfg:

    console_scripts =
     cs207rbtree = cs207rbtree.skeleton:run

Then run `python setup.py install` which will install the command `cs207rbtree`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""
from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging

from cs207rbtree import __version__

__author__ = "Team 1 SAnoke ABrennan CCochrane LWare"
__copyright__ = "Team 1 SAnoke ABrennan CCochrane LWare"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def fib(n):
    """
    Fibonacci example function

    :param n: integer
    :return: n-th Fibonacci number
    """
    assert n > 0
    a, b = 1, 1
    for i in range(n-1):
        a, b = b, a+b
    return a


def parse_args(args):
    """
    Parse command line parameters

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Team 1 RBTree Code for CS207")
    parser.add_argument(
        '--version',
        action='version',
        version='cs207rbtree {ver}'.format(ver="1.0"))
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)
    logging.basicConfig(level=args.loglevel, stream=sys.stdout)
    _logger.debug("Starting crazy calculations...")
    #print("The {}-th Fibonacci number is {}".format(args.n, fib(args.n)))
    print("Args here eventually...")
    _logger.info("Script ends here")


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
