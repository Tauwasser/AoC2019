#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import math

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

from lib import setup

example_input = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

@dataclass(frozen=True,order=True)
class Point:
    x: Union[int, float]
    y: Union[int, float]
    
    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)
    
    def _multiply(self, other: Union[int, float]) -> 'Point':
        if (isinstance(other, (int, float))):
            return Point(self.x * other, self.y * other)
        return NotImplemented
    
    def _divide(self, other: Union[int, float]) -> 'Point':
        if (isinstance(other, (int, float))):
            return Point(self.x / other, self.y / other)
        return NotImplemented
    
    def _intdivide(self, other: Union[int, float]) -> 'Point':
        if (isinstance(other, (int, float))):
            return Point(self.x // other, self.y // other)
        return NotImplemented
    
    def __floordiv__(self, other: Union[int, float]) -> 'Point':
        return self._intdivide(other)
    
    def __rfloordiv__(self, other: Union[int, float]) -> 'Point':
        return self._intdivide(other)
    
    def __truediv__(self, other: Union[int, float]) -> 'Point':
        return self._divide(other)
    
    def __rtruediv__(self, other: Union[int, float]) -> 'Point':
        return self._divide(other)
    
    def __mul__(self, other: Union[int, float]) -> 'Point':
        return self._multiply(other)
    
    def __rmul__(self, other: Union[int, float]) -> 'Point':
        return self._multiply(other)
    
    def __neg__(self):
        return Point(-self.x, -self.y)
    
    def __pos__(self):
        return self

# determinant of a 2x2 matrix
def det(col0: Point, col1: Point):
    return (col0.x * col1.y) - (col0.y * col1.x)

@dataclass
class Line:
    start: Point
    end: Point
    
    def __init__(self, start: Point, end: Point):
        #  order left to right
        self.start = min(start, end)
        self.end = max(start, end)
        
        # order bottom to top
        if (self.vertical and self.end.y < self.start.y):
            self.start, self.end = self.end, self.start
    
    def intersect(self, other: 'Line') -> Optional[Point]:
        
        # bring two lines into Bezier form
        # line AB --> A + t * (B - A)
        # line CD --> C + u * (D - C)
        vec_lhs = self.end - self.start
        vec_rhs = other.end - other.start
        
        # transform into linear system
        # A + t * (B - A) == C + u * (D - C)
        # => t * (B - A) - u * (D - C) == C - A
        # => [(B - A) -(D - C)] * [t u]T == C - A
        # use Cramer's rule to solve:
        # t := det([(C - A) -(D - C)]) / det([(B - A) -(D - C)])
        # u := det([(B - A)  (C - A)]) / det([(B - A) -(D - C)])
        
        divisor = det(vec_lhs, -vec_rhs)
        
        # lines are parallel
        if (0 == divisor):
            return None
        
        t = det(other.start - self.start, -vec_rhs) / divisor
        u = det(vec_lhs, other.start - self.start) / divisor
        
        if not (0.0 <= t <= 1.0):
            return None
        if not (0.0 <= u <= 1.0):
            return None
        
        # force integer computation of multiplication to not lose precision
        # return self.start + t * vec_lhs w/ t := det([(C - A) -(D - C)]) / det([(B - A) -(D - C)])
        return self.start + det(other.start - self.start, -vec_rhs) * vec_lhs / divisor
    
    def overlap(self, other: 'Line', diagonals=False) -> List[Point]:
        
        results = []
        
        if (self.horizontal and other.horizontal):
            # zero or more points
            if (self.start.y == other.start.y):
                for x in range(max(self.start.x, other.start.x), min(self.end.x, other.end.x) + 1):
                    results.append(Point(x, self.start.y))
        elif (self.vertical and other.vertical):
            # zero or more points
            if (self.start.x == other.start.x):
                for y in range(max(self.start.y, other.start.y), min(self.end.y, other.end.y) + 1):
                    results.append(Point(self.start.x, y))
        
        if (diagonals and (self.diagonal and other.diagonal)):
            # normalize vectors (should be either 1/1 or 1/-1)
            vec_lhs = self.end - self.start
            vec_rhs = other.end - other.start
            vec_lhs = vec_lhs / abs(vec_lhs.y)
            vec_rhs = vec_rhs / abs(vec_rhs.y)
            if (vec_lhs == vec_rhs):
                # make sure lines have the same y intercept
                # and actually overlap (instead of one ending before the other starts)
                yint_lhs = self.start - self.start.x * vec_lhs
                yint_rhs = other.start - other.start.x * vec_rhs
                if (yint_lhs == yint_rhs and ((self.start <= other.start <= self.end) or (other.start <= self.start <= other.end))):
                    # lines are the same
                    start = max(self.start, other.start)
                    end = min(self.end, other.end)
                    pt = start
                    while (pt <= end):
                        results.append(pt)
                        pt = pt + vec_lhs
        
        if (diagonals or (self.horizontal and other.vertical) or (self.vertical and other.horizontal)):
            # exactly one or zero points
            pt = self.intersect(other)
            # make sure points are on the grid
            if (pt is not None and (pt // 1) == pt):
                results.append(pt)
        
        return results
    
    @property
    def horizontal(self):
        return self.start.y == self.end.y
    
    @property
    def vertical(self):
        return self.start.x == self.end.x
    
    @property
    def diagonal(self):
        # lines are guaranteed to be either horizontals, verticals or (45°) diagonals
        return not self.horizontal and not self.vertical

def read_inputs(example=False) -> List[Line]:
    
    if (example):
        data = example_input
    else:
        with open('day5_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    lines = []
    
    for line in data:
        start, end = line.split('->')
        start_x, start_y = [int(v) for v in start.strip().split(',')]
        end_x, end_y = [int(v) for v in end.strip().split(',')]
        lines.append(Line(Point(start_x, start_y), Point(end_x, end_y)))
    
    return lines

def part1(lines: List[Line], diagonals=False):
    
    overlaps : Dict[Point, int] = defaultdict(lambda: 0)
    
    # find line intersecs
    for ix, lhs in enumerate(lines):
        for rhs in lines[ix+1:]:
            pts = lhs.overlap(rhs, diagonals=diagonals)
            for pt in pts:
                overlaps[pt] += 1
    
    return overlaps

def part2(lines: List[Line]):
    return part1(lines, diagonals=True)

def main(args):
    
    lines = read_inputs(args.example)
    overlaps = part1(lines)
    logging.info(f'Part 1: Found {len(overlaps)} overlaps total.')
    overlaps = part2(lines)
    logging.info(f'Part 2: Found {len(overlaps)} overlaps total (including diagonals)')
    
    with open('day5_debug', 'w', encoding='utf-8') as f:
        for overlap in sorted(overlaps):
            f.write(f'{overlap.x},{overlap.y}\n')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
