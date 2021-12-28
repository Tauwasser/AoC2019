#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import math

from enum import IntEnum, IntFlag
from dataclasses import dataclass, field
from sortedcontainers import SortedList
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""

@dataclass
class Field:
    data: List[List[int]]
    width: int
    height: int

class Direction(IntFlag):
    NONE   = 0
    TOP    = 1
    BOTTOM = 2
    LEFT   = 4
    RIGHT  = 8
    ALL    = TOP | BOTTOM | LEFT | RIGHT

@dataclass
class Node:
    x: int
    y: int
    risk: int
    explored: Direction

@dataclass
class Path:
    risk: int
    nodes: List[Node]
    
    @property
    def node(self):
        return self.nodes[-1]

def read_inputs(example=0) -> Field:
    
    if (example):
        data = example_input
    else:
        with open('day15_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = [[int(i, 10) for i in line] for line in data.splitlines()]
    width = len(data[0])
    height = len(data)
    
    return Field(data, width, height)

def part1(field: Field) -> Optional[Path]:
    
    start = Node(0, 0, field.data[0][0], Direction.TOP | Direction.LEFT)
    end = Node(field.width - 1, field.height - 1, field.data[field.height - 1][field.width - 1], Direction.RIGHT | Direction.BOTTOM)
    
    # count explored nodes
    explored = 0
    
    # list of paths (sorted ascending by risk)
    paths : SortedList[Path] = SortedList(key=lambda path: path.risk)
    paths.add(Path(0, [start]))
    
    # map of nodes (x, y) -> Node
    nodes : Dict[Tuple[int, int], Node] = {
        (start.x, start.y): start,
        (end.x, end.y):     end
    }
    
    def possible_directions(x, y):
        direction = Direction.NONE
        if (x == 0):
            direction |= Direction.LEFT
        if (y == 0):
            direction |= Direction.TOP
        if (x == field.width - 1):
            direction |= Direction.RIGHT
        if (y == field.height - 1):
            direction |= Direction.BOTTOM
        return direction
    
    # explore a path node
    def explore(path, direction, dx, dy):
        nonlocal explored
        
        if (path.node.explored & direction):
            return
        
        # get new node data
        x = path.node.x + dx
        y = path.node.y + dy
        risk = field.data[y][x]
        
        # mark node direction explored
        path.node.explored |= direction
        # get/create target node
        node = nodes.get((x, y), Node(x, y, risk, possible_directions(x, y)))
        nodes[(x, y)] = node
        
        # explore target node if not fully explored yet
        if (node.explored != Direction.ALL):
            
            # check if existing path might be cheaper
            existing = next(filter(lambda path: path.node.x == x and path.node.y == y, paths), None)
            if (existing is not None and (existing.risk <= path.risk + node.risk)):
                return
            
            logging.debug(f'Exploring Node at ({x}, {y}).')
            explored += 1
            paths.add(Path(path.risk + node.risk, path.nodes[:] + [node]))
    
    while (True):
        
        # explore node at cheapest path
        path = paths.pop(0)
        
        # we found the cheapest path to end node
        if (path.node.x == end.x and path.node.y == end.y):
            logging.info(f'Explored {explored} nodes.')
            return path
        
        # create nodes/paths for all unexplored directions
        explore(path, Direction.TOP,    0, -1)
        explore(path, Direction.BOTTOM, 0, +1)
        explore(path, Direction.LEFT,   -1, 0)
        explore(path, Direction.RIGHT,  +1, 0)
    
    return None

def part2():
    pass

def main(args):
    
    field = read_inputs(args.example)
    path = part1(field)
    logging.info(f'Part 1: {path.risk} risk for cheapest path ({len(path.nodes)} nodes).')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
