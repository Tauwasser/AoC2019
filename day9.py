#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

@dataclass(eq=True, frozen=True)
class Reading:
    id:     int
    values: tuple[int]

def read_inputs(example=0) -> list[Reading]:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day9_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    readings : list[Reading] = []
    
    for _id, line in enumerate(data, 1):
        readings.append(Reading(_id, tuple(int(v.strip()) for v in line.split(' ') if v)))
    
    return readings

def part1(readings: list[Reading]) -> list[int]:
    """Analyze OASIS readings and generate predictions"""
    
    predictions : list[int] = []
    
    def _predict(values: tuple[int]) -> int:
        
        if (all(v == values[0] for v in values)):
            return values[0]
        
        # calculate deltas
        deltas = tuple(map(lambda t0, t1: t1 - t0, values, values[1:]))
        nxt_delta = _predict(deltas)
        return values[-1] + nxt_delta
    
    for reading in readings:
        predictions.append(_predict(reading.values))
    
    return predictions

def part2():
    pass

def main(args):
    
    readings = read_inputs(args.example)
    predictions = part1(readings)
    logging.info(f'Part 1: {sum(predictions)} ({" ".join(str(v) for v in predictions)})')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
