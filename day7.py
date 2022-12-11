#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import logging

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

@dataclass
class DirEntryBase:
    name:   str
    @property
    def path(self) -> str:
        path = '' if (self.parent is None) else self.parent.path
        return f'{path}/{self.name}'

@dataclass
class DirEntryOpt:
    parent: Optional['DirEntry'] = None

@dataclass
class DirEntry(DirEntryOpt, DirEntryBase):
    pass

@dataclass
class FileBase(DirEntryBase):
    size: int

@dataclass
class File(DirEntryOpt, FileBase):
    pass

@dataclass
class Directory(DirEntry):
    children: List[DirEntry] = field(default_factory=list)

    def iter(self) -> DirEntry:
        
        for child in self.children:
            
            yield child

            if (type(child) is Directory):
                yield from child.iter()
    
    @property
    def size(self):
        return sum(child.size for child in self.children)

@dataclass
class Root(Directory):

    @property
    def path(self) -> str:
        return ''

def read_inputs(example=0) -> Root:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day7_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    
    # parse logic
    cur_dir : Directory = Root('')
    directories = {'/': cur_dir}

    def _parseCdCommand(argument: str):
        nonlocal cur_dir
        
        match (argument):
            case '..':
                cur_dir = cur_dir.parent
            case '/':
                cur_dir = directories['/']
            case name:
                cur_dir = directories[cur_dir.path + '/' + name]
    
    def _parseLsCommand(line: str):
        nonlocal cur_dir

        if (line.startswith('dir')):
            directory = Directory(line[4:], cur_dir)
            directories[directory.path] = directory
            cur_dir.children.append(directory)
        else:
            size, name = line.split(' ', 1)
            size = int(size)
            cur_dir.children.append(File(name, size, cur_dir))

    inside_ls = False

    for command in data:
        
        # abort ls output
        if (command.startswith('$')):
            inside_ls = False

        if (inside_ls):
            _parseLsCommand(command)
        elif (command.startswith('$ ')):
            match (command[2:].split(' ', 1)):
                case ['cd', argument]:
                    _parseCdCommand(argument)
                case ['ls']:
                    inside_ls = True
                case _:
                    raise RuntimeError(f'Encountered unknown command \'{command[2:]}\'!')
        else:
            raise RuntimeError(f'Encountered unknown line {command}!')

    return directories['/']

def printDirectories(root: Directory, indent=0) -> str:

    result = f'{" "*indent}- {root.name or "/"} (dir)\n'
    indent += 2

    for child in root.children:
        if (type(child) is File):
            result += f'{" "*indent} - {child.name} (file, size={child.size})\n'
        else:
            result += printDirectories(child, indent=indent)
    
    return result

def part1(root: Directory):
    listing = printDirectories(root)
    logging.debug(listing)

    candidate_directories = {dir.path: dir.size for dir in root.iter() if type(dir) is Directory and dir.size <= 100000}

    return candidate_directories

def part2():
    pass

def main(args):
    
    tree = read_inputs(args.example)
    candidate_directories = part1(tree)
    logging.info(f'Part 1: Candidate Directories {", ".join(candidate_directories)} Sum {sum(candidate_directories.values())}')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
