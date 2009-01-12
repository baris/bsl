#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SMError(Exception):
    '''StateMachine error handler'''
    pass

class StateMachine(object):
    '''An abstract state machine implementation,
    which will be used for file parsers'''
    
    __slots__ = "states", "startstate", "endstates"

    def __init__(self):
        self.states = []
        self.startstate = None
        self.endstates = []

    def add_state(self, new_state, startstate=False, endstate=False):
        if new_state in self.states:
            raise SMError, "State is allready in the states table"

        if startstate:
            if not self.startstate:
                self.startstate = new_state
            else:
                raise SMError,\
                      "We have a start state and don't have room for another one!"
        if endstate:
            self.endstates.append(new_state)

        #a new commer (state) is welcomed...
        self.states.append(new_state)


    def run(self, stuff):
        state = self.startstate

        #endless loop for our machine
        while True:
            (nextstate, stuff) = state(stuff)

            #if the state being processed is an endstate
            #just make it work and brake the loop
            if nextstate in self.endstates:
                nextstate(stuff)
                break
            elif nextstate not in self.states:
                raise SMError, "Request for an unknown state"
            else:
                state = nextstate


if __name__ == "__main__":
    import sys
    sys.stderr.write("Not a callable")


