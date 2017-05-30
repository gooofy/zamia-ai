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

def apply_am (rp, am):

    """ (recursive) helper function applying argument mapping to inlined predicate """

    if type(rp) is list:

        return map (lambda x: apply_am(x, am), rp)

    if isinstance (rp, Predicate):

        return Predicate (rp.name, map (lambda x: apply_am(x, am), rp.args))

    if isinstance (rp, Variable):

        if rp.name in am:
            return am[rp.name]
        else:
            return rp

    return rp

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
        self.register_directive('nlp_gens',            self.nlp_gens,            None)
        self.register_directive('nlp_test',            self.nlp_test,            None)

    def set_trace (self, trace):
        self.trace = trace

    def _get_variable(self, term, location):
        if not isinstance(term, Variable):
            raise PrologError('Variable expected, %s found instead.' % term.__class__, location)
        return term.name

    def nlp_macro(self, db, module_name, clause, user_data):

        args = clause.head.args

        if len(args) < 3:
            raise PrologError('nlp_macro: at least 3 args expected (+Lang, +MacroName, Vars...)', clause.location)
        
        if not isinstance(args[0], Predicate):
            raise PrologError('nlp_macro: arg 0: +Lang expected (e.g. en, de)', clause.location)

        lang = args[0].name
        name = args[1].s

        macro_vars = map (lambda v: self._get_variable (v, clause.location), args[2:])

        ai_rt = AIPrologRuntime(self.db, self.kb)

        solutions = ai_rt.search(clause)

        mappings = []

        for solution in solutions:

            mapping = {}
            for v in macro_vars:
                if not v in solution:
                    raise PrologError('Variable %s missing in macro %s solution' % (v, name), clause.location)
                mapping[v] = ai_rt.prolog_get_string (solution[v], {}, clause.location)
        
            mappings.append(mapping)

        self.macro_engine.define_named_macro(lang, name, mappings, module_name, clause.location)

    # nlp_gen(de, 
    #         '@HI:w @ADDRESSEE:w @VERB:w @PLEASE:w @MAL:w @WHAT:w @VERB:v',
    #         @WHAT:p, @VERB:p).

    def nlp_gen(self, db, module_name, clause, user_data):

        start_time = time()

        logging.debug (u'%fs nlp_gen: %s' % (time()-start_time, clause))

        args = clause.head.args

        if len(args) < 3:
            raise PrologError (u'nlp_gen: at least 3 arguments expected: lang, input, response(s) (got: %s)' % clause, clause.location)

        lang = args[0].name

        # extract arguments

        nlp_input = args[1].s
        response = u''

        response_parts = args[2:]

        # import pdb; pdb.set_trace()

        # response part could be inlined
        if len(response_parts)==1 and isinstance (response_parts[0], Predicate) and (response_parts[0].name==u'inline'):

            p_inl = response_parts[0]
            if len(p_inl.args) < 1 or not isinstance(p_inl.args[0], Predicate):
                raise PrologError (u'nlp_gen: inline expects at least one argument (predicate name, got: %s)' % clause, clause.location)
                
            p = p_inl.args[0]

            clauses = db.lookup (p.name)

            if len(clauses) == 0:
                raise PrologError (u'nlp_gen: inline predicate %s not found' % p.name, clause.location)
            if len(clauses) > 1:
                raise PrologError (u'nlp_gen: inline predicate %s not unique' % p.name, clause.location)

            h = clauses[0].head
            if len(h.args) != len(p_inl.args)-1:
                raise PrologError (u'nlp_gen: inline need %d additional args besides predicate name' % len(h.args), clause.location)

            am = {} # formal -> actual

            for i in range(len(h.args)):
                am[h.args[i].name] = p_inl.args[i+1]
                
            c = clauses[0].body
            if isinstance(c, Predicate) and c.name == 'and':
                response_parts = c.args
            else:
                response_parts = [c]
           
            response_parts = apply_am(response_parts, am)

        argc = 0
        num_string_literals = 0

        while argc < len(response_parts):

            a = response_parts[argc]

            if isinstance (a, Predicate):
                if len(response)>0:
                    response += u';'
                response += unicode(a)

            elif isinstance (a, MacroCall):

                if len(response)>0:
                    response += u';'
                response += u'@%s:%s' % (a.name, a.pred)

            else:

                raise PrologError (u'nlp_gen: unexpected response part: %s' % unicode(a), clause.location)
                

            logging.debug (u'arg[%d]: %s response: %s' % (argc, repr(response_parts[argc]), response))
            argc += 1

        # generate all macro-expansions

        logging.debug ("%fs nlp_gen: %s: generating macro expansions..." % (time()-start_time, clause.location))

        cnt = 0

        ds = self.macro_engine.macro_expand(lang, nlp_input, response, clause.location)

        logging.debug ("%fs nlp_gen: %s: creating discourse rounds..." % (time()-start_time, clause.location))

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


            self.discourse_rounds.append(model.DiscourseRound( lang      = lang,
                                                               module    = module_name,
                                                               inp       = inp, 
                                                               resp      = resp,
                                                               loc_fn    = clause.location.fn, 
                                                               loc_line  = clause.location.line,
                                                               loc_col   = clause.location.col
                                                               ))
            cnt += 1

        logging.debug (u"%fs nlp_gen: %s: %d generating macro expansions generated." % (time()-start_time, clause.location, cnt))

    def nlp_gens(self, db, module_name, clause, user_data):

        """ nlp_gens (+Lang, +Input, +Responses...) """

        args = clause.head.args

        if len(args) < 3:
            raise PrologError (u'nlp_gens: at least 3 arguments expected: +Lang, +Input, +Responses... (got: %s)' % clause, clause.location)

        lang = args[0].name

        # extract arguments

        nlp_input = args[1].s
        responses = []

        response_parts = args[2:]

        argc = 0

        while argc < len(response_parts):

            a = response_parts[argc]

            if isinstance (a, StringLiteral):

                if self.split_utterances:

                    # split strings into individual words
                    # generate one say(lang, word) predicate per word
                    # plus one eoa at the end to mark the end of the utterance

                    # make sure we keep punctuation when tokenizing
                    # so tts has a better chance at getting prosody right

                    response = u''

                    for token in tokenize(a.s, lang=lang, keep_punctuation=True):

                        t = token.strip()

                        if len(t) == 0:
                            continue

                        if len(response)>0:
                            response += u';'
                        response += u'sayz(I, %s, "%s")' % (lang, t)

                    responses.append(response)

                else:
                    responses.append(u'sayz(I, %s, "%s")' % (lang, a.s))

            else:
                raise PrologError (u'nlp_gens: unexpected response part: %s' % unicode(a), clause.location)

            argc += 1

        # generate all macro-expansions

        cnt = 0

        for response in responses:

            ds = self.macro_engine.macro_expand(lang, nlp_input, response, clause.location)

            for inp, resp in ds:

                if len(inp.strip()) == 0:
                    raise PrologError ('nlp_gens: empty input generated.', clause.location)

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


                self.discourse_rounds.append(model.DiscourseRound( lang      = lang,
                                                                   module    = module_name,
                                                                   inp       = inp, 
                                                                   resp      = resp,
                                                                   loc_fn    = clause.location.fn, 
                                                                   loc_line  = clause.location.line,
                                                                   loc_col   = clause.location.col
                                                                   ))
                cnt += 1

    def nlp_test(self, db, module_name, clause, user_data):

        # store test in DB

        name = 'test_%06d' % self.test_cnt
        self.test_cnt += 1

        nlptest = model.NLPTest(module   = module_name,
                                name     = name,
                                clause   = prolog_to_json(clause))

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

        self.macro_engine     = NLPMacroEngine(db.session)
        self.kb               = kb
        self.db               = db
        self.discourse_rounds = []

        if clear_module:
            self.clear_module(module_name, db)

        super(AIPrologParser, self).compile_file(filename, module_name, db)

        if self.discourse_rounds:

            # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

            start_time = time()
            logging.info (u'bulk saving %d discourse rounds to db...' % len(self.discourse_rounds))
            self.db.session.bulk_save_objects(self.discourse_rounds)
            self.db.commit()
            logging.info (u'bulk saving %d discourse rounds to db... done. Took %fs.' % (len(self.discourse_rounds), time()-start_time))

