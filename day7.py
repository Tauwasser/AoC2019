#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import logging

from itertools import permutations
from intcode import IntcodeComputer

class MultiLineFormatter(logging.Formatter):
    def format(self, record):
        str = logging.Formatter.format(self, record)
        header, footer = str.split(record.message)
        str = str.replace('\n', '\n' + ' '*len(header))
        return str

def main():

    with open('day7_input', 'r', encoding='utf-8') as f:
        numbers = f.readlines()
    
    program = ''.join(numbers)
    program = [int(x) for x in program.split(',')]
    
    computer = IntcodeComputer()
    
    original_program = program[:]
    
    # Part 1
    
    maxThrust = 0
    maxThrustPermutation = None
    
    for permutation in permutations([0, 1, 2, 3, 4]):
        
        input = 0
        logging.info('---------')
        for phase in permutation:
    
            outputs, trace = computer.compute(program, inputs=[phase, input])
            # collect output
            input = outputs[-1]
            # restore program
            program = original_program[:]
        
        if (outputs[-1] > maxThrust):
            maxThrust = outputs[-1]
            maxThrustPermutation = permutation
    
    logging.info(f'Max Thrust {maxThrust} for permutation {maxThrustPermutation}')
    
    # Part 2
    return 0
    
if __name__=='__main__':

    logLevelMap = {
        'debug':   logging.DEBUG,
        'info':    logging.INFO,
        'warning': logging.WARNING,
        'error':   logging.ERROR,
        }
    
    # Set up Logger
    l = logging.getLogger()
    h = logging.StreamHandler()
    h.setFormatter(MultiLineFormatter(fmt='[%(asctime)s][%(levelname)-8s] %(message)s', datefmt='%d %b %Y %H:%M:%S'))
    l.addHandler(h)
    l.setLevel(logging.INFO)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Advent of Code.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--loglevel', help='Loglevel, one of \'DEBUG\', \'INFO\' (default), \'WARNING\', \'ERROR\'.', type=str, default='INFO')

    # Parse arguments
    args = parser.parse_args()
    
    # Set User Loglevel
    logLevel = logLevelMap.get(args.loglevel.lower(), None)
    if (logLevel is None):
        logging.error('Invalid loglevel \'{0:s}\' passed. Exiting...'.format(args.loglevel))
        sys.exit(-1)
    
    l.setLevel(logLevel)
    
    sys.exit(main())
