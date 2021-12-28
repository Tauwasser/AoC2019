#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

def read_inputs(example=0) -> Tuple[str, Dict[str, str]]:
    
    if (example):
        data = example_input
    else:
        with open('day14_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    template = data[0]
    rules = {}
    assert(data[1] == '')
    
    for line in data[2:]:
        pair, insert = line.split(' -> ')
        rules[pair] = insert
    
    return template, rules

def part1(template: str, rules: Dict[str, str], steps=10) -> str:
    
    polymer = template
    
    for _ in range(steps):
        
        insertions = []
        offset = 0
        
        # find insertions
        for position in range(len(polymer) - 1):
            # get pair of elements
            pair = polymer[position:position+2]
            # find what (if any) element to insert
            element = rules.get(pair, None)
            if (element is None):
                continue
            # record insertion
            insertions.append((position + 1, element))
        
        # execute insertions
        for position, element in insertions:
            
            position += offset
            polymer = polymer[:position] + element + polymer[position:]
            # shift position offset
            offset += 1
    
    return polymer

def part2(polymer: str, rules: Dict[str, str], steps=40):
    return part1(polymer, rules, steps=steps)

def getMostAndLeastCommon(polymer: str) -> Tuple[Tuple[str, int], Tuple[str, int]]:
    
    counts = {key: polymer.count(key) for key in set(polymer)}
    sorted_counts = sorted(counts.items(), key=lambda keyvalue: keyvalue[1])
    
    return sorted_counts[-1], sorted_counts[0]

def main(args):
    
    template, rules = read_inputs(args.example)
    polymer = part1(template, rules, steps=10)
    most_common, least_common = getMostAndLeastCommon(polymer)
    logging.debug(f'Part 1: Polymer after 10 steps: {polymer}')
    logging.info(f'Part 1: Delta most/least common after 10 steps: {most_common[1] - least_common[1]} ({most_common[0]}: {most_common[1]} {least_common[0]}: {least_common[1]})')
    polymer = part2(template, rules, steps=40)
    most_common, least_common = getMostAndLeastCommon(polymer)
    logging.debug(f'Part 2: Polymer after 40 steps: {polymer}')
    logging.info(f'Part 2: Delta most/least common after 40 steps: {most_common[1] - least_common[1]} ({most_common[0]}: {most_common[1]} {least_common[0]}: {least_common[1]})')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
