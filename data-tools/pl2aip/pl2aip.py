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
# simple conversion helper tool for Zami Prolog -> AI Prolog
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
DEFAULT_OUTPUT = 'foo.aip'

# nlp_gens (en,"@SELF_ADDRESS:LABEL (all|) (men|women) are (all|) (alike|the same)",
#              "in what way?").

STATE_NORMAL = 0
STATE_MACRO  = 1
STATE_CHOICE = 2

TEST_OFFSET=0

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

    global outf

    lang  = pred.args[0].name
    ms    = pred.args[1].s.replace(u'@SELF_ADDRESS:LABEL ', u'')
    resps = pred.args[2:]

    # res = convert_macro_string(ms)

    outf.write(u'\n')
    outf.write(u"train(%s) :-\n" % lang)
    outf.write(u'    "%s",\n' % ms)

    if len(resps) == 1:
        outf.write(u'    "%s".\n' % resps[0].s)
    else:
        for i, r in enumerate(resps):
            if i == len(resps)-1:
                outf.write(u'       "%s").\n' %r.s)
            elif i == 0:
                outf.write(u'    or("%s",\n' %r.s)
            else:
                outf.write(u'       "%s",\n' %r.s)

def convert_nlp_macro(clause):

    global outf

    lang  = clause.head.args[0].name
    name  = clause.head.args[1].s.lower()
    mvars = clause.head.args[2:]

    outf.write(u'\n')
    outf.write(u"macro(%s, %s" % (lang, name))
    for v in mvars:
        outf.write(u", %s" % v)
    outf.write (u") :- %s.\n" % unicode(clause.body))


def convert_nlp_gen(pred):

    # print "% ", unicode(pred)

    lang = pred.args[0].name
    ms   = pred.args[1].s.replace(u'@SELF_ADDRESS:LABEL ', u'')

    outf.write(u'\n')
    outf.write(u"train(%s) :-\n" % lang)
    outf.write(u'    "%s",\n' % ms)
    for i, r in enumerate(pred.args[2:]):
        if i == len(pred.args)-3:
            outf.write(u'    %s.\n' % unicode(r))
        else:
            outf.write(u'    %s,\n' % unicode(r))

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

    global test_cnt, outf

    # print "% ", unicode(pred)

    lang      = pred.args[0].name
    test_name = 't%04d' % test_cnt
    test_cnt += 1

    outf.write(u'\n')
    outf.write(u"test(%s, %s) :-\n" % (lang, test_name))

    for i, ivr in enumerate(pred.args[1:]):
        
        ivr_in  = ivr.args[0].args[0].s
        ivr_out = ivr.args[1].args[0].s

        outf.write(u'    "%s",\n' % ivr_in)
        outf.write(u'    "%s"'    % ivr_out)

        if i == len(pred.args)-2:
            outf.write ('.\n')
        else:
            outf.write (',\n')

    # import pdb; pdb.set_trace()


#
# init, cmdline
#

misc.init_app('pl2aip')

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

with codecs.open(outputfn, 'w', 'utf8') as outf:

    outf.write('% prolog\n\n')

    outf.write("train_prefix('{self_address:L} ').\n\n")

    with codecs.open(inputfn, 'r', 'utf8') as f:

        parser.start(f, inputfn, module_name=MODULE_NAME)

        while parser.cur_sym != SYM_EOF:
            clauses = parser.clause(db=None)

            for clause in clauses:

                if clause.head.name == 'nlp_gens':
                    convert_nlp_gens(clause.head)
                elif clause.head.name == 'nlp_macro':
                    convert_nlp_macro(clause)
                elif clause.head.name == 'nlp_gen':
                    convert_nlp_gen(clause.head)
                # elif clause.head.name == 'answerz':
                #     convert_answerz(clause)
                elif clause.head.name == 'nlp_test':
                    convert_nlp_test(clause.head)
                    
                else:
                    outf.write(u"%% %s\n" % unicode(clause))
                    continue

logging.info ('%s written.' % outputfn)

