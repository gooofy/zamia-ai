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
# HAL-PROLOG parser with AI specific directives and macros added
#

import os
import sys
import logging
import codecs
import re
import rdflib
from rdflib.plugins.sparql.parserutils import CompValue

from copy import copy

import model
from nltools.tokenizer import tokenize
from kb import HALKB

from zamiaprolog.parser import PrologParser
from zamiaprolog.errors import PrologError
from zamiaprolog.logic  import *
from nlp_macro_engine   import NLPMacroEngine
from runtime            import AIPrologRuntime
from pl2algebra         import prolog_to_filter_expression, arg_to_rdf

TEST_CONTEXT_NAME = 'test'

class AIPrologParser(PrologParser):

    def __init__(self, trace = False, run_tests = False, print_utterances=False, split_utterances=False):

        super (AIPrologParser, self).__init__()

        self.trace            = trace
        self.run_tests        = run_tests
        self.print_utterances = print_utterances
        self.split_utterances = split_utterances

        # register directives

        self.register_directive('nlp_macro',           self.nlp_macro,           None)
        self.register_directive('nlp_gen',             self.nlp_gen,             None)
        self.register_directive('nlp_test',            self.nlp_test,            None)
        self.register_directive('set_context_default', self.set_context_default, None)

    def set_trace (self, trace):
        self.trace = trace

    def set_run_tests (self, run_tests):
        self.run_tests = run_tests

    def nlp_macro(self, module_name, clause, user_data):

        args = clause.head.args

        name = args[0].s

        macro_vars = map (lambda v: self.ai_rt.prolog_get_variable (v, {}), args[1:])
        # for v in args[1:]:
        #     if not isinstance(v, Variable):
        #         raise PrologError('nlp_macro: variable arg expected, %s found instead.' % v)
        #         
        #     macro_vars.append(v.name)

        solutions = self.ai_rt.search(clause)

        mappings = []

        for solution in solutions:

            mapping = {}
            for v in macro_vars:
                mapping[v] = self.ai_rt.prolog_get_string (solution[v], {})
        
            mappings.append(mapping)

        # for m in args[1:]:

        #     if m.name != 'map':
        #         raise Exception ('map structure expected in nlp_macro %s' % name)

        #     mapping = {}

        #     for p in m.args:
        #         mapping[p.name] = p.args[0].s

        #     mappings.append(mapping)

        # import pdb; pdb.set_trace()

        self.macro_engine.define_named_macro(name, mappings)

    # nlp_gen(de, 
    #         '@HI:w @ADDRESSEE:w @VERB:w @PLEASE:w @MAL:w @WHAT:w @VERB:v',
    #         @WHAT:p, @VERB:p).

    def nlp_gen(self, module_name, clause, user_data):

        logging.debug (u'nlp_gen: %s' % clause)

        args = clause.head.args

        if len(args) < 3:
            raise PrologError (u'nlp_gen: at least 3 arguments expected: lang, input, response(s) (got: %s)' % clause)

        lang = args[0].name

        # extract arguments

        nlp_input = args[1].s
        response = u''

        argc = 2

        while argc < len(args):

            a = args[argc]

            if isinstance (a, Predicate):
                if len(response)>0:
                    response += u';'
                response += unicode(a)

            elif isinstance (a, StringLiteral):

                if self.split_utterances:

                    # split strings into individual words
                    # generate one say(lang, word) predicate per word
                    # plus one eoa at the end to mark the end of the utterance

                    # make sure we keep punctuation when tokenizing
                    # so tts has a better chance at getting prosody right

                    for token in tokenize(a.s, lang=lang, keep_punctuation=True):

                        t = token.strip()

                        if len(t) == 0:
                            continue

                        if len(response)>0:
                            response += u';'
                        response += u'say(%s, "%s")' % (lang, t)

                    if len(response)>0:
                        response += u';'
                    response += u'eoa'

                else:
                    if len(response)>0:
                        response += u';'
                    response += u'say_eoa(%s, "%s")' % (lang, a.s)


            elif isinstance (a, MacroCall):

                if len(response)>0:
                    response += u';'
                response += u'@%s:%s' % (a.name, a.pred)

            else:

                raise PrologError (u'nlp_gen: unexpected argument: %s' % unicode(a))
                

            logging.debug (u'arg[%d]: %s response: %s' % (argc, repr(args[argc]), response))
            argc += 1

        # generate all macro-expansions

        ds = self.macro_engine.macro_expand(lang, nlp_input, response)

        for inp, resp in ds:

            if len(inp.strip()) == 0:
                raise PrologError ('nlp_gen: empty input generated.')

            if self.print_utterances:
                logging.info(u'inp: %s' % inp)

            dr = model.DiscourseRound( lang      = lang,
                                       module    = module_name,
                                       inp       = inp, 
                                       resp      = resp)
            self.db.session.add(dr)

    def nlp_test(self, module_name, clause, user_data):

        if not self.run_tests:
            return

        args = clause.head.args

        lang = args[0].name

        # extract test rounds, look up matching discourse_rounds, execute them

        nlp_test_parser = PrologParser()
        self.ai_rt.reset_context(TEST_CONTEXT_NAME)
        round_num = 0
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
               
            logging.info("nlp_test: %s round %d test_in     : %s" % (clause.location, round_num, test_in) )
            logging.info("nlp_test: %s round %d test_out    : %s" % (clause.location, round_num, test_out) )
            logging.info("nlp_test: %s round %d test_actions: %s" % (clause.location, round_num, test_actions) )

            # execute all matching clauses, collect actions

            self.ai_rt.reset_actions()

            for dr in self.db.session.query(model.DiscourseRound).filter(model.DiscourseRound.inp==test_in, lang==lang):
            
                prolog_s = ','.join(dr.resp.split(';'))

                logging.info("nlp_test: %s round %d %s" % (clause.location, round_num, prolog_s) )
                
                c = nlp_test_parser.parse_line_clause_body(prolog_s)
                # logging.debug( "Parse result: %s" % c)

                # logging.debug( "Searching for c: %s" % c )

                solutions = self.ai_rt.search(c)

                # if len(solutions) == 0:
                #     raise PrologError ('nlp_test: %s no solution found.' % clause.location)
            
                # print "round %d utterances: %s" % (round_num, repr(ai_rt.get_utterances())) 

            # check actual actions vs expected ones

            matching_abuf = None

            action_buffers = self.ai_rt.get_actions()
            for abuf in action_buffers:

                logging.info("nlp_test: %s round %d %s" % (clause.location, round_num, repr(abuf)) )

                # check utterance

                actual_out = u''
                utt_lang   = u'en'
                for action in abuf['actions']:
                    p = action[0].name
                    if p == 'say':
                        utt_lang = unicode(action[1])
                        actual_out += u' ' + unicode(action[2])

                if len(test_out) > 0:
                    if len(actual_out)>0:
                        actual_out = u' '.join(tokenize(actual_out, utt_lang))
                    if actual_out != test_out:
                        logging.info("nlp_test: %s round %d UTTERANCE MISMATCH." % (clause.location, round_num))
                        continue # no match

                logging.info("nlp_test: %s round %d UTTERANCE MATCHED!" % (clause.location, round_num))

                # check actions

                if len(test_actions)>0:

                    # import pdb; pdb.set_trace()

                    # print repr(test_actions)

                    actions_matched = True
                    for action in test_actions:
                        for act in abuf['actions']:
                            # print "    check action match: %s vs %s" % (repr(action), repr(act))
                            if action == act:
                                break
                        if action != act:
                            actions_matched = False
                            break

                    if not actions_matched:
                        logging.info("nlp_test: %s round %d ACTIONS MISMATCH." % (clause.location, round_num))
                        continue

                    logging.info("nlp_test: %s round %d ACTIONS MATCHED!" % (clause.location, round_num))

                matching_abuf = abuf
                break

            if not matching_abuf:
                raise PrologError (u'nlp_test: %s round %d no matching abuf found.' % (clause.location, round_num))
           
            self.ai_rt.execute_builtin_actions(matching_abuf)

            round_num += 1


    def set_context_default(self, module_name, clause, user_data):

        solutions = self.ai_rt.search(clause)

        # print "set_context_default: solutions=%s" % repr(solutions)

        if len(solutions) != 1:
            raise PrologError ('set_context_default: need exactly one solution.')

        args = clause.head.args

        name  = args[0].s
        key   = args[1].name

        value = args[2]
        if isinstance (value, Variable):
            value = solutions[0][value.name]

        self.ai_rt.set_context_default(name, key, value)

    def clear_module (self, module_name, db):

        logging.debug ('clearing discourses...')
        db.session.query(model.DiscourseRound).filter(model.DiscourseRound.module==module_name).delete()

        super(AIPrologParser, self).clear_module(module_name, db)

    def compile_file (self, filename, module_name, db, kb, clear_module=False):

        # setup compiler / test environment

        self.macro_engine = NLPMacroEngine()
        self.kb           = kb
        self.db           = db

        self.ai_rt = AIPrologRuntime(db, kb)
        self.ai_rt.set_trace(self.trace)
        self.ai_rt.set_context_name(TEST_CONTEXT_NAME)

        if clear_module:
            self.clear_module(module_name, db)

        super(AIPrologParser, self).compile_file(filename, module_name, db)

