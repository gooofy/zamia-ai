#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016 Guenter Bartsch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# HAL-PROLOG
# ----------
#
# parser, scanner
#
# HAL-PROLOG grammar
#
# clause        ::= relation [ ':-' term { ( ',' | ';' ) term } ] '.'
#
# relation      ::= name [ '(' term { ',' term } ')' ]
#
# term          ::= add-term { rel-op add-term }
#
# rel-op        ::= '=' | '\=' | '<' | '>' | '=<' | '>=' | 'is' 
#
# add-term      ::= mul-term { add-op mul-term } 
#
# add-op        ::= '+' | '-' 
#
# mul-term      ::= unary-term  { mul-op unary-term } 
#
# mul-op        ::= '*' | '/' | 'div' | 'rem' | '//' | 'rdiv' | 'gcd' 
#
# unary-term    ::= [ unary-op ] primary-term  
#
# unary-op      ::= '+' | '-' 
#
# macro_call    ::= '@' ( variable | name ) ':' ( variable | name )
#
# primary-term  ::= ( variable | number | string | relation | macro_call | '(' term { ',' term } ')' )
#

import os
import sys
import logging
import codecs
import re
import copy

from StringIO import StringIO

from logic import *

# lexer

REL_OP   = set ([u'=', u'\\=', u'<', u'>', u'=<', u'>=', u'is']) 
ADD_OP   = set ([u'+', u'-'])
MUL_OP   = set ([u'*', u'/', u'div', u'rem', u'//', u'rdiv', u'gcd'])
UNARY_OP = set ([u'+', u'-'])

NAME_CHARS = set(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                  'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                  '_','0','1','2','3','4','5','6','7','8','9'])

SIGN_CHARS = set([u'=',u'<',u'>',u'+',u'-',u'*',u'/',u'\\'])

SYM_NONE      =  0
SYM_EOF       =  1
SYM_STRING    =  2   # 'abc'
SYM_NAME      =  3   # abc aWord =< is div + 
SYM_VARIABLE  =  4   # X Avariable _Variable _
SYM_NUMBER    =  5  

SYM_IMPL      = 10   # :-
SYM_LPAREN    = 11   # (
SYM_RPAREN    = 12   # )
SYM_COMMA     = 13   # ,
SYM_PERIOD    = 14   # .
SYM_SEMICOLON = 15   # ;
SYM_AT        = 16   # @
SYM_COLON     = 17   # :

# structured comments
CSTATE_IDLE   = 0
CSTATE_HEADER = 1
CSTATE_BODY   = 2

class PrologError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    def __unicode__(self):
        return self.value

class PrologParser(object):

    def __init__(self):
        pass
    
    def report_error(self, s):
        raise PrologError ("%s: error in line %d col %d: %s" % (self.prolog_fn, self.cur_line, self.cur_col, s))

    def get_location(self):
        return SourceLocation(self.prolog_fn, self.cur_line, self.cur_col)

    def next_c(self):
        self.cur_c    = unicode(self.prolog_f.read(1))
        self.cur_col += 1

        if self.cur_c == u'\n':
            self.cur_line += 1
            self.cur_col   = 1
            if self.linecnt > 0 and self.cur_line % 100 == 0:
                print "%s: parsing line %6d / %6d (%3d%%)" % (self.prolog_fn, 
                                                              self.cur_line, 
                                                              self.linecnt, 
                                                              self.cur_line * 100 / self.linecnt)

        # print '[', self.cur_c, ']',

    def peek_c(self):
        peek_c = unicode(self.prolog_f.read(1))
        self.prolog_f.seek(-1,1)
        return peek_c

    def next_sym(self):

        # whitespace, comments

        self.cstate       = CSTATE_IDLE

        while True:
            # skip whitespace
            while not (self.cur_c is None) and self.cur_c.isspace():
                self.next_c()

            if self.cur_c is None or self.cur_c == u'':
                self.cur_sym = SYM_EOF
                return

            # skip comments
            if self.cur_c == u'%':

                comment_line = u''
                
                self.next_c()
                if self.cur_c == u'!':
                    self.cstate = CSTATE_HEADER
                    self.next_c()

                while True:
                    if self.cur_c is None:
                        self.cur_sym = SYM_EOF
                        return
                    if self.cur_c == u'\n':
                        self.next_c()
                        break
                    comment_line += self.cur_c
                    self.next_c()

                if self.cstate == CSTATE_HEADER:
                    m = re.match (r"^\s*doc\s+([a-zA-Z0-9_]+)", comment_line)
                    if m:
                        self.comment_pred = m.group(1)
                        self.comment = ''
                        self.cstate = CSTATE_BODY

                elif self.cstate == CSTATE_BODY:
                    if len(self.comment)>0:
                        self.comment += '\n'
                    self.comment += comment_line.lstrip().rstrip()

            else:
                break

        #if self.comment_pred:
        #    print "COMMENT FOR %s : %s" % (self.comment_pred, self.comment)

        self.cur_str = u''

        if self.cur_c == u'\'' or self.cur_c == u'"':
            self.cur_sym = SYM_STRING
            startc = self.cur_c

            while True:
                self.next_c()
                if self.cur_c is None:
                    self.report_error ("Unterminated string literal.")
                if self.cur_c == u'\\':
                    self.next_c()
                    self.cur_str += self.cur_c
                    self.next_c()

                if self.cur_c == startc:
                    self.next_c()
                    break

                self.cur_str += self.cur_c

        elif self.cur_c.isdigit():
            self.cur_sym = SYM_NUMBER

            while True:
                self.cur_str += self.cur_c
                self.next_c()
                if self.cur_c == '.' and not self.peek_c().isdigit():
                    break

                if not self.cur_c or (not self.cur_c.isdigit() and self.cur_c != '.'):
                    break

        elif self.cur_c in NAME_CHARS:
            self.cur_sym = SYM_VARIABLE if self.cur_c == u'_' or self.cur_c.isupper() else SYM_NAME

            while True:
                self.cur_str += self.cur_c
                self.next_c()
                if not self.cur_c or not (self.cur_c in NAME_CHARS):
                    break

        elif self.cur_c in SIGN_CHARS:
            self.cur_sym = SYM_NAME

            while True:
                self.cur_str += self.cur_c
                self.next_c()
                if not self.cur_c or not (self.cur_c in SIGN_CHARS):
                    break

        elif self.cur_c == u':':
            self.next_c()

            if self.cur_c == u'-':
                self.next_c()
                self.cur_sym = SYM_IMPL
            else:
                self.cur_sym = SYM_COLON

        elif self.cur_c == u'(':
            self.cur_sym = SYM_LPAREN
            self.next_c()
        elif self.cur_c == u')':
            self.cur_sym = SYM_RPAREN
            self.next_c()

        elif self.cur_c == u',':
            self.cur_sym = SYM_COMMA
            self.next_c()

        elif self.cur_c == u'.':
            self.cur_sym = SYM_PERIOD
            self.next_c()

        elif self.cur_c == u';':
            self.cur_sym = SYM_SEMICOLON
            self.next_c()

        elif self.cur_c == u'@':
            self.cur_sym = SYM_AT
            self.next_c()

        else:
            self.report_error ("Illegal character: " + repr(self.cur_c))

        #print "[%2d]" % self.cur_sym,


    #
    # parser starts here
    #

    def primary_term(self):

        res = None

        if self.cur_sym == SYM_VARIABLE:
            res = Variable (self.cur_str)
            self.next_sym()

        elif self.cur_sym == SYM_NUMBER:
            res = NumberLiteral (float(self.cur_str))
            self.next_sym()

        elif self.cur_sym == SYM_STRING:
            res = StringLiteral (self.cur_str)
            self.next_sym()

        elif self.cur_sym == SYM_NAME:
            res = self.relation()

        elif self.cur_sym == SYM_AT:
            self.next_sym()
            res = self.macro_call()

        elif self.cur_sym == SYM_LPAREN:
            self.next_sym()
            res = self.term()

            while (self.cur_sym == SYM_COMMA):
                self.next_sym()
                if not isinstance(res, list):
                    res = [res]
                res.append(self.term())

            if self.cur_sym != SYM_RPAREN:
                self.report_error ("primary term: ) expected.")
            self.next_sym()

        else:
            self.report_error ("primary term: variable / number / string / name / ( expected.")

        # logging.debug ('primary_term: %s' % str(res))

        return res

    def macro_call(self):

        if self.cur_sym != SYM_NAME and self.cur_sym != SYM_VARIABLE:
            self.report_error ("macro: name expected (%d)." % self.cur_sym)
        macro_name = self.cur_str
        self.next_sym()

        if self.cur_sym != SYM_COLON:        
            self.report_error ("macro: : expected.")
        self.next_sym()

        if self.cur_sym != SYM_NAME and self.cur_sym != SYM_VARIABLE:
            self.report_error ("macro: predicate name expected.")
        pred_name = self.cur_str
        self.next_sym()

        return NLPMacroCall(macro_name, pred_name)

    def unary_term(self):

        o = None

        if self.cur_sym == SYM_NAME and self.cur_str in UNARY_OP:
            o = self.cur_str
            self.next_sym()

        res = self.primary_term()
        if o:
            if not isinstance(res, list):
                res = [res]
            
            res = Predicate (o, res)

        return res


    def mul_term(self):

        args = []
        ops  = []

        args.append(self.unary_term())

        while self.cur_sym == SYM_NAME and self.cur_str in MUL_OP:
            ops.append(self.cur_str)
            self.next_sym()
            args.append(self.unary_term())

        res = None
        while len(args)>0:
            arg = args.pop()
            if not res:
                res = arg
            else:
                res = Predicate (o, [arg, res])

            if len(ops)>0:
                o = ops.pop()

        # logging.debug ('mul_term: ' + str(res))

        return res


    def add_term(self):

        args = []
        ops  = []

        args.append(self.mul_term())

        while self.cur_sym == SYM_NAME and self.cur_str in ADD_OP:
            ops.append(self.cur_str)
            self.next_sym()
            args.append(self.mul_term())

        res = None
        while len(args)>0:
            arg = args.pop()
            if not res:
                res = arg
            else:
                res = Predicate (o, [arg, res])

            if len(ops)>0:
                o = ops.pop()

        # logging.debug ('add_term: ' + str(res))

        return res

    def term(self):
       
        args = []
        ops  = []

        args.append(self.add_term())

        while self.cur_sym == SYM_NAME and self.cur_str in REL_OP:
            ops.append(self.cur_str)
            self.next_sym()
            args.append(self.add_term())

        res = None
        while len(args)>0:
            arg = args.pop()
            if not res:
                res = arg
            else:
                res = Predicate (o, [arg, res])

            if len(ops)>0:
                o = ops.pop()

        # logging.debug ('term: ' + str(res))

        return res


    def relation(self):

        if self.cur_sym != SYM_NAME:
            self.report_error ("Name expected.")
        name = self.cur_str
        self.next_sym()

        args = None

        if self.cur_sym == SYM_LPAREN:
            self.next_sym()

            args = []

            while True:

                args.append(self.term())

                if self.cur_sym != SYM_COMMA:
                    break
                self.next_sym()

            if self.cur_sym != SYM_RPAREN:
                self.report_error ("relation: ) expected.")
            self.next_sym()

        return Predicate (name, args)

    def clause_body(self):

        body  = []

        loc = self.get_location()

        while True:
            body.append(self.term())

            if self.cur_sym == SYM_SEMICOLON:
                res.append (Clause (head, body, location=loc))
                body = []
                loc = self.get_location()

            elif self.cur_sym != SYM_COMMA:
                break

            self.next_sym()

        return body

    def clause(self):

        res = []

        loc = self.get_location()

        head = self.relation()

        if self.cur_sym == SYM_IMPL:
            self.next_sym()

            body = self.clause_body()

            if len(body) > 0:
                res.append (Clause (head, body, location=loc))

        else:
            res.append (Clause (head, location=loc))

        if self.cur_sym != SYM_PERIOD:
            self.report_error ("clause: . expected.")
        self.next_sym()

        # logging.debug ('clause: ' + str(res))

        return res

    def start (self, prolog_f, prolog_fn, linecnt = 0):

        self.cur_c        = u' '
        self.cur_sym      = SYM_NONE
        self.cur_str      = u''
        self.cur_line     = 1
        self.cur_col      = 1
        self.prolog_f     = prolog_f
        self.prolog_fn    = prolog_fn
        self.linecnt      = linecnt

        self.cstate       = CSTATE_IDLE
        self.comment_pred = None
        self.comment      = u''

        self.next_c()
        self.next_sym()

    def parse_line_clause_body (self, line):

        self.start (StringIO(line), '<str>')
        body = self.clause_body()

        return Clause (None, body)

    def parse_line_clauses (self, line):

        self.start (StringIO(line), '<str>')
        return self.clause()

if __name__ == "__main__":

    # line = 'time_span(tomorrow, TS, TE) :- context(currentTime, T), stamp_date_time(T, date(Y, M, D, H, Mn, S, "local")), date_time_stamp(date(Y, M, +(D, 1.0), 0.0, 0.0, 0.0, "local"), TS), date_time_stamp(date(Y, M, +(D, 1.0), 23.0, 59.0, 59.0, "local"), TE).'
    line = 'time_span(TE) :- date_time_stamp(+(D, 1.0)).'

    parser = PrologParser()
    tree = parser.parse_line_clauses(line)

    print unicode(tree[0].body)



