#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from lib import setup

example1_input = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
"""

example2_input = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""

digit_map = {
    'abcefg':  0,
    'cf':      1,
    'acdeg':   2,
    'acdfg':   3,
    'bcdf':    4,
    'abdfg':   5,
    'abdefg':  6,
    'acf':     7,
    'abcdefg': 8,
    'abcdfg':  9,
}

@dataclass(frozen=True)
class Entry:
    patterns: List[str]
    digits:   List[str]

def read_inputs(example=0) -> List[Entry]:
    
    if (1 == example):
        data = example1_input
    elif (example):
        data = example2_input
    else:
        with open('day8_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    # parse logic
    entries = []
    for line in data:
        digit_patterns, number_patterns = line.split('|')
        digits = digit_patterns.split()
        numbers = number_patterns.split()
        entries.append(Entry(digits, numbers))
    
    return entries

def find_mapping(patterns: List[str]) -> Dict[str, str]:
    
    # find mapping for entries of length 2, 3 and 4 (unique)
    char_values: Dict[str, List[str]] = defaultdict(lambda: set('abcdefg'))
    char_map: Dict[str, str] = dict()
    
    def lengths(l):
        return lambda pattern: len(pattern) in l
    
    # for each character in known 7 segment digit patterns
    # encode all input patterns of same length as options
    for pattern in filter(lengths([2, 3, 4]), patterns):
        for known_digits in filter(lengths([2, 3, 4]), digit_map):
            if (len(pattern) == len(known_digits)):
                for char in known_digits:
                    char_values[char] &= set(pattern)
    
    # 'c', 'f' should now be down to two letter (three patterns all contain it)
    assert(char_values['c'] == char_values['f'])
    for char in filter(lambda char: char in 'abdeg', char_values):
        char_values[char] -= char_values['c']
    
    # we should now have a unique map for 'a' and 'b', 'd' down to two letters
    assert(len(char_values['a']) == 1)
    assert(len(char_values['b']) == 2)
    assert(char_values['b'] == char_values['d'])
    
    # store known map 'a'
    char_map['a'] = ''.join(char_values['a'])
    
    # find digit 9 to identify 'g' by way of elimination through 'a' and 'bcdf' (digit 4)
    target = set()
    for char in 'abcdf':
        target |= char_values[char]
    
    char_values['g'] = set(next(filter(lambda pattern: target <= set(pattern), filter(lengths([6]), patterns))))
    for char in 'abcdf':
        char_values['g'] -= char_values[char]
    
    # we should now have a unique map for 'g'
    assert(len(char_values['g']) == 1)
    
    # store known map 'g'
    char_map['g'] = ''.join(char_values['g'])
    
    # find digit 5 to identify 'f' by way of elimination through 'a', 'bd', and 'g'
    target = set()
    for char in 'abdg':
        target |= char_values[char]
    
    char_values['f'] = set(next(filter(lambda pattern: target <= set(pattern), filter(lengths([5]), patterns))))
    for char in 'abdg':
        char_values['f'] -= char_values[char]
    
    # find 'c' by eliminating 'f'
    char_values['c'] -= char_values['f']
    
    # we should now have a unique map for 'c', 'f'
    assert(len(char_values['c']) == 1)
    assert(len(char_values['f']) == 1)
    
    # store known map 'c', 'f'
    char_map['c'] = ''.join(char_values['c'])
    char_map['f'] = ''.join(char_values['f'])
    
    # find digit 8 to identify 'e' by way of elimination through 'a', 'bd', 'c', 'f', 'g'
    target = set()
    for char in 'abcdfg':
        target |= char_values[char]
    
    char_values['e'] = set(next(filter(lambda pattern: target <= set(pattern), filter(lengths([7]), patterns))))
    for char in 'abcdfg':
        char_values['e'] -= char_values[char]
    
    # we should now have a unique map for 'e'
    assert(len(char_values['e']) == 1)
    
    # store known map 'e'
    char_map['e'] = ''.join(char_values['e'])
    
    # find digits 2 and 3 to identify 'b' and 'd' by way of elimination through 'a', 'c', 'g'
    target = set()
    for char in 'acg':
        target |= char_values[char]
    
    digits_23 = filter(lambda pattern: target <= set(pattern), filter(lengths([5]), patterns))
    
    digit_2 = set(next(digits_23))
    digit_3 = set(next(digits_23))
    if (char_values['e'] <= digit_3):
        digit_2, digit_3 = digit_3, digit_2
    
    for char in 'aceg':
        digit_2 -= char_values[char]
    
    for char in 'acfg':
        digit_3 -= char_values[char]
    
    # only 'd' in common now
    assert(digit_2 == digit_3)
    
    char_values['d'] &= digit_2
    char_values['b'] -= char_values['d']
    
    # we should have a unique map for 'd', 'b' now
    assert(len(char_values['d']) == 1)
    assert(len(char_values['b']) == 1)
    
    char_map['b'] = ''.join(char_values['b'])
    char_map['d'] = ''.join(char_values['d'])
    
    return char_map

def decode_entry(entry: Entry) -> List[int]:
    
    char_map = find_mapping(entry.patterns)
    char_map = {ord(v): ord(k) for k,v in char_map.items()}
    
    digits = []
    for digit in entry.digits:
        digits.append(digit_map[''.join(sorted(digit.translate(char_map)))])
    
    return digits

def part1(entries: List[Entry]) -> List[int]:
    
    decoded_entries = []
    
    for entry in entries:
        decoded_entries.append(decode_entry(entry))
    
    return decoded_entries

def main(args):
    
    entries = read_inputs(args.example)
    decoded = part1(entries)
    decoded_1478 = [v for e in decoded for v in e if v in [1, 4, 7, 8]]
    logging.info(f'Part 1: {len(decoded_1478)} unique entries in input')
    sum_digits = sum(v * 10 ** i for elem in decoded for v, i in zip(elem, [3, 2, 1, 0]))
    logging.info(f'Part 2: Sum of 7-Segment Digits {sum_digits}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
