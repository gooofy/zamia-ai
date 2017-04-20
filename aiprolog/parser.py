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
from time import time
from rdflib.plugins.sparql.parserutils import CompValue

from copy import copy

import model
from nltools.tokenizer import tokenize

from zamiaprolog.parser import PrologParser
from zamiaprolog.errors import PrologError
from zamiaprolog.logic  import *
from nlp_macro_engine   import NLPMacroEngine
from runtime            import AIPrologRuntime

class AIPrologParser(PrologParser):

    def __init__(self, trace = False, print_utterances=False, split_utterances=False, warn_level=0):

        super (AIPrologParser, self).__init__()

        self.trace            = trace
        self.print_utterances = print_utterances
        self.split_utterances = split_utterances
        self.warn_level       = warn_level
        self.test_cnt         = 0

        # register directives

        self.register_directive('nlp_macro',           self.nlp_macro,           None)
        self.register_directive('nlp_gen',             self.nlp_gen,             None)
        self.register_directive('nlp_test',            self.nlp_test,            None)

    def set_trace (self, trace):
        self.trace = trace

    def _get_variable(self, term):
        if not isinstance(term, Variable):
            raise PrologRuntimeError('Variable expected, %s found instead.' % term.__class__)
        return term.name

    def nlp_macro(self, module_name, clause, user_data):

        args = clause.head.args

        name = args[0].s

        macro_vars = map (lambda v: self._get_variable (v), args[1:])

        ai_rt = AIPrologRuntime(self.db, self.kb)

        solutions = ai_rt.search(clause)

        mappings = []

        for solution in solutions:

            mapping = {}
            for v in macro_vars:
                if not v in solution:
                    raise PrologError('Variable %s missing in macro %s solution' % (v, name), clause.location)
                mapping[v] = ai_rt.prolog_get_string (solution[v], {})
        
            mappings.append(mapping)

        self.macro_engine.define_named_macro(name, mappings, module_name, clause.location)

    # nlp_gen(de, 
    #         '@HI:w @ADDRESSEE:w @VERB:w @PLEASE:w @MAL:w @WHAT:w @VERB:v',
    #         @WHAT:p, @VERB:p).

    def nlp_gen(self, module_name, clause, user_data):

        start_time = time()

        logging.debug (u'%fs nlp_gen: %s' % (time()-start_time, clause))

        args = clause.head.args

        if len(args) < 3:
            raise PrologError (u'nlp_gen: at least 3 arguments expected: lang, input, response(s) (got: %s)' % clause, clause.location)

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

        logging.debug ("%fs nlp_gen: %s: generating macro expansions..." % (time()-start_time, clause.location))

        cnt = 0

        ds = self.macro_engine.macro_expand(lang, nlp_input, response, clause.location)

        logging.debug ("%fs nlp_gen: %s: creating discourse rounds..." % (time()-start_time, clause.location))

        rounds = []

        for inp, resp in ds:

            if len(inp.strip()) == 0:
                raise PrologError ('nlp_gen: empty input generated.', clause.location)

            if self.print_utterances:
                logging.info(u'inp: %s' % inp)

            if self.warn_level > 0 :
                # in an ideal world, inputs should be unique
                dr = self.db.session.query(model.DiscourseRound).filter(model.DiscourseRound.inp==inp,  
                                                                        model.DiscourseRound.lang==lang).first()
                if dr:
                    msg = '%s: input not unique: found same input "%s" in module %s (r: %s vs %s)' % (clause.location, inp, dr.module, resp, dr.resp)
                    diff = resp != dr.resp

                    if self.warn_level == 1:
                        if diff:
                            logging.warning (msg) 
                    elif self.warn_level == 2:
                        if diff:
                            raise PrologError(msg, clause.location)
                        else:
                            logging.warning(msg)
                    else:
                        raise PrologError(msg, clause.location)


            rounds.append(model.DiscourseRound( lang      = lang,
                                                module    = module_name,
                                                inp       = inp, 
                                                resp      = resp))
            cnt += 1

        logging.debug (u'%fs nlp_gen: %s bulk save...' % (time()-start_time, clause.location))
        self.db.session.bulk_save_objects(rounds)

        logging.debug (u"%fs nlp_gen: %s: %d generating macro expansions generated." % (time()-start_time, clause.location, cnt))

    def nlp_test(self, module_name, clause, user_data):

        # store test in DB

        name = 'test_%06d' % self.test_cnt
        self.test_cnt += 1

        nlptest = model.NLPTest(module   = module_name,
                                name     = name,
                                test_src = unicode(clause),
                                location = str(clause.location))

        self.db.session.add(nlptest)
        
    def clear_module (self, module_name, db):

        logging.debug ('clearing discourses...')
        db.session.query(model.DiscourseRound).filter(model.DiscourseRound.module==module_name).delete()
        logging.debug ('clearing tests...')
        db.session.query(model.NLPTest).filter(model.NLPTest.module==module_name).delete()
        logging.debug ('clearing macros...')
        db.session.query(model.NLPMacro).filter(model.NLPMacro.module==module_name).delete()

        self.test_cnt = 0

        super(AIPrologParser, self).clear_module(module_name, db)

    def compile_file (self, filename, module_name, db, kb, clear_module=False):

        # setup compiler / test environment

        self.macro_engine = NLPMacroEngine(db.session)
        self.kb           = kb
        self.db           = db

        if clear_module:
            self.clear_module(module_name, db)

        super(AIPrologParser, self).compile_file(filename, module_name, db)

