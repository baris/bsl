#!/usr/bin/env python

class Opcoder:
    "BSL opcode writer"
    def __init__(self):
        self.global_codes = []
        self.functions = {}
    
    def write(self, name, args, op_type, to, func=None):
        """C style function calling:
        put arguments in reverse order while calling a function"""
        
        if op_type == 'function_call':
            if to == '_global':
                while True:
                    try:
                        arg = args.pop()
                    except IndexError:
                        break
                    if arg.startswith('"') and arg.endswith('"'):
                        self.global_codes.append('LOAD_CONST\t%s' %(arg))
                    else:
                        self.global_codes.append('LOAD\t%s' %(arg))
                self.global_codes.append('CALL_FUNC\t%s' %(name))

            if to == '_function' and func:
                while True:
                    try:
                        arg = args.pop()
                    except IndexError:
                        break
                    if arg.startswith('"') and arg.endswith('"'):
                        self.functions[func].append('LOAD_CONST\t%s' %(arg))
                    else:
                        self.functions[func].append('LOAD\t%s' %(arg))
                self.functions[func].append('CALL_FUNC\t%s' %(name))
        
        if op_type == 'function_decleration':
            if to == '_function' and func:
                self.functions[func] = []
                if args:
                    for arg in args:
                        self.functions[func].append('STORE\t%s' %(arg))
