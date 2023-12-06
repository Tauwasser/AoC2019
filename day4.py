#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass, field
from math import log2
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

@dataclass(eq=True, frozen=True)
class Scratchcard:
    id: int
    winners: set[int]
    numbers: set[int]

def read_inputs(example=0) -> list[Scratchcard]:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day4_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    result : list[Scratchcard] = []
    
    for line in data:
        card, rest = line.split(':')
        winners, numbers = rest.split(' | ')
        
        _id = int(card[len('Card '):])
        winners = set(int(winner.strip()) for winner in winners.split(' ') if winner)
        numbers = set(int(number.strip()) for number in numbers.split(' ') if number)
        result.append(Scratchcard(_id, winners, numbers))
    
    # parse logic
    return result

def part1(scratchcards: list[Scratchcard]) -> list[int]:
    """Calculate Points per Card"""
    
    result : list[int] = []
    
    for scratchcard in scratchcards:
        
        hits = scratchcard.winners & scratchcard.numbers
        len_hits = len(hits)
        if (len_hits == 0):
            result.append(0)
            continue
        
        result.append(2**(len_hits - 1))
    
    return result

def part2(scratchcards, points) -> list[int]:
    """Calculate total won Scratchcards"""
    N = len(scratchcards)
    totals : list[int] = [0] + [1 for _ in range(N)]
    
    sc_points = list(map(lambda p: 0 if (p == 0) else int(log2(p)) + 1, points))
    
    for scratchcard, points in zip(scratchcards, sc_points):
        
        for _id in range(scratchcard.id + 1, min(N, scratchcard.id + points) + 1):
            totals[_id] += totals[scratchcard.id]
    
    return totals[1:]

def main(args):
    
    scratchcards = read_inputs(args.example)
    points = part1(scratchcards)
    logging.info(f'Part 1: {sum(points)} ({", ".join(str(p) for p in points)})')
    num_scratchcards = part2(scratchcards, points)
    logging.info(f'Part 2: {sum(num_scratchcards)} ({", ".join(str(n) for n in num_scratchcards)})')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
