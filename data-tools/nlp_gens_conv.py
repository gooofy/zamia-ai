#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Guenter Bartsch
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
# simple conversion tool for nlp_gens clauses
#

import os
import sys
import traceback
import codecs
import logging
import random
import time

from zamiaprolog.parser  import PrologParser, SYM_EOF
from zamiaprolog.logic   import StringLiteral, ListLiteral, Predicate, Variable, Clause

from nltools             import misc

INPUT_FN = 'foo.pl'
MODULE_NAME = 'weather'

# nlp_gens (en,"@SELF_ADDRESS:LABEL (all|) (men|women) are (all|) (alike|the same)",
#              "in what way?").

STATE_NORMAL = 0
STATE_MACRO  = 1
STATE_CHOICE = 2

TEST_OFFSET=200

def convert_macro_string(ms):

    pos   = 0
    state = STATE_NORMAL
    curs  = u''
    res   = []
    while pos<len(ms):

        c = ms[pos]

        if state == STATE_NORMAL:
            
            if c=='@':
                if len(curs.strip())>0:
                    res.append(StringLiteral(curs.strip()))
                curs = u''
                state = STATE_MACRO
            elif c=='(':
                if len(curs.strip())>0:
                    res.append(StringLiteral(curs.strip()))
                curs = u''
                choices = []
                state = STATE_CHOICE
            else:
                curs += c

        elif state == STATE_MACRO:
            if c==' ':
                state = STATE_NORMAL
        elif state == STATE_CHOICE:
            if c==')':
                state = STATE_NORMAL
                choices.append(StringLiteral(curs))
                curs = u''
                res.append(ListLiteral(choices))
            elif c=='|':
                choices.append(StringLiteral(curs))
                curs = u''
            else:
                curs += c
        pos += 1
       
    if state == STATE_NORMAL:
        if len(curs.strip())>0:
            res.append(StringLiteral(curs.strip()))

    return ListLiteral(res)


def convert_nlp_gens(pred):

    # print "gens ", pred.args

    lang = pred.args[0].name
    ms   = pred.args[1].s
    resp = pred.args[2]

    res = convert_macro_string(ms)

    res = Predicate(name='nlp_gens', args=[StringLiteral(MODULE_NAME), Predicate(name=lang), res, resp])

    print unicode(res)+u'.'

    # import pdb; pdb.set_trace()
    
def convert_nlp_gen(pred):

    print "% ", unicode(pred)

    lang = pred.args[0].name
    ms   = pred.args[1].s

    res = convert_macro_string(ms)

    head = Predicate(name='nlp_%s_s' % MODULE_NAME, args=[Predicate(name=lang), Predicate(name='fixme'),
    Variable(name='S')])

    body = Predicate(name='hears', args=[Predicate(name=lang), Variable(name='S'), res])

    clause = Clause (head=head, body=body)

    print unicode(clause)

    # import pdb; pdb.set_trace()
    
def convert_answerz(c):

    pred = c.head

    lang = pred.args[1].name
    n    = pred.args[2].name

    pred = c.body

    s    = pred.args[2].s

    head = Predicate(name='nlp_%s_r' % MODULE_NAME, args=[Predicate(name=lang), Predicate(name=n), Variable(name='R')])

    body = Predicate(name='says', args=[Predicate(name=lang), Variable(name='R'), StringLiteral(s)])

    clause = Clause (head=head, body=body)

    print unicode(clause)

    # import pdb; pdb.set_trace()
    
test_cnt = TEST_OFFSET

def convert_nlp_test(pred):

    global test_cnt

    # print "% ", unicode(pred)

    lang    = pred.args[0].name
    ivr_in  = pred.args[1].args[0].args[0]
    ivr_out = pred.args[1].args[1].args[0]

    head = Predicate(name='nlp_test', args=[StringLiteral(MODULE_NAME), 
                                            Predicate(name=lang), 
                                            StringLiteral('t%04d' % test_cnt),
                                            Predicate(name='FIXME'),
                                            ListLiteral([ivr_in, ivr_out, ListLiteral([])])])

    test_cnt += 1

    clause = Clause (head=head)

    print unicode(clause)

    # import pdb; pdb.set_trace()
    
misc.init_app('nlp_gens_conv')

parser = PrologParser()

with codecs.open(INPUT_FN, 'r', 'utf8') as f:

    parser.start(f, INPUT_FN, module_name=MODULE_NAME)

    while parser.cur_sym != SYM_EOF:
        clauses = parser.clause(db=None)

        for clause in clauses:

            if clause.head.name == 'nlp_gens':
                convert_nlp_gens(clause.head)
            elif clause.head.name == 'nlp_gen':
                convert_nlp_gen(clause.head)
            elif clause.head.name == 'answerz':
                convert_answerz(clause)
            elif clause.head.name == 'nlp_test':
                convert_nlp_test(clause.head)
                
            else:
                print "%", unicode(clause)
                continue

