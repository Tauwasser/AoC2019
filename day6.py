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

def would_enter_loop(puzzle: Puzzle, guard: Guard, path: dict[tuple[int, int], tuple[int, int]]) -> bool:
    """Check if Guard enters loop when turning at current position
    
    Returns:
        True if Guard enters loop, else False.
    """
    # begin with turn
    guard = Guard(guard.x, guard.y, guard.dx, guard.dy)
    guard.turn()
    
    result = False
    
    # check only next 256 steps
    for _ in range(256):
        if not(0 <= guard.x < puzzle.width):
            break
        if not(0 <= guard.y < puzzle.height):
            break
        
        # check if we visited this location with same direction once before
        # because this means we enter a loop
        heading = path.get((guard.x, guard.y), (0, 0))
        if (heading == (guard.dx, guard.dy)):
            result = True
            break
        
        # turn if obstruction present
        pos = (guard.x + guard.dx, guard.y + guard.dy)
        if any(pos[0] == obj.x and pos[1] == obj.y for obj in puzzle.obstructions):
            guard.turn()
        else:
            # take a step
            guard.x = pos[0]
            guard.y = pos[1]
    
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
        if any(pos[0] == obj.x and pos[1] == obj.y for obj in puzzle.obstructions):
            guard.turn()
        else:
            # check if obstruction would cause loop
            obstruction = Obstruction(pos[0], pos[1])
            if would_enter_loop(puzzle, guard, path):
                result.append(obstruction)
            # take a step
            guard.x = pos[0]
            guard.y = pos[1]
    
    with open('day6_debug', 'w', encoding='utf-8') as f:
        for y in range(puzzle.height):
            for x in range(puzzle.width):
                pos = (x, y)
                obstruction = next(filter(lambda obj: obj.x == pos[0] and obj.y == pos[1], puzzle.obstructions), None)
                #new_obstruction = next(filter(lambda obj: obj.x == pos[0] and obj.y == pos[1], result), None)
                new_obstruction = None
                if (obstruction is not None):
                    f.write('#')
                elif (new_obstruction is not None):
                    f.write('O')
                elif(puzzle.guard.x == pos[0] and puzzle.guard.y == pos[1]):
                    f.write('^')
                else:
                    match path.get(pos, (0, 0)):
                        case (0, 0):
                            f.write('.')
                        case (1, 0):
                            f.write('-')
                        case (0, 1):
                            f.write('|')
                        case (-1, 0):
                            f.write('-')
                        case (0, -1):
                            f.write('|')
                    
            f.write('\n')
    
    return result

def main(args):
    
    puzzle = read_inputs(args.example)
    steps = part1(puzzle)
    logging.info(f'Part 1: {len(steps)}')
    obstructions = part2(puzzle)
    # 1843 too low
    # 2088 too high
    logging.info(f'Part 2: {len(obstructions)}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
