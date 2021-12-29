#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from math import sqrt
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """target area: x=20..30, y=-10..-5
"""

@dataclass
class TargetArea:
    x: range
    y: range

def read_inputs(example=0) -> TargetArea:
    
    if (example):
        data = example_input
    else:
        with open('day17_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    command = 'target area: '
    
    data = data.splitlines()[0]
    
    # parse logic
    entries = [entry.split('=') for entry in data[len(command):].split(', ')]
    ranges = list(map(lambda axis_r: (axis_r[0], *sorted(int(x) for x in axis_r[1].split('..')),), entries))
    x_range = next(filter(lambda entry: entry[0] == 'x', ranges))
    y_range = next(filter(lambda entry: entry[0] == 'y', ranges))
    
    return TargetArea(range(x_range[1], x_range[2] + 1), range(y_range[1], y_range[2] + 1))

def part1(target: TargetArea) -> Tuple[int, int, int]:
    
    # final (and highest) x position will be
    # x_0 + x_0 - 1 + x_0 - 2 etc.
    # --> x := sum(x_i) := sum of first N natural numbers
    # --> x := n * (n + 1) / 2 := x_0 * (x_0 + 1) / 2
    # --> find possible start velocities
    # --> solve x²_0 + x_0 - 2 * x = 0
    # x_0 := -1/2 + sqrt(1/4 + 2 * x)
    
    x0s = [int(f) for f in filter(lambda f: f.is_integer(),
                                  [-1/2 + sqrt(1/4 + 2 * x) for x in target.x]
                                  )]
    x_highs = [(x0 * (x0 + 1)) // 2 for x0 in x0s]
    
    # high y position (where dx == 0) will be
    # y_high := sum(y_i) for first x_0 steps
    # after that it might rise for (y_0 - x_0) steps (if y_0 > x_0)
    # after that, y will fall exponentially w/ linear velocity -1
    # 0, -1, -3, -6, -10, -15 etc. for _all_ trajectories
    
    # pre-compute some deltas
    def generate_ys():
        y = 0
        delta_y = -1
        while (True):
            y += delta_y
            delta_y -= 1
            yield y
    
    # generate first 200 y offset values (delta v applied to highest point)
    y_gen = generate_ys()
    y_offsets = [next(y_gen) for _ in range(200)]
    
    best_y_highest = 0
    best_x0 = None
    best_y0 = None
    
    for x0 in x0s:
        # sweep y_0 from 250 to x0 (45°)
        for y0 in range(250, x0 - 1, -1):
            # generate first 20 (or so...) points
            points = []
            x = 0
            y = 0
            dx = x0
            dy = y0
            for _ in range(x0):
                x += dx
                y += dy
                dx = max(dx - 1, 0)
                dy -= 1
                points.append((x, y))
            assert(dx == 0)
            # add delta if y0 > x0
            for _ in range(y0 - x0):
                y += dy
                dy -= 1
                points.append((x, y))
            assert(dy == 0)
            # add pre-computed y offsets
            for y_off in y_offsets:
                points.append((x, y + y_off))
            if any(x in target.x and y in target.y for x, y in points):
                y_highest = max(y for x, y in points)
                if (y_highest > best_y_highest):
                    best_y_highest = y_highest
                    best_x0 = x0
                    best_y0 = y0
    
    return best_x0, best_y0, best_y_highest

def part2():
    pass

def main(args):
    
    target = read_inputs(args.example)
    v_x, v_y, y_highest = part1(target)
    logging.info(f'Part 1: Initial Velocity {v_x}/{v_y} for highest y {y_highest}.')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
