#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass, field

from lib import setup

example_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


@dataclass
class Report:
    levels: list[int] = field(default_factory=list)
    
    def is_safe_pt1(self) -> bool:
        """Check whether Report is safe according to rules of Part 1"""
        
        deltas = list(map(lambda p, n: n - p, self.levels[:-1], self.levels[1:]))
        
        inc_dec = all(d > 0 for d in deltas) or all(d < 0 for d in deltas)
        if (not inc_dec):
            return False
        
        if (not all(1 <= abs(d) <= 3 for d in deltas)):
            return False
        
        return True
    
    def is_safe_pt2(self) -> bool:
        """Check whether Report is safe according to rules of Part 2"""
        
        # don't check anything if report is already safe
        if (self.is_safe_pt1()):
            return True
        
        # just brute-force by leaving individual numbers out
        for i in range(len(self.levels)):
            if (Report(self.levels[:i] + self.levels[i+1:]).is_safe_pt1()):
                return True
        
        return False


def read_inputs(example=0) -> list[Report]:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day2_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    
    # parse logic
    result : list[Report] = []
    for line in data:
        result.append(Report(list(int(level.strip()) for level in line.split(' '))))
    
    return result

def part1(reports: list[Report]) -> list[int]:
    """Check if Reports indicate safe Levels
    
    Returns
        List of Report indices that are safe.
    """
    return list(ix for ix, report in enumerate(reports, 1) if report.is_safe_pt1())

def part2(reports: list[Report]) -> list[int]:
    """Check if Reports indicate safe Levels with problem dampener
    
    Returns
        List of Report indices that are safe.
    """
    return list(ix for ix, report in enumerate(reports, 1) if report.is_safe_pt2())

def main(args):
    
    reports = read_inputs(args.example)
    safe_report_ixs = part1(reports)
    logging.info(f'Part 1: {len(safe_report_ixs)} ({", ".join(str(ix) for ix in safe_report_ixs[:10])})')
    safe_report_ixs = part2(reports)
    logging.info(f'Part 2: {len(safe_report_ixs)} ({", ".join(str(ix) for ix in safe_report_ixs[:10])})')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
