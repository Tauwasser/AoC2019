#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from copy import deepcopy
from dataclasses import dataclass, field
from math import prod
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

@dataclass
class Test:
    divisible: int
    true: Optional[int] = None
    false: Optional[int] = None
    
    def execute(self, worry: int) -> int:
        
        if (0 == worry % self.divisible):
            return self.true
        else:
            return self.false

@dataclass
class Item:
    worry: int

@dataclass
class Operation:
    operator: str
    value: Optional[int]
    
    def execute(self, worry: int) -> int:
        match (self.operator):
            case '+':
                return worry + self.value
            case '-':
                return worry - self.value
            case '*':
                return worry * self.value
            case '/':
                return worry / self.value
            case 'q':
                return worry * worry

@dataclass
class Monkey:
    ix: int
    items: List[Item] = field(default_factory=list)
    operation: Optional[Operation] = None
    test: Optional[Test] = None

def read_inputs(example=0) -> List[Monkey]:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day11_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    
    # parse logic
    monkeys = []
    monkey = None
    for line in data:
        
        line = line.strip()
        
        if (line.startswith('Monkey')):
            monkey = Monkey(int(line[7:line.index(':')]))
            monkeys.append(monkey)
        elif (line.startswith('Starting items:')):
            monkey.items = [Item(int(worry.strip())) for worry in line[16:].split(',')]
        elif (line.startswith('Operation:')):
            if (line[23:] == 'old'):
                monkey.operation = Operation('q', None)
            else:
                monkey.operation = Operation(line[21], int(line[23:]))
        elif (line.startswith('Test:')):
            monkey.test = Test(int(line[19:]))
        elif (line.startswith('If true:')):
            monkey.test.true = int(line[25:])
        elif (line.startswith('If false:')):
            monkey.test.false = int(line[26:])
    
    return monkeys

def simulate(monkeys: List[Monkey], relief=3, rounds=20) -> int:
    
    activity : Dict[int, int] = {i: 0 for i in range(len(monkeys))}
    big_divisor = prod(monkey.test.divisible for monkey in monkeys)
    
    # <rounds> rounds total
    for round in range(rounds):
        
        # each monkey gets a turn
        for monkey in monkeys:
            
            for item in monkey.items[:]:
                # monkey inspects item
                item.worry = monkey.operation.execute(item.worry)
                # monkey lets go of item
                item.worry //= relief
                # cound activity
                activity[monkey.ix] += 1
                # perform test
                recipient = monkey.test.execute(item.worry)
                # adapt value to keep worry down
                item.worry %= big_divisor
                # throw item
                monkeys[recipient].items.append(item)
                monkey.items.remove(item)
        
        #logging.info(f'Round {round}')
        #for monkey in monkeys:
        #    logging.info(f'Monkey {monkey.ix}: {", ".join(str(item.worry) for item in monkey.items)}')
    
    for ix, value in activity.items():
        logging.info(f'Monkey {ix} inspected items {value} times.')
    
    monkeys_by_activity = list(sorted(activity.items(), key=lambda ix_activity: ix_activity[1]))
    return monkeys_by_activity[-2:]

def part1(monkeys: List[Monkey]) -> int:
    return simulate(monkeys, relief=3, rounds=20)

def part2(monkeys: List[Monkey]) -> int:
    return simulate(monkeys, relief=1, rounds=10000)

def main(args):
    
    monkeys = read_inputs(args.example)
    monkey_business = part1(deepcopy(monkeys))
    logging.info(f'Part 1: level of monkey business is {monkey_business[0][1] * monkey_business[1][1]} (monkeys {monkey_business[0][0]}, {monkey_business[1][0]})')
    monkey_business = part2(deepcopy(monkeys))
    logging.info(f'Part 2: level of monkey business is {monkey_business[0][1] * monkey_business[1][1]} (monkeys {monkey_business[0][0]}, {monkey_business[1][0]})')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
