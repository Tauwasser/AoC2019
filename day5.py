#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import re

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

@dataclass
class Stack:
    crates : List[str] = field(default_factory=list)

@dataclass
class Command:
    src: int
    dst: int
    num: int

COMMAND_PATTERN = re.compile(r'move (\d+) from (\d+) to (\d+)')

def read_inputs(example=0) -> Tuple[List[Stack], List[Command]]:
    
    if (example):
        data = example_input
    else:
        with open('day5_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    # size stacks according to first line
    num_stacks = (len(data[0]) + 1) // 4
    stacks = [Stack() for _ in range(num_stacks)]
    commands = []
    
    # parse stacks first
    for i, line in enumerate(data):
        
        # found empty line
        if (line == ''):
            break
        
        for sid in range(0, num_stacks):
            crate_label = line[sid*4:(sid+1)*4].strip()
            if (crate_label == ''):
                continue
            
            # skip stack numbers
            if (len(crate_label) == 1):
                continue
            
            # make sure it's three chars
            if (len(crate_label) != 3 or crate_label[0] != '[' or crate_label[2] != ']'):
                raise RuntimeError(f'Found invalid crate label {crate_label} on line {i}.')
            
            # append crate
            stacks[sid].crates.append(crate_label[1])
    
    # parse commands
    for line in data[i+1:]:
        m = COMMAND_PATTERN.match(line)
        num, src, dst = (int(g) for g in m.groups())
        commands.append(Command(src, dst, num))
    
    for stack in stacks:
        stack.crates.reverse()
    
    return stacks, commands

def _draw_stacks(stacks: List[Stack]):
    
    max_height = max(len(stack.crates) for stack in stacks)
    image = ''
    
    for height in range(max_height - 1, -1, -1):
        line = ''
        for stack in stacks:
            if (len(stack.crates) <= height):
                line += '    '
            else:
                line += f'[{stack.crates[height]}] '
        image += line
        image += '\n'
    
    image += (''.join(f' {i}  ' for i in range(1, len(stacks) + 1)))
    logging.info(image)

def part1(stacks: List[Stack], commands: List[Command]) -> str:
    
    # draw initial state
    _draw_stacks(stacks)
    
    for command in commands:
        
        logging.info(f'Move {command.num} from {command.src} to {command.dst}')
        
        src = stacks[command.src - 1]
        dst = stacks[command.dst - 1]
        dst.crates += src.crates[:-command.num-1:-1]
        src.crates = src.crates[:-command.num]
        _draw_stacks(stacks)
    
    labels = ''
    # determine top crates
    for stack in stacks:
        if (len(stack.crates) > 0):
            labels += stack.crates[-1]
    
    return labels

def part2():
    pass

def main(args):
    
    stacks, commands = read_inputs(args.example)
    crates_on_top = part1(stacks, commands)
    logging.info(f'Part 1: Crates on top {crates_on_top}')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
