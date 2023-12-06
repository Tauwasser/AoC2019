#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import sys
import logging

from dataclasses import dataclass
from functools import reduce
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """Time:      7  15   30
Distance:  9  40  200
"""

@dataclass(eq=True, frozen=True)
class Race:
    id :    int
    time:   int
    """Time in Milliseconds"""
    distance: int
    """Distance in Millimeters"""

def read_inputs(example=0) -> list[Race]:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day6_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    races : list[Race] = []
    
    # first line is time
    time, millis = data[0].split(':')
    if (time != 'Time'):
        raise RuntimeError("Expected Time on line 1.")
    
    distance, dists = data[1].split(':')
    if (distance != 'Distance'):
        raise RuntimeError("Expected Distance on line 1.")
    
    milliseconds = (int(ms.strip()) for ms in millis.split(' ') if ms)
    distances = (int(dist.strip()) for dist in dists.split(' ') if dist)
    
    for _id, (ms, dist) in enumerate(zip(milliseconds, distances)):
        races.append(Race(_id, ms, dist))
    
    return races

def part1(races: list[Race]) -> list[tuple[int, int]]:
    """Calculate the minimum and maximum hold time for each race"""
    
    # d [mm] = x * 1mm/ms * (t - x) [ms]
    # 0 = t*x - x² - d
    # 0 = -t*x + x² + d
    #
    # use p/q formula:
    # x1/2 = -p/2 ± √[(p/2)² - q]
    # => x1/2 = t/2 ± √[t² / 4 - d]
    
    # the lower bound must be rounded up
    # the upper bound must be rounded down
    
    # we have to *beat* the record, not just meet it
    # therefore we have to deal with x1/x2 that are integer
    # values to begin with
    
    results : list[tuple[int, int]] = []
    
    for race in races:
        
        t = race.time
        d = race.distance
        
        x1 = t / 2 - math.sqrt(t * t / 4 - d)
        x2 = t / 2 + math.sqrt(t * t / 4 - d)
        
        x1 = int(math.ceil(x1)) + (1 if x1.is_integer() else 0)
        x2 = int(math.floor(x2)) + (-1 if x2.is_integer() else 0)
        
        results.append((x1, x2))
    
    return results

def part2(races: list[Race]):
    
    times = ''
    distances = ''
    
    for race in races:
        times += str(race.time)
        distances += str(race.distance)
    
    race = Race(-1, int(times), int(distances))
    return part1([race])

def main(args):
    
    races = read_inputs(args.example)
    times = part1(races)
    logging.info(f'Part 1: {reduce(lambda lhs, rhs: lhs * rhs, (t[1] - t[0] + 1 for t in times))} ({", ".join(str(t) for t in times)})')
    times = part2(races)
    logging.info(f'Part 2: {reduce(lambda lhs, rhs: lhs * rhs, (t[1] - t[0] + 1 for t in times))} ({", ".join(str(t) for t in times)})')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
