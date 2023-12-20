#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass, field
from itertools import combinations
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

@dataclass(eq=True,frozen=True)
class Galaxy:
    id: int
    x:  int
    y:  int
    
    def distance(self, other):
        if self.__class__ is other.__class__:
            return abs(other.x - self.x) + abs(other.y - self.y)
        return NotImplemented

@dataclass
class Universe:
    width: int  = 0
    height: int = 0
    galaxies: list[Galaxy] = field(default_factory=list, repr=False)

def read_inputs(example=0) -> Universe:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day11_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    universe = Universe(width=len(data[0]), height=len(data))
    _id = 0
    
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if (char == '#'):
                universe.galaxies.append(Galaxy(_id, x, y))
                _id += 1
    
    return universe

def part1(universe: Universe, scale: int=2) -> int:
    
    # find x, y values of galaxies
    xs = set(galaxy.x for galaxy in universe.galaxies)
    ys = set(galaxy.y for galaxy in universe.galaxies)
    
    xexp = set(range(universe.width)) - xs
    yexp = set(range(universe.height)) - ys
    logging.info(f'Expanded Rows:    {", ".join(str(y) for y in sorted(yexp))}')
    logging.info(f'Expanded Columns: {", ".join(str(x) for x in sorted(xexp))}')
    
    # create short-hand for x/y deltas
    xdelta = {x: (dx * (scale -1)) for x, dx in zip(sorted(xexp, reverse=True), range(len(xexp), 0, -1))}
    ydelta = {y: (dy * (scale -1)) for y, dy in zip(sorted(yexp, reverse=True), range(len(yexp), 0, -1))}
    
    # create expanded universe
    expanded = Universe(width=universe.width + len(xexp), height=universe.height + len(yexp))
    
    for galaxy in universe.galaxies:
        _, dx = next(filter(lambda x_dx: x_dx[0] <= galaxy.x, xdelta.items()), (galaxy.x, 0))
        _, dy = next(filter(lambda y_dy: y_dy[0] <= galaxy.y, ydelta.items()), (galaxy.y, 0))
        expanded.galaxies.append(Galaxy(galaxy.id, galaxy.x + dx, galaxy.y + dy))
    
    # iterate over pairs of galaxies and calculate distances
    distances = (lhs.distance(rhs) for lhs, rhs in combinations(expanded.galaxies, 2))
    
    return sum(distances)

def main(args):
    
    universe = read_inputs(args.example)
    distance = part1(universe)
    logging.info(f'Part 1: sum of distances at scale 1: {distance}')
    distance = part1(universe, scale=1_000_000)
    logging.info(f'Part 2: sum of distances at scale 1M: {distance}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
