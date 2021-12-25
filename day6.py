#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """3,4,3,1,2
"""

def read_inputs(example=False) -> Dict[int, int]:
    
    if (example):
        data = example_input
    else:
        with open('day6_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    # parse logic
    fish = defaultdict(lambda: 0)
    for v in [int(v.strip(), 10) for v in data.split(',')]:
        fish[v] += 1
    return {k: fish.get(k, 0) for k in range(8 + 1)}

def simLanternfish(fish: Dict[int, int]):
    
    # advance fish by one day
    result = {(k-1): fish[k] for k in range(1, 8 + 1)}
    
    # take mature fish and spawn new fish
    result[8] = fish[0]
    # reset mature fish counter
    result[6] += fish[0]
    
    # update fish state
    fish.update(result)

def part1(fish: Dict[int, int], days=80):
    
    for day in range(1, days + 1):
        simLanternfish(fish)
        logging.debug(f'After {day} day(s) there are {sum(fish.values())} fish.')
        logging.debug(f'Fish: {fish}')

def part2(fish: Dict[int, int]):
    pass

def main(args):
    
    fish = read_inputs(args.example)
    fish_pt1 = {**fish}
    fish_pt2 = {**fish}
    part1(fish_pt1)
    logging.info(f'Part 1: After 80 days there are {sum(fish_pt1.values())} fish.')
    part2(fish_pt2)
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
