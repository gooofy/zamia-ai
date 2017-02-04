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
# generates all possible macro-expansions of macro-expressions
#

import os
import sys
import logging
import re
import unittest
from copy import copy

from nltools import misc
from nltools.tokenizer import tokenize

class NLPMacroEngine(object):

    def __init__(self):

        self.named_macros = {}

    def define_named_macro(self, name, mappings):
        self.named_macros[name] = mappings

    def macro_expand(self, lang, nlps, preds):

        logging.debug ('macro_expand: nlps=%s, preds=%s' % (repr(nlps), repr(preds)))

        # handle implicit macros

        implicit_macros = {}

        nlps2 = []

        for nlp in nlps:

            nlp2 = ''

            i = 0
            while i<len(nlp):

                if nlp[i] == '(':

                    j = nlp[i+1:].find(')')
                    if j<0:
                        raise Exception (') missing')
                    j += i

                    # extract macro

                    macro_s = nlp[i+1:j+1]

                    # print "macro_s: %s" % macro_s

                    macro_name = '__INTERNAL_MACRO_%06d__' % len(implicit_macros)

                    implicit_macros[macro_name] = []
                    for s in macro_s.split('|'):
                        implicit_macros[macro_name].append({'w': s.strip()})

                    nlp2 += '@' + macro_name + ':w '

                    i = j+2
                else:

                    nlp2 += nlp[i]
                    i+=1

            nlps2.append(nlp2)

            # print "after implicit macro handling: %s" % nlp2

        # print "implicit macros: %s" % repr(implicit_macros)

        # extract all macros used

        macro_names = set()

        for nlp in nlps2:

            # print nlp

            for pos, char in enumerate(nlp):

                if char == '@':

                    macro = re.match(r'@([A-Z0-9_]+):', nlp[pos:])

                    # print "MACRO:", macro.group(1)

                    macro_names.add(macro.group(1))

        # print "macro names used: %s" % macro_names

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

                macro_dict = implicit_macros if macro_name in implicit_macros else self.named_macros

                for v in macro_dict[macro_name]:

                    new_mappings = copy(mappings)
                    new_mappings[macro_name] = v

                    todo.append ( (idx+1, new_mappings) )

            else:

                # generate discourse for this set of mappings

                # print 'mappings:', repr(mappings)

                discourse = []

                argc      = 1
                for s, p in zip(nlps2, preds):

                    # print s,p

                    for k in mappings:

                        for v in mappings[k]:

                            s = s.replace('@'+k+':'+v, mappings[k][v])
                            p = p.replace('@'+k+':'+v, mappings[k][v])

                    inp_raw = misc.compress_ws(s.lstrip().rstrip())
                    p       = misc.compress_ws(p.lstrip().rstrip())

                    # print s
                    # print p

                    inp_tokenized = ' '.join(tokenize(inp_raw, lang))

                    discourse.append((inp_tokenized, p))

                logging.debug ('macro_expand:    discourse : %s' % (repr(discourse)))

                discourses.append(discourse)

        return discourses

class TestMacroEngine (unittest.TestCase):

    def setUp(self):
        pass

    def testLocalMacros(self):

        me = NLPMacroEngine()
        me.macro_expand('de', [u'(HAL,|Computer,|Du,|) (Ich bin|Ich fühle mich|Man bin ich|Da bin ich) (zufrieden|so zufrieden|glücklich|so glücklich|froh|so froh)'],[u''])

if __name__ == "__main__":

    unittest.main()

