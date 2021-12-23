#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import math

from lib import setup

def read_inputs():
    with open('day3_input', 'r', encoding='utf-8') as f:
        diagnostics = [int(v, 2) for v in f.read().splitlines()]
    return diagnostics

def part1(diagnostics):
    
    gamma = 0x00
    epsilon = 0x00

    # find largest power of two in input
    max_log2 = math.floor(math.log2(max(diagnostics)))

    logging.debug(f'max_log2: {max_log2}')

    total = len(diagnostics)

    for i in range(max_log2 + 1):
        num_set_bits = sum(map(lambda v: (v >> i) & 0x01, diagnostics))
        if (num_set_bits > total / 2):
            gamma |= (1 << i)
        elif (num_set_bits < total / 2):
            epsilon |= (1 << i)

    logging.info(f'Part 1: Power Consumption {gamma * epsilon} (γ: {gamma:04X} ε: {epsilon:04X})')

def part2(diagnostics):
    pass

def main():
    
    diagnostics = read_inputs()
    part1(diagnostics[::])
    part2(diagnostics[::])

if __name__ == '__main__':
    setup()
    sys.exit(main())
