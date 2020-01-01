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

def printOrbitMap(orbitMap):
    
    for name, entry in orbitMap.items():
        
        logEntry = f'Object {name} [{entry["checksum"]}] orbits:'
        if (entry['orbits'] is not None):
            logEntry += '\n'
            logEntry += f'    {entry["orbits"]} (d)'
        
        for orbited in entry['orbited']:
            logEntry += '\n'
            logEntry += f'    {orbited}'
        
        logging.debug(logEntry)

def main():

    with open('day6_input', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # parse Orbit Map
    
    orbitMap = {}
    for line in lines:
        
        lhs, rhs = line.strip().split(')')
        orbitMap.setdefault(rhs, {'orbits': None, 'orbited': [], 'checksum': -1, 'visited': False})['orbits'] = lhs
        orbitMap.setdefault(lhs, {'orbits': None, 'orbited': [], 'checksum': -1, 'visited': False})['orbited'].append(rhs)
    
    # compute direct, indirect orbits
    def calcChecksum(parent, node):
        
        node['checksum'] = parent['checksum'] + 1
        for orbited in node['orbited']:
            calcChecksum(node, orbitMap[orbited])
    
    calcChecksum({'checksum': -1}, orbitMap['COM'])
    
    printOrbitMap(orbitMap)
    
    # Part 1
    count = 0
    
    for name, entry in orbitMap.items():
    
        count += entry['checksum']
    
    logging.info(f'Orbit Checksum: {count}')
    
    # Part 2
    
    # find objects YOU and SAN are orbiting
    youObj = orbitMap['YOU']['orbits']
    sanObj = orbitMap['SAN']['orbits']
    
    # idea: find commonly orbited object (OBJ) and calc paths from there
    
    youPath = []
    curObj = youObj
    
    while (curObj != 'COM'):
        youPath.append(curObj)
        entry = orbitMap[curObj]
        
        entry['visited'] = True
        curObj = entry['orbits']
    
    sanPath = []
    curObj = sanObj
    
    while (curObj != 'COM'):
        
        sanPath.append(curObj)
        entry = orbitMap[curObj]
        
        if (entry['visited']):
            break
        curObj = entry['orbits']
    
    obj = sanPath[-1]
    logging.info(f'First Common Object: {obj}')
    
    # index is number of objects from youObj to obj (inclusive)
    ix = youPath.index(obj)
    
    # length of sanPath is number of objects from sanObj to obj (inclusive)
    # therefore number of orbital transfers is number of objects from youObj to obj + sanObj to obj - 1
    logging.info(f'Number of required orbital transfers: {ix+len(sanPath) - 1}')
    
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
