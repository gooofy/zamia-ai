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
        self.register_directive('rdf_macro',           self.rdf_macro,           None)
        self.register_directive('sparql_macro',        self.sparql_macro,        None)
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

        mappings = []

        for m in args[1:]:

            if m.name != 'map':
                raise Exception ('map structure expected in nlp_macro %s' % name)

            mapping = {}

            for p in m.args:
                mapping[p.name] = p.args[0].s

            mappings.append(mapping)

        self.macro_engine.define_named_macro(name, mappings)

    def _query_result_to_strings(self, result):

        # turn result into lists of strings we can then bind to macro variables

        res_map  = {} 
        res_vars = {} # variable idx -> variable name

        for binding in result:

            logging.debug(' binding labels: %s' % repr(binding.labels))

            for v in binding.labels:

                l = binding[v]

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

        logging.debug("res_map : '%s'" % repr(res_map))
        logging.debug("res_vars: '%s'" % repr(res_vars))

        return res_map, res_vars

    def rdf_macro(self, module_name, clause, user_data):

        args = clause.head.args

        if not isinstance (args[0], StringLiteral):
            raise PrologError (u'rdf_macro: arg 0 unexpected type: %s. StringLiteral expected.' % args[0].__class__)

        name             = args[0].s

        distinct         = False
        triples          = []
        optional_triples = []
        filters          = []

        arg_idx          = 1
        var_map          = {}   # string -> rdflib.term.Variable
        env              = {}   # we do not have bindings at compile time
        pe               = None # we do not have a runtime at compile time either

        while arg_idx < len(args):

            arg_s = args[arg_idx]

            # check for optional structure
            if isinstance(arg_s, Predicate) and arg_s.name == 'optional':

                s_args = arg_s.args

                if len(s_args) != 3:
                    raise PrologError('rdf: optional: triple arg expected')

                arg_s = s_args[0]
                arg_p = s_args[1]
                arg_o = s_args[2]

                logging.debug ('rdf: optional arg triple: %s' %repr((arg_s, arg_p, arg_o)))

                optional_triples.append((arg_to_rdf(arg_s, env, pe, var_map), 
                                         arg_to_rdf(arg_p, env, pe, var_map), 
                                         arg_to_rdf(arg_o, env, pe, var_map)))

                arg_idx += 1

            # check for filter structure
            elif isinstance(arg_s, Predicate) and arg_s.name == 'filter':

                logging.debug ('rdf: filter structure detected: %s' % repr(arg_s.args))

                s_args = arg_s.args

                if len(s_args) != 1:
                    raise PrologError('rdf: filter: single expression expected')

                filters.append(prolog_to_filter_expression(s_args[0], env, pe, var_map))
                
                arg_idx += 1

            # check for distinct
            elif isinstance(arg_s, Predicate) and arg_s.name == 'distinct':

                distinct = True
                arg_idx += 1

            else:

                if arg_idx > len(args)-3:
                    raise PrologError('rdf: not enough arguments for triple')

                arg_p = args[arg_idx+1]
                arg_o = args[arg_idx+2]

                logging.debug ('rdf: arg triple: %s' %repr((arg_s, arg_p, arg_o)))

                triples.append((arg_to_rdf(arg_s, env, pe, var_map), 
                                arg_to_rdf(arg_p, env, pe, var_map), 
                                arg_to_rdf(arg_o, env, pe, var_map)))

                arg_idx += 3

        logging.debug ('rdf: triples: %s' % repr(triples))
        logging.debug ('rdf: optional_triples: %s' % repr(optional_triples))
        logging.debug ('rdf: filters: %s' % repr(filters))

        if len(triples) == 0:
            raise PrologError('rdf: at least one non-optional triple expected')

        var_list = var_map.values()
        var_set  = set(var_list)

        p = CompValue('BGP', triples=triples, _vars=var_set)

        for t in optional_triples:
            p = CompValue('LeftJoin', p1=p, p2=CompValue('BGP', triples=[t], _vars=var_set),
                                      expr = CompValue('TrueFilter', _vars=set([])))

        for f in filters:
            p = CompValue('Filter', p=p, expr = f, _vars=var_set)

        if distinct:
            p = CompValue('Distinct', p=p, _vars=var_set)

        algebra = CompValue ('SelectQuery', p = p, datasetClause = None, PV = var_list, _vars = var_set)
       
        result = self.kb.query_algebra (algebra)

        logging.debug ('rdf_macro: result (len: %d): %s' % (len(result), repr(result)))

        res_map, res_vars = self._query_result_to_strings(result)

        # transform bindings into macro mappings

        res_var_names = res_map.keys()

        # [ {u'PERSON': u'http://www.wikidata.org/entity/Q2571', 
        #    u'LABEL': u'Walter Scheel'}, 
        #   {u'PERSON': u'http://www.wikidata.org/entity/Q2518', 
        #    u'LABEL': u'Helmut Kohl'}, 
        #   {u'PERSON': u'http://www.wikidata.org/entity/Q2516', 
        #    u'LABEL': u'Helmut Schmidt'} ...]

        mappings = []

        for binding_idx in range(len(res_map[res_vars[0]])):

            mapping = {}

            for res_var_name in res_var_names:

                mapping[res_var_name] = res_map[res_var_name][binding_idx]

            mappings.append(mapping)

        logging.debug ('rdf_macro: resulting mappings: %s' % repr(mappings))

        self.macro_engine.define_named_macro(name, mappings)

    def sparql_macro(self, module_name, clause, user_data):

        args = clause.head.args

        if not isinstance (args[0], StringLiteral):
            raise PrologError (u'sparql_macro: arg 0 unexpected type: %s. StringLiteral expected.' % args[0].__class__)
        if not isinstance (args[1], StringLiteral):
            raise PrologError (u'sparql_macro: arg 1 unexpected type: %s. StringLiteral expected.' % args[0].__class__)

        name  = args[0].s
        query = args[1].s

        result = self.kb.query (query)

        logging.debug ('ran query. resulting bindings: %s' % repr(result.bindings))

        res_map, res_vars = self._query_result_to_strings(result)

        # transform bindings into macro mappings

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
                    # plus one eou at the end to mark the end of the utterance

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
                    response += u'eou'

                else:
                    if len(response)>0:
                        response += u';'
                    response += u'say_eou(%s, "%s")' % (lang, a.s)


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
               
            for dr in self.db.session.query(model.DiscourseRound).filter(model.DiscourseRound.inp==test_in, lang==lang):
            
                prolog_s = ','.join(dr.resp.split(';'))

                logging.info("nlp_test: %s %s => %s" % (clause.location, dr.inp, prolog_s) )
                
                c = nlp_test_parser.parse_line_clause_body(prolog_s)
                # logging.debug( "Parse result: %s" % c)

                # logging.debug( "Searching for c: %s" % c )

                self.ai_rt.reset_utterances()
                self.ai_rt.reset_actions()
                solutions = self.ai_rt.search(c)

                if len(solutions) == 0:
                    raise PrologError ('nlp_test: %s no solution found.' % clause.location)
            
                # print "round %d utterances: %s" % (round_num, repr(ai_rt.get_utterances())) 

                # check actual utterances vs expected one

                utterance_matched = False
                actual_out = ''
                utts = self.ai_rt.get_utterances()

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
                    acts = self.ai_rt.get_actions()
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

        value = unicode(value)

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

