#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('day1_input', 'r', encoding='utf-8') as f:
    depths = [int(i) for i in f.readlines()]

deltas = map(lambda cur, next: 1 if (next > cur) else 0, depths, depths[1:])
increments = sum(deltas)

print(f'Part 1: depth increases: {increments}')
