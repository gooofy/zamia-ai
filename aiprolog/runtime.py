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
# HAL-Prolog runtime with builtin predicates for AI use
#

import sys
import logging

from zamiaprolog.runtime import PrologRuntime
from zamiaprolog.errors  import PrologRuntimeError
from zamiaprolog.logic   import NumberLiteral, StringLiteral, ListLiteral, DictLiteral, Variable, Predicate, Clause, SourceLocation
from nltools.tokenizer   import tokenize
from nltools.misc        import edit_distance

import model

USER_PREFIX        = u'user'
DEFAULT_USER       = USER_PREFIX + u'Default'

def builtin_tokenize(g, pe):

    """ tokenize (+Lang, +Str, -Tokens) """

    pe._trace ('CALLED BUILTIN tokenize', g)

    pred = g.terms[g.inx]
    args = pred.args
    if len(args) != 3:
        raise PrologRuntimeError('tokenize: 3 args expected.', g.location)

    arg_lang    = pe.prolog_eval (args[0], g.env, g.location)
    if not isinstance(arg_lang, Predicate) or len(arg_lang.args) >0:
        raise PrologRuntimeError('tokenize: first argument: constant expected, %s found instead.' % repr(args[0]), g.location)

    arg_str     = pe.prolog_get_string   (args[1], g.env, g.location)
    arg_tokens  = pe.prolog_get_variable (args[2], g.env, g.location)

    tokens = map(lambda s: StringLiteral(s), tokenize(arg_str, lang=arg_lang.name))

    g.env[arg_tokens] = ListLiteral(tokens)

    return True

def builtin_edit_distance(g, pe):

    """" edit_distance (+Tokens1, +Tokens2, -Distance) """

    pe._trace ('CALLED BUILTIN edit_distance', g)

    pred = g.terms[g.inx]
    args = pred.args
    if len(args) != 3:
        raise PrologRuntimeError('edit_distance: 3 args expected.', g.location)

    arg_tok1  = pe.prolog_get_list     (args[0], g.env, g.location)
    arg_tok2  = pe.prolog_get_list     (args[1], g.env, g.location)
    arg_dist  = pe.prolog_get_variable (args[2], g.env, g.location)

    g.env[arg_dist] = NumberLiteral(edit_distance(arg_tok1.l, arg_tok2.l))

    return True

class AIPrologRuntime(PrologRuntime):

    def __init__(self, db):

        super(AIPrologRuntime, self).__init__(db)

        # natural language processing

        self.register_builtin          ('tokenize',        builtin_tokenize)            # tokenize (+Lang, +Str, -Tokens)
        self.register_builtin          ('edit_distance',   builtin_edit_distance)       # edit_distance (+Str1, +Str2, -Distance)

    def prolog_eval (self, term, env, location):
        
        """ implement Pseudo-Variables and -Predicates, e.g. USER:NAME """

        if not isinstance (term, Variable) and not isinstance (term, Predicate):
            return super(AIPrologRuntime, self).prolog_eval(term, env, location)
        
        if not (":" in term.name):
            return super(AIPrologRuntime, self).prolog_eval(term, env, location)

        parts = term.name.split(':')

        # import pdb; pdb.set_trace()

        v = parts[0]
        for part in parts[1:]:
            
            solutions = self.search_predicate (part, [v, 'X'], env=env, err_on_missing=False)
            if len(solutions)<1:
                return term
            v = solutions[0]['X']

        return v

