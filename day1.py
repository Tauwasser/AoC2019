#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import logging

from typing import Dict, List, Optional, Tuple

from lib import setup

example1_input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

example2_input = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

def read_inputs(example=0):
    
    match (example):
        case 1 if (example):
            data = example1_input
        case 2 if (example):
            data = example2_input
        case _:
            with open('day1_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    
    # parse logic
    return data

def part1(lines: List[str]) -> List[int]:
    
    values = []
    pattern = re.compile(r'^[^\d]*(\d)(?:.*(\d))?[^\d]*$')
    
    for line in lines:
        m = pattern.match(line)
        if (m is None):
            raise RuntimeError(f'Line {line} does not match regular expression!')
        num0, num1 = m.groups()
        num = int(num0) * 10 + int(num1 or num0)
        values.append(num)
    
    return values

def part2(lines: List[str]) -> List[int]:
    
    values = []
    
    pattern = {
        '1': 1, 'one':   1,
        '2': 2, 'two':   2,
        '3': 3, 'three': 3,
        '4': 4, 'four':  4,
        '5': 5, 'five':  5,
        '6': 6, 'six':   6,
        '7': 7, 'seven': 7,
        '8': 8, 'eight': 8,
        '9': 9, 'nine':  9,
    }
    
    for line in lines:
        num0 = next(iter(sorted(filter(lambda vi: vi[1] >= 0, ((value, line.find(key)) for key, value in pattern.items())), key=lambda vi: vi[1])), None)
        num1 = next(iter(sorted(filter(lambda vi: vi[1] >= 0, ((value, line.rfind(key)) for key, value in pattern.items())), key=lambda vi: -vi[1])), None)
        if (num0 is None):
            raise RuntimeError(f'No number found in line {line}!')
        num = num0[0] * 10 + (num1 or num0)[0]
        values.append(num)
    
    return values

def main(args):
    
    lines = read_inputs(args.example)
    #values = part1(lines)
    #logging.info(f'Part 1: {sum(values)} ({", ".join((str(v) for v in values))})')
    values = part2(lines)
    logging.info(f'Part 2: {sum(values)} ({", ".join((str(v) for v in values))})')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
