#!/bin/python

import sys, os
import re

from gtts import gTTS
from playsound import playsound
from tempfile import mktemp

# owo what's this
# uwulang is a simple-ass interpreted language for furries
# do whatever the fuck you want, this is distibuted under WTFPL

# WARNING: THIS CODE WAS WRITTEN LATE AT NIGHT

VERSION = '1.0.0'

class uwulang:
    # all variables
    vars = {'_uwu_vewsion':VERSION}
    # do we need to abort on error?
    abort = False

    def err(self, text):
        print('Ewwow: ' + text)
        if self.abort:
            exit()

    def parse_expr(self, text):
        # if an empty string was given, that's None
        if text == '':
            return None
        # replace stuff in brackets with values
        left_brackets = [m.start() for m in re.finditer('\\(', text)]
        right_brackets = [m.start() for m in re.finditer('\\)', text)]
        if len(left_brackets) != len(right_brackets):
            self.err('opening and closing bwackets don\'t match')
        elif len(left_brackets) > 0 and len(right_brackets) > 0:
            # evaluate the expression
            e = text[left_brackets[0]+1 : right_brackets[-1]]
            v = self.parse_expr(e)
            # replace the original one with brackets with the value
            text = text[:left_brackets[0]] + str(v) + text[right_brackets[-1]+1:]
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
        # a list defintion is in square brackets
        elif text.startswith('[') and text.endswith(']'):
            return [self.parse_expr(x) for x in text[1:-1].split(',')]
        # it's probably a text value if it's in single quotes
        if text.startswith('\'') and text.endswith('\''):
            return text[1:-1]
        # if the text is a... pure text that doesn't start with a number, that must be a variable name
        elif re.match('[a-zA-Z0-9_\\[\\]]', text) and text[0] not in [str(x) for x in range(0, 10)]:
            # detect possible index
            idx = None
            var_name = text
            if text[-1] == ']' and text.find('[') != -1:
                idx = self.parse_expr(text[text.find('[')+1 :-1])
                var_name = text[:text.find('[')]
            if not var_name in self.vars:
                self.err('vawiable \'' + var_name + '\' doesn\'t exist')
            else:
                if idx == None:
                    return self.vars[text]
                else:
                    if idx < len(self.vars[var_name]):
                        return self.vars[var_name][idx]
                    else:
                        self.err('youw index is too lawge, senpai O_O')
        # if the text only contains only numbers, it must be a number
        elif re.match('[0-9]', text):
            return int(text)

    def interpret_line(self, line):
        l = line.strip()
        # everything after the hash is a comment
        l = line.split('#')[0]
        # the letter 'R' is not allowed!
        if 'r' in l or 'R' in l:
            self.err('the lettew \'r\' is not allowed! use \'w\' instead!')
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
        # say expression value
        elif l.startswith('speawk'):
            if len(args) < 2:
                self.err('\'speawk\' takes one awgument like this: \'speawk expwession\'')
            else:
                expr = ' '.join(args[1:])
                val = self.parse_expr(expr)
                try:
                    path = mktemp('_uwulang.mp3')
                    gTTS(text=str(val), lang='en', slow=False).save(path)
                    playsound(path)
                except:
                    self.err('\'speawk\' failed. Do you have an intewnet connection OwO?')
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
        # empty line... uh, okay
        elif l == '':
            pass
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