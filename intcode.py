#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class IntcodeComputer:
    
    class Instruction:
    
        def __init__(self, position, opcode, instruction, operation):
            self._position = position
            self._opcode = opcode
            self._instruction = instruction
            self._operation = operation
        
        def __str__(self):
            return f'{self._opcode:02d}@{self._position:03d}: {self._instruction:<8s}{": " if self._operation else ""}{self._operation}'
    
    class ArgReference:
        
        def __init__(self, position, value):
            self.position = position
            self.value = value
        
        def __str__(self):
            return f'{self.value}@{self.position}'
    
    def getValueByReference(self, pos):
        
        if (pos >= self._size):
            raise RuntimeError(f'Instruction at {self._position} tried to access value at {pos}.')
        if (self._program[pos] >= self._size):
            raise RuntimeError(f'Instruction at {self._position} references value at {self._program[pos]}.')
        return self._program[pos], self._program[self._program[pos]]
    
    def getParameters(self, pos, num):
        args = []
        for i in range(pos, pos + num):
            args.append(IntcodeComputer.ArgReference(*self.getValueByReference(i)))
        
        return args
    
    def compute(self, program, pos=0):
        
        instructions = []
        
        self._program = program
        self._position = pos
        self._size = len(program)
        
        position = self._position
        Instruction = IntcodeComputer.Instruction
        
        opcodeMap = {
             1: {'name': 'add', 'args': 3, 'fun': self._add},
             2: {'name': 'multiply', 'args': 3, 'fun': self._multiply},
            99: {'name': 'halt', 'args': 0, 'fun': None},
            }
        
        while (position < self._size):
        
            opcode = opcodeMap.get(program[position], None)
            
            if (opcode is None):
                raise RuntimeError(f'Program reached invalid opcode {program[position]} at position {position}.\n{chr(10).join(str(x) for x in instructions)}')
            
            arg = self.getParameters(position + 1, opcode['args'])
            f = opcode['fun'] or self._nop
            instructions.append(Instruction(position, program[position], opcode['name'], f(arg)))
            position += 1 + opcode['args']
            
            if (opcode['fun'] is None):
                break
        
        return instructions
    
    def _nop(self, arg):
        return ''
    
    def _add(self, arg):
        
        result = arg[0].value + arg[1].value
        self._program[arg[2].position] = result
        return f'{arg[0]} + {arg[1]} = {result} -> {arg[2]}'
    
    def _multiply(self, arg):
        
        result = arg[0].value * arg[1].value
        self._program[arg[2].position] = result
        return f'{arg[0]} * {arg[1]} = {result} -> {arg[2]}'
