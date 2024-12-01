#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import sys

from typing import Callable

__all__ = [
    'MultiLineFormatter',
    'setup',
]

class MultiLineFormatter(logging.Formatter):
    def format(self, record):
        str = logging.Formatter.format(self, record)
        header, footer = str.split(record.message)
        str = str.replace('\n', '\n' + ' '*len(header))
        return str

def setup(install_arguments: Callable[[argparse.ArgumentParser], None] = None) -> argparse.Namespace:
    # Set up Logger
    l = logging.getLogger()
    h = logging.StreamHandler()
    h.setFormatter(MultiLineFormatter(fmt='[%(asctime)s][%(levelname)-8s] %(message)s', datefmt='%d %b %Y %H:%M:%S'))
    l.addHandler(h)
    l.setLevel(logging.INFO)
    
    loglevel_def = 'INFO'
    loglevel_choices = tuple(lvl for lvl in logging.getLevelNamesMapping().keys() if lvl not in ('WARN', 'NOTSET'))
    loglevel_usage = (f"'{lvl}'" + ('' if (lvl != loglevel_def) else ' (default)') for lvl in loglevel_choices)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Advent of Code.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--loglevel', help=f'Log level, one of {", ".join(loglevel_usage)}.', choices=loglevel_choices, default=loglevel_def)
    parser.add_argument('--example', help='Use example data.', type=int, choices=range(1,10+1), default=0)
    if (install_arguments is not None):
        install_arguments(parser)

    # Parse arguments
    args = parser.parse_args()

    if (sys.version_info < (3, 8)):
        logging.fatal(f'Python version {".".join(sys.version_info)} is less than minimum required version 3.8.')
        sys.exit(-1)
    
    # Set User Loglevel
    try:
        l.setLevel(args.loglevel)
    except Exception as e:
        logging.error(f'Invalid loglevel {args.loglevel}:\n{e!s}')
        sys.exit(-1)
    
    return args
