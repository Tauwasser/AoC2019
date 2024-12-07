#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass, field

from lib import setup

example_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


@dataclass
class Object:
    x: int
    y: int


@dataclass
class Obstruction(Object):
    pass


@dataclass
class Guard(Object):
    dx: int
    dy: int
    
    def turn(self):
        """Turn 90° to the right"""
        match (self.dx, self.dy):
            case ( 0, -1):
                self.dx = 1
                self.dy = 0
            case ( 1,  0):
                self.dx = 0
                self.dy = 1
            case ( 0,  1):
                self.dx = -1
                self.dy = 0
            case (-1,  0):
                self.dx = 0
                self.dy = -1


@dataclass
class Puzzle:
    width: int
    height: int
    guard: Guard
    obstructions: dict[tuple[int, int], Obstruction] = field(default_factory=dict)


def read_inputs(example=0) -> Puzzle:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day6_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    
    # parse logic
    puzzle = Puzzle(height=len(data), width=len(data[0]), guard=Guard(x=0, y=0, dx=0, dy=-1))
    
    for y in range(len(data)):
        for x in range(len(data[y])):
            match (data[y][x]):
                case '^':
                    # parse guard
                    logging.info(f'Guard initially at {x}/{y}.')
                    puzzle.guard.x = x
                    puzzle.guard.y = y
                case '#':
                    # parse obstruction
                    puzzle.obstructions[(x, y)] = Obstruction(x, y)
    return puzzle

def part1(puzzle: Puzzle) -> set[tuple[int, int]]:
    """Calculate distinct positions visited by Guard
    
    Returns:
        Set of district positions visited by guard (x/y tuples).
    """
    result: set[tuple[int, int]] = set()
    
    # copy puzzle guard
    guard = Guard(puzzle.guard.x, puzzle.guard.y, puzzle.guard.dx, puzzle.guard.dy)
    
    while True:
        # abort if guard stepped outside of map
        if not(0 <= guard.x < puzzle.width):
            break
        if not(0 <= guard.y < puzzle.height):
            break
        # include current guard position
        result.add((guard.x, guard.y))
        # take a step if no obstruction
        pos = (guard.x + guard.dx, guard.y + guard.dy)
        obstruction = puzzle.obstructions.get(pos, None)
        if (obstruction is not None):
            guard.turn()
        else:
            guard.x = pos[0]
            guard.y = pos[1]
    
    return result

def part2():
    pass

def main(args):
    
    puzzle = read_inputs(args.example)
    steps = part1(puzzle)
    logging.info(f'Part 1: {len(steps)}')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
