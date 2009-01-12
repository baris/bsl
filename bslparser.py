#!/usr/bin/env python

'''BSL parser

Does the real job of parsing.
Parses the token list and returns:
(vars{}, functions[], opcodes[])
'''

from bslstatemachine import StateMachine
import bslopcoder


class Parser(StateMachine):
    def __init__(self, token_list):
        super(Parser, self).__init__()

        self.tl = token_list
        self.token_index = 0

        self.in_function = ''
        self.funcname = ''
        self.funcargs = []
        self.opcoder = bslopcoder.Opcoder()

        self.add_state(self._global, startstate=True)
        self.add_state(self._function)
        self.add_state(self._eot, endstate=True)

    def run(self):
        "run the parser"
        stuff = (self.tl, 'main')
        super(Parser, self).run(stuff)
        return self.opcoder

    def write_opcode(self, op_type, caller):

        if self.in_function:
            self.opcoder.write(self.funcname, self.funcargs,\
                          op_type, caller, self.in_function)
        else:
            self.opcoder.write(self.funcname, self.funcargs,\
                          op_type, caller)

        self.funcname = ''
        self.funcargs = []


    # -- states --
    def _global(self, stuff):
        tl, caller = stuff

        while True:
            try:
                token = tl[self.token_index]
            except IndexError:
                return self._eot, (tl, '_global')                
            self.token_index += 1
            
            # function definition
            if token == 'function':
                return self._function, (tl, '_global')

            # or function call
            if token == ';':
                self.write_opcode('function_call', '_global')
                continue
            if not self.funcname:
                self.funcname = token
                continue
            self.funcargs.append(token)
            
    def _function(self, stuff):
        tl, caller = stuff
        self.funcname = tl[self.token_index]
        self.in_function = self.funcname

        self.token_index += 1
        if tl[self.token_index] == '(':
            self.token_index += 1
            token = tl[self.token_index]
            while token <> ')':
                self.funcargs.append(token)
                self.token_index += 1
                token = tl[self.token_index]
        self.write_opcode('function_decleration', '_function')

        self.token_index += 1
        token = tl[self.token_index]
        if token == '{':
            while token <> '}':
                self.token_index += 1
                token = tl[self.token_index]
                if token == '}':
                    self.token_index += 1
                    break
                if token == ';':
                    self.write_opcode('function_call', '_function')
                    continue
                if not self.funcname:
                    self.funcname = token
                    continue
                self.funcargs.append(token)

        self.in_function = ''
        return self._global, (tl, '_function')

    def _eot(self, stuff):
        pass

if __name__ == "__main__":
    pass
