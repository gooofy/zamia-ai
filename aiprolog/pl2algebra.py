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
# helper functions to translate from prolog logic tree to sparqlalchemy algebra
#

import sys
import datetime
import dateutil.parser
import time
import pytz # $ pip install pytz
import rdflib
from rdflib.plugins.sparql.parserutils import CompValue
import logging

from tzlocal import get_localzone # $ pip install tzlocal

from zamiaprolog.errors  import PrologError
from zamiaprolog.logic   import NumberLiteral, StringLiteral, ListLiteral, Variable, Predicate

import model

from kb import HALKB

def arg_to_rdf(term, env, pe, var_map, kb):

    if pe:
        a = pe.prolog_eval(term, env)
    else:
        a = term

    if (not pe or not a) and isinstance (term, Variable):
        if not term.name in var_map:
            var_map[term.name] = rdflib.term.Variable(term.name)
        return var_map[term.name]

    if isinstance (a, Predicate):
        return rdflib.term.URIRef(kb.resolve_aliases_prefixes(a.name))

    if isinstance (a, NumberLiteral):
        return rdflib.term.Literal (str(a.f), datatype=rdflib.namespace.XSD.decimal)

    if isinstance (a, StringLiteral):
        if a.s.startswith('http://'): # a URL/URI/IRI, apparently
            return rdflib.term.URIRef (a.s)
        return rdflib.term.Literal (a.s)
        
    if isinstance (a, ListLiteral):
        if len(a.l) == 0:
            rl = rdflib.term.Literal(None)
            return rl

        raise PrologError('arg_to_rdf: for list literals, only the empty list (representing NULL) is supported.')

    raise PrologError('arg_to_rdf: unknown argument type: %s (%s)' % (a.__class__, repr(a)))

def _prolog_relational_expression (op, args, env, pe, var_map, kb):

    if len(args) != 2:
        raise PrologError ('_prolog_relational_expression: 2 args expected.')

    expr  = prolog_to_filter_expression (args[0], env, pe, var_map, kb)
    other = prolog_to_filter_expression (args[1], env, pe, var_map, kb)

    return CompValue ('RelationalExpression', 
                      op=op, 
                      expr  = expr,
                      other = other,
                      _vars = set(var_map.values()))

def _prolog_conditional_expression (name, args, env, pe, var_map, kb):

    if len(args) != 2:
        raise PrologError ('_prolog_conditional_expression %s: 2 args expected.' % name)

    return CompValue (name, 
                      expr  = prolog_to_filter_expression (args[0], env, pe, var_map, kb),
                      other = [ prolog_to_filter_expression (args[1], env, pe, var_map, kb) ],
                      _vars = set(var_map.values()))

def prolog_to_filter_expression(e, env, pe, var_map, kb):

    if isinstance (e, Predicate):
    
        if e.name == '=':
            return _prolog_relational_expression ('=', e.args, env, pe, var_map, kb)
        elif e.name == '\=':
            return _prolog_relational_expression ('!=', e.args, env, pe, var_map, kb)
        elif e.name == '<':
            return _prolog_relational_expression ('<', e.args, env, pe, var_map, kb)
        elif e.name == '>':
            return _prolog_relational_expression ('>', e.args, env, pe, var_map, kb)
        elif e.name == '=<':
            return _prolog_relational_expression ('<=', e.args, env, pe, var_map, kb)
        elif e.name == '>=':
            return _prolog_relational_expression ('>=', e.args, env, pe, var_map, kb)
        elif e.name == 'is':
            pre = _prolog_relational_expression ('is', e.args, env, pe, var_map, kb)
            return pre
        elif e.name == 'and':
            return _prolog_conditional_expression ('ConditionalAndExpression', e.args, env, pe, var_map, kb)
        elif e.name == 'or':
            return _prolog_conditional_expression ('ConditionalOrExpression', e.args, env, pe, var_map, kb)
        elif e.name == 'lang':
            if len(e.args) != 1:
                raise PrologError ('lang filter expression: one argument expected.')

            return CompValue ('Builtin_LANG', 
                              arg  = prolog_to_filter_expression (e.args[0], env, pe, var_map, kb),
                              _vars = set(var_map.values()))

    return arg_to_rdf (e, env, pe, var_map, kb)

