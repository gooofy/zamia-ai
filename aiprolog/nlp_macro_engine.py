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
# NLP Macro Expansion Engine
#
# persists named macros in our DB (macros are global that way, all macros available in all modules)
# generates all possible macro-expansions of macro-expressions
#

import os
import sys
import logging
import re
import unittest
import json
from copy import copy, deepcopy

from nltools import misc
from nltools.tokenizer  import tokenize
from zamiaprolog.errors import PrologError
from zamiaprolog.parser import NAME_CHARS_EXTENDED

from sqlalchemy.orm import sessionmaker
import model

class NLPMacroEngine(object):

    def __init__(self, session):

        self.named_macros = {}
        self.session      = session

    def define_named_macro(self, name, mappings, module_name, location):
        if not name in self.named_macros:
            self.named_macros[name] = []
        self.named_macros[name].extend(mappings)

        # persist in DB

        nlpm = self.session.query(model.NLPMacro).filter(model.NLPMacro.name==name).first()
        if nlpm:

            if nlpm.module != module_name:
                raise PrologError('macro %s defined in more than one module: %s vs %s' % (name, module_name, nlpm.module), location)

            nlpm.mappings = json.dumps(self.named_macros[name])
        else:
            nlpm = model.NLPMacro (module   = module_name,
                                   name     = name,
                                   mappings = json.dumps(self.named_macros[name]),
                                   location = str(location))
            self.session.add(nlpm)

    def lookup_named_macro (self, name, location):

        if not name in self.named_macros:
            nlpm = self.session.query(model.NLPMacro).filter(model.NLPMacro.name==name).first()
            if not nlpm:
                raise PrologError('undefined macro %s' % name, location)

            self.named_macros[name] = json.loads(nlpm.mappings)

        return self.named_macros[name]

    def macro_expand(self, lang, nlp_input, response, location):

        logging.debug ('macro_expand: nlp_input=%s, response=%s' % (repr(nlp_input), repr(response)))

        # handle implicit macros

        implicit_macros = {}

        nlp_input2 = ''

        i = 0
        while i<len(nlp_input):

            if nlp_input[i] == '(':

                j = nlp_input[i+1:].find(')')
                if j<0:
                    raise PrologError (') missing', location)
                j += i

                # extract macro

                macro_s = nlp_input[i+1:j+1]

                # print "macro_s: %s" % macro_s

                macro_name = 'MACRO_%d' % len(implicit_macros)

                implicit_macros[macro_name] = []
                for s in macro_s.split('|'):
                    implicit_macros[macro_name].append({'W': s.strip()})

                nlp_input2 += '@' + macro_name + ':W '

                i = j+2
            else:

                nlp_input2 += nlp_input[i]
                i+=1

        # print "implicit macros: %s" % repr(implicit_macros)

        # extract all macros used

        nlp_tokens = tokenize (nlp_input2, lang=lang, keep_macros=True)

        #logging.debug('nlp_tokens: %s' % repr(nlp_tokens))

        macro_names = set()

        for i, token in enumerate(nlp_tokens):
            if token[0] != '@':
                continue
            token = token.upper()
            nlp_tokens[i] = token
            parts = token[1:].split(':')
            if len(parts) != 2:
                raise PrologError('invalid macro call detected: %s (@macroname:variable expected)' % token, location)
                
            macro_names.add(parts[0])
                
        #logging.debug('macro names used: %s' % repr(macro_names))

        # generate all macro-expansions

        macro_names = sorted(macro_names)
        todo        = [ (0, {}) ]
        discourses  = []

        while True:

            if len(todo) == 0:
                break

            idx, mappings = todo.pop(0)

            if idx < len(macro_names):

                macro_name = macro_names[idx]

                macro = implicit_macros[macro_name] if macro_name in implicit_macros else self.lookup_named_macro(macro_name, location)

                for v in macro:

                    new_mappings = copy(mappings)
                    new_mappings[macro_name] = v

                    todo.append ( (idx+1, new_mappings) )

            else:

                # generate discourse_round for this set of mappings

                resp_mappings = deepcopy(mappings)

                #logging.debug('mappings: %s' % repr(mappings))

                # process input from left to right, keep track of tokens
                # while expanding macros

                s = []
                for i, token in enumerate(nlp_tokens):

                    if token[0] != '@':
                        s.append(token)
                        continue

                    mexp = token[1:]

                    mparts = mexp.split(':')
                    if len(mparts) != 2:
                        raise PrologError('invalid macro call detected: %s (@macroname:variable expected)' % mexp, location)
                    mname = mparts[0]
                    if not mname in mappings:
                        raise PrologError('undefined macro used: %s' % mname, location)
                    mvar  = mparts[1]
                    if not mvar in mappings[mname]:
                        raise PrologError('undefined macro variable used: %s' % mexp, location)

                    tstart = len(s)
                    s.extend(tokenize(mappings[mname][mvar], lang=lang))
                    tend   = len(s)

                    # logging.debug ('macro detected: "%s", tstart=%d, tend=%d' % (mexp, tstart, tend))
                    # logging.debug ('macro detected: s=%s' % s)

                    #
                    # create TSTART_VAR_OCCURENCE and TEND_VAR_OCCURENCE
                    #

                    occurence = 0
                    while True:
                        tvn = 'TSTART_%s_%s' % (mvar, occurence)
                        if not tvn in resp_mappings[mname]:
                            break
                        occurence += 1

                    resp_mappings[mname][tvn] = str(tstart)
                    tvn = 'TEND_%s_%s' % (mvar, occurence)
                    resp_mappings[mname][tvn] = str(tend)

                #logging.debug('resp_mappings: %s' % repr(resp_mappings))

                s = u' '.join(s)

                p = response

                for k in resp_mappings:
                    for v in resp_mappings[k]:
                        p = p.replace('@'+k+':'+v, resp_mappings[k][v])

                p       = misc.compress_ws(p.lstrip().rstrip())

                discourse = (s, p)
                discourses.append(discourse)

                # logging.debug ('macro_expand:    discourse : %s' % (repr(discourse)))

        return discourses

