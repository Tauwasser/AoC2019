#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """2199943210
3987894921
9856789892
8767896789
9899965678
"""

@dataclass
class Extreme:
    x: int
    y: int
    risk: int

def read_inputs(example=0) -> Tuple[List[List[int]], int, int]:
    
    if (example):
        data = example_input
    else:
        with open('day9_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    field = []
    # parse logic
    for line in data:
        field.append([int(v, 10) for v in f'9{line}9'])
    
    height = len(field)
    width = len(field[0])
    field = [[9] * width, *field, [9] * width]
    
    return field, width - 2, height

def part1(field, width, height) -> List[Extreme]:
    
    extremes = []
    
    for y in range(1, height + 1):
        for x in range(1, width + 1):
            p = field[y][x]
            t = field[y-1][x]
            b = field[y+1][x]
            l = field[y][x-1]
            r = field[y][x+1]
            
            if all(v > p for v in [t, b, l, r]):
                # record coords + risk (one more than height)
                extremes.append(Extreme(x, y, p + 1))
    
    return extremes

def part2():
    pass

def main(args):
    
    field, width, height = read_inputs(args.example)
    minima = part1(field, width, height)
    risk = sum(map(lambda extreme: extreme.risk, minima))
    logging.info(f'Part 1: Cumulative risk is {risk}.')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
