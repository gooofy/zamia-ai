#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016, 2017 Guenter Bartsch
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
# HAL-PROLOG compiler
#

import os
import sys
import logging
import codecs
import re
import rdflib

from copy import copy

import model
from logic import *
from logicdb import *
from prolog_parser import PrologParser, SYM_EOF, PrologError
from prolog_ai_engine import PrologAIEngine
from nltools.tokenizer import tokenize
from nlp_macros import NLPMacroEngine
from kb import HALKB

class PrologCompiler(object):

    def __init__(self, session, trace = False, run_tests = False, print_utterances=False, split_utterances=False):

        self.session          = session
        self.trace            = trace
        self.run_tests        = run_tests
        self.print_utterances = print_utterances
        self.split_utterances = split_utterances

    def set_trace (self, trace):
        self.trace = trace

    def set_run_tests (self, run_tests):
        self.run_tests = run_tests

    def nlp_macro(self, clause):

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

        self.macro_engine.define_named_macro(name, mappings)

    def sparql_macro(self, clause):

        args = clause.head.args

        if not isinstance (args[0], StringLiteral):
            raise PrologError (u'sparql_macro: arg 0 unexpected type: %s. StringLiteral expected.' % args[0].__class__)
        if not isinstance (args[1], StringLiteral):
            raise PrologError (u'sparql_macro: arg 1 unexpected type: %s. StringLiteral expected.' % args[0].__class__)

        name  = args[0].s
        query = args[1].s

        result = self.kb.query (query)

        logging.debug ('ran query. resulting bindings: %s' % repr(result.bindings))

        # turn result into lists of strings we can then bind to macro variables

        res_map  = {} 
        res_vars = {} # variable idx -> variable name

        for binding in result:

            for v in binding.labels:

                l = binding[v]

                logging.debug('l class: %s' % l.__class__)

                value = unicode(l)

                if isinstance (l, rdflib.term.Literal):

                    if l.datatype:

                        datatype = str(l.datatype)

                        if datatype == 'http://www.w3.org/2001/XMLSchema#decimal':
                            value = unicode(value)
                        elif datatype == 'http://www.w3.org/2001/XMLSchema#float':
                            value = unicode(value)
                        # FIXME elif datatype == 'http://www.w3.org/2001/XMLSchema#dateTime':
                        # FIXME     dt = dateutil.parser.parse(value)
                        # FIXME     value = NumberLiteral(time.mktime(dt.timetuple()))
                        else:
                            raise PrologError('sparql_macro: unknown datatype %s .' % datatype)
                   
                    else:
                        value = unicode(value)

                if not v in res_map:
                    res_map[v] = []
                    res_vars[binding.labels[v]] = v

                res_map[v].append(value)

        logging.debug("sparql_macro: res_map : '%s'" % repr(res_map))
        logging.debug("sparql_macro: res_vars: '%s'" % repr(res_vars))

        # transform bindings into macro mappings

        # v_idx = 0

        # for arg in args[1:]:

        #     sparql_var = res_vars[v_idx]
        #     prolog_var = pe.prolog_get_variable(arg, g.env)
        #     value      = res_map[sparql_var]

        #     # logging.debug("builtin_sparql_query mapping %s -> %s: '%s'" % (sparql_var, prolog_var, value))

        #     g.env[prolog_var] = ListLiteral(value)

        #     v_idx += 1

        mappings = []

        for binding_idx in range(len(res_map[res_vars[0]])):

            mapping = {}

            for i, m in enumerate(args[2:]):

                if not isinstance (m, Variable):
                    raise PrologError (u'sparql_macro: arg %d unexpected type: %s. Variable expected.' % (i+2, m.__class__))

                mapping[m.name] = res_map[res_vars[i]][binding_idx]

            mappings.append(mapping)

        logging.debug ('sparql_macro: resulting mappings: %s' % repr(mappings))

        self.macro_engine.define_named_macro(name, mappings)

    def nlp_gen(self, module_name, clause):

        args = clause.head.args

        lang = args[0].name

        # extract arguments

        nlps  = []
        preds = []

        argc = 1
        while argc < len(args):

            logging.debug ('arg[%d]: %s' % (argc, repr(args[argc])))
            argc += 1

        argc = 1
        while argc < len(args):

            n = args[argc].s
            argc += 1

            p = u''

            while argc < len(args):

                a = args[argc]

                if isinstance (a, Predicate):
                    if a.name == 'nnr':
                        argc += 1
                        break

                    if len(p)>0:
                        p += u';'
                    p += unicode(a)

                elif isinstance (a, StringLiteral):

                    if self.split_utterances:

                        # split strings into individual words
                        # generate one say(lang, word) predicate per word
                        # plus one eou at the end to mark the end of the utterance

                        # make sure we keep punctuation when tokenizing
                        # so tts has a better chance at getting prosody right

                        for token in tokenize(a.s, lang=lang, keep_punctuation=True):

                            t = token.strip()

                            if len(t) == 0:
                                continue

                            if len(p)>0:
                                p += u';'
                            p += u'say(%s, "%s")' % (lang, t)

                        if len(p)>0:
                            p += u';'
                        p += u'eou'

                    else:
                        if len(p)>0:
                            p += u';'
                        p += u'say_eou(%s, "%s")' % (lang, a.s)


                elif isinstance (a, NLPMacroCall):

                    if len(p)>0:
                        p += u';'
                    p += u'@%s:%s' % (a.name, a.pred)

                else:

                    raise PrologError (u'nlp_gen: unexpected argument: %s' % unicode(a))
                    

                logging.debug (u'arg[%d]: %s p: %s' % (argc, repr(args[argc]), p))
                argc += 1

            nlps.append(n)
            preds.append(p)

        # generate all macro-expansions

        ds = self.macro_engine.macro_expand(lang, nlps, preds)

        for d in ds:

            discourse = model.Discourse(num_participants = 2,
                                        lang             = lang,
                                        module           = module_name)
            self.session.add(discourse)

            round_num = 0
            for inp, resp in d:

                if len(inp.strip()) == 0:
                    raise PrologError ('nlp_gen: empty input generated.')

                if self.print_utterances:
                    logging.info(u'inp: %s' % inp)

                dr = model.DiscourseRound(inp       = inp, 
                                          resp      = resp,  
                                          discourse = discourse, 
                                          round_num = round_num)
                self.session.add(dr)

                round_num += 1

    def nlp_test(self, clause):

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
            test_actions = []

            for e in ivr.args:

                if e.name == 'in':
                    test_in = ' '.join(tokenize(e.args[0].s, lang))
                elif e.name == 'out':
                    test_out = ' '.join(tokenize(e.args[0].s, lang))
                elif e.name == 'action':
                    test_actions.append(e.args)
                else:
                    raise PrologError (u'nlp_test: ivr predicate: unexpected arg: ' + unicode(e))
               
            rounds.append((test_in, test_out, test_actions))

            # look up matching discourse_ids:

            d_ids = set()
            
            for dr in self.session.query(model.DiscourseRound).filter(model.DiscourseRound.inp_tokenized==test_in) \
                                                              .filter(model.DiscourseRound.round_num==round_num).all():
                d_ids.add(dr.discourse_id)

            if round_num==0:
                discourse_ids = d_ids
            else:
                discourse_ids = discourse_ids & d_ids

            # print 'discourse_ids:', repr(discourse_ids)

            round_num += 1

        if len(discourse_ids) == 0:
            raise PrologError ('nlp_test: %s: no matching discourse found.' % clause.location)

        nlp_test_parser = PrologParser()

        # run the test(s): look up reaction to input in db, execute it, check result
        for did in discourse_ids:
            self.nlp_test_engine.reset_context()

            round_num = 0
            for dr in self.session.query(model.DiscourseRound).filter(model.DiscourseRound.discourse_id==did) \
                                                              .order_by(model.DiscourseRound.round_num):
            
                prolog_s = ','.join(dr.resp.split(';'))

                logging.info("nlp_test: %s round=%3d, %s => %s" % (clause.location, round_num, dr.inp_tokenized, prolog_s) )

                c = nlp_test_parser.parse_line_clause_body(prolog_s)
                # logging.debug( "Parse result: %s" % c)

                # logging.debug( "Searching for c: %s" % c )

                self.nlp_test_engine.reset_utterances()
                self.nlp_test_engine.reset_actions()
                solutions = self.nlp_test_engine.search(c)

                if len(solutions) == 0:
                    raise PrologError ('nlp_test: %s no solution found.' % clause.location)
            
                # print "round %d utterances: %s" % (round_num, repr(nlp_test_engine.get_utterances())) 

                # check actual utterances vs expected one

                test_in, test_out, test_actions = rounds[round_num]

                utterance_matched = False
                actual_out = ''
                utts = self.nlp_test_engine.get_utterances()

                if len(utts) > 0:
                    for utt in utts:
                        actual_out = ' '.join(tokenize(utt['utterance'], utt['lang']))
                        if actual_out == test_out:
                            utterance_matched = True
                            break
                else:
                    utterance_matched = len(test_out) == 0

                if utterance_matched:
                    if len(utts) > 0:
                        logging.info("nlp_test: %s round=%3d *** UTTERANCE MATCHED!" % (clause.location, round_num))
                else:
                    raise PrologError (u'nlp_test: %s round=%3d actual utterance \'%s\' did not match expected utterance \'%s\'.' % (clause.location, round_num, actual_out, test_out))
                
                # check actions

                if len(test_actions)>0:

                    # print repr(test_actions)

                    actions_matched = True
                    acts = self.nlp_test_engine.get_actions()
                    for action in test_actions:
                        for act in acts:
                            # print "    check action match: %s vs %s" % (repr(action), repr(act))
                            if action == act:
                                break
                        if action != act:
                            actions_matched = False
                            break

                    if actions_matched:
                        logging.info("nlp_test: %s round=%3d *** ACTIONS MATCHED!" % (clause.location, round_num))
                        
                    else:
                        raise PrologError (u'nlp_test: %s round=%3d ACTIONS MISMATCH.' % (clause.location, round_num))

                round_num += 1

    def set_context_default(self, clause):

        solutions = self.nlp_test_engine.search(clause)

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

        self.db.set_context_default(name, key, value)

    def do_compile (self, pl_fn, module_name):

        # quick source line count for progress output below

        linecnt = 0
        with codecs.open(pl_fn, encoding='utf-8', errors='ignore', mode='r') as f:
            while f.readline():
                linecnt += 1
        logging.info("%s: %d lines." % (pl_fn, linecnt))

        # setup compiler / test environment

        self.db           = LogicDB(self.session)

        parser            = PrologParser()

        self.macro_engine = NLPMacroEngine()
        self.kb           = HALKB()

        self.nlp_test_engine = PrologAIEngine(self.db)
        self.nlp_test_engine.set_trace(self.trace)
        self.nlp_test_engine.set_context_name('test')


        with codecs.open(pl_fn, encoding='utf-8', errors='ignore', mode='r') as f:
            parser.start(f, pl_fn)

            while parser.cur_sym != SYM_EOF:
                clauses = parser.clause()

                for clause in clauses:
                    logging.debug(u"%7d / %7d (%3d%%) > %s" % (parser.cur_line, linecnt, parser.cur_line * 100 / linecnt, unicode(clause)))

                    # compiler directive?

                    if clause.head.name == 'nlp_macro':
                        self.nlp_macro(clause)

                    elif clause.head.name == 'sparql_macro':
                        self.sparql_macro(clause)

                    elif clause.head.name == 'nlp_gen':
                        self.nlp_gen(module_name, clause)

                    elif clause.head.name == 'nlp_test':
                        if self.run_tests:
                            self.nlp_test(clause)

                    elif clause.head.name == 'set_context_default':
                        self.set_context_default(clause)

                    else:
                        self.db.store (module_name, clause)

                if parser.comment_pred:

                    self.db.store_doc (module_name, parser.comment_pred, parser.comment)

                    parser.comment_pred = None
                    parser.comment = ''

        logging.info("Compilation succeeded.")

