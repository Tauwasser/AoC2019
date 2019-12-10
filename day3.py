#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

class Vec:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)
    
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
    
    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)
    
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
    
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)
    
    def __lt__(self, other):
        return (self.x < other.x or self.y < other.y)
    
    def __gt__(self, other):
        return (self.x > other.x or self.y > other.y)
    
    def norm(self):
        return abs(self.x) + abs(self.y)
    
    def __str__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y})'

class LineSegment:
    
    def __init__(self, beg, end=None, delta=None):
        
        self.begin = beg
        self.end = end or self.begin + delta
        self.dir = 'h' if (self.begin.x == self.end.x) else 'v'
    
    def intersect(self, other):
        
        sBegin = min(self.begin, self.end)
        sEnd = max(self.begin, self.end)
        oBegin = min(other.begin, other.end)
        oEnd = max(other.begin, other.end)
        
        # lines are perpendicular
        # assume lines not parallel, overlap in same direction
        if   (self.dir != other.dir):
            
            print(f'Checking {self} <-> {other}')
            
            if (oBegin.x <= sBegin.x <= oEnd.x and sBegin.y <= oBegin.y <= sEnd.y):
                # vertical case
                return Vec(sBegin.x, oBegin.y)
            elif (oBegin.y <= sBegin.y <= oEnd.y and sBegin.x <= oBegin.x <= oEnd.x):
                # horizontal case
                return Vec(oBegin.x, sBegin.y)
        
        return None
    
    def __str__(self):
        return f'{self.__class__.__name__}(begin={self.begin!s}, end={self.end!s}, command={vector2command(self.end-self.begin)})'

def command2vector(cmd):
    
    if (len(cmd) < 2):
        raise RuntimeError(f'Illegal command length for \'{cmd}\'...')
    
    delta = int(cmd[1:])
    
    if (cmd[0] == 'U'):
        return Vec(0, delta)
    elif (cmd[0] == 'D'):
        return Vec(0, -delta)
    elif (cmd[0] == 'L'):
        return Vec(-delta, 0)
    elif (cmd[0] == 'R'):
        return Vec(delta, 0)
    else:
        raise RuntimeError(f'Unknown command \'{cmd[0]}\'.')

def vector2command(vec):
    
    if (vec.x < 0):
        return f'L{-vec.x}'
    elif (vec.y < 0):
        return f'D{-vec.y}'
    elif (vec.x > 0):
        return f'R{vec.x}'
    elif (vec.y > 0):
        return f'U{vec.y}'
    else:
        return 'R0'

def main():

    with open('day3_input', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    #lines = ['', '']
    #lines[0] = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'
    #lines[1] = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
        
    wire_commands = [[command2vector(x) for x in line.split(',')] for line in lines]
    num_wires = len(wire_commands)

    print(f'Num Wires: {num_wires}')

    wires = [{'position': Vec(0, 0), 'extents': LineSegment(Vec(0,0), end=Vec(0,0))} for _ in range(0, num_wires)]

    def calcSegment(ix, vec):
        
        pos = wires[ix]['position']
        extents = wires[ix]['extents']
        
        result = LineSegment(pos, delta=vec)
        wires[ix]['position'] = result.end
        pos = wires[ix]['position']
        
        # update extents
        if (pos.x < extents.begin.x):
            extents.begin.x = pos.x
        if (pos.x > extents.end.x):
            extents.end.x = pos.x
        if (pos.y < extents.begin.y):
            extents.begin.y = pos.y
        if (pos.y > extents.end.y):
            extents.end.y = pos.y
        
        return result

    wire_segments = [[calcSegment(ix, vec) for vec in commands] for ix, commands in enumerate(wire_commands)]
    
    for ix, wire in enumerate(wires):
        
        print(f'Wire {ix} Position {wire["position"]} Extents {wire["extents"]}')
        
        for segment in wire_segments[ix]:
            
            print(f'{segment}')
    
    intersections = []
    
    # stupidly intersect everything with everything
    for lhs in range(0, num_wires):
        
        for rhs in range(lhs + 1, num_wires):
            
            for segmentLhs in wire_segments[lhs]:
                
                for segmentRhs in wire_segments[rhs]:
                    
                    intersection = segmentLhs.intersect(segmentRhs)
                    
                    if (intersection is not None and not (intersection.x == 0 and intersection.y == 0)):
                        print(f'{segmentLhs} intersects {segmentRhs} at {intersection}')
                        intersections.append(intersection)
    
    minInterset = min(intersections, key=lambda x: x.norm())
    
    print(f'Closest intersection: {minInterset} ({minInterset.norm()})')

if __name__=='__main__':
    sys.exit(main())