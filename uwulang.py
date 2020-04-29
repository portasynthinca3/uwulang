#!/bin/python

import sys, os
import re

# owo what's this
# uwulang is a simple-ass interpreted language for fucking furries
# do whatever the fuck you want, this is distibuted under WTFPL

# WARNING: THIS CODE WAS WRITTEN LATE AT NIGHT

VERSION = '1.0.0'

class uwulang:
    # all variables
    vars = {'_uwu_vewsion':VERSION}
    # do we need to abort on error?
    abort = False

    def err(self, text):
        print('Error: ' + text)
        if self.abort:
            exit()

    def parse_expr(self, text):
        # recursive shit, I don't really like this
        # split the text by possible operators, recursively parse them
        text = text.strip(' ')
        if '+' in text:
            adds = text.split('+')
            res = self.parse_expr(adds[0])
            for t in adds[1:]:
                r = self.parse_expr(t)
                if isinstance(res, str) and isinstance(r, int):
                    res = res + str(r)
                elif isinstance(res, int) and isinstance(r, str):
                    res = str(res) + r
                else:
                    res = res + r
            return res
        if '-' in text:
            subs = text.split('-')
            res = self.parse_expr(subs[0])
            for t in subs[1:]:
                res = res - self.parse_expr(t)
            return res
        if '*' in text:
            muls = text.split('*')
            res = self.parse_expr(muls[0])
            for t in muls[1:]:
                res = res * self.parse_expr(t)
            return res
        if '/' in text:
            divs = text.split('/')
            res = self.parse_expr(divs[0])
            for t in divs[1:]:
                res = res / self.parse_expr(t)
            return res
        # if an empty string was given, that's a NULL
        if text == '':
            return None
        # it's probably a text value if it's in single quotes
        if text.startswith('\'') and text.endswith('\''):
            return text[1:-1]
        # if the text is a... pure text that doesn't start with a number, that must be a variable name
        elif re.match('[a-zA-Z0-9]', text) and text[0] not in [str(x) for x in range(0, 10)]:
            if not text in self.vars:
                self.err('vawiable \'' + text + '\' doesn\'t exist')
            else:
                return self.vars[text]
        # if the text only contains only numbers, it must be a number
        elif re.match('[0-9]', text):
            return int(text)

    def interpret_line(self, line):
        l = line.strip()
        # the letter 'R' is not allowed!
        if 'r' in l or 'R' in l:
            self.err('the lettew \'r\' is not allowed! use \'w\' only!')
            return
        args = l.split(' ')
        # exit
        if l == 'bye owo':
            exit()
        # load an expression value into the variable
        elif l.startswith('loawd'):
            if len(args) < 3:
                self.err('\'loawd\' takes one awgument like this: \'loawd vawiable_name expwession\'')
            else:
                var_name = args[1]
                expr = ' '.join(args[2:])
                self.vars[var_name] = self.parse_expr(expr)
        # print expression value
        elif l.startswith('owo whats'):
            if len(args) < 3:
                self.err('\'owo whats\' takes one awgument like this: \'owo whats expwession\'')
            else:
                expr = ' '.join(args[2:])
                print(self.parse_expr(expr))
        # input a numeric value
        elif l.startswith('pawbsnum'):
            if len(args) != 2:
                self.err('\'pawbsnum\' takes one awgument like this: \'pawbsnum vawiable_name\'')
            else:
                var_name = args[1]
                self.vars[var_name] = int(input('> '))
        # input a value
        elif l.startswith('pawbs'):
            if len(args) != 2:
                self.err('\'pawbs\' takes one awgument like this: \'pawbs vawiable_name\'')
            else:
                var_name = args[1]
                self.vars[var_name] = input('> ')
        # what?
        else:
            self.err('unknown commnd. please twy hawder owo')

# if an argument was passed to the program, it must be a file (hopefully)
if len(sys.argv) == 2:
    # open this file
    with open(sys.argv[1], 'r') as file:
        # create a language state class
        lang = uwulang()
        lang.abort = True
        # interpret each line
        for line in file.read().split('\n'):
            lang.interpret_line(line,)
# if no arguments were passed, run in interactive mode
elif len(sys.argv) == 1:
    print('uwulang v. ' + VERSION + '\nintewactive shell')
    lang = uwulang()
    lang.abort = False
    while True:
        line = input('>>> ')
        lang.interpret_line(line)
# too many arguments were passed
else:
    # aww, this is beautiful, I already like this
    print('An ewwow occuwed. That\'s not UwU. Use this scwipt as follows:\n'
          '    uwulang filename - to wun the file\n'
          '    uwulang          - to wun in intewactive mode')