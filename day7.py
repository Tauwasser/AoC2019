#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from collections.abc import Iterable
from dataclasses import dataclass, field

from lib import setup

example_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


@dataclass
class Equation:
    result: int
    numbers: tuple[int]


@dataclass
class Puzzle:
    equations: list[Equation] = field(default_factory=list)


def read_inputs(example=0) -> Puzzle:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day7_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    
    # parse logic
    puzzle = Puzzle()
    
    for line in data:
        result, numbers = line.split(':')
        puzzle.equations.append(Equation(int(result.strip()), tuple(int(n.strip()) for n in numbers.split(' ') if n)))
    
    return puzzle

OPERATORS_PT1 = {
    '+': 0,
    '*': 1,
}
"""Map of Operators to neutral elements for Part 1"""

OPERATORS_PT2 = {
    '+': 0,
    '*': 1,
    '||': 0,
}
"""Map of Operators to neutral elements for Part 2"""

def apply_operator(operator: str, equation: Equation, result: int, term: int, operators: Iterable[str]) -> bool:
    """Apply Operator and check if Equation could be true"""
    
    # no more terms: check result
    if not equation.numbers[term:]:
        return equation.result == result
    
    match (operator):
        case '+':
            result += equation.numbers[term]
        case '*':
            result *= equation.numbers[term]
        case '||':
            result = int(str(result) + str(equation.numbers[term]))
    
    term += 1
    return any(apply_operator(op, equation, result, term, operators) for op in operators)

def part1_2(puzzle: Puzzle, operators: dict[str, int]) -> list[Equation]:
    """Calculate Equations possibly True"""
    
    result = []
    
    for equation in puzzle.equations:
        
        for operator, neutral_element in operators.items():
            if apply_operator(operator, equation, neutral_element, 0, operators):
                result.append(equation)
                break;
    
    return result

def main(args):
    
    puzzle = read_inputs(args.example)
    equations = part1_2(puzzle, OPERATORS_PT1)
    logging.info(f'Part 1: {sum(eq.result for eq in equations)} ({", ".join(str(eq.result) for eq in equations[:10])})')
    equations = part1_2(puzzle, OPERATORS_PT2)
    logging.info(f'Part 2: {sum(eq.result for eq in equations)} ({", ".join(str(eq.result) for eq in equations[:10])})')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
