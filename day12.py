#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
import sys
import logging

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from lib import setup

# 10 paths, 36 paths (small twice)
example1_input = """start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

# 19 paths, 103 paths (small twice)
example2_input = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""

# 226 paths, 3509 paths (small twice)
example3_input = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""

# forward-declare Cave
class Cave:
    pass

@dataclass
class Cave:
    name: str
    big:  bool
    caves: List[Cave] = field(default_factory=list)

def read_inputs(example=0) -> Dict[str, Cave]:
    
    if (1 == example):
        data = example1_input
    elif (2 == example):
        data = example2_input
    elif (example):
        data = example3_input
    else:
        with open('day12_input', 'r', encoding='utf-8') as f:
            data = f.read()
    
    data = data.splitlines()
    
    caves = {
        'start': Cave('start', False),
        'end': Cave('end', False),
    }
    
    # parse logic
    for line in data:
        _from, _to = line.split('-')
        
        caves[_from] = caves.get(_from, Cave(_from, _from.isupper()))
        caves[_to] = caves.get(_to, Cave(_to, _to.isupper()))
        
        # record paths
        caves[_from].caves.append(caves[_to])
        caves[_to].caves.append(caves[_from])
    
    return caves

def part1(caves: Dict[str, Cave]) -> List[List[str]]:
    
    start = caves['start']
    end = caves['end']
    
    def _explore(_from: Cave, path_so_far = None):
        
        path_so_far = [*(path_so_far or []), _from.name]
        result = []
        
        for cave in _from.caves:
            
            # skip small caves that were already visited
            if (not cave.big and cave.name in path_so_far):
                continue
            
            # break if we found the end node
            # (do not explore it)
            if (cave is end):
                result.append([*path_so_far, cave.name])
                continue
            
            next_paths = _explore(cave, path_so_far=path_so_far)
            if (next_paths):
                result += next_paths
        
        return result
    
    return _explore(start)

def part2(caves: Dict[str, Cave]) -> List[List[str]]:
    
    start = caves['start']
    end = caves['end']
    
    def _explore(_from: Cave, path_so_far = None, visit_count = None):
        
        path_so_far = [*(path_so_far or []), _from.name]
        visit_count = defaultdict(lambda: 0, visit_count or {})
        result = []
        
        for cave in _from.caves:
            
            # do not visit start twice
            if (cave is start):
                continue
            
            # break if we found the end node
            # (do not explore it)
            if (cave is end):
                result.append([*path_so_far, cave.name])
                continue
            
            # local copy of visit count when taking this branch
            branch_visit_count = visit_count.copy()
            
            # check small cave rules
            if (not cave.big):
                # skip small caves that were already visited twice
                if (visit_count.get(cave.name, 0) >= 2):
                    continue
                # skip small caves that were already visited when any small cave was visited twice
                if (visit_count.get(cave.name, 0) == 1 and any(x >= 2 for x in visit_count.values())):
                    continue
                # increment small cave visit count
                branch_visit_count[cave.name] += 1
            
            next_paths = _explore(cave, path_so_far=path_so_far, visit_count=branch_visit_count)
            if (next_paths):
                result += next_paths
        
        return result
    
    return _explore(start)

def main(args):
    
    caves = read_inputs(args.example)
    paths = part1(caves)
    logging.info(f'Part 1: There are {len(paths)} unique paths.')
    paths = part2(caves)
    logging.info(f'Part 2: There are {len(paths)} unique paths (visit small twice)')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
