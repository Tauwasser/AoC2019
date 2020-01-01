#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from intcode import IntcodeComputer

with open('day2_input', 'r', encoding='utf-8') as f:
    numbers = f.readlines()

program = ''.join(numbers)
program = [int(x) for x in program.split(',')]

# restore to 1202 program alarm
program[1] = 12
program[2] = 2

computer = IntcodeComputer()

original_program = program[:]

_, trace = computer.compute(program)

print('\n'.join(str(x) for x in trace))

print(f'Final program[0] value: {program[0]}')

# Brute-force solution for part 2

for noun in range(0, 100):
    for verb in range(0, 100):
        
        program = original_program[:]
        program[1] = noun
        program[2] = verb
        computer.compute(program)
        
        if (program[0] == 19690720):
            print(f'Noun: {noun} Verb: {verb} Sum: {100*noun + verb}')
