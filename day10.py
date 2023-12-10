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
    
    def __radd__(self, other):
        if self.__class__ is other.__class__:
            return Position(self.x + other.x, self.y + other.y)
        elif (other.__class__ is tuple and len(other) == 2):
            return Position(self.x + other[0], self.y + other[1])
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
    
    def to_string(self, print_start: bool = True, print_position: Position = Position(-1, -1)) -> str:
        """Print Pipe Network to a String"""
        
        result = ''
        
        for y in range(self.height):
            for x in range(self.width):
                position = Position(x, y)
                if (print_start and self.start == position):
                    result += 'S'
                elif (print_position == position):
                    result += 'X'
                else:
                    result += self.pipes.get(position, '.')
            result += '\n'
        
        # write result to file for debug
        with open('day10_network', 'w', encoding='utf-8') as f:
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
    
    logging.info(f'Parsed Network:\n{network.to_string()}')
    
    # cull unconnected loops
    network.cull_unconnected()
    
    logging.info(f'Parsed Network:\n{network.to_string()}')
    
    # find type of start node
    network.determine_start_node()
    
    logging.info(f'Parsed Network:\n{network.to_string(print_start=False)}')
    
    return network

def part1(network: PipeNetwork) -> tuple[int, Position]:
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
    
    return length, pipes[length // 2]

def part2():
    pass

def main(args):
    
    network = read_inputs(args.example)
    length, pos = part1(network)
    logging.info(f'Part 1: Length {length} (Opposite at {pos}; length {length // 2})')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
