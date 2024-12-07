#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import re

from collections import defaultdict
from functools import cmp_to_key
from dataclasses import dataclass, field

from lib import setup

example_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


@dataclass
class Update:
    pages: tuple[int]


@dataclass
class Puzzle:
    rules: dict[int, set[int]]
    updates: list[Update]


def read_inputs(example=0) -> Puzzle:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day5_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    lines = iter(data)
    
    orderings = []
    
    # parse logic
    before = defaultdict(lambda: set())
    
    # parse orderings
    for line in lines:
        m = re.match(r'(\d+)\|(\d+)', line)
        if (m is None):
            break
        lhs, rhs = int(m.group(1)), int(m.group(2))
        before[rhs].add(lhs)
    
    # parse page updates
    updates = list(Update(tuple(int(i.strip()) for i in line.split(','))) for line in lines)
    return Puzzle({**before}, updates)

def part1(puzzle: Puzzle) -> list[Update]:
    """Determine correctly-ordered Updates
    
    Returns:
        List of correctly-ordered updates.
    """
    result = []
    
    # check each update
    for ix, update in enumerate(puzzle.updates, 1):
        # check each page
        for pg in range(len(update.pages)):
            # check if any following pages should actually be printed before
            # current page
            after = set(update.pages[pg+1:])
            after &= puzzle.rules.get(update.pages[pg], set())
            if (after):
                logging.info(f'Update #{ix}: Page(s) {", ".join(str(page) for page in after)} must be printed before page {update.pages[pg]}!')
                break
        else:
            result.append(update)
    
    return result

def part2(puzzle: Puzzle, correctly_ordered_updates: list[Update]) -> list[Update]:
    """Produce correctly-ordered Updates from incorrectly-ordered Updates and Rules
    
    Returns:
        List of newly created correctly-ordered updates.
    """
    result = []
    
    # custom comparison function
    def cmp(lhs: int, rhs: int):
        if (rhs in puzzle.rules.get(lhs, set())):
            return +1
        elif (lhs in puzzle.rules.get(rhs, set())):
            return -1
        return 0
    
    # check each update
    for ix, update in enumerate(puzzle.updates, 1):
        # skip correctly-ordered updates
        if (update in correctly_ordered_updates):
            continue
        result.append(Update(tuple(sorted(update.pages, key=cmp_to_key(cmp)))))
    
    return result

def main(args):
    
    puzzle = read_inputs(args.example)
    updates = part1(puzzle)
    logging.info(f'Part 1: {sum(update.pages[len(update.pages) // 2] for update in updates)} ({" + ".join(str(update.pages[len(update.pages) // 2]) for update in updates[:10])})')
    updates = part2(puzzle, updates)
    logging.info(f'Part 2: {sum(update.pages[len(update.pages) // 2] for update in updates)} ({" + ".join(str(update.pages[len(update.pages) // 2]) for update in updates[:10])})')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
