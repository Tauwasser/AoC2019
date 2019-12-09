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
        
        while (position < self._size):
            if (program[position] == 1):
                # add
                arg = self.getParameters(position + 1, 3)
                
                result = arg[0].value + arg[1].value
                operation = f'{arg[0]} + {arg[1]} = {result} -> {arg[2]}'
                instructions.append(Instruction(position, program[position], 'add', operation))
                program[arg[2].position] = result
                position += 4
                
            elif (program[position] == 2):
                # multiply
                arg = self.getParameters(position + 1, 3)
                
                result = arg[0].value * arg[1].value
                operation = f'{arg[0]} * {arg[1]} = {result} -> {arg[2]}'
                instructions.append(Instruction(position, program[position], 'multiply', operation))
                program[arg[2].position] = result
                position += 4
                
            elif (program[position] == 99):
                instructions.append(Instruction(position, program[position], 'return', ''))
                position += 1
                break
            else:
                raise RuntimeError(f'Program reached invalid opcode {program[position]} at position {position}.\n{chr(10).join(str(x) for x in instructions)}')
        
        return instructions
