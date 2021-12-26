#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from collections import defaultdict
from dataclasses import dataclass, field
from functools import reduce
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """2199943210
3987894921
9856789892
8767896789
9899965678
"""

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Extreme:
    x: int
    y: int
    risk: int

@dataclass
class Basin:
    id: int
    size: int = 0
    points: List[Point] = field(default_factory=list)

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

def part2(field, width, height) -> List[Basin]:
    
    basins = []
    
    combined_basins = defaultdict(lambda: set())
    
    VALLEY   = -1
    MOUNTAIN = 9999
    
    # combine all low points, mountains
    for y in range(0, height + 2):
        for x in range(0, width + 2):
            field[y][x] = VALLEY if (field[y][x] < 9) else MOUNTAIN
    
    # collect basins
    for y in range(1, height + 1):
        for x in range(1, width + 1):
            # skip if mountain
            if (field[y][x] == MOUNTAIN):
                continue
            t = field[y-1][x]
            l = field[y][x-1]
            
            # differentiate two cases:
            # - new basin
            # - point in basin
            #   - middle        (top/left same basin)
            #   - meeting point (top/left different basin)
            if (t == MOUNTAIN and l == MOUNTAIN):
                # new basin
                basin_id = len(basins)
                basins.append(Basin(id=basin_id, size=1, points=[Point(x, y)]))
                field[y][x] = basin_id
            else:
                if (t != MOUNTAIN and l != MOUNTAIN and t != l):
                    # two basins meet, we need to add a merge entry
                    key = min(t, l)
                    combined_basins[key].add(max(t, l))
                
                basin_id = min(t, l)
                basin = basins[basin_id]
                basin.size += 1
                basin.points.append(Point(x, y))
                field[y][x] = basin_id
    
    # figure out which basins to copy directly
    copy_basin_ids = set(list(range(len(basins))))
    copy_basin_ids -= set(list(combined_basins.keys()))
    copy_basin_ids -= reduce(set.union, combined_basins.values())
    
    # recursively combine basin ID sets
    def _merge_basin_lists(keys):
        result = set()
        for key in keys:
            result.add(key)
            result |= _merge_basin_lists(combined_basins.get(key, set()))
        return result
    
    seen_basins = set()
    
    for key in combined_basins:
        if (key in seen_basins):
            continue
        combined_basins[key] = _merge_basin_lists(combined_basins[key])
        seen_basins.update(combined_basins[key])
    
    for key in seen_basins:
        if (key in combined_basins):
            del combined_basins[key]
    
    results = [basins[i] for i in copy_basin_ids]
    
    for key, values in combined_basins.items():
        basin = basins[key]
        results.append(basin)
        for value in values:
            other = basins[value]
            basin.size += other.size
            basin.points += other.points
    
    return list(sorted(results, key=lambda basin: -basin.size))

def main(args):
    
    field, width, height = read_inputs(args.example)
    minima = part1(field, width, height)
    risk = sum(map(lambda extreme: extreme.risk, minima))
    logging.info(f'Part 1: Cumulative risk is {risk}.')
    basins = part2(field, width, height)
    largest_basins = basins[:3]
    logging.info(f'Part 2: three largest basins: {", ".join(f"Basin {basin.id} ({basin.size})" for basin in largest_basins)}')
    multiplied_size = reduce(int.__mul__, [basin.size for basin in largest_basins])
    logging.info(f'Part 2: Multiplied Basin Size: {multiplied_size}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
