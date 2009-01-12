#!/usr/bin/env python

'''Tokenizer for BSL

BSL tokenizer gets an input stream and returns the
tokens for parser to use.
'''

class TokenizerError(Exception):
    pass

class Tokenize:
    "BSL lexical analyzer class"
    def __init__(self, instream):
        self.instream = instream
        self.commenter = '#'
        self.wordchars = ('abcdfeghijklmnopqrstuvwxyz'
                         'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
        self.whitespace = ' \t\r\n'
        self.quote = '"'
        self.state = 'walk'
        self.token = ''
        self.readchar = ''

    def get_tokens(self):
        token_list = []
        while True:
            t = self.read()
            if t == 'EOF':
                break
            token_list.append(t)
        return token_list
    
    def read(self):
        self.token = ''
        while True:
            if self.state == 'walk':
                self.readchar = self.instream.read(1)
                if not self.readchar:
                    self.state = 'EOF'
                    continue
                if self.readchar in self.wordchars:
                    self.token += self.readchar
                    continue
                elif self.readchar in self.whitespace:
                    if self.token:
                        break
                    continue
                elif self.readchar in self.commenter and self.state <> 'quote':
                    self.instream.readline()
                    continue
                elif self.readchar in self.quote:
                    self.state = 'quote'
                    self.token = self.readchar
                    continue
                else:
                    self.state = 'other'
                    if self.token:
                        break
                    continue

            if self.state == 'quote':
                self.readchar = self.instream.read(1)
                if not self.readchar:
                    raise TokenizerError, \
                          "reading quoted string but reached EOF"
                if self.readchar in self.quote:
                    self.state = 'walk'
                    self.token += self.readchar
                    break
                else:
                    self.token += self.readchar
                    continue
                
            if self.state == 'other' and self.readchar:
                self.state = 'walk'
                self.token = self.readchar
                break

            if self.state == 'EOF':
                self.token = 'EOF'
                break

        return self.token

if __name__ == "__main__":
    import sys

    try:
        f = open(sys.argv[1], "r")
    except:
        sys.stderr.write("Can't open source file\n")
        sys.exit(1)

    t = Tokenize(f)
    print t.get_tokens()
