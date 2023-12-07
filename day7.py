#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import enum
import sys
import functools
import logging

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

Card = enum.IntEnum('Card', '2 3 4 5 6 7 8 9 T J Q K A')

@classmethod
def card_from_string(cls, value):
    obj = cls.__members__.get(value, None)
    if (obj is None):
        raise ValueError(f"'{value}' is not a valid {cls.__name__}")
    return obj

Card.from_string = card_from_string

HandType = enum.IntEnum('HandType', 'HIGH PAIR_1 PAIR_2 KIND_3 FULL_HOUSE KIND_4 KIND_5')

@dataclass(eq=True, frozen=True)
class Hand:
    cards: tuple[Card]
    bid:   int
    
    @functools.cached_property
    def type(self):
        
        card_counts = defaultdict(lambda: 0)
        
        for card in self.cards:
            card_counts[card] += 1
        
        match (tuple(sorted(card_counts.values(), reverse=True))):
            case (5,):
                return HandType.KIND_5
            case (4, 1):
                return HandType.KIND_4
            case (3, 2):
                return HandType.FULL_HOUSE
            case (3, 1, 1):
                return HandType.KIND_3
            case (2, 2, 1):
                return HandType.PAIR_2
            case (2, 1, 1, 1):
                return HandType.PAIR_1
            case _:
                return HandType.HIGH
    
    def __repr__(self):
        """Repr w/ better readability and include type"""
        return f'Hand(cards={"".join(c._name_ for c in self.cards)}, type={self.type._name_}, bid={self.bid})'
    
    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        # compare types
        if (self.type != other.type):
            return False
        
        # same type: all cards must be same too in same order
        return all(lhs == rhs for lhs, rhs in zip(self.cards, other.cards))
    
    def __ne__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        # compare types
        if (self.type != other.type):
            return True
        
        # same type: at least one card must differ
        return any(lhs != rhs for lhs, rhs in zip(self.cards, other.cards))
    
    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        # compare types
        if (self.type > other.type):
            return False
        elif (self.type < other.type):
            return True
        else:
            # compare cards
            for lhs, rhs in zip(self.cards, other.cards):
                if (lhs < rhs):
                    return True
                if (lhs == rhs):
                    continue
                break
        return False
    
    def __gt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        # compare types
        if (self.type < other.type):
            return False
        elif (self.type > other.type):
            return True
        else:
            # compare cards
            for lhs, rhs in zip(self.cards, other.cards):
                if (lhs > rhs):
                    return True
                if (lhs == rhs):
                    continue
                break
        return False
    
    def __le__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        # compare types
        if (self.type > other.type):
            return False
        elif (self.type < other.type):
            return True
        
        # same type: all cards must be same too in same order
        return all(lhs == rhs for lhs, rhs in zip(self.cards, other.cards))
    
    def __ge__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        # compare types
        if (self.type < other.type):
            return False
        elif (self.type > other.type):
            return True
        
        # same type: all cards must be same too in same order
        return all(lhs == rhs for lhs, rhs in zip(self.cards, other.cards))

def read_inputs(example=0):
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day7_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    hands : list[Hand] = []
    
    for line in data:
        cards, bid = line.split(' ')
        
        hands.append(Hand(tuple(Card.from_string(c) for c in cards), int(bid)))
    
    return hands

def part1(hands: list[Hand]) -> list[int]:
    """Compute ranks of Hands"""
    ranks = sorted(hands)
    return [ranks.index(hand) + 1 for hand in hands]

def part2():
    pass

def main(args):
    
    hands = read_inputs(args.example)
    ranks = part1(hands)
    logging.info(f'Part 1: {sum(map(lambda r, h: r * h.bid, ranks, hands))} ({", ".join(str(rh) for rh in zip(ranks, hands))})')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
