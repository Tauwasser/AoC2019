#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import logging

from intcode import IntcodeComputer

class MultiLineFormatter(logging.Formatter):
    def format(self, record):
        str = logging.Formatter.format(self, record)
        header, footer = str.split(record.message)
        str = str.replace('\n', '\n' + ' '*len(header))
        return str

def main(input):

    with open('day5_input', 'r', encoding='utf-8') as f:
        numbers = f.readlines()
    
    program = ''.join(numbers)
    program = [int(x) for x in program.split(',')]
    
    computer = IntcodeComputer()
    
    original_program = program[:]
    
    # Part 1
    
    trace = computer.compute(program, input=(input or 1))
    print('\n'.join(str(x) for x in trace))
    
    # Part 2
    program = original_program[:]
    trace = computer.compute(program, input=(input or 5))
    print('\n'.join(str(x) for x in trace))
    
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
    parser.add_argument('--input', type=int, help='IntCode Input', default=None)

    # Parse arguments
    args = parser.parse_args()
    
    # Set User Loglevel
    logLevel = logLevelMap.get(args.loglevel.lower(), None)
    if (logLevel is None):
        logging.error('Invalid loglevel \'{0:s}\' passed. Exiting...'.format(args.loglevel))
        sys.exit(-1)
    
    l.setLevel(logLevel)
    
    sys.exit(main(args.input))
