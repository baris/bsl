#!/usr/bin/env python

'''BSL

This is the interprater to be called.
'''

import sys

import bsltokenizer
import bslparser

built_in = ['print']

class VMError(Exception):
    pass

class Stack:
    def __init__(self):
        self.stack = []
    def push(self, val):
        self.stack.append(val)
    def pop(self):
        return self.stack.pop()
        

try:
    f = open(sys.argv[1])
except IOError:
    raise VMError, "Can't open file %s" %(sys.argv[1])
except IndexError:
    raise VMError, "Need a BSL source file"
    
variables = {}

t = bsltokenizer.Tokenize(f)
p = bslparser.Parser(t.get_tokens())
op = p.run()
stack = Stack()

def call_function(name):
    global stack, op, variables

    #defined function
    if name in op.functions.keys():
        for code in op.functions[name]:
            c = code.split('\t')
            if c[0] == 'STORE':
                variables[c[1]] = stack.pop()
            if c[0] == 'LOAD_CONST':
                stack.push(c[1])
            if c[0] == 'LOAD':
                stack.push(variables[c[1]])
            if c[0] == 'CALL_FUNC':
                call_function(c[1])
                

    #built-in function
    elif name in built_in:
        # print function
        if name == 'print':
            print stack.pop()
    
for code in op.global_codes:
    c = code.split('\t')
    
    if c[0] == 'CALL_FUNC':
        call_function(c[1])
    if c[0] == 'LOAD_CONST':
        stack.push(c[1])
    if c[0] == 'LOAD':
        stack.push(variables[c[1]])
    if c[0] == 'STORE':
        variables[c[1]] = stack.pop()
    
        
        
#debug
#print
#print "GLOBALS:", op.global_codes
#print "FUNCTIONS:", op.functions

f.close()
