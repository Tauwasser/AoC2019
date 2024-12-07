#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import re

from dataclasses import dataclass, field

from lib import setup

example1_input = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

example2_input = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

@dataclass
class Mul:
    x: int
    y: int
    
    def result(self) -> int:
        return self.x * self.y
    
    def __str__(self):
        return f'{self.x}*{self.y}'


@dataclass
class Range:
    start: int
    stop: int
    
    def __contains__(self, item: int):
        return (self.start <= item < self.stop)


def read_inputs(example=0) -> str:
    
    match (example):
        case 1 if (example):
            data = example1_input
        case 2 if (example):
            data = example2_input
        case _:
            with open('day3_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    return data

def part1(memory: str) -> list[Mul]:
    """Scan Memory for mul(<num>,<num>) commands
    
    Returns
        List of parsed Mul commands.
    """
    # match using regex
    mul_pattern = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
    
    return list(Mul(int(m[0]), int(m[1])) for m in mul_pattern.findall(memory))

def part2(memory: str) -> list[Mul]:
    """Scan Memory for mul(<num>,<num>) commands respecting do(), don't() commands.
    
    Returns
        List of parsed enabled Mul commands.
    """
    # match using regex
    enable_pattern = re.compile(r'(do(?:n\'t)?)\(\)')
    mul_pattern = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
    
    do_matches = tuple((m.end(), m.group(1)) for m in enable_pattern.finditer(memory))
    mul_matches = tuple((m.start(), Mul(int(m.group(1)), int(m.group(2)))) for m in mul_pattern.finditer(memory))
    
    # start whole range enabled
    MEMORY_LEN = len(memory)
    enabled_ranges = [
        Range(0, MEMORY_LEN)
    ]
    cur_range = enabled_ranges[-1]
    
    # apply do/don't commands
    for ix, kind in do_matches:
        
        match (kind):
            case 'do' if cur_range is None:
                enabled_ranges.append(Range(ix, MEMORY_LEN))
                cur_range = enabled_ranges[-1]
            case 'don\'t' if cur_range is not None:
                cur_range.stop = ix
                cur_range = None
            case _:
                # range already enabled resp. disabled
                pass
    
    # return filtered mul commands
    return list(filter(None, map(lambda mul_match: mul_match[1] if any(mul_match[0] in r for r in enabled_ranges) else None, mul_matches)))

def main(args):
    
    memory = read_inputs(args.example)
    mul_cmds = part1(memory)
    logging.info(f'Part 1: {sum(mul.result() for mul in mul_cmds)} ({"  ".join(str(mul) for mul in mul_cmds[:10])})')
    mul_cmds = part2(memory)
    logging.info(f'Part 2: {sum(mul.result() for mul in mul_cmds)} ({"  ".join(str(mul) for mul in mul_cmds[:10])})')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
