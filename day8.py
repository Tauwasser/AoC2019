#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """30373
25512
65332
33549
35390
"""

@dataclass
class Grid:
    width: int
    height: int
    data : List[List[int]] = field(default_factory=list)

def read_inputs(example=0) -> List[List[int]]:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day8_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    
    grid = []
    # parse logic
    for line in data:
        grid.append(list(int(v) for v in line))

    logging.info(f'Parsed a {len(grid)}x{len(grid[0])} grid of trees')
    return Grid(len(grid[0]), len(grid), grid)

def _makeBitmap(grid: Grid, level: int):
    
    data = [[0 for _ in range(grid.width)] for _ in range(grid.height)]
    
    for h in range(0, grid.height):
        for w in range(0, grid.width):
            
            if (grid.data[h][w] >= level):
                data[h][w] = 1
    
    return data

def part1(grid: Grid) -> int:
    
    visible_trees = 0
    
    # make grids for heights 0 thru 9
    bitmaps = {lvl: _makeBitmap(grid, lvl) for lvl in range(0, 10)}
    
    for h in range(0, grid.height):
        for w in range(0, grid.width):
            
            if (w == 0 or w == grid.width - 1):
                visible_trees += 1
            elif (h == 0 or h == grid.height - 1):
                visible_trees += 1
            else:
                # interior tree
                height = grid.data[h][w]
                visible = False
                bitmap = bitmaps[height]
                
                # check vertical
                if not any(bitmap[dh][w] for dh in range(0, h)) or not any(bitmap[dh][w] for dh in range(h + 1, grid.height)):
                    visible = True
                # check horizontal
                if not any(bitmap[h][dw] for dw in range(0, w)) or not any(bitmap[h][dw] for dw in range(w + 1, grid.width)):
                    visible = True
                
                logging.debug(f'Tree {height} @{w},{h} is {"not " if not visible else ""}visible')
                
                if visible:
                    visible_trees += 1
                
    
    return visible_trees

def part2():
    pass

def main(args):
    
    grid = read_inputs(args.example)
    visible_trees = part1(grid)
    logging.info(f'Part 1: {visible_trees} trees are visible')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
