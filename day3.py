#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import math

from lib import setup

example_input = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

def read_inputs(example=False):

    if (example):
        data = example_input
    else:
        with open('day3_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    return [int(v, 2) for v in data.splitlines() if v]

def part1(diagnostics):
    
    gamma = 0x00
    epsilon = 0x00

    # find largest power of two in input
    max_log2 = math.floor(math.log2(max(diagnostics)))

    logging.debug(f'max_log2: {max_log2}')

    total = len(diagnostics)

    for i in range(max_log2 + 1):
        num_set_bits = sum(map(lambda v: (v >> i) & 0x01, diagnostics))
        if (num_set_bits >= total / 2):
            gamma |= (1 << i)
        else:
            epsilon |= (1 << i)

    logging.info(f'Part 1: Power Consumption {gamma * epsilon} (γ: {gamma:04X} ε: {epsilon:04X})')

def part2(diagnostics):
    
    # find largest power of two in input
    max_log2 = math.floor(math.log2(max(diagnostics)))

    logging.debug(f'max_log2: {max_log2}')

    diag_o2 = diagnostics[::]
    diag_co2 = diagnostics[::]

    for i in range(max_log2, -1, -1):

        o2_keep = 0x00
        co2_keep = 0x00

        num_set_bits_o2 = sum(map(lambda v: (v >> i) & 0x01, diag_o2))
        num_set_bits_co2 = sum(map(lambda v: (v >> i) & 0x01, diag_co2))

        if (num_set_bits_o2 >= len(diag_o2) / 2):
            o2_keep = (1 << i)
        if (num_set_bits_co2 < len(diag_co2) / 2):
            co2_keep = (1 << i)

        if (len(diag_o2) > 1):
            diag_o2 = list(filter(lambda v: v & (1 << i) == o2_keep, diag_o2))
        if (len(diag_co2) > 1):
            diag_co2 = list(filter(lambda v: v & (1 << i) == co2_keep, diag_co2))
        
    o2 = diag_o2[0]
    co2 = diag_co2[0]

    logging.info(f'Part 2: Life Support Rating: {o2 * co2} (O₂: {o2} CO₂: {co2})')

def main(args):
    
    diagnostics = read_inputs(args.example)
    part1(diagnostics[::])
    part2(diagnostics[::])

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
