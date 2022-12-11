#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from abc import ABC, abstractmethod
from typing import ClassVar, Dict, List, Optional, Tuple

from lib import setup

example1_input = """noop
addx 3
addx -5
"""

example2_input = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

RegisterFile = Dict[str, int]

class Opcode(ABC):
    name: ClassVar[str]
    cycles: ClassVar[int]
    
    opcodes = dict()
    
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def execute(self, registers: RegisterFile):
        pass
    
    def parse(name, *args, **kwargs):
        return Opcode.opcodes[name](*args, **kwargs)
    
    def __str__(self):
        return self.name

def register_opcode(opcode_cls):
    Opcode.opcodes[opcode_cls.name] = opcode_cls
    return opcode_cls

@register_opcode
class Nop(Opcode):
    name = 'noop'
    cycles = 1
    
    def __init__(self, *args, **kwargs):
        super().__init__()
    
    def execute(self, registers: RegisterFile):
        pass

@register_opcode
class AddX(Opcode):
    name = 'addx'
    cycles = 2
    
    def __init__(self, value, *args, **kwargs):
        super().__init__()
        self.value = int(value)
    
    def __str__(self):
        return f'{self.name} {self.value}'
    
    def execute(self, registers: RegisterFile):
        registers['X'] += self.value

def read_inputs(example=0) -> List[Opcode]:
    
    match (example):
        case 1:
            data = example1_input
        case _ if (example):
            data = example2_input
        case _:
            with open('day10_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    opcodes = []
    
    # parse logic
    for line in data:
        args = line.split(' ')
        opcode = Opcode.parse(args[0], *args[1:])
        opcodes.append(opcode)
    
    return opcodes

class CPU:
    
    def __init__(self):
        self.registers = {'X': 1}
        self.cycles = 1
    
    def execute(self, opcode: Opcode):
        opcode.execute(self.registers)
        self.cycles += opcode.cycles

def part1(opcodes: List[Opcode]):
    
    cpu = CPU()
    signal_stengths = {}
    cycle = 1
    
    for opcode in opcodes:
        # record registers during cycle
        registers = {**cpu.registers}
        # execute opcode
        cpu.execute(opcode)
        # determine signal stengths
        for cycle in range(cycle, cpu.cycles):
            signal_stengths[cycle] = registers['X'] * cycle
        cycle = cpu.cycles
    
    # return sum of signal stengths of cycles 20, 60, 100, 140, 180, 220
    return sum(signal_stengths[c] for c in [20, 60, 100, 140, 180, 220])

def part2():
    pass

def main(args):
    
    opcodes = read_inputs(args.example)
    signal_stengths = part1(opcodes)
    logging.info(f'Part 1: Sum of Signal Stengths = {signal_stengths}')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
