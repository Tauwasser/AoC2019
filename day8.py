#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import logging

from dataclasses import dataclass, field
from itertools import cycle
from typing import Dict, List, Optional, Tuple

from lib import setup

example1_input = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

example2_input = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

example3_input = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

NodeId = str

@dataclass(eq=True, frozen=True)
class Node:
    id:    NodeId
    left:  NodeId
    right: NodeId

@dataclass(eq=True)
class PuzzleMap:
    instructions: list[str] = field(default_factory=list)
    nodes : dict[NodeId, Node] = field(default_factory=dict, repr=False)

def read_inputs(example=0) -> PuzzleMap:
    
    match (example):
        case 1 if (example):
            data = example1_input
        case 2 if (example):
            data = example2_input
        case 3 if (example):
            data = example3_input
        case _:
            with open('day8_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    puzzle = PuzzleMap()
    
    # line 0 is instructions left/right (L/R)
    puzzle.instructions = data[0]
    pattern = re.compile(r'([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)')
    
    for line in data[2:]:
        
        m = pattern.match(line)
        if (m is None):
            raise RuntimeError(f'Line \'{line}\' does not match expected format!')
        
        _id, _lhs, _rhs = m.groups()
        puzzle.nodes[_id] = Node(_id, _lhs, _rhs)
    
    return puzzle

def part1(puzzle: PuzzleMap) -> int:
    """Traverse Puzzle Map to find out how many steps it takes from AAA to ZZZ"""
    
    AAA = puzzle.nodes.get('AAA', None)
    ZZZ = puzzle.nodes.get('ZZZ', None)
    
    cur = AAA
    num_steps = 0
    
    if (AAA is None or ZZZ is None):
        logging.error(f'Could not find AAA/ZZZ Nodes...')
        return num_steps
    
    for step in cycle(puzzle.instructions):
        
        num_steps += 1
        nxt = cur.left if (step == 'L') else cur.right
        cur = puzzle.nodes[nxt]
        
        if (cur is ZZZ):
            break
        
    return num_steps

def part2(puzzle: PuzzleMap):
    """Traverse Puzzle Map to find out how many steps it takes from ??A to ??Z
    
    Iterate paths simultaneously until all current nodes end in Z.
    """
    
    cur = [puzzle.nodes[key] for key in puzzle.nodes.keys() if key.endswith('A')]
    num_steps = 0
    
    for step in cycle(puzzle.instructions):
        
        num_steps += 1
        
        # update all nodes
        for ix, node in enumerate(cur):
            nxt = node.left if (step == 'L') else node.right
            cur[ix] = puzzle.nodes[nxt]
        
        if all(node.id.endswith('Z') for node in cur):
            break
    
    return num_steps

def main(args):
    
    puzzle = read_inputs(args.example)
    num_steps = part1(puzzle)
    logging.info(f'Part 1: {num_steps} from AAA to ZZZ')
    num_steps = part2(puzzle)
    logging.info(f'Part 2: {num_steps} from ??A to ??Z simultaneously')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
