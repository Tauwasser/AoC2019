#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import re

from dataclasses import dataclass, field
from itertools import chain
from enum import StrEnum

from lib import setup

example_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


@dataclass
class Puzzle:
    height: int
    width: int
    data: list[str]


class MatchDirection(StrEnum):
    HOR_FWD       = 'HF',
    HOR_REV       = 'HR'
    VERT_DOWN     = 'VD',
    VERT_UP       = 'VU',
    DIAG_DOWN_FWD = 'DDF',
    DIAG_DOWN_REV = 'DDR',
    DIAG_UP_FWD   = 'DUF',
    DIAG_UP_REV   = 'DUR',
    HOR_VERT      = 'HV'
    DIAGONAL      = 'D'


@dataclass
class Match:
    x: int
    y: int
    kind: MatchDirection


@dataclass
class MatchParams:
    dx: int
    dy: int
    kind: MatchDirection


def read_inputs(example=0) -> Puzzle:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day4_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    return Puzzle(len(data), len(data[0]), data)

def find_matches(puzzle: Puzzle, params: MatchParams, word: str, adjust: bool=False) -> list[Match]:
    
    def _getDx():
        
        dx = 0
        while (True):
            yield dx
            dx += params.dx
    
    def _getDy():
        
        dy = 0
        while (True):
            yield dy
            dy += params.dy
    
    # chars to adjust match position by
    num_adjust = (len(word) // 2) if (adjust) else 0
    
    # prepare word as tuple of characters + None
    word = tuple(c for c in word) + (None,)
    
    # results
    results : list[Match] = []
    
    for x in range(puzzle.width):
        for y in range(puzzle.height):
            
            for c, dx, dy in zip(word, _getDx(), _getDy()):
                
                # we found a match
                if (c is None):
                    results.append(Match(x + num_adjust * params.dx, y + num_adjust * params.dy, params.kind))
                
                # make sure Y in bounds
                if not(0 <= y+dy < puzzle.height):
                    break
                
                # make sure X in bounds
                if not(0 <= x+dx < puzzle.width):
                    break
                
                # make sure word character matches
                if puzzle.data[y+dy][x+dx] != c:
                    break
    
    return results

def part1(puzzle: Puzzle, word: str='XMAS') -> tuple[Match]:
    
    # find all horizontal forward matches
    hf_matches = find_matches(puzzle, MatchParams(+1,  0, MatchDirection.HOR_FWD), word)
    # find all horizontal reverse matches
    hr_matches = find_matches(puzzle, MatchParams(-1,  0, MatchDirection.HOR_REV), word)
    # find all vertical down matches
    vd_matches = find_matches(puzzle, MatchParams( 0, +1, MatchDirection.VERT_DOWN), word)
    # find all vertical up matches
    vu_matches = find_matches(puzzle, MatchParams( 0, -1, MatchDirection.VERT_UP), word)
    # find all diagonal down forward matches
    ddf_matches = find_matches(puzzle, MatchParams(+1, +1, MatchDirection.DIAG_DOWN_FWD), word)
    # find all diagonal down reverse matches
    ddr_matches = find_matches(puzzle, MatchParams(-1, -1, MatchDirection.DIAG_DOWN_REV), word)
    # find all diagonal up forward matches
    duf_matches = find_matches(puzzle, MatchParams(+1, -1, MatchDirection.DIAG_UP_FWD), word)
    # find all diagonal up reverse matches
    dur_matches = find_matches(puzzle, MatchParams(-1, +1, MatchDirection.DIAG_UP_REV), word)
    
    # join all matches
    return (*hf_matches, *hr_matches, *vd_matches, *vu_matches, *ddf_matches, *ddr_matches, *duf_matches, *dur_matches)

def part2(puzzle: Puzzle, word: str='MAS') -> tuple[Match]:
    
     # find all horizontal forward matches
    hf_matches = find_matches(puzzle, MatchParams(+1,  0, MatchDirection.HOR_FWD), word, adjust=True)
    # find all horizontal reverse matches
    hr_matches = find_matches(puzzle, MatchParams(-1,  0, MatchDirection.HOR_REV), word, adjust=True)
    # find all vertical down matches
    vd_matches = find_matches(puzzle, MatchParams( 0, +1, MatchDirection.VERT_DOWN), word, adjust=True)
    # find all vertical up matches
    vu_matches = find_matches(puzzle, MatchParams( 0, -1, MatchDirection.VERT_UP), word, adjust=True)
    
    # keep only horizontal matches whose positions match vertical matches
    h_matches = (*hf_matches, *hr_matches)
    v_matches = (*vd_matches, *vu_matches)
    
    hv_matches = tuple(Match(h.x, h.y, MatchDirection.HOR_VERT) for h in h_matches if any(h.x == v.x and h.y == v.y for v in v_matches))
    # apparently only diagonal matches count
    hv_matches = ()
    
    # find all diagonal down forward matches
    ddf_matches = find_matches(puzzle, MatchParams(+1, +1, MatchDirection.DIAG_DOWN_FWD), word, adjust=True)
    # find all diagonal down reverse matches
    ddr_matches = find_matches(puzzle, MatchParams(-1, -1, MatchDirection.DIAG_DOWN_REV), word, adjust=True)
    # find all diagonal up forward matches
    duf_matches = find_matches(puzzle, MatchParams(+1, -1, MatchDirection.DIAG_UP_FWD), word, adjust=True)
    # find all diagonal up reverse matches
    dur_matches = find_matches(puzzle, MatchParams(-1, +1, MatchDirection.DIAG_UP_REV), word, adjust=True)
    
    # keep only diagonal down matches whose positions match diagonal up matches
    dd_matches = (*ddf_matches, *ddr_matches)
    du_matches = (*duf_matches, *dur_matches)
    
    d_matches = tuple(Match(dd.x, dd.y, MatchDirection.DIAGONAL) for dd in dd_matches if any(dd.x == du.x and dd.y == du.y for du in du_matches))
    return (*hv_matches, *d_matches)

def main(args):
    
    puzzle = read_inputs(args.example)
    matches = part1(puzzle)
    logging.info(f'Part 1: {len(matches)}')
    matches = part2(puzzle)
    logging.info(f'Part 2: {len(matches)}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
