#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def reqFuel(i):
    return max((i // 3) - 2, 0)

def reqFuelAdjusted(i):
    fuel_sum = 0
    additional_fuel = reqFuel(i)
    while (additional_fuel != 0):
        fuel_sum += additional_fuel
        additional_fuel = reqFuel(additional_fuel)
    return fuel_sum

with open('day1_input', 'r', encoding='utf-8') as f:
    numbers = f.readlines()

numbers = [int(i) for i in numbers]

fuel = [reqFuel(i) for i in numbers]

fuel_sum = sum(fuel)

print('-'*72)
print('Bullshit test:')
print(' Input    Output')

for i, o in zip(numbers[:2] + ['...'] + numbers[-2:], fuel[:2] + ['...'] + fuel[-2:]):
    print(f'{i:>6}    {o:>6}')

print(f'Fuel Sum: {fuel_sum}')

fuel_adjusted = [reqFuelAdjusted(i) for i in numbers]

fuel_sum = sum(fuel_adjusted)

print(f'Fuel Adjusted: {fuel_sum}')