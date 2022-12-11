#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from typing import Dict, List, Optional, Tuple

from lib import setup

example1_input = """bvwbjplbgvbhsrlpgdmjqwftvncz"""
example2_input = """nppdvjthqldpwncqszvftbrmjlhg"""
example3_input = """nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"""
example4_input = """zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"""

def read_inputs(example=0) -> str:
    
    match (example):
        case 1:
            data = example1_input
        case 2:
            data = example2_input
        case 3:
            data = example3_input
        case 4:
            data = example4_input
        case other:
            with open('day6_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    return data[0]

def part1(transmission: str) -> Optional[int]:
    """Find Start-of-Packet marker in transmission
    and output position of payload after marker.
    """

    result = None

    for i in range(0, len(transmission) - 4 + 1):
        if (len(set(transmission[i:i+4])) == 4):
            result = i + 4
            break
    
    return result

def part2():
    pass

def main(args):
    
    transmission = read_inputs(args.example)
    payload_pos = part1(transmission)
    logging.info(f'Part 1: Payload starts at {payload_pos}')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
