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
import datetime
import dateutil.parser
import time
import pytz # $ pip install pytz
import rdflib
from rdflib.plugins.sparql.parserutils import CompValue
import logging

from tzlocal import get_localzone # $ pip install tzlocal

from zamiaprolog.runtime import PrologRuntime
from zamiaprolog.errors  import PrologRuntimeError
from zamiaprolog.logic   import NumberLiteral, StringLiteral, ListLiteral, DictLiteral, Variable, Predicate, Clause, SourceLocation
from pl2rdf              import pl_to_rdf, pl_literal_to_rdf, prolog_to_filter_expression, rdf_to_pl
from nltools.tokenizer   import tokenize
from nltools.misc        import edit_distance

import model

CONTEXT_GRAPH_NAME = u'http://ai.zamia.org/context'
KB_PREFIX          = u'http://ai.zamia.org/kb/'
USER_PREFIX        = u'http://ai.zamia.org/kb/user/'
USER_PROP_PREFIX   = u'http://ai.zamia.org/kb/user/prop/'
CURIN              = u'http://ai.zamia.org/kb/curin'
DEFAULT_USER       = USER_PREFIX + u'default'

def builtin_rdf(g, pe):

    pe._trace ('CALLED BUILTIN rdf', g)

    return _rdf_exec (g, pe, g.location)

def builtin_rdf_lists(g, pe):

    pe._trace ('CALLED BUILTIN rdf_lists', g)

    return _rdf_exec (g, pe, g.location, generate_lists=True)

def build_algebra(var_map, triples, optional_triples=[], filters=[], limit=0, offset=0, distinct=False):

    var_list = var_map.values()
    var_set  = set(var_list)

    p = CompValue('BGP', triples=triples, _vars=var_set)

    for t in optional_triples:
        p = CompValue('LeftJoin', p1=p, p2=CompValue('BGP', triples=[t], _vars=var_set),
                                  expr = CompValue('TrueFilter', _vars=set([])))

    for f in filters:
        p = CompValue('Filter', p=p, expr = f, _vars=var_set)

    if limit>0:
        p = CompValue('Slice', start=offset, length=limit, p=p, _vars=var_set)

    if distinct:
        p = CompValue('Distinct', p=p, _vars=var_set)

    algebra = CompValue ('SelectQuery', p = p, datasetClause = None, PV = var_list, _vars = var_set)

    return algebra

def _rdf_exec (g, pe, location, generate_lists=False):

    # rdflib.plugins.sparql.parserutils.CompValue
    #
    # class CompValue(OrderedDict):
    #     def __init__(self, name, **values):
    #
    # SelectQuery(
    #   p =
    #     Project(
    #       p =
    #         LeftJoin(
    #           p2 =
    #             BGP(
    #               triples = [(rdflib.term.Variable(u'leaderobj'), rdflib.term.URIRef(u'http://dbpedia.org/ontology/leader'), rdflib.term.Variable(u'leader'))]
    #               _vars = set([rdflib.term.Variable(u'leaderobj'), rdflib.term.Variable(u'leader')])
    #             )
    #           expr =
    #             TrueFilter(
    #               _vars = set([])
    #             )
    #           p1 =
    #             BGP(
    #               triples = [(rdflib.term.Variable(u'leader'), rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.term.URIRef(u'http://schema.org/Person')), (rdflib.term.Variable(u'leader'), rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#label'), rdflib.term.Variable(u'label'))]
    #               _vars = set([rdflib.term.Variable(u'label'), rdflib.term.Variable(u'leader')])
    #             )
    #           _vars = set([rdflib.term.Variable(u'leaderobj'), rdflib.term.Variable(u'label'), rdflib.term.Variable(u'leader')])
    #         )
    #       PV = [rdflib.term.Variable(u'leader'), rdflib.term.Variable(u'label'), rdflib.term.Variable(u'leaderobj')]
    #       _vars = set([rdflib.term.Variable(u'leaderobj'), rdflib.term.Variable(u'label'), rdflib.term.Variable(u'leader')])
    #     )
    #   datasetClause = None
    #   PV = [rdflib.term.Variable(u'leader'), rdflib.term.Variable(u'label'), rdflib.term.Variable(u'leaderobj')]
    #   _vars = set([rdflib.term.Variable(u'leaderobj'), rdflib.term.Variable(u'label'), rdflib.term.Variable(u'leader')])
    # )

    pred = g.terms[g.inx]
    args = pred.args
    # if len(args) == 0 or len(args) % 3 != 0:
    #     raise PrologRuntimeError('rdf: one or more argument triple(s) expected, got %d args' % len(args))

    distinct         = False
    triples          = []
    optional_triples = []
    filters          = []
    limit            = 0
    offset           = 0

    arg_idx          = 0
    var_map          = {} # string -> rdflib.term.Variable

    while arg_idx < len(args):

        arg_s = args[arg_idx]

        # check for optional structure
        if isinstance(arg_s, Predicate) and arg_s.name == 'optional':

            s_args = arg_s.args

            if len(s_args) != 3:
                raise PrologRuntimeError('rdf: optional: triple arg expected', location)

            arg_s = s_args[0]
            arg_p = s_args[1]
            arg_o = s_args[2]

            logging.debug ('rdf: optional arg triple: %s' %repr((arg_s, arg_p, arg_o)))

            optional_triples.append((pl_to_rdf(arg_s, g.env, pe, var_map, pe.kb, location), 
                                     pl_to_rdf(arg_p, g.env, pe, var_map, pe.kb, location), 
                                     pl_to_rdf(arg_o, g.env, pe, var_map, pe.kb, location)))

            arg_idx += 1

        # check for filter structure
        elif isinstance(arg_s, Predicate) and arg_s.name == 'filter':

            logging.debug ('rdf: filter structure detected: %s' % repr(arg_s.args))

            s_args = arg_s.args

            # transform multiple arguments into explicit and-tree

            pl_expr = s_args[0]
            for a in s_args[1:]:
                pl_expr = Predicate('and', [pl_expr, a])

            filters.append(prolog_to_filter_expression(pl_expr, g.env, pe, var_map, pe.kb, location))
            
            arg_idx += 1


        # check for distinct
        elif isinstance(arg_s, Predicate) and arg_s.name == 'distinct':

            s_args = arg_s.args
            if len(s_args) != 0:
                raise PrologRuntimeError('rdf: distinct: unexpected arguments.', location)

            distinct = True
            arg_idx += 1

        # check for limit/offset
        elif isinstance(arg_s, Predicate) and arg_s.name == 'limit':

            s_args = arg_s.args
            if len(s_args) != 1:
                raise PrologRuntimeError('rdf: limit: one argument expected.', location)

            limit = pe.prolog_get_int(s_args[0], g.env, location)
            arg_idx += 1

        elif isinstance(arg_s, Predicate) and arg_s.name == 'offset':

            s_args = arg_s.args
            if len(s_args) != 1:
                raise PrologRuntimeError('rdf: offset: one argument expected.', location)

            offset = pe.prolog_get_int(s_args[0], g.env, location)
            arg_idx += 1

        else:

            if arg_idx > len(args)-3:
                raise PrologRuntimeError('rdf: not enough arguments for triple', location)

            arg_p = args[arg_idx+1]
            arg_o = args[arg_idx+2]

            logging.debug ('rdf: arg triple: %s' %repr((arg_s, arg_p, arg_o)))

            triples.append((pl_to_rdf(arg_s, g.env, pe, var_map, pe.kb, location), 
                            pl_to_rdf(arg_p, g.env, pe, var_map, pe.kb, location), 
                            pl_to_rdf(arg_o, g.env, pe, var_map, pe.kb, location)))

            arg_idx += 3

    logging.debug ('rdf: triples: %s' % repr(triples))
    logging.debug ('rdf: optional_triples: %s' % repr(optional_triples))
    logging.debug ('rdf: filters: %s' % repr(filters))

    if len(triples) == 0:
        raise PrologRuntimeError('rdf: at least one non-optional triple expected', location)

    algebra = build_algebra(var_map, triples, optional_triples, filters, limit, offset, distinct)
    
    result = pe.kb.query_algebra (algebra)

    logging.debug ('rdf: result (len: %d): %s' % (len(result), repr(result)))

    if len(result) == 0:
        return False

    if generate_lists:

        # bind each variable to list of values

        for binding in result:

            for v in binding.labels:

                l = binding[v]

                value = rdf_to_pl(l)

                if not v in g.env:
                    g.env[v] = ListLiteral([])

                g.env[v].l.append(value)

        return True

    else:

        # turn result into list of bindings

        res_bindings = []
        for binding in result:

            res_binding = {}

            for v in binding.labels:

                l = binding[v]

                value = rdf_to_pl(l)

                res_binding[v] = value

            res_bindings.append(res_binding)

        if len(res_bindings) == 0 and len(result)>0:
            res_bindings.append({}) # signal success

        logging.debug ('rdf: res_bindings: %s' % repr(res_bindings))

        return res_bindings

def builtin_rdf_assert(g, pe):

    """ rdf_assert (+S, +P, +O) """

    pe._trace ('CALLED BUILTIN rdf_assert', g)

    pred = g.terms[g.inx]
    args = pred.args

    if len(args) != 3:
        raise PrologRuntimeError('rdf_assert: 3 args expected, got %d args' % len(args), location)

    arg_s = args[0]
    arg_p = args[1]
    arg_o = args[2]

    quads = [ (pl_to_rdf(arg_s, {}, pe, {}, pe.kb, location), 
               pl_to_rdf(arg_p, {}, pe, {}, pe.kb, location), 
               pl_to_rdf(arg_o, {}, pe, {}, pe.kb, location),
               pe.context_gn) ]

    pe.kb.addN(quads)


def builtin_uriref_fn(pred, env, rt, location):

    """ uriref(+URI) """

    rt._trace_fn ('CALLED FUNCTION uriref', env)

    args = pred.args
    if len(args) != 1:
        raise PrologRuntimeError('uriref: 1 arg (+URI) expected.', location)

    if not isinstance(args[0], Predicate):
        raise PrologRuntimeError('uriref: first argument: predicate expected, %s found instead.' % repr(args[0]), g.location)

    return StringLiteral(rt.kb.resolve_aliases_prefixes(args[0].name))

def builtin_uriref(g, pe):

    pe._trace ('CALLED BUILTIN uriref', g)

    pred = g.terms[g.inx]
    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('uriref: 2 args expected.', g.location)

    if not isinstance(args[0], Predicate):
        raise PrologRuntimeError('uriref: first argument: predicate expected, %s found instead.' % repr(args[0]), g.location)

    if not isinstance(args[1], Variable):
        raise PrologRuntimeError('uriref: second argument: variable expected, %s found instead.' % repr(args[1]), g.location)

    g.env[args[1].name] = StringLiteral(pe.kb.resolve_aliases_prefixes(args[0].name))

    return True

def builtin_sparql_query(g, pe):

    pe._trace ('CALLED BUILTIN sparql_query', g)

    pred = g.terms[g.inx]
    args = pred.args
    if len(args) < 1:
        raise PrologRuntimeError('sparql_query: at least 1 argument expected.', g.location)

    query = pe.prolog_get_string(args[0], g.env, g.location)

    # logging.debug("builtin_sparql_query called, query: '%s'" % query)

    # run query

    result = pe.kb.query (query)

    # logging.debug("builtin_sparql_query result: '%s'" % repr(result))

    if len(result) == 0:
        return False

    # turn result into lists of literals we can then bind to prolog variables

    res_map  = {} 
    res_vars = {} # variable idx -> variable name

    for binding in result:

        for v in binding.labels:

            l = binding[v]

            value = rdf_to_pl(l)

            if not v in res_map:
                res_map[v] = []
                res_vars[binding.labels[v]] = v

            res_map[v].append(value)

    # logging.debug("builtin_sparql_query res_map : '%s'" % repr(res_map))
    # logging.debug("builtin_sparql_query res_vars: '%s'" % repr(res_vars))

    # apply bindings to environment vars

    v_idx = 0

    for arg in args[1:]:

        sparql_var = res_vars[v_idx]
        prolog_var = pe.prolog_get_variable(arg, g.env)
        value      = res_map[sparql_var]

        # logging.debug("builtin_sparql_query mapping %s -> %s: '%s'" % (sparql_var, prolog_var, value))

        g.env[prolog_var] = ListLiteral(value)

        v_idx += 1

    return True

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

    g.env[arg_tokens] = ListLiteral(tokenize(arg_str, lang=arg_lang.name))

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

    def __init__(self, db, kb):

        super(AIPrologRuntime, self).__init__(db)

        # our knowledge base

        self.kb = kb

        # sparql / rdf

        self.register_builtin          ('sparql_query',    builtin_sparql_query)
        self.register_builtin          ('rdf',             builtin_rdf)
        self.register_builtin          ('rdf_lists',       builtin_rdf_lists)
        self.register_builtin          ('rdf_assert',      builtin_rdf_assert)          # rdf_assert (+S, +P, +O)
        self.register_builtin          ('uriref',          builtin_uriref)
        self.register_builtin_function ('uriref',          builtin_uriref_fn)           # uriref(+URI)

        # natural language processing

        self.register_builtin          ('tokenize',        builtin_tokenize)            # tokenize (+Lang, +Str, -Tokens)
        self.register_builtin          ('edit_distance',   builtin_edit_distance)       # edit_distance (+Str1, +Str2, -Distance)


