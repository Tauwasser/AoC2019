#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass, field
from sortedcontainers import SortedListWithKey
from typing import cast, Dict, List, Optional, Tuple, Union

from lib import setup

example_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

@dataclass
class ElevationMap:
    height: int
    width: int
    elevation: List[List[int]] = field(default_factory=list)

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    
    def __eq__(self, other: Union['Point', 'Node']) -> bool:
        return self.x == other.x and self.y == other.y
    
    def distance(self, other: 'Point') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

@dataclass(frozen=True)
class Node:
    pos:      Point
    steps:    int
    distance: int
    value:    int
    
    @property
    def x(self):
        return self.pos.x
    
    @property
    def y(self):
        return self.pos.y

def read_inputs(example=0) -> Tuple[ElevationMap, Point, Point]:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day12_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    
    # parse logic
    start = None
    end = None
    elevations : List[List[int]] = []
    
    for y, row in enumerate(data, 0):
        elevation : List[int] = []
        for x, value in enumerate(row, 0):
            
            if (value == 'S'):
                elevation.append(0)
                start = Point(x, y)
            elif (value == 'E'):
                elevation.append(25)
                end = Point(x, y)
            else:
                elevation.append(ord(value) - ord('a'))
        elevations.append(elevation)
    
    height = len(elevations)
    width = len(elevations[0])
    
    return (ElevationMap(height, width, elevations), start, end)

def part1(m: ElevationMap, s: Point, e: Point) -> int:
    
    sn = Node(s, 0, s.distance(e), 0)
    explore : SortedListWithKey[Node] = SortedListWithKey(key=lambda node: node.steps + node.distance)
    explore.add(sn)
    seen : Dict[Point, Node] = {s: sn}
    
    def _get_elevation(p: Point) -> Optional[int]:
        
        if (0 <= p.x < m.width and 0 <= p.y < m.height):
            return m.elevation[p.y][p.x]
        
        return None
    
    while (len(explore) > 0):
        
        n = cast(Node, explore.pop(0))
        if (n == e):
            break
        
        #logging.info(f'Explore {n.x}/{n.y} (steps {n.steps} distance {n.distance})')
        steps = n.steps + 1
        
        # explore neighboring nodes
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            
            p = Point(n.x + dx, n.y + dy)
            
            # check to see if we run in circles
            sp = seen.get(p, None)
            if (sp is not None and sp.steps <= steps):
                # already explored with better (or same) step count
                continue
            elif (sp is not None):
                # already explored with worse step count
                explore.discard(sp)
            
            # actually explore node
            v = _get_elevation(p)
            if (v is None):
                continue
            if (n.value + 1 < v):
                continue
            np = Node(p, steps, p.distance(e), v)
            explore.add(np)
            seen[p] = np
    else:
        # return a negative number to signify failure
        return -1
    
    # return winning node steps
    return n.steps

def part2(m: ElevationMap, s: Point, e: Point) -> int:
    
    points = [Point(x, y) for x in range(m.width) for y in range(m.height)
              if m.elevation[y][x] == 0
              ]
    logging.info(f'Found {len(points)} possible starting points.')
    return min(filter(lambda s: s > 0, (part1(m, p, e) for p in points)))

def main(args):
    
    m, s, e = read_inputs(args.example)
    fewest_steps = part1(m, s, e)
    logging.info(f'Part 1: fewest steps {fewest_steps}')
    fewest_steps_scenic = part2(m, s, e)
    logging.info(f'Part 2: fewest scenic steps {fewest_steps_scenic}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
