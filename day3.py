#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import logging
from io import StringIO
from timeit import default_timer as timer

class MultiLineFormatter(logging.Formatter):
    def format(self, record):
        str = logging.Formatter.format(self, record)
        header, footer = str.split(record.message)
        str = str.replace('\n', '\n' + ' '*len(header))
        return str

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
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        return (self.x < other.x or self.y < other.y)
    
    def __gt__(self, other):
        return (self.x > other.x or self.y > other.y)
    
    def norm(self):
        return abs(self.x) + abs(self.y)
    
    def __repr__(self):
        return f'{self!s} at 0x{id(self):08X}'
    
    def __str__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y})'

class LineSegment:
    
    def __init__(self, beg, end=None, delta=None):
        
        self.begin = beg
        self.end = end or self.begin + delta
        self.dir = 'v' if (self.begin.x == self.end.x) else 'h'
        self.start = min(beg, self.end)
        self.finish = max(beg, self.end)
    
    def intersect(self, other, sameWire=False):
        
        # remove intersection due to touching in start, finish
        if (sameWire):
            if (self.finish == other.start \
                or self.start == other.finish \
                or self.finish == other.finish \
                or self.start == other.start):
                return None
        
        # lines are perpendicular
        # assume lines not parallel, overlap in same direction
        if (self.dir != other.dir):
            
            if (other.start.x <= self.start.x <= other.finish.x and self.start.y <= other.start.y <= self.finish.y):
                # vertical case
                return Vec(self.start.x, other.start.y)
            elif (other.start.y <= self.start.y <= other.finish.y and self.start.x <= other.start.x <= self.finish.x):
                # horizontal case
                return Vec(other.start.x, self.start.y)
        
        return None
    
    def __repr__(self):
        return f'{self!s} at 0x{id(self):08X}'
    
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
    
    def __repr__(self):
        return f'{self!s} at 0x{id(self):08X}'
        
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
    
    xOffset = -bb.begin.x
    yOffset = bb.begin.y
    
    xSize = bb.end.x - bb.begin.x + 1
    ySize = bb.end.y - bb.begin.y + 1
    
    # add 1 field outline
    xOffset += 1
    yOffset -= 1
    xSize += 2
    ySize += 2
    
    sparseField = {}
    
    def toX(x):
        return x + xOffset
    
    def toY(y):
        return ySize - y - 1 + yOffset
    
    hbars = {
        0: '-',
        1: '=',
        2: '═',
        }
    vbars = {
        0: '|',
        1: '¦',
        2: '║',
        }
    
    # draw lines
    for ix, wire in enumerate(wires):
    
        hbar = hbars.get(ix, '-')
        vbar = vbars.get(ix, '|')
    
        for segment in wire['segments']:
            
            # yBegin/yEnd switched, because .y is cartesian, but yBegin/yEnd is line number
            xBegin = toX(segment.start.x)
            yBegin = toY(segment.finish.y)
            
            xEnd = toX(segment.finish.x)
            yEnd = toY(segment.start.y)
            
            line = hbar if segment.dir == 'h' else vbar
            
            # draw line
            for x in range(xBegin, xEnd + 1):
                for y in range(yBegin, yEnd + 1):
                    sparseField[(x, y)] = line
            
            # draw begin
            sparseField[(xBegin, yBegin)] = '+'
            
            # draw end
            sparseField[(xEnd, yEnd)] = '+'
    
    # draw intersection points
    for intersection in intersections:
        x = toX(intersection.x)
        y = toY(intersection.y)
        sparseField[(x, y)] = 'x'
    
    # draw self intersection points
    for wire in wires:
        for intersection in wire['self_intersections']:
            x = toX(intersection.x)
            y = toY(intersection.y)
            sparseField[(x, y)] = 'S'
    
    # draw closes intersection point
    if (minIntersect is not None):
        x = toX(minIntersect.x)
        y = toY(minIntersect.y)
        sparseField[(x, y)] = 'X'
    
    # draw origin
    sparseField[(toX(0), toY(0))] = 'O'
    
    with open(filename, 'w', encoding='utf-8') as f:
        for y in range(0, ySize):
            buffer=StringIO()
            for x in range(0, xSize):
                char = sparseField.get((x, y), ' ')
                buffer.write(char)
            buffer.write('\n')
            f.write(buffer.getvalue())
    
def calcWireIntersectCost(wire, intersection):
    
    cost = 0
    begin_cost = 0
    cost_offset = 0
    self_intersection_status = {position: {'visited': False, 'cost': 0} for position in wire['self_intersections']}
    
    logging.debug('--------------------------')
    logging.debug(f'{intersection}')
    
    for segment in wire['segments']:
        
        logging.debug(f'Segment {segment} -- {cost}')
        begin_cost = cost
        
        #for position, attr in self_intersection_status.items():
        #    logging.debug(f'  {position}: visited {attr["visited"]} cost {attr["cost"]}')
        
        # check if intersection reached
        wireIntersection = next(filter(lambda x: x['position'] == intersection, wire['segment_intersections'].get(segment, [])), None)
        
        # check if any self-intersection already visited
        for self_intersection in wire['segment_self_intersections'].get(segment, []):
            status = self_intersection_status[self_intersection['position']]
            
            if (not status['visited']):
                continue
            
            # additional check if we reached intersection
            if (wireIntersection is not None):
                # self intersection must be _after_ wire intersection for shortcut
                logging.debug(f'Wire intersection w/ self intersection: {wireIntersection["position"]} -- {self_intersection["position"]}\n'
                              f'on Segment {segment.begin}--{segment.end}')
                if (segment.begin < segment.end and wireIntersection['position'] < self_intersection['position']):
                    continue
                if (segment.begin > segment.end and wireIntersection['position'] > self_intersection['position']):
                    continue
                logging.debug(f'Wire intersection after self intersection.')
            
            # take better cost of two
            logging.debug(f'Taking {self_intersection["position"]} cost: {cost} old: {status["cost"]}')
            if ((cost + self_intersection['cost']) > status['cost']):
                cost_offset = self_intersection['cost']
                cost = status['cost']
            break
        
        # mark all current self-intersections visited
        for self_intersection in wire['segment_self_intersections'].get(segment, []):
            status = self_intersection_status[self_intersection['position']]
            # shouldn't matter as no point is visited thrice
            # but be safe
            if (status['visited']):
                continue
            status['visited'] = True
            # distinguish between self intersection that is after current self intersection we switched to
            # and self intersection that is located before current self intersection we switched to
            # if after: take adjusted cost and add delta of cost from current self intersection to this
            #           self intersection (which means cost of begin of section to this self intersection minus cost
            #           from begin of section to current self intersection)
            # if before: take original cost from begin of section and add cost of begin of section to this
            #            self intersection that was calculated in main
            if (self_intersection['cost'] >= cost_offset):
                status['cost'] = cost + self_intersection['cost'] - cost_offset
            else:
                status['cost'] = begin_cost + self_intersection['cost'] 
            logging.debug(f'Visiting {self_intersection["position"]} cost: {cost} total: {status["cost"]}')
        
        # check if we're done
        if (wireIntersection is not None):
            cost += wireIntersection['cost'] - cost_offset
            break
        
        
        # add traveling cost
        cost += (segment.end - segment.begin).norm() - cost_offset
        cost_offset = 0
    
    logging.debug(f'------------/{cost}/------------')
    
    return cost
    
def calcIntersectCost(wires, intersection):
    
    # find cheapest path for each wire
    return sum(calcWireIntersectCost(wire, intersection) for wire in wires)
    
    
def main(draw=False):

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
    
    # Custom
    #lines = ['', '']
    #lines[0] = 'D1,R2'
    #lines[1] = 'R3,D2,L2,U3,R3,D2,L2'
    
    start = timer()
    
    wire_commands = [[command2vector(x) for x in line.split(',')] for line in lines]
    num_wires = len(wire_commands)
    end = timer()

    logging.info(f'Num Wires: {num_wires}')
    logging.error(f'Parsing: {end-start:g}s')

    wires = [{
              'position': Vec(0, 0),
              'extents': BoundingBox(),
              'segments': [],
              'segment_intersections': {},
              'segment_self_intersections': {}
              }
             for _ in range(0, num_wires)]

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
        wires[ix]['segment_self_intersections'] = {}
    
    for ix, wire in enumerate(wires):
        
        logging.debug(f'Wire {ix} Position {wire["position"]} Extents {wire["extents"]}')
        
        for segment in wire['segments']:
            
            logging.debug(f'{segment}')
    
    origin = Vec(0, 0)
    intersections = []
    
    start = timer()
    
    for wire in wires:
        self_intersects = []
        for ixLhs, segmentLhs in enumerate(wire['segments']):
            logging.info(f'Segment LHS: {segmentLhs}')
            for segmentRhs in wire['segments'][ixLhs+1:]:
                logging.info(f'  Segment RHS: {segmentRhs}')
                intersection = segmentLhs.intersect(segmentRhs, sameWire=True)
                if (intersection is not None and (intersection != origin)):
                    self_intersects.append(intersection)
                    wire['segment_self_intersections'].setdefault(segmentLhs, []).append({'position': intersection, 'cost': (intersection - segmentLhs.begin).norm(), 'other': segmentLhs})
                    wire['segment_self_intersections'].setdefault(segmentRhs, []).append({'position': intersection, 'cost': (intersection - segmentRhs.begin).norm(), 'other': segmentLhs})
            for entry, data in wire['segment_self_intersections'].items():
                logging.info(f'--> {entry}: {data}')
        wire['self_intersections'] = self_intersects
        
    end = timer()
    logging.error(f'Self intersects: {end-start:g}s')
    
    start = timer()
    # stupidly intersect everything with everything
    for lhs, wireLhs in enumerate(wires):
        
        for rhs, wireRhs in enumerate(wires[lhs + 1:], lhs + 1):
            
            for segmentLhs in wireLhs['segments']:
                
                for segmentRhs in wireRhs['segments']:
                    
                    intersection = segmentLhs.intersect(segmentRhs)
                    
                    if (intersection is not None and (intersection != origin)):
                        wireLhs['segment_intersections'].setdefault(segmentLhs, []).append({'position': intersection, 'cost': (intersection - segmentLhs.begin).norm(), 'other': segmentRhs})
                        wireRhs['segment_intersections'].setdefault(segmentRhs, []).append({'position': intersection, 'cost': (intersection - segmentRhs.begin).norm(), 'other': segmentLhs})
                        intersections.append(intersection)
    
    end = timer()
    logging.error(f'Wire intersects: {end-start:g}s')
    
    # Part 1
    
    start=timer()
    minIntersect = min(intersections, key=lambda x: x.norm(), default=None)
    end = timer()
    
    logging.info(f'Closest intersection: {minIntersect} ({minIntersect.norm()})')
    logging.error(f'Part 1: {end-start:g}s')
    
    # Part 2
    start=timer()
    minStepInterset, steps = min(zip(intersections, map(lambda x: calcIntersectCost(wires, x), intersections)), key=lambda x: x[1], default=None)
    end = timer()
    
    logging.info(f'Cheapest intersection: {minStepInterset} ({steps})')
    logging.error(f'Part 2: {end-start:g}s')
    
    if (draw):
        drawWires(wires, intersections, minIntersect)

if __name__=='__main__':

    logLevelMap = {
        'debug':   logging.DEBUG,
        'info':    logging.INFO,
        'warning': logging.WARNING,
        'error':   logging.ERROR,
        }
    
    # Set up Logger
    l = logging.getLogger()
    h = logging.StreamHandler()
    h.setFormatter(MultiLineFormatter(fmt='[%(asctime)s][%(levelname)-8s] %(message)s', datefmt='%d %b %Y %H:%M:%S'))
    l.addHandler(h)
    l.setLevel(logging.INFO)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Advent of Code.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--loglevel', help='Loglevel, one of \'DEBUG\', \'INFO\' (default), \'WARNING\', \'ERROR\'.', type=str, default='INFO')
    parser.add_argument('--draw', help='Draw output diagram', action='store_true', default=False)

    # Parse arguments
    args = parser.parse_args()
    
    # Set User Loglevel
    logLevel = logLevelMap.get(args.loglevel.lower(), None)
    if (logLevel is None):
        logging.error('Invalid loglevel \'{0:s}\' passed. Exiting...'.format(args.loglevel))
        sys.exit(-1)
    
    l.setLevel(logLevel)
    
    sys.exit(main(draw=args.draw))
