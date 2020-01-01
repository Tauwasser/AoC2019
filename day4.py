#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import logging

class MultiLineFormatter(logging.Formatter):
    def format(self, record):
        str = logging.Formatter.format(self, record)
        header, footer = str.split(record.message)
        str = str.replace('\n', '\n' + ' '*len(header))
        return str

PASSWORD_DIGITS = 6

def twoAdjacentDigitsSame(num):
    
    lastDigit = None
    
    for i in range(PASSWORD_DIGITS - 1, 0 - 1, -1):
        
        digit = (num // (10**i)) % 10
        
        if (lastDigit == digit):
            return True
        lastDigit = digit
    
    return False

def atLeastExactlyTwoAdjacentDigitsSame(num):
    
    lastDigit = None
    count = 1
    countBuckets = []
    
    fmt = f'{{num:0{PASSWORD_DIGITS}d}}!'
    str = fmt.format(num=num)
    
    for digit in str:
        
        if (lastDigit == digit):
            count += 1
        
        if (lastDigit != digit and lastDigit is not None):
            countBuckets.append(count)
            count = 1
        lastDigit = digit
    
    return 2 in countBuckets

def monotonousDigits(num):
    
    lastDigit = -1
    
    for i in range(PASSWORD_DIGITS - 1, 0 - 1, -1):
        
        digit = (num // (10**i)) % 10
        
        if (lastDigit > digit):
            return False
        lastDigit = digit
        
    return True

def main(draw=False):

    with open('day4_input', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    low, high = [int(x) for x in lines[0].split('-')]

    logging.info(f'Range: {low}--{high}')
    
    # Part 1
    
    count = 0
    for number in range(low, high + 1):
        
        if not(twoAdjacentDigitsSame(number)):
            continue
        if not(monotonousDigits(number)):
            continue
        count += 1
    
    logging.info(f'Number of passwords matching criteria Pt 1: {count}')
    
    # Part 2
    
    count = 0
    for number in range(low, high + 1):
        
        if not(twoAdjacentDigitsSame(number)):
            continue
        if not(monotonousDigits(number)):
            continue
        if not(atLeastExactlyTwoAdjacentDigitsSame(number)):
            continue
        count += 1
    
    logging.info(f'Number of passwords matching criteria Pt 2: {count}')
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
