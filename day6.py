#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import re

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

def would_enter_loop(puzzle: Puzzle, guard: Guard, path: dict[tuple[int, int], tuple[int, int]]) -> bool:
    """Check if Guard enters loop when turning at current position
    
    Returns:
        True if Guard enters loop, else False.
    """
    # begin with turn
    guard = Guard(guard.x, guard.y, guard.dx, guard.dy)
    guard.turn()
    
    result = False
    
    for _ in range(8192):
        if not(0 <= guard.x < puzzle.width):
            break
        if not(0 <= guard.y < puzzle.height):
            break
        
        # check if we arrived in existing path
        direction = path.get((guard.x, guard.y), (0, 0))
        if (direction[0] == guard.dx and direction[1] == guard.dy):
            result = True
            break
        
        pos = (guard.x + guard.dx, guard.y + guard.dy)
        
        obstruction = puzzle.obstructions.get(pos, None)
        if (obstruction is not None):
            # turn if obstruction present
            guard.turn()
        else:
            # take a step
            guard.x = pos[0]
            guard.y = pos[1]
    else:
        # assume if it took that many steps, that we entered
        # a loop that we just haven't stepped into before
        result = True
    
    return result

def part2(puzzle: Puzzle) -> list[Obstruction]:
    """Calculate possible locations for new Obstructions
    
    Returns:
        List of possible new obstructions.
    """
    path: dict[tuple[int, int], tuple[int, int]] = {}
    result: list[Obstruction] = []
    
    # copy puzzle guard
    guard = Guard(puzzle.guard.x, puzzle.guard.y, puzzle.guard.dx, puzzle.guard.dy)
    
    while True:
        # abort if guard stepped outside of map
        if not(0 <= guard.x < puzzle.width):
            break
        if not(0 <= guard.y < puzzle.height):
            break
        
        # include current guard position
        path[(guard.x, guard.y)] = (guard.dx, guard.dy)
        
        # turn if obstruction present
        pos = (guard.x + guard.dx, guard.y + guard.dy)
        obstruction = puzzle.obstructions.get(pos, None)
        if (obstruction is not None):
            guard.turn()
        else:
            # cannot place obstacle where we already went
            visited = path.get(pos, None)
            if (visited is None and not (pos[0] == puzzle.guard.x and pos[1] == puzzle.guard.y)):
                # check if obstruction would cause loop
                obstruction = Obstruction(pos[0], pos[1])
                puzzle.obstructions[pos] = obstruction
                if would_enter_loop(puzzle, guard, path):
                    result.append(obstruction)
                # remove new obstruction
                del puzzle.obstructions[pos]
            # take a step
            guard.x = pos[0]
            guard.y = pos[1]
    
    return result

def main(args):
    
    puzzle = read_inputs(args.example)
    steps = part1(puzzle)
    logging.info(f'Part 1: {len(steps)}')
    obstructions = part2(puzzle)
    logging.info(f'Part 2: {len(obstructions)}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
