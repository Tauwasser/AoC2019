#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import logging

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

@dataclass(eq=True, frozen=True)
class Number:
    x: int
    y: int
    length: int
    value: int

@dataclass(eq=True, frozen=True)
class Symbol:
    x: int
    y: int
    symbol: str

@dataclass
class Schematic:
    width: int
    height: int
    numbers: list[Number] = field(default_factory=list, repr=False)
    symbols: list[Symbol] = field(default_factory=list, repr=False)

@dataclass(eq=True, frozen=True)
class Gear:
    x: int
    y: int
    lhs: Number
    rhs: Number

def read_inputs(example=0) -> Schematic:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day3_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    pattern = re.compile(r'(?P<number>\d+)|(?P<symbol>[^.\d\n])')
    line_length = data.find('\n') + 1
    num_lines = data.count('\n')
    
    schematic = Schematic(line_length - 1, num_lines)
    
    for match in pattern.finditer(data):
        
        # retrieve start, end position
        start, end = match.span()
        
        # find common attributes
        x = start % line_length
        y = start // line_length
        l = end - start
        value = match.group('number') or match.group('symbol')
        
        if (match.group('number') is not None):
            schematic.numbers.append(Number(x, y, l, int(value)))
        elif (match.group('symbol') is not None):
            schematic.symbols.append(Symbol(x, y, value))
    
    return schematic

def part1(schematic: Schematic) -> List[Number]:
    
    result : list[Number] = []
    X = schematic.width - 1
    Y = schematic.height - 1
    
    symbol_pos = set(map(lambda symbol: (symbol.x, symbol.y), schematic.symbols))
    
    for number in schematic.numbers:
        
        # all possible positions
        x = number.x
        y = number.y
        l = number.length
        # previous line
        adjacent_pos = [(xx, y - 1) for xx in range(x - 1, x + l + 1) if y - 1 >= 0 and 0 <= xx <= X]
        # next line
        adjacent_pos += [(xx, y + 1) for xx in range(x - 1, x + l + 1) if y + 1 <= Y and 0 <= xx <= X]
        # same line
        adjacent_pos += [(x + xx, y) for xx in (-1, l) if 0 <= x + xx <= X]
        
        # check if any symbol at adjacent position
        if any(pos in symbol_pos for pos in adjacent_pos):
            result.append(number)
    
    return result

def part2(schematic: Schematic) -> list[Gear]:
    
    result : list[Gear] = []
    X = schematic.width - 1
    Y = schematic.height - 1
    
    number_map = {(xx, number.y): number for number in schematic.numbers for xx in range(number.x, number.x + number.length)}
    possible_gears = list(filter(lambda symbol: symbol.symbol == '*', schematic.symbols))
    
    for symbol in possible_gears:
        
        # all possible positions
        x = symbol.x
        y = symbol.y
        
        # previous line
        adjacent_pos = [(xx, y - 1) for xx in range(x - 1, x + 1 + 1) if y - 1 >= 0 and 0 <= xx <= X]
        # next line
        adjacent_pos += [(xx, y + 1) for xx in range(x - 1, x + 1 + 1) if y + 1 <= Y and 0 <= xx <= X]
        # same line
        adjacent_pos += [(x + xx, y) for xx in (-1, +1) if 0 <= x + xx <= X]
        
        # check if any two numbers are adjacent
        adjacent_numbers = set(filter(None, map(number_map.get, adjacent_pos)))
        
        if (len(adjacent_numbers) != 2):
            continue
        
        lhs = adjacent_numbers.pop()
        rhs = adjacent_numbers.pop()
        result.append(Gear(x, y, lhs, rhs))
    
    return result

def main(args):
    
    schematic = read_inputs(args.example)
    part_numbers = part1(schematic)
    logging.info(f'Part 1: {sum(num.value for num in part_numbers)} ({", ".join(str(num.value) for num in part_numbers)})')
    gears = part2(schematic)
    logging.info(f'Part 2: {sum(gear.lhs.value * gear.rhs.value for gear in gears)} ({", ".join(f"({gear.x}, {gear.y})" for gear in gears)})')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
