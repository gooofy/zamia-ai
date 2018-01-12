#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017, 2018 Guenter Bartsch
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
# simple conversion helper tool for AI Prolog -> Python
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

DEFAULT_OUTPUT = 'foo.py'

td_count = 0
ts_count = 0

def convert_train_prefix(pred):

    global outf

    prefix = pred.args[0].s

    outf.write(u"    k.dte.set_prefixes([u'%s'])\n" % prefix)

def convert_test(clause):

    global outf, ts_count

    logging.debug (u'convert_test: %s' % unicode(clause))

    lang = clause.head.args[0].name

    if not isinstance(clause.body, Predicate) or clause.body.name != 'and':
        outf.write(u"#    %s\n" % unicode(clause))
        return

    outf.write(u"    k.dte.ts('%s', '%s', [" % (clause.head.args[0], clause.head.args[1]))

    idx  = 0
    prep = []
    while idx < len(clause.body.args) and isinstance (clause.body.args[idx], Predicate):
        prep.append(clause.body.args[idx])
        idx += 1

    first = True
    while idx < len(clause.body.args):

        if first:
            first = False
        else:
            outf.write(u',\n                               ')

        inp  = clause.body.args[idx].s  
        idx += 1
        resp = clause.body.args[idx].s
        idx += 1 

        actions = []

        while idx < len(clause.body.args) and isinstance(clause.body.args[idx], Predicate):
            actions.append(unicode(clause.body.args[idx]))
            idx += 1
                    

        outf.write(u'(u"%s", u"%s", %s)' % (inp, resp, repr(actions)) )

    outf.write(u"]")
    if prep:
        outf.write(u", prep=%s" % unicode(prep))
    outf.write(u")\n")

    ts_count += 1
    if ts_count % 2 == 0:
        outf.write("\n")

def convert_train(clause):

    global outf, td_count

    lang = clause.head.args[0].name

    if not isinstance(clause.body, Predicate) or clause.body.name != 'and':
        outf.write(u"#    %s\n" % unicode(clause))
        return

    if len(clause.body.args) != 2:
        outf.write(u"#    %s\n" % unicode(clause))
        return

    if isinstance(clause.body.args[0], StringLiteral):
        inp = clause.body.args[0].s
    elif isinstance(clause.body.args[0], Predicate) and clause.body.args[0].name == 'or':
        inp = []
        for a in clause.body.args[0].args:
            if not isinstance(a, StringLiteral):
                outf.write(u"#    %s\n" % unicode(clause))
                return
            inp.append(a.s)
    else:
        outf.write(u"#    %s\n" % unicode(clause))
        return

    if isinstance(clause.body.args[1], StringLiteral):
        resp = clause.body.args[1].s
    elif isinstance(clause.body.args[1], Predicate) and clause.body.args[1].name == 'or':
        resp = []
        for a in clause.body.args[1].args:
            if not isinstance(a, StringLiteral):
                outf.write(u"#    %s\n" % unicode(clause))
                return
            resp.append(a.s)
    else:
        resp = clause.body.args[1]
        # outf.write(u"#    %s\n" % unicode(clause))
        # return

    outf.write(u"    k.dte.dt('%s', " % lang)

    if isinstance(inp,basestring) and isinstance(resp,basestring):
        outf.write(u"u\"%s\", u\"%s\")\n" % (inp, resp))
    else:
        if isinstance(inp, basestring):
            outf.write(u"u\"%s\",\n" % inp)
        else:
            if len(inp) == 0:
                outf.write(u"[],\n")
            else:
                outf.write(u"[u\"%s\"" % inp[0])
                for i in inp[1:]:
                    outf.write(u",\n")
                    outf.write(u"                    u\"%s\"" % i)
                outf.write (u"],\n")

        if isinstance(resp, basestring):
            outf.write(u"                   u\"%s\"" % resp)
        elif isinstance(resp, list):
            if len(resp) == 0:
                outf.write(u"                   []")
            else:
                outf.write(u"                   [u\"%s\"" % resp[0])
                for i in resp[1:]:
                    outf.write(u",\n")
                    outf.write(u"                    u\"%s\"" % i)
                outf.write (u"]")
        else:
                outf.write(u"                   %% %s" % unicode(resp))

        outf.write(u")\n")

    td_count += 1
    if td_count % 2 == 0:
        outf.write("\n")

#
# init, cmdline
#

misc.init_app('aip2py')

parser = OptionParser("usage: %prog [options] foo.aip")

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


db = None

parser = PrologParser(db, do_inline = False)

with codecs.open(outputfn, 'w', 'utf8') as outf:

    outf.write('#!/usr/bin/env python\n')
    outf.write('# -*- coding: utf-8 -*-\n\n')

    outf.write('def get_data(k):\n')

    with codecs.open(inputfn, 'r', 'utf8') as f:

        parser.start(f, inputfn, module_name='foo')

        while parser.cur_sym != SYM_EOF:
            clauses = parser.clause()

            for clause in clauses:

                if clause.head.name == 'train_prefix':
                    convert_train_prefix(clause.head)
                elif clause.head.name == 'train':
                    convert_train(clause)
                elif clause.head.name == 'test':
                    convert_test(clause)
                    
                else:
                    outf.write(u"    def %s:\n        %s\n" % (unicode(clause.head), unicode(clause.body)))
                    continue

logging.info ('%s written.' % outputfn)

