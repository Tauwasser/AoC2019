#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """
"""

def read_inputs(example=0):
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('dayN_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    
    # parse logic
    return None

def part1():
    pass

def part2():
    pass

def main(args):
    
    read_inputs(args.example)
    part1()
    logging.info(f'Part 1: ')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
