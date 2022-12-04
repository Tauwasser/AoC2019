#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """A Y
B X
C Z
"""

class OppHand(Enum):
    ROCK     = ('A')
    PAPER    = ('B')
    SCISSORS = ('C')
    
    def __new__(cls, ltr):
        obj = object.__new__(cls)
        obj._value_ = ltr
        return obj

class YourHand(Enum):
    ROCK     = ('X', 1, OppHand.SCISSORS, OppHand.PAPER)
    PAPER    = ('Y', 2, OppHand.ROCK,     OppHand.SCISSORS)
    SCISSORS = ('Z', 3, OppHand.PAPER,    OppHand.ROCK)
    
    def __new__(cls, ltr, pts, beats, beat_by):
        obj = object.__new__(cls)
        obj._value_ = ltr
        obj.pts = pts
        obj.beats = beats
        obj.beat_by = beat_by
        return obj
    
    def score(self, other: OppHand) -> int:
        
        logging.debug(f'Mine {self} Other {other}')
        
        if self.beats == other:
            # won
            return self.pts + 6
        if self.beat_by == other:
            # lost
            return self.pts + 0
        # draw
        return self.pts + 3

class Result(Enum):
    LOSE = ('X')
    DRAW = ('Y')
    WIN  = ('Z')
    
    def __new__(cls, ltr):
        obj = object.__new__(cls)
        obj._value_ = ltr
        return obj
    
    def resolve(self, other: OppHand) -> int:
        
        match self:
            case Result.LOSE:
                hand = next(filter(lambda h: h.beat_by == other, YourHand))
            case Result.DRAW:
                hand = next(filter(lambda h: h.beat_by != other and h.beats != other, YourHand))
            case Result.WIN:
                hand = next(filter(lambda h: h.beats == other, YourHand))
        
        return hand.score(other)

@dataclass
class Round:
    mine: YourHand
    theirs: OppHand
    result: Result

def read_inputs(example=0) -> List[Round]:
    
    if (example):
        data = example_input
    else:
        with open('day2_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    rounds = []
    # parse logic
    for line in data:
        lhs, rhs = line.split(' ')
        rounds.append(Round(YourHand(rhs), OppHand(lhs), Result(rhs)))
    
    return rounds

def part1(rounds: List[Round]) -> int:
    
    total = 0
    for round in rounds:
        total += round.mine.score(round.theirs)
    
    return total

def part2(rounds: List[Round]) -> int:
    
    total = 0
    for round in rounds:
        total += round.result.resolve(round.theirs)
    
    return total

def main(args):
    
    rounds = read_inputs(args.example)
    score = part1(rounds)
    logging.info(f'Part 1: Score {score}')
    score = part2(rounds)
    logging.info(f'Part 2: Adjusted Score {score}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
