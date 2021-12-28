#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import math

from enum import IntEnum, IntFlag
from dataclasses import dataclass, field
from sortedcontainers import SortedList
from typing import Dict, List, Optional, Tuple, Union

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

# forward-declare Node
class Node:
    pass

@dataclass
class Node:
    x: int
    y: int
    risk: int
    heur: int
    explored: Direction
    cost: Union[float,int] = math.inf
    prev: Node = None

@dataclass
class Path:
    cost: int
    nodes: List[Node] = field(default_factory=list)

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
    
    start = Node(0, 0, field.data[0][0], field.height + field.width - 2, Direction.TOP | Direction.LEFT, cost=0)
    end = Node(field.width - 1, field.height - 1, field.data[field.height - 1][field.width - 1], 0, Direction.RIGHT | Direction.BOTTOM)
    
    # count explored nodes
    explored = 0
    
    # list of nodes (sorted ascending by heuristic)
    node_list : SortedList[Node] = SortedList(key=lambda node: node.cost + node.heur)
    node_list.add(start)
    
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
    
    # explore a node
    def explore(node: Node, direction: Direction, dx: int, dy: int):
        nonlocal explored
        
        if (node.explored & direction):
            return
        
        # get new node data
        x = node.x + dx
        y = node.y + dy
        risk = field.data[y][x]
        heur = end.x - x + end.y - y
        
        # mark node direction explored
        node.explored |= direction
        # get/create target node
        next = nodes.get((x, y), Node(x, y, risk, heur, possible_directions(x, y)))
        nodes[(x, y)] = next
        
        # explore target node if not fully explored yet
        if (next.explored != Direction.ALL):
            
            # check if existing path might be cheaper
            if (next.cost <= node.cost + next.risk):
                return
            
            # store cheapest cost to reach node
            next.cost = min(next.cost, node.cost + next.risk)
            next.prev = node
            node_list.add(next)
    
    while (True):
        
        # explore node at cheapest path
        node = node_list.pop(0)
        explored += 1
        logging.debug(f'Exploring Node at ({node.x}, {node.y}).')
        
        # we found the cheapest path to end node
        if (node is end):
            break
        
        # create nodes/paths for all unexplored directions
        explore(node, Direction.TOP,    0, -1)
        explore(node, Direction.BOTTOM, 0, +1)
        explore(node, Direction.LEFT,   -1, 0)
        explore(node, Direction.RIGHT,  +1, 0)
    
    logging.info(f'Explored {explored} nodes.')
    result = Path(node.cost, [node])
    # sum all previous nodes
    while (node is not start):
        result.nodes.append(node.prev)
        node = node.prev
    result.nodes.reverse()
    return result

def part2(field: Field) -> Path:
    
    w = field.width
    h = field.height
    width = field.width * 5
    height = field.height * 5
    
    # new data array
    data = [[0 for _ in range(width)] for _ in range(height)]
    
    # scale field data
    for cpy_y in range(0, 5):
        for cpy_x in range(0, 5):
            offset = cpy_y + cpy_x
            for y in range(h):
                for x in range(w):
                    data[cpy_y*h + y][cpy_x*w + x] = 1 + (offset + field.data[y][x] - 1) % 9
    
    field = Field(data, width, height)
    return part1(field)

def main(args):
    
    logging.info('Start A* search')
    field = read_inputs(args.example)
    path = part1(field)
    logging.info(f'Part 1: {path.cost} risk for cheapest path ({len(path.nodes)} nodes).')
    path = part2(field)
    logging.info(f'Part 2: {path.cost} risk for cheapest 5x5 path ({len(path.nodes)} nodes).')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
