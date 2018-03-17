#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# simple conversion helper tool for prolog -> nlp
#

import os
import sys
import traceback
import codecs
import logging
import random
import time

from optparse import OptionParser

from zamiaprolog.parser  import PrologParser, SYM_EOF
from zamiaprolog.logic   import StringLiteral, ListLiteral, Predicate, Variable, Clause

from nltools             import misc

MODULE_NAME    = 'weather'
DEFAULT_OUTPUT = 'foo.nlp'

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

    # res = convert_macro_string(ms)

    print
    print u"@start:%s" % lang
    print u"%s" % ms
    for r in pred.args[2:]:
        print r.s


    # import pdb; pdb.set_trace()
    
def convert_nlp_gen(pred):

    # print "% ", unicode(pred)

    lang = pred.args[0].name
    ms   = pred.args[1].s

    # res = convert_macro_string(ms)

    # head = Predicate(name='nlp_%s_s' % MODULE_NAME, args=[Predicate(name=lang), Predicate(name='fixme'),
    # Variable(name='S')])

    # body = Predicate(name='hears', args=[Predicate(name=lang), Variable(name='S'), res])

    # clause = Clause (head=head, body=body)

    # print unicode(clause)

    print
    print u"@start:%s" % lang
    print u"%s" % ms
    for r in pred.args[2:]:
        print unicode(r)
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


#
# init, cmdline
#

misc.init_app('pl2nlp')

parser = OptionParser("usage: %prog [options] foo.pl")

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")
parser.add_option ("-o", "--output", dest="outputfn", type = "string", default=DEFAULT_OUTPUT,
                   help="output file, default: %s" % DEFAULT_OUTPUT)

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if len(args) != 1:
    logging.error('exactly one input file needed.')
    parser.print_help()
    sys.exit(1)

inputfn  = args[0]
outputfn = options.outputfn

#
# main
#


parser = PrologParser()

with codecs.open(inputfn, 'r', 'utf8') as f:

    parser.start(f, inputfn, module_name=MODULE_NAME)

    while parser.cur_sym != SYM_EOF:
        clauses = parser.clause(db=None)

        for clause in clauses:

            if clause.head.name == 'nlp_gens':
                convert_nlp_gens(clause.head)
            elif clause.head.name == 'nlp_gen':
                convert_nlp_gen(clause.head)
            # elif clause.head.name == 'answerz':
            #     convert_answerz(clause)
            # elif clause.head.name == 'nlp_test':
            #     convert_nlp_test(clause.head)
                
            else:
                print "# ", unicode(clause)
                continue

