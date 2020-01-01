#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

class IntcodeComputer:
    
    class Instruction:
    
        def __init__(self, position, opcode, mode, instruction, operation):
            self._position = position
            self._opcode = opcode
            self._mode = mode
            self._instruction = instruction
            self._operation = operation
        
        def __str__(self):
            return f'{self._mode:04d} {self._opcode:02d}@{self._position:03d}: {self._instruction:<8s}{": " if self._operation else ""}{self._operation}'
    
    class ArgReference:
        
        def __init__(self, position, value):
            self.position = position
            self.value = value
        
        def __str__(self):
            return f'{self.value}@{self.position}'
    
    class ArgImmediate:
        
        def __init__(self, value):
            self.value = value
        
        def __str__(self):
            return f'#{self.value}'
    
    def getValueByReference(self, pos):
        
        if (pos >= self._size):
            raise RuntimeError(f'Instruction at {self._position} tried to access value at {pos}.')
        if (self._program[pos] >= self._size):
            raise RuntimeError(f'Instruction at {self._position} references value at {self._program[pos]}.')
        return self._program[pos], self._program[self._program[pos]]
    
    def getValue(self, pos):
        
        if (pos >= self._size):
            raise RuntimeError(f'Instruction at {self._position} tried to access value at {pos}.')
        return self._program[pos]
    
    def getParameters(self, pos, mode, num):
        args = []
        for i in range(pos, pos + num):
            # parameter mode
            if (mode & 1):
                args.append(IntcodeComputer.ArgImmediate(self.getValue(i)))
            else:
                args.append(IntcodeComputer.ArgReference(*self.getValueByReference(i)))
            mode //= 10
        
        return args
    
    def compute(self, program, pos=0, input=0):
        
        instructions = []
        
        self._program = program
        self._position = pos
        self._size = len(program)
        self._input = input
        
        Instruction = IntcodeComputer.Instruction
        
        opcodeMap = {
             1: {'name': 'add', 'args': 3, 'fun': self._add},
             2: {'name': 'multiply', 'args': 3, 'fun': self._multiply},
             3: {'name': 'store', 'args': 1, 'fun': self._storeInput},
             4: {'name': 'output', 'args': 1, 'fun': self._printValue},
             5: {'name': 'btru', 'args': 2, 'fun': self._branchTrue, 'branch': True},
             6: {'name': 'bfal', 'args': 2, 'fun': self._branchFalse, 'branch': True},
             7: {'name': 'lt', 'args': 3, 'fun': self._lessThan},
             8: {'name': 'eq', 'args': 3, 'fun': self._equals},
            99: {'name': 'halt', 'args': 0, 'fun': None},
            }
        
        while (self._position < self._size):
            
            position = self._position
            code = program[position] % 100
            mode = program[position] // 100
            opcode = opcodeMap.get(code, None)
            
            if (opcode is None):
                raise RuntimeError(f'Program reached invalid opcode {program[position]} at position {position}.\n{chr(10).join(str(x) for x in instructions)}')
            
            arg = self.getParameters(position + 1, mode, opcode['args'])
            f = opcode['fun'] or self._nop
            branch, trace = f(arg)
            logging.debug(Instruction(position, code, mode, opcode['name'], trace))
            instructions.append(Instruction(position, code, mode, opcode['name'], trace))
            if (not branch):
                self._position += 1 + opcode['args']
            
            if (opcode['fun'] is None):
                break
        
        return instructions
    
    def _nop(self, arg):
        return False, ''
    
    def _add(self, arg):
        
        result = arg[0].value + arg[1].value
        self._program[arg[2].position] = result
        return False, f'{arg[0]} + {arg[1]} = {result} -> {arg[2]}'
    
    def _multiply(self, arg):
        
        result = arg[0].value * arg[1].value
        self._program[arg[2].position] = result
        return False, f'{arg[0]} * {arg[1]} = {result} -> {arg[2]}'
    
    def _storeInput(self, arg):
        
        self._program[arg[0].position] = self._input
        return False, f'!{self._input} -> {arg[0]}'
    
    def _printValue(self, arg):
        
        logging.info(f'Print: {arg[0].value}')
        return False, f'{arg[0]}'
    
    def _branchTrue(self, arg):
        
        trace = f'{arg[0]} != 0 --> {arg[1]}'
        
        if (arg[0].value != 0):
            self._position = arg[1].value
            return True, trace
        
        return False, trace
    
    def _branchFalse(self, arg):
    
        trace = f'{arg[0]} == 0 --> {arg[1]}'
        
        if (arg[0].value == 0):
            self._position = arg[1].value
            return True, trace
        
        return False, trace
    
    def _lessThan(self, arg):
        
        result = 1 if arg[0].value < arg[1].value else 0
        self._program[arg[2].position] = result
        return False, f'{arg[0]} < {arg[1]} = {result} -> {arg[2]}'
    
    def _equals(self, arg):
        
        result = 1 if arg[0].value == arg[1].value else 0
        self._program[arg[2].position] = result
        return False, f'{arg[0]} == {arg[1]} = {result} -> {arg[2]}'
