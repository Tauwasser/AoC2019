#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('day2_input', 'r', encoding='utf-8') as f:
    commands = f.readlines()

# initial position
x = 0
y = 0

for command in commands:
    cmd, arg = command.split(' ', 1)
    arg = int(arg)
    if (cmd == 'forward'):
        x += arg
    elif (cmd == 'down'):
        y -= arg
    elif (cmd == 'up'):
        y += arg
    else:
        raise RuntimeError(f'Illegal Command {command}.')
    if (y > 0):
        print(f'Command {command} made submarine fly.')

print(f'Part 1: destination x {x:04d} y {y:04d}')
