#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from lib import setup

example1_input = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

example2_input = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

example3_input = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

@dataclass(eq=True, frozen=True)
class Position:
    x: int
    y: int
    
    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def __add__(self, other):
        if self.__class__ is other.__class__:
            return Position(self.x + other.x, self.y + other.y)
        elif (other.__class__ is tuple and len(other) == 2):
            return Position(self.x + other[0], self.y + other[1])
        return NotImplemented
    
    def __sub__(self, other):
        if self.__class__ is other.__class__:
            return Position(self.x - other.x, self.y - other.y)
        elif (other.__class__ is tuple and len(other) == 2):
            return Position(self.x - other[0], self.y - other[1])
        return NotImplemented
    
    def __mul__(self, other):
        if (other.__class__ is tuple and len(other) == 2):
            return Position(self.x * other[0], self.y * other[1])
        elif (other.__class__ is int):
            return Position(self.x * other, self.y * other)
        return NotImplemented
    
    def __floordiv__(self, other):
        if (other.__class__ is tuple and len(other) == 2):
            return Position(self.x // other[0], self.y // other[1])
        elif (other.__class__ is int):
            return Position(self.x // other, self.y // other)
        return NotImplemented

@dataclass
class PipeNetwork:
    
    PIPE_PROPERTIES = {
        '|': {
            (0, -1): ('|', 'F', '7', 'S'),
            (0, +1): ('|', 'L', 'J', 'S'),
        },
        '-': {
            (-1, 0): ('-', 'L', 'F', 'S'),
            (+1, 0): ('-', 'J', '7', 'S'),
        },
        'L': {
            (0, -1): ('|', 'F', '7', 'S'),
            (+1, 0): ('-', 'J', '7', 'S'),
        },
        'J': {
            (0, -1): ('|', 'F', '7', 'S'),
            (-1, 0): ('-', 'L', 'F', 'S'),
        },
        'F': {
            (0, +1): ('|', 'L', 'J', 'S'),
            (+1, 0): ('-', 'J', '7', 'S'),
        },
        '7': {
            (0, +1): ('|', 'L', 'J', 'S'),
            (-1, 0): ('-', 'L', 'F', 'S'),
        },
        'S': {
            (0, -1): ('|', 'F', '7'),
            (0, +1): ('|', 'L', 'J'),
            (-1, 0): ('-', 'L', 'F'),
            (+1, 0): ('-', 'J', '7'),
        },
        '.': {
        },
    }
    
    START_PIPE = {
        ('.', '|', '.', '|'): '|',
        ('-', '.', '-', '.'): '-',
        ('.', '.', '-', '|'): 'L',
        ('-', '.', '.', '|'): 'J',
        ('.', '|', '-', '.'): 'F',
        ('-', '|', '.', '.'): '7',
    }
    
    start: Position = field(default=Position(0, 0))
    width: int = 0
    height: int = 0
    pipes: dict[Position, str] = field(default_factory=dict, repr=False)
    inside: set[Position] = field(default_factory=set, repr=False)
    
    def to_string(self, print_start: bool = True, print_position: Position = Position(-1, -1), outside: set[Position] = {}, filename: str = None) -> str:
        """Print Pipe Network to a String"""
        
        result = ''
        
        for y in range(self.height):
            for x in range(self.width):
                position = Position(x, y)
                if (print_start and self.start == position):
                    result += 'S'
                elif (print_position == position):
                    result += 'X'
                elif (position in self.inside):
                    result += 'I'
                elif (position in outside):
                    result += 'O'
                else:
                    result += self.pipes.get(position, '.')
            result += '\n'
        
        # write result to file for debug
        if (filename is not None):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result)
        
        return result
    
    def delete_pipe(self, position):
        """Delete Pipe at Position"""
        
        delete_pos = [position]
        
        while (delete_pos):
            pos = delete_pos.pop()
            pipe = self.pipes.get(pos, None)
            # skip pipes already removed
            if (pipe is None):
                continue
            
            # delete pipe
            del self.pipes[pos]
            
            # check connections by props
            props = PipeNetwork.PIPE_PROPERTIES[pipe]
            for delta in props.keys():
                connected_pipe = self.pipes.get(pos + delta, None)
                if (connected_pipe is not None):
                    delete_pos.append(pos + delta)
    
    def cull_unconnected(self):
        """Cull unconnected Pipes"""
        
        for pos in tuple(self.pipes.keys()):
            
            pipe = self.pipes.get(pos, None)
            # skip if pipe was already removed
            if (pipe is None):
                continue
            # skip if pipe is start
            if (pipe == 'S'):
                continue
            
            # check connections by props
            props = PipeNetwork.PIPE_PROPERTIES[pipe]
            
            for delta, pipes in props.items():
                
                connected_pipe = self.pipes.get(pos + delta, None)
                if (connected_pipe not in pipes):
                    self.delete_pipe(pos)
                    break
    
    def determine_start_node(self):
        
        pos = self.start
        props = PipeNetwork.PIPE_PROPERTIES['S']
        
        def _get_connected_pipe(delta):
            pipe = self.pipes.get(pos + delta, '.')
            pipes = props[delta]
            
            if (pipe in pipes):
                pipe = pipes[0]
            else:
                pipe = '.'
            
            return pipe
        
        tpipe = _get_connected_pipe((0, -1))
        bpipe = _get_connected_pipe((0, +1))
        lpipe = _get_connected_pipe((-1, 0))
        rpipe = _get_connected_pipe((+1, 0))
        
        start_pipe = PipeNetwork.START_PIPE.get((lpipe, bpipe, rpipe, tpipe), None)
        if (start_pipe is None):
            raise RuntimeError(f'Could not determine Start Pipe Type from {(lpipe, bpipe, rpipe, tpipe)}.')
        
        self.pipes[self.start] = start_pipe

def read_inputs(example=0) -> PipeNetwork:
    
    match (example):
        case 1 if (example):
            data = example1_input
        case 2 if (example):
            data = example2_input
        case 3 if (example):
            data = example3_input
        case _:
            with open('day10_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    
    # parse and pre-process map
    # goal is to eliminate as many tiles as possible that cannot be part of loop
    # before running more complex algorithms
    
    eline = '.' * len(data[0])
    network = PipeNetwork()
    
    for y, (line, tline, bline) in enumerate(zip(data, [eline] + data, data[1:] + [eline])):
        for x, (pipe, lpipe, rpipe, tpipe, bpipe) in enumerate(zip(line, '.' + line, line[1:] + '.', tline, bline)):
            
            position = Position(x, y)
            props = PipeNetwork.PIPE_PROPERTIES[pipe]
            
            # grab all compatible pipes
            # in case compatibility does not matter, accept current t/b/l/r
            # pipe as compatible by default
            tpipes = props.get((0, -1), (tpipe,))
            bpipes = props.get((0, +1), (bpipe,))
            lpipes = props.get((-1, 0), (lpipe,))
            rpipes = props.get((+1, 0), (rpipe,))
            
            match(pipe):
                case 'S':
                    network.start = position
                    network.pipes[position] = pipe
                case '.':
                    pass
                case _:
                    # only store if compatible top/bottom/left/right pipe
                    if (tpipe in tpipes and bpipe in bpipes and lpipe in lpipes and rpipe in rpipes):
                        network.pipes[position] = pipe
    
    # save width/height
    network.width = x + 1
    network.height = y + 1
    
    logging.info(f'Parsed Network:\n{network.to_string(filename="day10_network")}')
    
    # cull unconnected loops
    network.cull_unconnected()
    
    logging.info(f'Parsed Network:\n{network.to_string(filename="day10_network")}')
    
    # find type of start node
    network.determine_start_node()
    
    logging.info(f'Parsed Network:\n{network.to_string(filename="day10_network", print_start=False)}')
    
    return network

def part1(network: PipeNetwork) -> tuple[int, list[Position]]:
    "Determine Pipe Length and half-way Position"
    
    length = 1
    last_pos = Position(-1, -1)
    cur_pos = network.start
    
    pipes = [cur_pos]
    
    while (True):
        
        # get properties
        props = PipeNetwork.PIPE_PROPERTIES[network.pipes[cur_pos]]
        # get next position that is not last position
        for delta in props.keys():
            nxt_pos = cur_pos + delta
            if (nxt_pos != last_pos):
                # store last position
                last_pos = cur_pos
                # upddate current position
                cur_pos = nxt_pos
                break
        
        # check if we reached the end
        if (cur_pos == network.start):
            break
        
        # increment length
        length += 1
        
        # store position
        pipes.append(cur_pos)
    
    return length, pipes

def part2(network: PipeNetwork, pipes: list[Position]) -> int:
    """Find Inside Area of Pipe Network"""
    
    # delete all pipes that are not part of the network
    network.pipes = {position: network.pipes[position] for position in pipes}
    logging.info(f'Reduced Network:\n{network.to_string(filename="day10_network", print_start=False)}')
    
    # create a temporary network at twice the resolution
    tmp_network = PipeNetwork(network.start * 2, network.width * 2 + 2, network.height * 2 + 2)
    offset = (1, 1)
    
    for pos, pipe in network.pipes.items():
        tmp_network.pipes[pos * 2 + offset] = pipe
        
        if (pipe in ('|', 'F', '7')):
            tmp_network.pipes[pos * 2 + offset + (0, +1)] = '|'
        if (pipe in ('-', 'F', 'L')):
            tmp_network.pipes[pos * 2 + offset + (+1, 0)] = '-'
    
    logging.info(f'Widened Network:\n{tmp_network.to_string(filename="day10_network_wide", print_start=False)}')
    nxt_outside: set[Position] = set()
    
    # add layer of OUTSIDE around network
    for x in range(tmp_network.width):
        nxt_outside.add(Position(x, 0))
        nxt_outside.add(Position(x, tmp_network.height - 1))
    for y in range(1, tmp_network.height - 1):
        nxt_outside.add(Position(0, y))
        nxt_outside.add(Position(tmp_network.width - 1, y))
    
    logging.info(f'Outside Prep Network:\n{tmp_network.to_string(filename="day10_network_wide", outside=nxt_outside, print_start=False)}')
    
    outside = set(o for o in nxt_outside)
    
    while nxt_outside:
        base = nxt_outside.pop()
        for delta in ((0, +1), (0, -1), (+1, 0), (-1, 0)):
            # calc position
            pos = base + delta
            
            # make sure position is inside network
            if not(0 <= pos.x < tmp_network.width):
                continue
            if not(0 <= pos.y < tmp_network.height):
                continue
            
            # check pipes
            pipe = tmp_network.pipes.get(pos, None)
            # pipes cannot be outside
            if (pipe is not None):
                continue
            # outside is already outside
            if (pos in outside):
                continue
            # add to lists of all outside positions and list of outside positions to check
            outside.add(pos)
            nxt_outside.add(pos)
    
    logging.info(f'Outside Fill Network:\n{tmp_network.to_string(filename="day10_network_wide", outside=outside, print_start=False)}')
    
    # determine inside from non-pipe/non-outside areas
    for y in range(1, tmp_network.height - 1, 2):
        for x in range(1, tmp_network.width - 1, 2):
            pos = Position(x, y)
            pipe = tmp_network.pipes.get(pos, None)
            # pipes cannot be inside
            if (pipe is not None):
                continue
            # outside cannot be inside
            if (pos in outside):
                continue
            network.inside.add((pos - offset) // 2)
    
    logging.info(f'Inside Network:\n{network.to_string(filename="day10_network", print_start=False)}')
    return len(network.inside)

def main(args):
    
    network = read_inputs(args.example)
    length, pipes = part1(network)
    logging.info(f'Part 1: Length {length} (Opposite at {pipes[length // 2]}; length {length // 2})')
    inside = part2(network, pipes)
    logging.info(f'Part 2: Inside {inside}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
