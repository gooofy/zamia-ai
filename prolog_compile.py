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
from prolog_parser import PrologParser, SYM_EOF, PrologError
from prolog_ai_engine import PrologAIEngine
import utils

from speech_tokenizer import tokenize

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

    
def nlp_gen(src, clause):

    global nlp_macros, session

    args = clause.head.args

    lang = args[0].name

    # extract all macros used

    macro_names = set()

    argc = 1
    while argc < len(args):

        nlp   = args[argc  ].s
        preds = args[argc+1].s

        argc += 2

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

            # generate discourse for this set of mappings

            # print repr(mappings)

            # create discourse in db

            discourse = model.Discourse(num_participants = 2,
                                        lang             = lang,
                                        src              = src)
            session.add(discourse)

            argc       = 1
            round_num = 0
            while argc < len(args):

                s = args[argc  ].s
                p = args[argc+1].s

                argc += 2

                for k in mappings:

                    for v in mappings[k]:

                        s = s.replace('@'+k+':'+v, mappings[k][v])
                        p = p.replace('@'+k+':'+v, mappings[k][v])

                inp_raw = utils.compress_ws(s.lstrip().rstrip())
                p       = utils.compress_ws(p.lstrip().rstrip())

                # print s
                # print p

                # tokenize strings, wrap them into say() calls

                inp_tokenized = ' '.join(tokenize(inp_raw, lang))

                preds = p.split(';')
                np = ''
                for pr in preds:
                    if not pr.startswith('"'):
                        if len(np)>0:
                            np += ';'
                        np += pr.strip()
                        continue

                    for word in tokenize (pr, lang):
                        if len(np)>0:
                            np += ';'
                        np += 'say(' + lang + ', "' + word + '")'

                    if len(p) > 2:
                        if p[len(p)-2] in ['.', '?', '!']:
                            if len(np)>0:
                                np += ';'
                            np += 'say(' + lang + ', "' + p[len(p)-2] + '")'
                    np += ';eou'


                dr = model.DiscourseRound(inp_raw       = inp_raw, 
                                          inp_tokenized = inp_tokenized,
                                          response      = np, 
                                          discourse     = discourse, 
                                          round_num     = round_num)
                session.add(dr)

                round_num += 1

def nlp_test_setup(clause):

    global nlp_test_engine, db

    nlp_test_context = 'test'

    db.disable_all_modules()
    db.enable_module(parser.module)

    for arg in clause.head.args:

        if arg.name == 'requires':

            module = arg.args[0].s
            db.enable_module(module)

        elif arg.name == 'context':

            nlp_test_context = arg.args[0].s

        else:
            raise PrologError ('nlp_test_setup: only requires / context args allowed')

    nlp_test_engine.set_context_name(nlp_test_context)

def nlp_test(clause):

    global nlp_test_engine, db

    args = clause.head.args

    lang = args[0].name

    # extract test rounds, look up matching discourses

    rounds        = [] # [ (in, out, actions), ...]
    round_num     = 0
    discourse_ids = set()

    for ivr in args[1:]:

        if ivr.name != 'ivr':
            raise PrologError ('nlp_test: ivr predicate args expected.')

        test_in = ''
        test_out = ''
        test_actions = set()

        for e in ivr.args:

            if e.name == 'in':
                test_in = ' '.join(tokenize(e.args[0].s, lang))
            elif e.name == 'out':
                test_out = ' '.join(tokenize(e.args[0].s, lang))
            elif e.name == 'action':
                test_actions.add(unicode(e))
            else:
                raise PrologError (u'nlp_test: ivr predicate: unexpected arg: ' + unicode(e))
           
        rounds.append((test_in, test_out, test_actions))

        # look up matching discourse_ids:

        d_ids = set()
        
        for dr in session.query(model.DiscourseRound).filter(model.DiscourseRound.inp_tokenized==test_in) \
                                                     .filter(model.DiscourseRound.round_num==round_num).all():
            d_ids.add(dr.discourse_id)

        if round_num==0:
            discourse_ids = d_ids
        else:
            discourse_ids = discourse_ids & d_ids

        print 'discourse_ids:', repr(discourse_ids)

        round_num += 1

    if len(discourse_ids) == 0:
        raise PrologError ('nlp_test: no matching discourse found.')

    # run the test(s): look up reaction to input in db, execute it, check result
    for did in discourse_ids:
        nlp_test_engine.reset_context()

        round_num = 0
        for dr in session.query(model.DiscourseRound).filter(model.DiscourseRound.discourse_id==did) \
                                                     .order_by(model.DiscourseRound.round_num):
        
            prolog_s = ','.join(dr.response.split(';'))

            print
            print "Round:", round_num, dr.inp_tokenized, '=>', prolog_s

            c = parser.parse_line_clause_body(prolog_s)
            # logging.debug( "Parse result: %s" % c)

            # logging.debug( "Searching for c: %s" % c )

            nlp_test_engine.reset_utterances()
            solutions = nlp_test_engine.search(c)

            if len(solutions) == 0:
                raise PrologError ('nlp_test: no solution found.')
        
            print "round %d utterances: %s" % (round_num, repr(nlp_test_engine.get_utterances())) 

            # check actual utterances vs expected one

            test_in, test_out, test_actions = rounds[round_num]

            found = False
            for utt in nlp_test_engine.get_utterances():
                actual_out = ' '.join(tokenize(utt['utterance'], utt['lang']))
                if actual_out == test_out:
                    found = True
                    break

            if found:
                print "***MATCHED!"
            else:
                raise PrologError ('nlp_test: actual utterance did not match.')
            

            # FIXME: check actions

            round_num += 1

def init_src(ref, name):

    global session

    session.query(model.Source).filter(model.Source.ref==ref).delete()
    src = model.Source(ref  = ref,
                       name = name)
    session.add(src)
    return src

def set_context_default(clause):

    global db, nlp_test_engine

    solutions = nlp_test_engine.search(clause)

    # print "set_context_default: solutions=%s" % repr(solutions)

    if len(solutions) != 1:
        raise PrologError ('set_context_default: need exactly one solution.')

    args = clause.head.args

    name  = args[0].s
    key   = args[1].name

    value = args[2]
    if isinstance (value, Variable):
        value = solutions[0][value.name]

    value = unicode(value)

    db.set_context_default(name, key, value)

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

parser.add_option("-g", "--trace", action="store_true", dest="trace",
                  help="trace test execution")

parser.add_option("-C", "--clear-all", action="store_true", dest="clear_all",
                  help="clear all modules in db")

# parser.add_option ("-T", "--tests", dest="testsfn", type = "str", default=TESTSFN,
#            help="tests filename (default: %s)" % TESTSFN)

(options, args) = parser.parse_args()

# session, connect to db

Session = sessionmaker(bind=model.engine)

session = Session()

#
# main
#

db = LogicDB(session)

if options.clear_all:
    db.clear_all_modules()

first = True

parser = PrologParser()
for pl_fn in args:

    linecnt = 0
    with codecs.open(pl_fn, encoding='utf-8', errors='ignore', mode='r') as f:
        while f.readline():
            linecnt += 1
    print "%s: %d lines." % (pl_fn, linecnt)

    nlp_macros      = {}
    src             = None
    nlp_test_engine = PrologAIEngine(db)
    nlp_test_engine.set_trace(options.trace)

    with open (pl_fn, 'r') as f:
        parser.start(f, pl_fn)

        while parser.cur_sym != SYM_EOF:
            clauses = parser.clause()

            if first:
                if not parser.module:
                    raise Exception ("No module name given!")

                db.clear_module(parser.module)
                db.store_module_requirements(parser.module, parser.requirements)

                first = False

            for clause in clauses:
                print u"%7d / %7d (%3d%%) > %s" % (parser.cur_line, linecnt, parser.cur_line * 100 / linecnt, unicode(clause))

                # compiler directive?

                if clause.head.name == 'nlp_macro':
                    nlp_macro(clause)

                elif clause.head.name == 'nlp_gen':
                    if not src:
                        src = init_src(pl_fn, parser.module)
                    nlp_gen(src, clause)

                elif clause.head.name == 'nlp_test_setup':
                    nlp_test_setup(clause)

                elif clause.head.name == 'nlp_test':
                    nlp_test(clause)

                elif clause.head.name == 'set_context_default':
                    set_context_default(clause)

                else:
                    db.store (parser.module, clause)

            if parser.comment_pred:

                db.store_doc (parser.module, parser.comment_pred, parser.comment)

                parser.comment_pred = None
                parser.comment = ''

session.commit()


