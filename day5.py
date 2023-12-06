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

@dataclass(eq=True, frozen=True)
class AlmanacMap:
    src: int
    dst: int
    len: int

@dataclass(eq=True, frozen=True)
class AlmanacRange:
    beg: int
    len: int

@dataclass
class Almanac:
    seeds:               list[int]        = field(default_factory=list, repr=False)
    seed_ranges:          list[AlmanacRange] = field(default_factory=list, repr=False)
    seed_to_soil:        list[AlmanacMap] = field(default_factory=list, repr=False)
    soil_to_fertilizer:  list[AlmanacMap] = field(default_factory=list, repr=False)
    fertilizer_to_water: list[AlmanacMap] = field(default_factory=list, repr=False)
    water_to_light:      list[AlmanacMap] = field(default_factory=list, repr=False)
    light_to_temp:       list[AlmanacMap] = field(default_factory=list, repr=False)
    temp_to_humid:       list[AlmanacMap] = field(default_factory=list, repr=False)
    humid_to_loc:        list[AlmanacMap] = field(default_factory=list, repr=False)

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
            # map original seeds
            almanac.seeds = [int(seed.strip()) for seed in seeds.split(' ') if seed]
            # map seed range
            for beg, len in zip(almanac.seeds[::2], almanac.seeds[1::2]):
                almanac.seed_ranges.append(AlmanacRange(beg, len))
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
            field.append(AlmanacMap(src, dst, len))
    
    return almanac

def part1(almanac: Almanac) -> list[int]:
    """Map seeds to locations using almanac"""
    
    locations : list[int] = []
    
    def _map_index(field, src_ix):
        _map = next(filter(lambda m: m.src <= src_ix < m.src + m.len, field), AlmanacMap(src_ix, src_ix, 1))
        return _map.dst + (src_ix - _map.src)
    
    for seed in almanac.seeds:
        
        # get soil
        soil = _map_index(almanac.seed_to_soil, seed)
        # get fertilizer
        fertilizer = _map_index(almanac.soil_to_fertilizer, soil)
        # get water
        water = _map_index(almanac.fertilizer_to_water, fertilizer)
        # get light
        light = _map_index(almanac.water_to_light, water)
        # get temperature
        temperature = _map_index(almanac.light_to_temp, light)
        # get humidity
        humidity = _map_index(almanac.temp_to_humid, temperature)
        # get location
        location = _map_index(almanac.humid_to_loc, humidity)
        
        # catch result
        locations.append(location)
    
    return locations

def part2(almanac: Almanac) -> list[int]:
    """Map seed ranges to locations using almanac"""
    
    locations : list[int] = []
    
    def _map_index(field, src_ix):
        _map = next(filter(lambda m: m.src <= src_ix < m.src + m.len, field), AlmanacMap(src_ix, src_ix, 1))
        return _map.dst + (src_ix - _map.src)
    
    for seed_range in almanac.seed_ranges:
        
        for seed in range(seed_range.beg, seed_range.beg + seed_range.len):
            
            # get soil
            soil = _map_index(almanac.seed_to_soil, seed)
            # get fertilizer
            fertilizer = _map_index(almanac.soil_to_fertilizer, soil)
            # get water
            water = _map_index(almanac.fertilizer_to_water, fertilizer)
            # get light
            light = _map_index(almanac.water_to_light, water)
            # get temperature
            temperature = _map_index(almanac.light_to_temp, light)
            # get humidity
            humidity = _map_index(almanac.temp_to_humid, temperature)
            # get location
            location = _map_index(almanac.humid_to_loc, humidity)
            
            # catch result
            locations.append(location)
    
    return locations

def main(args):
    
    almanac = read_inputs(args.example)
    seed_locations = part1(almanac)
    logging.info(f'Part 1: {min(seed_locations)} ({", ".join(str(loc) for loc in seed_locations)})')
    seed_locations = part2(almanac)
    logging.info(f'Part 2: {min(seed_locations)} ({", ".join(str(loc) for loc in seed_locations)})')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
