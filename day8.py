#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass, field
from math import prod
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

def _makeHorizontalCounts(grid: Grid) -> Tuple[List[List[Dict[int, int]]]]:
    
    view_t = [[{i: 0 for i in range(10)} for _ in range(grid.width)] for _ in range(grid.height)]
    
    for h in range(1, grid.height):
        for w in range(0, grid.width):
            for i in range(10):
                view_t[h][w][i] = view_t[h - 1][w][i]
                if (grid.data[h - 1][w] < i):
                    view_t[h][w][i] += 1
                else:
                    view_t[h][w][i] = 1
    
    view_b = [[{i: 0 for i in range(10)} for _ in range(grid.width)] for _ in range(grid.height)]
    
    for h in range(grid.height - 2, -1, -1):
        for w in range(0, grid.width):
            for i in range(10):
                view_b[h][w][i] = view_b[h + 1][w][i]
                if (grid.data[h + 1][w] < i):
                    view_b[h][w][i] += 1
                else:
                    view_b[h][w][i] = 1

    return view_t, view_b

def _makeVerticalCounts(grid: Grid) -> Tuple[List[List[Dict[int, int]]]]:
    
    view_l = [[{i: 0 for i in range(10)} for _ in range(grid.width)] for _ in range(grid.height)]
    
    for w in range(1, grid.width):
        for h in range(0, grid.height):
            for i in range(10):
                view_l[h][w][i] = view_l[h][w - 1][i]
                if (grid.data[h][w - 1] < i):
                    view_l[h][w][i] += 1
                else:
                    view_l[h][w][i] = 1
    
    view_r = [[{i: 0 for i in range(10)} for _ in range(grid.width)] for _ in range(grid.height)]
    
    for w in range(grid.width - 2, -1, -1):
        for h in range(0, grid.height):
            for i in range(10):
                view_r[h][w][i] = view_r[h][w + 1][i]
                if (grid.data[h][w + 1] < i):
                    view_r[h][w][i] += 1
                else:
                    view_r[h][w][i] = 1
    
    return view_l, view_r

def part2(grid: Grid) -> Tuple[int, int, int]:
    
    # compute scores by row/column in each direction
    view_t, view_b = _makeHorizontalCounts(grid)
    view_l, view_r = _makeVerticalCounts(grid)
    # scenic scores per tree
    scores = [[0 for _ in range(grid.width)] for _ in range(grid.height)]
    
    # scenic score as sum of score in each direction
    for h in range(0, grid.height):
        for w in range(0, grid.width):
            i = grid.data[h][w]
            scores[h][w] = prod(v[h][w][i] for v in [view_t, view_b, view_l, view_r])
    
    max = 0
    max_h = 0
    max_w = 0
    
    for h in range(grid.height):
        for w in range(grid.width):
            if (max < scores[h][w]):
                max = scores[h][w]
                max_h = h
                max_w = w
    
    return max_w, max_h, max, grid.data[max_h][max_w]

def main(args):
    
    grid = read_inputs(args.example)
    visible_trees = part1(grid)
    logging.info(f'Part 1: {visible_trees} trees are visible')
    x, y, score, value = part2(grid)
    logging.info(f'Part 2: Tree {value} @{x},{y} with score {score}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
