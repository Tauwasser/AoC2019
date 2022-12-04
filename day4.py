#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

@dataclass
class Section:
    begin: int
    end:   int
    
    def contains(self, other: 'Section') -> bool:
        
        if (self.begin <= other.begin and self.end >= other.end):
            return True
        return False

@dataclass
class ElfPair:
    lhs: Section
    rhs: Section

def read_inputs(example=0) -> List[ElfPair]:
    
    if (example):
        data = example_input
    else:
        with open('day4_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    elf_pairs = []
    # parse logic
    for line in data:
        lhs, rhs = tuple(map(lambda section: Section(*(int(v) for v in section.split('-', 1))), line.split(',', 1)))
        elf_pairs.append(ElfPair(lhs, rhs))
    
    return elf_pairs

def part1(elf_pairs: List[ElfPair]):
    
    need_reassignment = 0
    for elf_pair in elf_pairs:
        if (elf_pair.lhs.contains(elf_pair.rhs)):
            need_reassignment += 1
            continue
        if (elf_pair.rhs.contains(elf_pair.lhs)):
            need_reassignment += 1
            continue
    
    return need_reassignment

def part2():
    pass

def main(args):
    
    elf_pairs = read_inputs(args.example)
    need_reassignment = part1(elf_pairs)
    logging.info(f'Part 1: {need_reassignment} elf pairs need reassignment')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
