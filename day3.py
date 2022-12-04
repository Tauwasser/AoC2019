#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

@dataclass
class Rucksack:
    lhs: str
    rhs: str

def read_inputs(example=0) -> List[Rucksack]:
    
    if (example):
        data = example_input
    else:
        with open('day3_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    rucksacks = []
    # parse logic
    for line in data:
        items = len(line) // 2
        rucksacks.append(Rucksack(line[:items], line[items:]))
    
    return rucksacks

def get_priority(char: str):
    
    if (char >= 'a' and char <= 'z'):
        return ord(char[0]) - ord('a') + 1
    return ord(char[0]) - ord('A') + 27

def part1(rucksacks: List[Rucksack]) -> int:
    
    priorities = 0
    for rucksack in rucksacks:
        # set intersect to find item
        item = set(rucksack.lhs) & set(rucksack.rhs)
        priorities += get_priority(''.join(item))
    
    return priorities

def part2():
    pass

def main(args):
    
    rucksacks = read_inputs(args.example)
    sum_priorities = part1(rucksacks)
    logging.info(f'Part 1: Sum of Priorities {sum_priorities}')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
