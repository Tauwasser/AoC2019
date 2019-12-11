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
        self.dir = 'v' if (self.begin.x == self.end.x) else 'h'
        self.start = min(beg, self.end)
        self.finish = max(beg, self.end)
    
    def intersect(self, other):
        
        # lines are perpendicular
        # assume lines not parallel, overlap in same direction
        if   (self.dir != other.dir):
            
            #print(f'Checking {self} <-> {other}')
            
            if (other.start.x <= self.start.x <= other.finish.x and self.start.y <= other.start.y <= self.finish.y):
                # vertical case
                return Vec(self.start.x, other.start.y)
            elif (other.start.y <= self.start.y <= other.finish.y and self.start.x <= other.start.x <= self.finish.x):
                # horizontal case
                return Vec(other.start.x, self.start.y)
        
        return None
    
    def __str__(self):
        return f'{self.__class__.__name__}(begin={self.begin!s}, end={self.end!s}, command={vector2command(self.end-self.begin)})'

class BoundingBox:
    
    def __init__(self, begin=None, end=None):
        self.begin = begin or Vec(0,0)
        self.end = end or Vec(0,0)
    
    def update(self, vec):
        
        if (vec.x < self.begin.x):
            self.begin.x = vec.x
        if (vec.x > self.end.x):
            self.end.x = vec.x
        if (vec.y < self.begin.y):
            self.begin.y = vec.y
        if (vec.y > self.end.y):
            self.end.y = vec.y
        
    def union(self, bb):
        
        xBeg = min(bb.begin.x, self.begin.x)
        yBeg = min(bb.begin.y, self.begin.y)
        xEnd = max(bb.end.x, self.end.x)
        yEnd = max(bb.end.y, self.end.y)
        
        return BoundingBox(begin=Vec(xBeg, yBeg), end=Vec(xEnd, yEnd))
        
    def __str__(self):
        return f'{self.__class__.__name__}(begin={self.begin}, end={self.end})'
        
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

def drawWires(wires, intersections, minIntersect, filename='day3_output.txt'):
    
    bb = BoundingBox()
    
    for wire in wires:
        bb = bb.union(wire['extents'])
    
    print(bb)
    
    xOffset = -bb.begin.x
    yOffset = bb.begin.y
    
    xSize = bb.end.x - bb.begin.x + 1
    ySize = bb.end.y - bb.begin.y + 1
    
    # add 1 field outline
    xOffset += 1
    yOffset -= 1
    xSize += 2
    ySize += 2
    
    field = [[['.'] for _ in range(0, xSize)] for _ in range(0, ySize)]
    
    def toX(x):
        return x + xOffset
    
    def toY(y):
        return ySize - y - 1 + yOffset
    
    # draw lines
    for wire in wires:
        for segment in wire['segments']:
            
            # yBegin/yEnd switched, because .y is cartesian, but yBegin/yEnd is line number
            xBegin = toX(segment.start.x)
            yBegin = toY(segment.finish.y)
            
            xEnd = toX(segment.finish.x)
            yEnd = toY(segment.start.y)
            
            line = '-' if segment.dir == 'h' else '|'
            
            # draw line
            for x in range(xBegin, xEnd + 1):
                for y in range(yBegin, yEnd + 1):
                    field[y][x] = line
            
            # draw begin
            field[yBegin][xBegin] = '+'
            
            # draw end
            field[yEnd][xEnd] = '+'
    
    # draw intersection points
    for intersection in intersections:
        
        x = toX(intersection.x)
        y = toY(intersection.y)
        field[y][x] = 'x'
    
    # draw closes intersection point
    if (minIntersect is not None):
        x = toX(minIntersect.x)
        y = toY(minIntersect.y)
        field[y][x] = 'X'
    
    # draw origin
    field[toY(0)][toX(0)] = 'O'
    
    with open(filename, 'w', encoding='utf-8') as f:
        for line in field:
            f.write(''.join(x[0] for x in line))
            f.write('\n')
    
def main():

    with open('day3_input', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Example 1
    #lines = ['', '']
    #lines[0] = 'R8,U5,L5,D3'
    #lines[1] = 'U7,R6,D4,L4'
    
    # Example 2
    #lines = ['', '']
    #lines[0] = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
    #lines[1] = 'U62,R66,U55,R34,D71,R55,D58,R83'
    
    # Example 3
    #lines = ['', '']
    #lines[0] = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'
    #lines[1] = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
    
    wire_commands = [[command2vector(x) for x in line.split(',')] for line in lines]
    num_wires = len(wire_commands)

    print(f'Num Wires: {num_wires}')

    wires = [{'position': Vec(0, 0), 'extents': BoundingBox(), 'segments': []} for _ in range(0, num_wires)]

    def calcSegment(ix, vec):
        
        pos = wires[ix]['position']
        extents = wires[ix]['extents']
        
        result = LineSegment(pos, delta=vec)
        wires[ix]['position'] = result.end
        # update extents
        extents.update(result.end)
        return result

    for ix, commands in enumerate(wire_commands):
        wires[ix]['segments'] = [calcSegment(ix, vec) for vec in commands]
    
    for ix, wire in enumerate(wires):
        
        print(f'Wire {ix} Position {wire["position"]} Extents {wire["extents"]}')
        
        for segment in wire['segments']:
            
            print(f'{segment}')
    
    intersections = []
    
    # stupidly intersect everything with everything
    for lhs in range(0, num_wires):
        
        for rhs in range(lhs + 1, num_wires):
            
            for segmentLhs in wires[lhs]['segments']:
                
                for segmentRhs in wires[rhs]['segments']:
                    
                    intersection = segmentLhs.intersect(segmentRhs)
                    
                    if (intersection is not None and not (intersection.x == 0 and intersection.y == 0)):
                        print(f'{segmentLhs} intersects {segmentRhs} at {intersection}')
                        intersections.append(intersection)
    
    minIntersect = min(intersections, key=lambda x: x.norm(), default=None)
    
    print(f'Closest intersection: {minIntersect} ({minIntersect.norm()})')
    
    drawWires(wires, intersections, minIntersect)

if __name__=='__main__':
    sys.exit(main())