#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('day1_input', 'r', encoding='utf-8') as f:
    depths = [int(i) for i in f.readlines()]

deltas = map(lambda cur, next: 1 if (next > cur) else 0, depths, depths[1:])
increments = sum(deltas)

print(f'Part 1: depth increases: {increments}')

windows = list(map(lambda a, b, c: a + b + c, depths[::], depths[1::], depths[2::]))
window_deltas = map(lambda cur, next: 1 if (next > cur) else 0, windows, windows[1:])
window_increments = sum(window_deltas)

print(f'Part 2: depth increases: {window_increments}')
