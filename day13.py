#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass, field
from enum import Enum
from itertools import zip_longest
from typing import Dict, List, Optional, Tuple, Union

from lib import setup

example_input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

Contents = Union[int, List['Contents']]

class Ternary(Enum):
    FALSE = 0
    MAYBE = 1
    TRUE  = 2
    
    @staticmethod
    def fromBool(b: bool) -> 'Ternary':
        return Ternary.TRUE if (b) else Ternary.FALSE

@dataclass
class Packet:
    contents: Contents = field(default_factory=list)

@dataclass
class Pair:
    index: int
    lhs: Packet
    rhs: Packet

def read_inputs(example=0) -> List[Pair]:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day13_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    pairs : List[Pair] = []
    
    def _parse_packet(line: str):
        
        result = Packet()
        stack = [result.contents]
        cur = result.contents
        
        if (line[0] != '['):
            raise RuntimeError(f'Line {line} does not begin with opening bracket!')
        
        i = 1
        l = len(line)
        while i < l:
            
            if (line[i] == '['):
                new = []
                cur.append(new)
                stack.append(cur)
                cur = new
                i += 1
            elif (line[i] == ']'):
                cur = stack.pop(-1)
                i += 1
            elif (line[i] == ','):
                i += 1
            else:
                jb = line.find(']', i)
                jc = line.find(',', i)
                j = min(jb, jc) if (jb > -1 and jc > -1) else (jb if (jb > -1) else jc)
                cur.append(int(line[i:j]))
                i = j
        
        if (line.replace(',', ', ') != str(result.contents)):
            raise RuntimeError(f'Line: {line} Result: {str(result.contents)}')
        
        return result
    
    # parse logic
    for ix, (line0, line1, _) in enumerate(zip_longest(*[iter(data)] * 3, fillvalue=''), 1):
        
        lhs = _parse_packet(line0)
        rhs = _parse_packet(line1)
        pairs.append(Pair(ix, lhs, rhs))
    
    return pairs

def _is_content_sorted(lhs: Contents, rhs: Contents) -> bool:
    
    if (type(lhs) is int and type(rhs) is int):
        # both int: decide by comparison
        return Ternary.MAYBE if (lhs == rhs) else Ternary.fromBool(lhs < rhs)
    elif (type(lhs) is int):
        # lhs is list --> boost to list itself
        return _is_content_sorted([lhs], rhs)
    elif (type(rhs) is int):
        # rhs is list --> boost to list itself
        return _is_content_sorted(lhs, [rhs])
    else:
        for _lhs, _rhs in zip_longest(lhs, rhs, fillvalue=None):
            if (_lhs is None):
                # lhs is shorter than rhs
                return Ternary.TRUE
            if (_rhs is None):
                # rhs is shorter than lhs
                return Ternary.FALSE
            # check next level
            if (Ternary.MAYBE == (result := _is_content_sorted(_lhs, _rhs))):
                continue
            return result
        # same length no inner decision
        return Ternary.MAYBE

def part1(pairs: List[Pair]) -> List[Pair]:
    
    right_order = list(filter(lambda p: Ternary.TRUE == _is_content_sorted(p.lhs.contents, p.rhs.contents), pairs))
    return right_order

def part2():
    pass

def main(args):
    
    pairs = read_inputs(args.example)
    sorted_pairs = part1(pairs)
    logging.info(f'Part 1: sorted pair indice sum {sum(p.index for p in sorted_pairs)} (pairs {", ".join(str(p.index) for p in sorted_pairs)})')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
