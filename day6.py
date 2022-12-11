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

def findMarker(transmission: str, len_marker: int) -> Optional[int]:
    """Find n-character marker in transmission
    and output position after marker.
    """
    result = None

    for i in range(0, len(transmission) - len_marker + 1):
        if (len(set(transmission[i:i+len_marker])) == len_marker):
            result = i + len_marker
            break
    
    return result

def part1(transmission: str) -> Optional[int]:
    """Find Start-of-Packet marker in transmission
    and output position of payload after marker.
    """
    return findMarker(transmission, len_marker=4)

def part2(transmission: str) -> Optional[int]:
    """Find Start-of-Message marker in transmission
    and output position of payload after marker.
    """
    return findMarker(transmission, len_marker=14)

def main(args):
    
    transmission = read_inputs(args.example)
    payload_pos = part1(transmission)
    logging.info(f'Part 1: Payload starts at {payload_pos}')
    message_pos = part2(transmission)
    logging.info(f'Part 2: Message starts at {message_pos}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
