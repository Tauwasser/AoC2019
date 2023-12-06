#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

@dataclass
class Almanac:
    seeds:               list[int]      = field(default_factory=list, repr=False)
    seed_to_soil:        dict[int, int] = field(default_factory=dict, repr=False)
    soil_to_fertilizer:  dict[int, int] = field(default_factory=dict, repr=False)
    fertilizer_to_water: dict[int, int] = field(default_factory=dict, repr=False)
    water_to_light:      dict[int, int] = field(default_factory=dict, repr=False)
    light_to_temp:       dict[int, int] = field(default_factory=dict, repr=False)
    temp_to_humid:       dict[int, int] = field(default_factory=dict, repr=False)
    humid_to_loc:        dict[int, int] = field(default_factory=dict, repr=False)

def read_inputs(example=0) -> Almanac:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day5_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    
    almanac = Almanac()
    
    idata = iter(data)
    
    fields = {
        'seed-to-soil':            almanac.seed_to_soil,
        'soil-to-fertilizer':      almanac.soil_to_fertilizer,
        'fertilizer-to-water':     almanac.fertilizer_to_water,
        'water-to-light':          almanac.water_to_light,
        'light-to-temperature':    almanac.light_to_temp,
        'temperature-to-humidity': almanac.temp_to_humid,
        'humidity-to-location':    almanac.humid_to_loc,
    }
    
    while (line := next(idata, '')):
        
        if (line.startswith('seeds: ')):
            _, seeds = line.split(': ')
            almanac.seeds = [int(seed.strip()) for seed in seeds.split(' ') if seed]
            # consume one more line
            next(idata)
            continue
        
        if (not line.endswith(' map:')):
            raise RuntimeError(f'Unexpected line \'{line}\'!')
        
        field = fields.get(line[:-5])
        
        if (field is None):
            raise RuntimeError(f'Could not map \'{line[:-5]}\'!')
        
        while (entry := next(idata, '')):
            dst, src, len = (int(v.strip()) for v in entry.split(' '))
            
            for l in range(len):
                field[src + l] = dst + l
    
    return almanac

def part1(almanac: Almanac) -> list[int]:
    """Map seeds to locations using almanac"""
    
    locations : list[int] = []
    
    for seed in almanac.seeds:
        
        # get soil
        soil = almanac.seed_to_soil.get(seed, seed)
        # get fertilizer
        fertilizer = almanac.soil_to_fertilizer.get(soil, soil)
        # get water
        water = almanac.fertilizer_to_water.get(fertilizer, fertilizer)
        # get light
        light = almanac.water_to_light.get(water, water)
        # get temperature
        temperature = almanac.light_to_temp.get(light, light)
        # get humidity
        humidity = almanac.temp_to_humid.get(temperature, temperature)
        # get location
        location = almanac.humid_to_loc.get(humidity, humidity)
        
        # catch result
        locations.append(location)
    
    return locations

def part2():
    pass

def main(args):
    
    almanac = read_inputs(args.example)
    seed_locations = part1(almanac)
    logging.info(f'Part 1: {min(seed_locations)} ({", ".join(str(loc) for loc in seed_locations)})')
    part2()
    logging.info(f'Part 2: ')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
