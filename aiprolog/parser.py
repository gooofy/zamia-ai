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

    def __init__(self, trace = False, print_utterances=False, warn_level=0):

        super (AIPrologParser, self).__init__()

        self.trace            = trace
        self.print_utterances = print_utterances
        self.warn_level       = warn_level
        self.test_cnt         = 0

        # register directives

        self.register_directive('nlp_test',            self.nlp_test,            None)

    def set_trace (self, trace):
        self.trace = trace

    def _get_variable(self, term, location):
        if not isinstance(term, Variable):
            raise PrologError('Variable expected, %s found instead.' % term.__class__, location)
        return term.name

    def nlp_test(self, db, module_name, clause, user_data):

        # store test in DB

        name = 'test_%06d' % self.test_cnt
        self.test_cnt += 1

        nlptest = model.NLPTest(module   = module_name,
                                name     = name,
                                clause   = prolog_to_json(clause))

        self.db.session.add(nlptest)
        
    def clear_module (self, module_name, db):

        logging.debug ('clearing tests...')
        db.session.query(model.NLPTest).filter(model.NLPTest.module==module_name).delete()

        self.test_cnt = 0

        super(AIPrologParser, self).clear_module(module_name, db)

    def compile_file (self, filename, module_name, db, kb, clear_module=False):

        # setup compiler / test environment

        self.kb               = kb
        self.db               = db

        if clear_module:
            self.clear_module(module_name, db)

        super(AIPrologParser, self).compile_file(filename, module_name, db)

