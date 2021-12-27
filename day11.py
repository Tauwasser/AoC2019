#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from collections import defaultdict
from functools import reduce
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

def read_inputs(example=0) -> Tuple[List[List[int]], int, int]:
    
    if (example):
        data = example_input
    else:
        with open('day11_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    field = []
    # parse logic
    for line in data:
        field.append([int(v, 10) for v in f'0{line}0'])
    
    height = len(field)
    width = len(field[0])
    
    field = [[0]* width, *field, [0] * width]
    
    # field is surrounded by band of dummy dumbo octupuses with zero energy
    return field, width - 2, height

def part1(field, width, height, steps=100):
    
    # keep a dynamic list of flashing dumbo octopuses
    # to prevent polynomial/exponential run-time
    
    flashes = 0
    octopuses = []
    
    ys = range(1, height + 1)
    xs = range(1, width + 1)
    
    def inc(x, y):
        nonlocal flashes
        field[y][x] += 1
        # only record octopus on first flash this step
        if (field[y][x] == 10 and y in ys and x in xs):
            flashes += 1
            octopuses.append((x, y))
    
    for _ in range(steps):
        
        # increment energy
        for y in range(1, height + 1):
            for x in range(1, width + 1):
                inc(x, y)
        
        # evaluate dynamic list of flashing octopuses
        while (octopuses):
            
            x, y = octopuses.pop(0)
            # this row (left/right)
            inc(x - 1, y)
            inc(x + 1, y)
            # next row
            inc(x - 1, y + 1)
            inc(x,     y + 1)
            inc(x + 1, y + 1)
            # previous row
            inc(x - 1, y - 1)
            inc(x,     y - 1)
            inc(x + 1, y - 1)
        
        # reset flashed octopuses
        for y in range(1, height + 1):
            for x in range(1, width + 1):
                if (field[y][x] > 9):
                    field[y][x] = 0
    
    return flashes

def part2(field, width, height):
    pass

def main(args):
    
    field, width, height = read_inputs(args.example)
    flashes = part1(field, width, height, steps=100)
    logging.info(f'Part 1: {flashes} flashes after 100 steps.')
    part2(field, width, height)
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
