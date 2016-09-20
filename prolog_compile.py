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
# HAL-PROLOG compiler frontend
#

import os
import sys
import logging
import codecs
import re

from optparse import OptionParser
from StringIO import StringIO
from copy import copy

from sqlalchemy.orm import sessionmaker

import model
from logic import *
from logicdb import *
from prolog_parser import PrologParser, SYM_EOF
import utils

TRANSCRIPTFN = 'ts.txt'
SEMANTICSFN  = 'sem.txt'
TESTSFN      = 'test.txt'

logging.basicConfig(level=logging.DEBUG)

def nlp_macro(clause):

    global nlp_macros

    args = clause.head.args

    name = args[0].s

    mappings = []

    for m in args[1:]:

        if m.name != 'map':
            raise Exception ('map structure expected in nlp_macro %s' % name)

        mapping = {}

        for p in m.args:
            mapping[p.name] = p.args[0].s

        mappings.append(mapping)

    # print repr(mappings)

    nlp_macros[name] = mappings

    
def nlp_gen(clause):

    global nlp_macros, nlp_segments

    args = clause.head.args

    nlp = args[0].s
    preds = args[1].s

    # extract all macros used

    macro_names = set()

    for pos, char in enumerate(nlp):

        if char == '@':

            macro = re.match(r'@([A-Z]+):', nlp[pos:])

            # print "MACRO:", macro.group(1)

            macro_names.add(macro.group(1))

    # generate all macro-expansions

    macro_names = sorted(macro_names)
    todo = [ (0, {}) ]

    while True:

        if len(todo) == 0:
            break

        idx, mappings = todo.pop(0)

        if idx < len(macro_names):

            macro_name = macro_names[idx]

            for v in nlp_macros[macro_name]:

                nm = copy(mappings)
                # nm[macro_name] = (v, nlp_macros[macro_name][v])
                nm[macro_name] = v

                todo.append ( (idx+1, nm) )

        else:
            # print repr(mappings)

            s = nlp
            p = preds

            for k in mappings:

                for v in mappings[k]:

                    s = s.replace('@'+k+':'+v, mappings[k][v])
                    p = p.replace('@'+k+':'+v, mappings[k][v])

            s = utils.compress_ws(s.lstrip().rstrip())
            p = utils.compress_ws(p.lstrip().rstrip())

            # print s
            # print p

            # terms = map(lambda x: x.rstrip().lstrip(), p.split(';'))
            # print repr(terms)

            # FIXME model.add_segment(session, doc, s, terms)

            nlp_segments.append((s, p))            

def nlp_test(clause):

    global nlp_tests

    args = clause.head.args

    cnt = 0
    for ivr in args:

        # print "nlp_test: ivr=%s %s" % (repr(ivr), ivr.__class__)

        if ivr.name != 'ivr':
            raise PrologError ('nlp_test: ivr predicate args expected.')

        test_in = ''
        test_out = ''
        test_actions = set()

        for e in ivr.args:

            if e.name == 'in':
                test_in = e.args[0].s
            elif e.name == 'out':
                test_out = e.args[0].s
            elif e.name == 'action':
                test_actions.add(unicode(e))
            else:
                raise PrologError (u'nlp_test: ivr predicate: unexpected arg: ' + unicode(e))
            
        nlp_tests.append((cnt, test_in, test_out, test_actions))
            
        cnt += 1

    # print repr(nlp_tests)

#
# init terminal
#

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

#
# commandline
#

parser = OptionParser("usage: %prog [options] [foo.pl ...] ")

parser.add_option ("-t", "--transcript", dest="transcriptfn", type = "str", default=TRANSCRIPTFN,
           help="transcript filename (default: %s)" % TRANSCRIPTFN)

parser.add_option ("-s", "--semantics", dest="semanticsfn", type = "str", default=SEMANTICSFN,
           help="semantics filename (default: %s)" % SEMANTICSFN)

parser.add_option ("-T", "--tests", dest="testsfn", type = "str", default=TESTSFN,
           help="tests filename (default: %s)" % TESTSFN)

# 
# parser.add_option ("-n", "--kb-name", dest="kb_name", type = "str", default=KB_DEFAULT_NAME,
#            help="KB Name (default: %s)" % KB_DEFAULT_NAME)
# 
# parser.add_option ("-p", "--kb-prefix", dest="kb_prefix", type = "str", default='',
#            help="KB Prefix (default: none)")
# 
# parser.add_option ("-l", "--license", dest="kb_license", type = "str", default=KB_DEFAULT_LICENSE,
#            help="KB License (default: %s)" % KB_DEFAULT_LICENSE)
# 
# parser.add_option ("-u", "--uri", dest="kb_uri", type = "str", default=KB_DEFAULT_URI,
#            help="KB URI (default: %s)" % KB_DEFAULT_URI)
# 
# parser.add_option ("-c", "--clear", dest="clear", action="store_true",
#            help="clear old KB entries first (default: false)")

(options, args) = parser.parse_args()

# session, connect to db

Session = sessionmaker(bind=model.engine)

session = Session()

#
# main
#

db = LogicDB(session)

first = True

parser = PrologParser()
for pl_fn in args:

    linecnt = 0
    with codecs.open(pl_fn, encoding='utf-8', errors='ignore', mode='r') as f:
        while f.readline():
            linecnt += 1
    print "%s: %d lines." % (pl_fn, linecnt)

    nlp_macros   = {}
    nlp_segments = []
    nlp_tests    = []

    with open (pl_fn, 'r') as f:
        parser.start(f, pl_fn)

        while parser.cur_sym != SYM_EOF:
            clauses = parser.clause()

            if first:
                if not parser.module:
                    raise Exception ("No module name given!")

                db.clear_module(parser.module)
                first = False

            for clause in clauses:
                print u"%7d / %7d (%3d%%) > %s" % (parser.cur_line, linecnt, parser.cur_line * 100 / linecnt, unicode(clause))

                if clause.head.name == 'nlp_macro':
                    nlp_macro(clause)
                elif clause.head.name == 'nlp_gen':
                    nlp_gen(clause)
                elif clause.head.name == 'nlp_test':
                    nlp_test(clause)
                else:
                    db.store (parser.module, clause)

            if parser.comment_pred:

                db.store_doc (parser.module, parser.comment_pred, parser.comment)

                parser.comment_pred = None
                parser.comment = ''

    if len(nlp_segments)>0:

        with codecs.open (options.transcriptfn, 'w', 'utf8') as tf:

            for segment in nlp_segments:
                tf.write(u'%s\n' % segment[0])

            print "%s written." % options.transcriptfn

        with codecs.open (options.semanticsfn, 'w', 'utf8') as sf:

            for segment in nlp_segments:
                sf.write(u'%s;%s\n' % (segment[0],segment[1]))

            print "%s written." % options.semanticsfn

    if len(nlp_tests)>0:
        with codecs.open (options.testsfn, 'w', 'utf8') as sf:

            for test in nlp_tests:
                sf.write(u'%d;%s;%s;%s\n' % (test[0],
                                             test[1],
                                             test[2],
                                             ';'.join(test[3])))

            print "%s written." % options.testsfn

session.commit()


