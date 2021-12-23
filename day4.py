#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import sys
import logging
import math

from typing import List, Optional, Tuple

from lib import setup

example_input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

BOARD_DIM = 5

# square board
class Board:
    
    def __init__(self, data: List[List[int]], dimension: int = BOARD_DIM):
        self._dim = dimension
        self._data: List[List[Optional[int]]] = data
    
    def __repr__(self):
        return f'<Board at 0x{id(self):016X}>'
    
    def row(self, y: int):
        return self._data[y]
    
    def col(self, x: int):
        return [self._data[y][x] for y in range(self._dim)]
    
    def mark(self, value):
        
        for y in range(self._dim):
            for x in range(self._dim):
                if (self._data[y][x] == value):
                    self._data[y][x] = None
    
    def won(self):
        
        for x in range(self._dim):
            if all(v is None for v in self.row(x)):
                return True
        
        for y in range(self._dim):
            if all(v is None for v in self.col(y)):
                return True
        
        return False
    
    def score(self):
        return sum(sum(map(lambda row: [v or 0 for v in row], self._data), start=[]))

def read_inputs(example=False) -> Tuple[List[int], List[Board]]:
    
    if (example):
        data = example_input
    else:
        with open('day4_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    # parse first line as list of numbers drawn
    numbers = [int(v, 10) for v in data[0].split(',')]
    
    # next line needs to be empty
    if (data[1] != ''):
        raise RuntimeError('Wrong input')
    
    boards = []
    it = iter(data[2:] + [''])
    
    # i blatanty stole this from https://stackoverflow.com/a/4628446
    for lines in zip(*[it]*(BOARD_DIM+1)):
        board = []
        for line in lines[:-1]:
            board.append([int(v, 10) for v in line.split()])
        # next line must be empty
        if (lines[-1] != ''):
            raise RuntimeError('Wrong input')
        
        boards.append(Board(board))
    
    return (numbers, boards)

def part1(numbers, boards) -> Tuple[int, int]:
    
    # draw a number
    for number in numbers:
        
        # mark number on all boards
        # and check if any board won
        for ix, board in enumerate(boards, 1):
            board.mark(number)
            if (board.won()):
                return board.score() * number, ix
    
    return 0, -1

def part2(numbers, boards):
    pass
    
def main(args):
    
    numbers, boards = read_inputs(args.example)
    final_score, board_ix = part1(numbers[::], copy.deepcopy(boards))
    logging.info(f'Part 1: Final Score {final_score} with board {board_ix}.')
    part2(numbers[::], copy.deepcopy(boards))

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
