#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

@dataclass
class Paper:
    width: int
    height: int
    data: List[str]
    
    def __str__(self):
        return '\n'.join(self.data)

class Fold(ABC):
    
    @abstractmethod
    def perform(self, paper: Paper) -> Paper:
        pass

class HorizontalFold(Fold):
    
    def __init__(self, x):
        self.x = x
    
    def perform(self, paper: Paper) -> Paper:
        
        width = max(self.x, paper.width - self.x - 1)
        height = paper.height
        offset = width - self.x
        data = [[paper.data[y][x] for x in range(width)] for y in range(height)]
        
        for y in range(height):
            for x in range(self.x + 1, paper.width - offset):
                # right_x := self.x - (x - self.x) => 2*self.x - x
                left_x = 2 * self.x - x
                data[y][left_x] = '#' if (paper.data[y][left_x] == '#' or paper.data[y][x] == '#') else '.'
        
        # copy right half that protrudes over left side of paper
        # and convert overlapped left half to string
        data = [row_r[:paper.width - offset:-1] + ''.join(row_l) for row_l, row_r in zip(data, paper.data)]
        
        return Paper(width, height, data)

class VerticalFold(Fold):
    
    def __init__(self, y):
        self.y = y
    
    def perform(self, paper: Paper) -> Paper:
        
        width = paper.width
        height = max(self.y, paper.height - self.y - 1)
        offset = height - self.y
        data = [[paper.data[y][x] for x in range(width)] for y in range(height)]
        
        for y in range(self.y + 1, paper.height - offset):
            for x in range(width):
                # top_y := self.y - (y - self.y) => 2*self.y - y
                top_y = 2 * self.y - y
                data[top_y][x] = '#' if (paper.data[top_y][x] == '#' or paper.data[y][x] == '#') else '.'
        
        # copy top half that protrudes over top of paper
        # and convert overlapped bottom half to string
        data = list(reversed(paper.data[paper.height - offset:])) + [''.join(row) for row in data]
        
        return Paper(width, height, data)

def read_inputs(example=0) -> Tuple[Paper, List[Fold]]:
    
    if (example):
        data = example_input
    else:
        with open('day13_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    dots = []
    folds = []
    it = iter(data)
    
    # parse dots
    while (True):
        line = next(it)
        # found separator between dots and instructions
        if (line == ''):
            break
        x, y = [int(i, 10) for i in line.split(',')]
        dots.append((x, y))
    
    # parse instructions
    instr = 'fold along '
    try:
        while (True):
            line = next(it)
            # found end of fold instructions
            if (line == ''):
                break
            
            if not(line.startswith(instr)):
                raise RuntimeError(f'Unsupported fold instruction {line}.')
            
            axis, pos = line[len(instr):].split('=')
            pos = int(pos, 10)
            
            if (axis == 'x'):
                folds.append(HorizontalFold(pos))
            elif (axis == 'y'):
                folds.append(VerticalFold(pos))
            else:
                raise RuntimeError(f'Unsupported fold axis {axis}.')
            
    except StopIteration:
        pass
    
    # create Paper
    width = max(map(lambda xy: xy[0], dots)) + 1
    height = max(map(lambda xy: xy[1], dots)) + 1
    data = [['.'] * width for _ in range(height)]
    
    for x, y in dots:
        data[y][x] = '#'
    
    data = [''.join(row) for row in data]
    
    return Paper(width, height, data), folds

def part1(paper: Paper, fold: Fold) -> Paper:
    return fold.perform(paper)

def part2(paper: Paper, folds: List[Fold]) -> Paper:
    for fold in folds:
        paper = fold.perform(paper)
    return paper

def main(args):
    
    isEnabledForDebug = logging.getLogger().isEnabledFor(logging.DEBUG)
    
    paper, folds = read_inputs(args.example)
    logging.debug(f'Initial Paper:\n{paper}')
    
    ##### Part 1 #####
    paper_pt1 = part1(paper, folds[0])
    num_dots = ''.join(paper_pt1.data).count('#')
    logging.info(f'Part 1: There are {num_dots} dots on the paper.')
    # print to file
    if (isEnabledForDebug):
        with open(f'day13_pt1', 'w', encoding='utf-8') as f:
            f.write('\n'.join(paper_pt1.data))
    
    ##### Part 2 #####
    paper_pt2 = part2(paper, folds)
    logging.info(f'Part 2:\n{paper_pt2}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
