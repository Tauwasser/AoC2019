#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import math

from typing import List, Tuple

from lib import setup

example_input = """16,1,2,0,4,2,7,1,2,14
"""

def read_inputs(example=False) -> List[int]:
    
    if (example):
        data = example_input
    else:
        with open('day7_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    # parse logic
    return [int(v.strip(), 10) for v in data.split(',')]

def part1(crab_positions: List[int]) -> Tuple[int, int]:
    
    # sort crab positions
    crab_positions = sorted(crab_positions)
    num_crabs = len(crab_positions)
    
    # determine median crab position
    median_pos = crab_positions[num_crabs // 2]
    
    fuel = sum(map(lambda pos: abs(pos - median_pos), crab_positions))
    
    return fuel, median_pos

def part2(crab_positions: List[int]) -> Tuple[int, int]:
    
    def cost(steps):
        return steps * (steps + 1) / 2
    
    min_pos = min(crab_positions)
    max_pos = max(crab_positions)
    result_pos = None
    result_fuel = math.inf
    
    # sweep through all possible positions and determine total cost to move all crabs
    for pos in range(min_pos, max_pos + 1):
        fuel = 0
        for crab in crab_positions:
            fuel += cost(abs(crab - pos))
            # maybe optimize
            if (fuel > result_fuel):
                break;
        if (fuel < result_fuel):
            result_fuel = fuel
            result_pos = pos
    
    return result_fuel, result_pos

def main(args):
    
    crab_positions = read_inputs(args.example)
    fuel, pos = part1(crab_positions[:])
    logging.info(f'Part 1: Need {fuel} fuel to move all crabs to {pos}.')
    fuel, pos = part2(crab_positions[:])
    logging.info(f'Part 2: Need {fuel} fuel to move all crabs to {pos}.')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
