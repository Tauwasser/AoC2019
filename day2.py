#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import logging

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from lib import setup

example_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

@dataclass
class Draw:
    red:   int
    green: int
    blue:  int

@dataclass
class Game:
    id: int
    draws: List[Draw] = field(default_factory=list, repr=False)

def read_inputs(example=0) -> List[Game]:
    
    match (example):
        case _ if (example):
            data = example_input
        case _:
            with open('day2_input', 'r', encoding='utf-8') as f:
                data = f.read()
    
    data = data.splitlines()
    id_pos = len('Game ')
    games : List[Game] = []
    pattern = re.compile('(?:(\d+) (red|green|blue), )?(?:(\d+) (red|green|blue), )?(\d+) (red|green|blue)')
    
    for line in data:
        
        ix = line.find(':')
        g = Game(int(line[id_pos:ix]))
        
        draws = line[ix + 2:].split('; ')
        
        for draw in draws:
            m = pattern.match(draw)
            if (m is None):
                raise RuntimeError(f'Line {draw} does not match draw pattern!')
            kwargs = {'red': 0, 'blue': 0, 'green': 0}
            
            for num, kind in zip(*[iter(m.groups())] * 2):
                if (kind is None):
                    continue
                kwargs[kind] = int(num)
            
            g.draws.append(Draw(**kwargs))
        
        games.append(g)
    
    # parse logic
    return games

def part1(games: List[Game], *, red: int, green: int, blue: int) -> List[Game]:
    
    def _filter(game: Game):
        
        min_red   = max(draw.red for draw in game.draws)
        min_green = max(draw.green for draw in game.draws)
        min_blue  = max(draw.blue for draw in game.draws)
        
        if (min_red <= red and min_green <= green and min_blue <= blue):
            return True
        
        return False
    
    return list(filter(_filter, games))

def part2(games: List[Game]) -> List[int]:
    
    def _power(game: Game):
        
        min_red   = max(draw.red for draw in game.draws)
        min_green = max(draw.green for draw in game.draws)
        min_blue  = max(draw.blue for draw in game.draws)
        
        return min_red * min_green * min_blue
    
    return list(map(_power, games))

def main(args):
    
    games = read_inputs(args.example)
    poss_games = part1(games, red=12, green=13, blue=14)
    logging.info(f'Part 1: {sum(g.id for g in poss_games)} ({", ".join(str(g.id) for g in poss_games)})')
    powers = part2(games)
    logging.info(f'Part 2: {sum(powers)} ({", ".join(str(p) for p in powers)})')

if __name__ == '__main__':
    args = setup()
    sys.exit(main(args))
