#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple, Union

from lib import setup

example_input = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""

error_scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

chunk_types = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

def singleton(name):
    class Singleton(object):
        def __repr__(self):
            return name
        def __str__(self):
            return name
    return Singleton()

Valid = singleton('Valid')
Incomplete = singleton('Incomplete')
Corrupted = singleton('Corrupted')

# forward-declare Chunk
class Chunk:
    pass

@dataclass
class Chunk:
    type: str
    chunks: List[Chunk] = field(default_factory=list)

@dataclass
class Line:
    raw: str
    classification: object = Valid
    error: Tuple[int, Chunk] = (-1, None)
    chunks: List[Chunk] = field(default_factory=list)

class ParsingError(Exception):
    
    def __init__(self, chunk: Chunk):
        self.chunk = chunk

class CorruptedError(ParsingError):
    
    def __init__(self, position: int, chunk: Chunk):
        super().__init__(chunk)
        self.position = position

class IncompleteError(ParsingError):
    pass

def read_inputs(example=0) -> List[str]:
    
    if (example):
        data = example_input
    else:
        with open('day10_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    # parse logic
    return data

def _parseChunks(container: Union[Line, Chunk], it: Iterable[Tuple[int, str]]):
    
    try:
        # try to parse consecutive chunks
        while(True):
            
            pos, char = next(it)
        
            if (char in chunk_types):
                # new chunk
                chunk = Chunk(char)
                container.chunks.append(chunk)
                # recurse into chunk
                _parseChunks(chunk, it)
            elif (isinstance(container, Line)):
                # encountered closing character as first character in line
                raise CorruptedError(pos, None)
            elif (char in chunk_types.values()):
                # we know isinstance(container, Chunk) is True
                if (chunk_types[container.type] != char):
                    raise CorruptedError(pos, container)
                # chunk ended regularly, go up one level
                return
            else:
                raise RuntimeError(f'Found unknown character \'{char}\' at {pos}.')
    except StopIteration:
        if (isinstance(container, Chunk)):
            raise IncompleteError(container)

def part1(navigation: List[str]) -> List[Line]:
    
    stack = []
    result = []
    
    for line in navigation:
        
        parsed_line = Line(line)
        result.append(parsed_line)
        it = enumerate(iter(line))
        
        try:
            _parseChunks(parsed_line, it)
        except IncompleteError as e:
            parsed_line.classification = Incomplete
            parsed_line.error = (-1, e.chunk)
        except CorruptedError as e:
            parsed_line.classification = Corrupted
            parsed_line.error = (e.position, e.chunk)
    
    return result
    
def part2():
    pass

def main(args):
    
    navigation = read_inputs(args.example)
    parsed = part1(navigation)
    corrupted = list(filter(lambda line: line.classification == Corrupted, parsed))
    score = sum(map(lambda line: error_scores[line.raw[line.error[0]]], corrupted))
    logging.info(f'Part 1: Error Score of {len(corrupted)} corrupted lines is {score}.')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
