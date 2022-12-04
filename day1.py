#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

def read_inputs(example=0):
    
    if (example):
        data = example_input
    else:
        with open('day1_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    # parse logic
    calories = []
    entry = []
    
    for line in data:
        if (line != ''):
            entry.append(int(line))
            continue
        calories.append(entry)
        entry = []
    
    if (entry):
        calories.append(entry)
    
    return calories

def part1(calories : List[List[int]]) -> int:
    
    calories_per_elf = list(map(sum, calories))
    return max(calories_per_elf)

def part2(calories : List[List[int]]) -> int:
    
    calories_per_elf = list(map(sum, calories))
    return sum(sorted(calories_per_elf)[-3:])

def main(args):
    
    calorie_lists = read_inputs(args.example)
    max_calories = part1(calorie_lists)
    logging.info(f'Part 1: Max Calories {max_calories}')
    top_calories = part2(calorie_lists)
    logging.info(f'Part 2: Top 3 Calories {top_calories}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
