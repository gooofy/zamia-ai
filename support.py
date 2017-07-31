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
# all sorts of support/convenience functions to support python code generated 
#

import sys
import datetime
import dateutil.parser
import time
import pytz # $ pip install pytz
import json
import rdflib
import logging

from rdflib.plugins.sparql.parserutils import CompValue
from copy                              import deepcopy, copy
from tzlocal                           import get_localzone

DT_JSON            = u'http://ai.zamia.org/types/json'

#
# helper functions to translate from python to rdflib and back
#

def rdf_to_py(l):

    value    = unicode(l)

    if isinstance (l, rdflib.Literal) :
        if l.datatype:

            datatype = str(l.datatype)

            if datatype == 'http://www.w3.org/2001/XMLSchema#decimal':
                value = float(value)
            elif datatype == 'http://www.w3.org/2001/XMLSchema#float':
                value = float(value)
            elif datatype == 'http://www.w3.org/2001/XMLSchema#integer':
                value = int(value)
            elif datatype == 'http://www.w3.org/2001/XMLSchema#dateTime':
                value = dateutil.parser.parse(value)
            elif datatype == 'http://www.w3.org/2001/XMLSchema#date':
                value = dateutil.parser.parse(value).replace(tzinfo=get_localzone())
            elif datatype == DT_JSON:
                value = json.loads(value)
            else:
                raise Exception('rdf_to_py: unknown datatype %s .' % datatype)
        else:
            if l.value is None:
                value = None
    return value
    
def py_to_rdf(kb, a, var_map):

    if isinstance (a, basestring) and a[0].isupper():
        if not a in var_map:
            var_map[a] = rdflib.term.Variable(a)
        return var_map[a]

    if isinstance (a, (int, long)):
        return rdflib.term.Literal (str(a), datatype=rdflib.namespace.XSD.integer)

    if isinstance (a, float):
        return rdflib.term.Literal (str(a), datatype=rdflib.namespace.XSD.decimal)

    if isinstance (a, basestring):
        a = kb.resolve_aliases_prefixes(a)
        if a.startswith('http://'): # a URL/URI/IRI, apparently
            return rdflib.term.URIRef (a)
        return rdflib.term.Literal (a)
    
    # FIXME ?
    # if isinstance (a, ListLiteral):
    #     return rdflib.term.Literal (prolog_to_json(a), datatype=DT_JSON)

    # if isinstance (a, DictLiteral):
    #     return rdflib.term.Literal (prolog_to_json(a), datatype=DT_JSON)

    return rdflib.term.Literal (json.dumps(a), datatype=DT_JSON)

def _python_relational_expression (kb, op, args, var_map):

    if len(args) != 2:
        raise Exception ('_python_relational_expression: 2 args expected.')

    expr  = py_to_expr (kb, args[0], var_map)
    other = py_to_expr (kb, args[1], var_map)

    return CompValue ('RelationalExpression', 
                      op=op, 
                      expr  = expr,
                      other = other,
                      _vars = set(var_map.values()))

def _python_conditional_expression (kb, name, args, var_map):

    if len(args) != 2:
        raise Exception ('_python_conditional_expression %s: 2 args expected.' % name)

    return CompValue (name, 
                      expr  =   py_to_expr (kb, args[0], var_map),
                      other = [ py_to_expr (kb, args[1], var_map) ],
                      _vars = set(var_map.values()))
 
def py_to_expr(kb, e, var_map):

    if isinstance (e, tuple):
    
        if e[0] == '=':
            return _python_relational_expression (kb,  '=', e[1:], var_map)
        elif e[0] == '\=':
            return _python_relational_expression (kb, '!=', e[1:], var_map)
        elif e[0] == '<':
            return _python_relational_expression (kb,  '<', e[1:], var_map)
        elif e[0] == '>':
            return _python_relational_expression (kb,  '>', e[1:], var_map)
        elif e[0] == '=<':
            return _python_relational_expression (kb, '<=', e[1:], var_map)
        elif e[0] == '>=':
            return _python_relational_expression (kb, '>=', e[1:], var_map)
        elif e[0] == 'is':
            return _python_relational_expression (kb, 'is', e[1:], var_map)
        elif e[0] == 'and':
            return _python_conditional_expression (kb, 'ConditionalAndExpression', e[1:], var_map)
        elif e[0] == 'or':
            return _python_conditional_expression (kb,  'ConditionalOrExpression', e[1:], var_map)
        elif e[0] == 'lang':
            if len(e) != 2:
                raise Exception ('lang filter expression: one argument expected.')

            return CompValue ('Builtin_LANG', 
                              arg  = py_to_expr (kb, e[1], var_map),
                              _vars = set(var_map.values()))

    return py_to_rdf (kb, e, var_map)

#
# basic RDF / Wikidata utils
#

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

rdf_cache = {} # query -> result

def rdf ( kb, 
          triples          = [],
          distinct         = False,
          optional_triples = [],
          filters          = [],
          limit            = 0,
          offset           = 0):

    global rdf_cache

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

    var_map  = {} # string -> rdflib.term.Variable

    # convert triples/filters to rdflib

    triples          = map(lambda t: (py_to_rdf(kb, t[0], var_map), py_to_rdf(kb, t[1], var_map), py_to_rdf(kb, t[2], var_map)), triples)
    optional_triples = map(lambda t: (py_to_rdf(kb, t[0], var_map), py_to_rdf(kb, t[1], var_map), py_to_rdf(kb, t[2], var_map)), optional_triples)
    filters          = map(lambda f: py_to_expr(kb, f, var_map), filters)

    logging.debug ('rdf: triples: %s' % repr(triples))
    logging.debug ('rdf: optional_triples: %s' % repr(optional_triples))
    logging.debug ('rdf: filters: %s' % repr(filters))

    if len(triples) == 0:
        raise PrologRuntimeError('rdf: at least one non-optional triple expected', location)

    rdf_signature = repr((var_map, triples, optional_triples, filters, limit, offset, distinct))

    if rdf_signature in rdf_cache:
        # print "HIT  _rdf (%s)" % rdf_signature

        result = rdf_cache[rdf_signature]

    else:
        # print "MISS _rdf (%s)" % rdf_signature

        algebra = build_algebra(var_map, triples, optional_triples, filters, limit, offset, distinct)
    
        result = kb.query_algebra (algebra)

        rdf_cache[rdf_signature] = result

    # import pdb; pdb.set_trace()

    logging.debug ('rdf: result (len: %d): %s' % (len(result), repr(result)))

    # turn result into list of dicts

    res_bindings = []
    for binding in result:

        res_binding = {}

        for v in binding.labels:

            l = binding[v]

            value = rdf_to_py(l)

            res_binding[v] = value

        res_bindings.append(res_binding)

    logging.debug ('rdf: res_bindings: %s' % repr(res_bindings))

    return res_bindings

def rdf_get_single ( kernal, s, p, langfilter = None ) :

    # import pdb; pdb.set_trace()

    filters = []
    if langfilter:
        filters = [ ('=', ('lang', 'X'), langfilter) ]

    res = rdf (kernal.kb, triples = [ ( s, p, 'X') ], distinct=True, filters=filters, limit=1)

    if not res:
        return None

    return res[0]

def rdf_set (kernal, s, p, o):

    import pdb; pdb.set_trace()

    s = kernal.kb.resolve_aliases_prefixes(s)
    p = kernal.kb.resolve_aliases_prefixes(p)

    kernal.kb.remove((s, p, None, None))
    kernal.kb.addN([(s, p, o, kernal.context_gn)])

def r_say (context, s):

    r = context['resp']

    if len(r)==0:
        r.append([])

    r[len(r)-1].append(('say', s))

    # print "r_say (%s) called -> %s" % (s, repr(r[len(r)-1]))

def r_bor (context):
    context['resp'].append([])

def r_action (context, a):

    r = context['resp']

    if len(r)==0:
        r.append([])

    r[len(r)-1].append(('action', a))

def r_score (context, s):

    r = context['resp']

    if len(r)==0:
        r.append([])

    r[len(r)-1].append(('score', s))

