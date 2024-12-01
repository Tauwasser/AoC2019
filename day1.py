#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import logging

from collections import defaultdict

from lib import setup

example_input = """3   4
4   3
2   5
1   3
3   9
3   3
"""

def read_inputs(example=0) -> tuple[tuple[int, int]]:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day1_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    
    # parse logic
    pattern = re.compile(r'(\d+)\s+(\d+)')
    
    lhs = []
    rhs = []
    
    for line in data:
        m = pattern.match(line)
        if (m is None):
            raise RuntimeError(f'Cannot parse line: {line}')
        lhs.append(int(m.group(1)))
        rhs.append(int(m.group(2)))
    
    return (tuple(lhs), tuple(rhs))

def part1(lhs: tuple[int], rhs: tuple[int]) -> tuple[int]:
    """Take left-hand side and right-hand side list and calculate distances."""
    return tuple(map(lambda l, r: l -r if (l > r) else r - l, sorted(lhs), sorted(rhs)))

def part2(lhs: tuple[int], rhs: tuple[int]) -> tuple[int]:
    """Calculate similarity score from left-hand side and right-hand side lists."""
    
    num_in_rhs = defaultdict(lambda: 0)
    
    for value in rhs:
        num_in_rhs[value] += 1
    
    return tuple(map(lambda l: l * num_in_rhs.get(l, 0), lhs))

def main(args):
    
    lhs, rhs = read_inputs(args.example)
    distances = part1(lhs, rhs)
    logging.info(f'Part 1: {sum(distances)} ({" + ".join(str(d) for d in distances[:20])})')
    similarities = part2(lhs, rhs)
    logging.info(f'Part 2: {sum(similarities)} ({" + ".join(str(s) for s in similarities[:20])})')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
