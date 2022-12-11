#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass
from enum import StrEnum
from math import copysign
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

class Direction(StrEnum):
    RIGHT = ('R',  1,  0)
    LEFT  = ('L', -1,  0)
    UP    = ('U',  0,  1)
    DOWN  = ('D',  0, -1)
    
    def __new__(cls, ltr, dx, dy):
        obj = str.__new__(cls)
        obj._value_ = ltr
        obj._dx = dx
        obj._dy = dy
        return obj
    
    @property
    def dx(self) -> int:
        return self._dx
    
    @property
    def dy(self) -> int:
        return self._dy

@dataclass(frozen=True)
class Vector:
    dx: int
    dy: int
    
    def normalize(self) -> 'Vector':
        dx = int(copysign(min(abs(self.dx), 1), self.dx))
        dy = int(copysign(min(abs(self.dy), 1), self.dy))
        return Vector(dx, dy)

@dataclass
class Point:
    x: int
    y: int
    
    def distance(self, other: 'Point') -> Tuple[int, Vector]:
        # calculate manhattan distance
        distance = max(abs(self.x - other.x), abs(self.y - other.y))
        return (distance, Vector(other.x - self.x, other.y - self.y))

@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    w: int
    h: int

@dataclass(frozen=True)
class Command:
    dir:    Direction
    steps : int

def read_inputs(example=0) -> Tuple[Rect, List[Command]]:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day9_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    
    # parse logic
    top_right = Point(0, 0)
    btm_left = Point(0, 0)
    cur = Point(0, 0)
    commands = []
    
    for line in data:
        ltr, steps = line.split(' ', 1)
        steps = int(steps)
        
        command = Command(Direction(ltr), steps)
        commands.append(command)
        # replay command
        cur.x += (command.dir.dx) * command.steps
        cur.y += (command.dir.dy) * command.steps
        
        # track size of field
        top_right.x = max(cur.x, top_right.x)
        top_right.y = max(cur.y, top_right.y)
        btm_left.x = min(cur.x, btm_left.x)
        btm_left.y = min(cur.y, btm_left.y)
    
    field = Rect(btm_left.x, btm_left.y, top_right.x - btm_left.x +1 , top_right.y - btm_left.y + 1)
    return (field, commands)

def drawField(field: Rect, head: Optional[Point], tail: Optional[Point], visited: List[Point] = []):
    
    diagram = [['.' for _ in range(field.w)] for _ in range(field.h)]
    
    # draw visited
    for point in visited:
        diagram[point.y-field.y][point.x-field.x] = '#'
    
    # draw origin
    diagram[0-field.y][0-field.x] = 's'
    
    # draw tail
    if (tail is not None):
        diagram[tail.y-field.y][tail.x-field.x] = 'T'
    
    # draw head
    if (head is not None):
        diagram[head.y-field.y][head.x-field.x] = 'H'
    
    diagram_str = '\n'.join(''.join(diagram[h]) for h in range(field.h -1, -1, -1))
    logging.info(diagram_str)

def part1(field: Rect, commands: List[Command]) -> int:
    
    head = Point(0, 0)
    tail = Point(0, 0)
    visited = set()
    
    #logging.info(f'== Initial State ==')
    #drawField(field, head, tail)
    
    for command in commands:
        
        #logging.info(f'== {command.dir._value_} {command.steps} ==')
        
        for _ in range(command.steps):
            head.x += command.dir.dx
            head.y += command.dir.dy
            
            d, v = tail.distance(head)
            if (d >= 2):
                v = v.normalize()
                tail.x += v.dx
                tail.y += v.dy
            
            visited.add((tail.x, tail.y))
            #drawField(field, head, tail)
    
    drawField(field, None, None, visited=[Point(x, y) for x, y in visited])
    
    return len(visited)

def part2():
    pass

def main(args):
    
    field, commands = read_inputs(args.example)
    num_points = part1(field, commands)
    logging.info(f'Part 1: There were {num_points} unique points visited by Tail')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
