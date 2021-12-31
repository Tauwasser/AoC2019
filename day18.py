#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import logging

from copy import deepcopy
from typing import Dict, List, Optional, Tuple, Union

from lib import setup

# [[[[1,1],[2,2]],[3,3]],[4,4]]
example1_input = """[1,1]
[2,2]
[3,3]
[4,4]
"""

# [[[[3,0],[5,3]],[4,4]],[5,5]] <-- explosion
example2_input = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
"""

# [[[[5,0],[7,4]],[5,5]],[6,6]] <-- explosion
example3_input = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
"""

# [[[[0,7],4],[[7,8],[6,0]]],[8,1]] <-- explode and split
example4_input = """[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]
"""

# [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
example5_input = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
"""

# [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
example6_input = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""

class SnailfishNumber:
    
    def __init__(self, lhs: Union[int, 'SnailfishNumber'], rhs: Union[int, 'SnailfishNumber']):
        self.lhs = lhs
        self.rhs = rhs
    
    def __str__(self):
        return f'[{self.lhs!s},{self.rhs!s}]'
    
    def __repr__(self):
        return f'<SnailfishNumber |{int(self)}| at 0x{id(self):016X}>'
    
    def __eq__(self, other: 'SnailfishNumber'):
        if not isinstance(other, SnailfishNumber):
            return NotImplemented
        # two snailfish numbers
        return self.lhs == other.lhs and self.rhs == other.rhs
    
    # implement explicit int() operator to calculate magnitude
    def __int__(self):
        return 3 * int(self.lhs) + 2 * int(self.rhs)
    
    def __add__(self, other: 'SnailfishNumber'):
        if not isinstance(other, SnailfishNumber):
            return NotImplemented
        
        return SnailfishNumber(deepcopy(self), deepcopy(other)).reduce()
    
    def reduce(self) -> 'SnailfishNumber':
        
        logging.debug(f'Reduce {self!s}')
        while (True):
            # 1st action: explode
            explode, _, lhs, rhs = self.explode()
            if (explode):
                logging.debug(f'Explode {self!s}')
                continue
            # 2nd action: split
            split = self.split()
            if (split):
                logging.debug(f'Split {self!s}')
                continue
            # reduction stopped
            break
            
        return self
    
    def explode(self, level=0) -> Tuple[bool, bool, Optional[int], Optional[int]]:
        
        if (4 == level):
            assert(isinstance(self.lhs, int))
            assert(isinstance(self.rhs, int))
            # explode this Snailfish Number
            return True, True, self.lhs, self.rhs
        
        explode = False
        lhs, rhs = None, None
        
        if (isinstance(self.lhs, SnailfishNumber)):
            explode, remove, lhs, rhs = self.lhs.explode(level=level + 1)
            # pair exploded
            if (remove): self.lhs = 0
            if (rhs is not None): rhs = rhs | self
        
        if (explode):
            return explode, False, lhs, rhs
        
        if (isinstance(self.rhs, SnailfishNumber)):
            explode, remove, lhs, rhs = self.rhs.explode(level=level + 1)
            # pair exploded
            if (remove): self.rhs = 0
            if (lhs is not None): lhs = self | lhs
        
        return explode, False, lhs, rhs
    
    def split(self) -> bool:
        
        if (isinstance(self.lhs, int)):
            if (self.lhs >= 10):
                self.lhs = SnailfishNumber(self.lhs // 2, (self.lhs + 1) // 2)
                return True
        elif (self.lhs.split()):
            # we tried (and succeeded) to split lhs
            return True
        
        if (isinstance(self.rhs, int)):
            if (self.rhs >= 10):
                self.rhs = SnailfishNumber(self.rhs // 2, (self.rhs + 1) // 2)
                return True
        elif (self.rhs.split()):
            # we tried (and succeeded) to split rhs
            return True
        
        return False
    
    # Abuse XOR operation to apply explosion result from outside
    def __xor__(self, other: int) -> Optional[int]:
        if not isinstance(other, int):
            return NotImplemented
        
        if (isinstance(self.rhs, int)):
            self.rhs += other
            return None
        return self.rhs ^ other
    
    def __rxor__(self, other: int) -> Optional[int]:
        if not isinstance(other, int):
            return NotImplemented
        
        if (isinstance(self.lhs, int)):
            self.lhs += other
            return None
        
        return other ^ self.lhs
    
    # Abuse OR operation to apply explosion result from inside
    def __or__(self, other: int) -> Optional[int]:
        if not isinstance(other, int):
            return NotImplemented
        
        if (isinstance(self.lhs, int)):
            self.lhs += other
            return None
        
        return self.lhs ^ other
    
    def __ror__(self, other: int) -> Optional[int]:
        if not isinstance(other, int):
            return NotImplemented
        
        if (isinstance(self.rhs, int)):
            self.rhs += other
            return None
        return other ^ self.rhs
    
def read_inputs(example=0) -> List[SnailfishNumber]:
    
    if (1 == example):
        data = example1_input
    elif (2 == example):
        data = example2_input
    elif (3 == example):
        data = example3_input
    elif (4 == example):
        data = example4_input
    elif (5 == example):
        data = example5_input
    elif (example):
        data = example6_input
    else:
        with open('day18_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    def _parseSnailfish(l: List):
        if (len(l) > 2):
            logging.error(f'List {l} has more than two elements.')
        
        lhs = l[0]
        rhs = l[1]
        if (isinstance(lhs, list)):
            lhs = _parseSnailfish(lhs)
        if (isinstance(rhs, list)):
            rhs = _parseSnailfish(rhs)
        
        return SnailfishNumber(lhs, rhs)
    
    # parse logic
    data = data.splitlines()
    numbers = []
    
    # use json to avoid using eval to parse string :)
    for line in data:
        numbers.append(_parseSnailfish(json.loads(line)))
    
    return numbers

def part1(numbers: List[SnailfishNumber]) -> SnailfishNumber:
    
    result = numbers[0]
    
    for number in numbers[1:]:
        result += number
    
    return result

def part2(numbers: List[SnailfishNumber]) -> SnailfishNumber:
    
    # |[0,0]| = 0
    largest_number = SnailfishNumber(0, 0)
    
    for ix, lhs in enumerate(numbers):
        for rhs in numbers[ix+1:]:
            # try lhs + rhs fist
            result = lhs + rhs
            if (int(result) > int(largest_number)):
                largest_number = result
            # try rhs + lhs next
            result = rhs + lhs
            if (int(result) > int(largest_number)):
                largest_number = result
    
    return largest_number

def main(args):
    
    numbers = read_inputs(args.example)
    result = part1(numbers)
    logging.info(f'Part 1: Result of adding {len(numbers)} Snailfish Numbers: {result!r}.\n{result!s}')
    result = part2(numbers)
    logging.info(f'Part 2: Largest Snailfish Number by Magnitude: {result!r}.\n{result!s}')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
