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
from zamiaprolog.logic   import NumberLiteral, StringLiteral, ListLiteral, Variable, Predicate
from pl2algebra          import arg_to_rdf, prolog_to_filter_expression

import model

from kb import HALKB

def builtin_context(g, pe):

    pe._trace ('CALLED BUILTIN context', g)

    pred = g.terms[g.inx]
    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('context: 2 args expected.')

    key     = args[0].name
    arg_v   = pe.prolog_get_variable(args[1], g.env)

    # currentTime is special in production contexts
    if key=='currentTime' and pe.context_name != 'test':
        v = NumberLiteral(time.time())
    else:
        v = pe.read_context(pe.context_name, key)
        if not v:
            return False

    # print u"builtin_context: %s -> %s" % (key, unicode(v.body))

    g.env[arg_v] = v

    return True

def builtin_set_context(g, pe):

    pe._trace ('CALLED BUILTIN set_context', g)

    pred = g.terms[g.inx]
    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('context: 2 args expected.')

    key   = args[0].name
    value = pe.prolog_eval(args[1], g.env)

    # print u"builtin_set_context: %s -> %s" % (key, unicode(value))
    pe.write_context(pe.context_name, key, value)

    return True

def builtin_say(g, pe):

    pe._trace ('CALLED BUILTIN say', g)

    pred = g.terms[g.inx]
    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('say: 2 args expected.')

    arg_L   = args[0].name
    arg_S   = pe.prolog_get_string(args[1], g.env)

    pe.add_action([Predicate('say'), arg_L, arg_S])

    return True

def builtin_eoa(g, pe):

    pe._trace ('CALLED BUILTIN eoa', g)

    pe.end_action()

    return True

def builtin_say_eoa(g, pe):

    pe._trace ('CALLED BUILTIN say_eoa', g)

    builtin_say(g, pe)
    builtin_eoa(g, pe)

    return True

def builtin_action(g, pe):

    pe._trace ('CALLED BUILTIN action', g)

    pred = g.terms[g.inx]
    args = pred.args

    evaluated_args = map (lambda v: pe.prolog_eval(v, g.env), args)

    pe.add_action(evaluated_args)

    return True

def _literal_rdf2pl(l):

    value    = unicode(l)

    if isinstance (l, rdflib.Literal) :
        if l.datatype:

            datatype = str(l.datatype)

            if datatype == 'http://www.w3.org/2001/XMLSchema#decimal':
                value = NumberLiteral(float(value))
            elif datatype == 'http://www.w3.org/2001/XMLSchema#float':
                value = NumberLiteral(float(value))
            elif datatype == 'http://www.w3.org/2001/XMLSchema#integer':
                value = NumberLiteral(float(value))
            elif datatype == 'http://www.w3.org/2001/XMLSchema#dateTime':
                dt = dateutil.parser.parse(value)
                value = NumberLiteral(time.mktime(dt.timetuple()))
            elif datatype == 'http://www.w3.org/2001/XMLSchema#date':
                dt = dateutil.parser.parse(value)
                value = NumberLiteral(time.mktime(dt.timetuple()))
            else:
                raise PrologRuntimeError('sparql_query: unknown datatype %s .' % datatype)
        else:
            if l.value is None:
                value = ListLiteral([])
            else:
                value = StringLiteral(value)
   
    else:
        value = StringLiteral(value)

    return value
    
def builtin_rdf(g, pe):

    pe._trace ('CALLED BUILTIN rdf', g)

    return _rdf_exec (g, pe)

def builtin_rdf_lists(g, pe):

    pe._trace ('CALLED BUILTIN rdf_lists', g)

    return _rdf_exec (g, pe, generate_lists=True)

def _rdf_exec (g, pe, generate_lists=False):

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
                raise PrologRuntimeError('rdf: optional: triple arg expected')

            arg_s = s_args[0]
            arg_p = s_args[1]
            arg_o = s_args[2]

            logging.debug ('rdf: optional arg triple: %s' %repr((arg_s, arg_p, arg_o)))

            optional_triples.append((arg_to_rdf(arg_s, g.env, pe, var_map, pe.kb), 
                                     arg_to_rdf(arg_p, g.env, pe, var_map, pe.kb), 
                                     arg_to_rdf(arg_o, g.env, pe, var_map, pe.kb)))

            arg_idx += 1

        # check for filter structure
        elif isinstance(arg_s, Predicate) and arg_s.name == 'filter':

            logging.debug ('rdf: filter structure detected: %s' % repr(arg_s.args))

            s_args = arg_s.args

            # transform multiple arguments into explicit and-tree

            pl_expr = s_args[0]
            for a in s_args[1:]:
                pl_expr = Predicate('and', [pl_expr, a])

            filters.append(prolog_to_filter_expression(pl_expr, g.env, pe, var_map, pe.kb))
            
            arg_idx += 1


        # check for distinct
        elif isinstance(arg_s, Predicate) and arg_s.name == 'distinct':

            s_args = arg_s.args
            if len(s_args) != 0:
                raise PrologRuntimeError('rdf: distinct: unexpected arguments.')

            distinct = True
            arg_idx += 1

        # check for limit/offset
        elif isinstance(arg_s, Predicate) and arg_s.name == 'limit':

            s_args = arg_s.args
            if len(s_args) != 1:
                raise PrologRuntimeError('rdf: limit: one argument expected.')

            limit = pe.prolog_get_int(s_args[0], g.env)
            arg_idx += 1

        elif isinstance(arg_s, Predicate) and arg_s.name == 'offset':

            s_args = arg_s.args
            if len(s_args) != 1:
                raise PrologRuntimeError('rdf: offset: one argument expected.')

            offset = pe.prolog_get_int(s_args[0], g.env)
            arg_idx += 1

        else:

            if arg_idx > len(args)-3:
                raise PrologRuntimeError('rdf: not enough arguments for triple')

            arg_p = args[arg_idx+1]
            arg_o = args[arg_idx+2]

            logging.debug ('rdf: arg triple: %s' %repr((arg_s, arg_p, arg_o)))

            triples.append((arg_to_rdf(arg_s, g.env, pe, var_map, pe.kb), 
                            arg_to_rdf(arg_p, g.env, pe, var_map, pe.kb), 
                            arg_to_rdf(arg_o, g.env, pe, var_map, pe.kb)))

            arg_idx += 3

    logging.debug ('rdf: triples: %s' % repr(triples))
    logging.debug ('rdf: optional_triples: %s' % repr(optional_triples))
    logging.debug ('rdf: filters: %s' % repr(filters))

    if len(triples) == 0:
        raise PrologRuntimeError('rdf: at least one non-optional triple expected')

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
    
    result = pe.kb.query_algebra (algebra)

    logging.debug ('rdf: result (len: %d): %s' % (len(result), repr(result)))

    if len(result) == 0:
        return False

    if generate_lists:

        # bind each variable to list of values

        for binding in result:

            for v in binding.labels:

                l = binding[v]

                value = _literal_rdf2pl(l)

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

                value = _literal_rdf2pl(l)

                res_binding[v] = value

            res_bindings.append(res_binding)

        if len(res_bindings) == 0 and len(result)>0:
            res_bindings.append({}) # signal success

        logging.debug ('rdf: res_bindings: %s' % repr(res_bindings))

        return res_bindings

def builtin_uriref(g, pe):

    pe._trace ('CALLED BUILTIN uriref', g)

    pred = g.terms[g.inx]
    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('uriref: 2 args expected.')

    if not isinstance(args[0], Predicate):
        raise PrologRuntimeError('uriref: first argument: predicate expected, %s found instead.' % repr(args[0]))

    if not isinstance(args[1], Variable):
        raise PrologRuntimeError('uriref: second argument: variable expected, %s found instead.' % repr(args[1]))

    g.env[args[1].name] = StringLiteral(pe.kb.resolve_aliases_prefixes(args[0].name))

    return True

def builtin_sparql_query(g, pe):

    pe._trace ('CALLED BUILTIN sparql_query', g)

    pred = g.terms[g.inx]
    args = pred.args
    if len(args) < 1:
        raise PrologRuntimeError('sparql_query: at least 1 argument expected.')

    query = pe.prolog_get_string(args[0], g.env)

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

            value = _literal_rdf2pl(l)

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

class AIPrologRuntime(PrologRuntime):

    def __init__(self, db, kb):

        super(AIPrologRuntime, self).__init__(db)

        # our knowledge base

        self.kb = kb

        # contexts (i.e. global settings stored in DB)

        self.register_builtin('context',         builtin_context)
        self.register_builtin('set_context',     builtin_set_context)
        self.context_name = 'production'

        # topic stack, useful in disambiguation

        # FIXME self.topic_stack   = []
        self.action_score  = 0

        # FIXME self.register_builtin('push_topic',      builtin_push_topic)
        # FIXME self.register_builtin('check_topic',     builtin_check_topic)

        # actions

        self.action_buffer = []

        self.register_builtin('action',          builtin_action)
        self.register_builtin('eoa',             builtin_eoa)      # eoa: End Of Action

        self.register_builtin('say',             builtin_say)      # shortcut for action(say, lang, str)
        self.register_builtin('say_eoa',         builtin_say_eoa)  # shortcut for say followed by eoa

        # sparql / rdf

        self.register_builtin('sparql_query',    builtin_sparql_query)
        self.register_builtin('rdf',             builtin_rdf)
        self.register_builtin('rdf_lists',       builtin_rdf_lists)
        self.register_builtin('uriref',          builtin_uriref)

    def set_context_name(self, context_name):
        self.context_name = context_name

    def reset_actions(self):
        self.action_buffer = []

    def get_actions(self, highscore_only=True):

        if not highscore_only:
            return self.action_buffer

        # determine highest score

        highscore = 0
        for ab in self.action_buffer:
            if ab['score'] > highscore:
                highscore = ab[score]

        # filter out any lower scoring action:

        hs_actions = []
        for ab in self.action_buffer:
            if ab['score'] < highscore:
                continue
            hs_actions.append(ab)
        return hs_actions


    def add_action(self, args):
        
        # do we have an open action?
        n = len(self.action_buffer)
        if n>0 and not self.action_buffer[n-1]['finished']:
            self.action_buffer[n-1]['actions'].append(args)
        else:
            self.action_buffer.append({'finished' : False, 
                                       'actions'  : [args],
                                       'score'    : 0       })
    def end_action(self):
        n = len(self.action_buffer)
        if n>0:
            self.action_buffer[n-1]['finished'] = True
            self.action_buffer[n-1]['score']    = self.action_score
        self.action_score = 0

    #
    # manage stored contexts in db
    #

    def read_context (self, name, key):

        ctx = self.db.session.query(model.Context).filter(model.Context.name==name, model.Context.key==key).first()
        if not ctx:
            return None

        if ctx.prolog_type == 'string':
            return StringLiteral(ctx.value)

        if ctx.prolog_type == 'number':
            return NumberLiteral(float(ctx.value))
        
        if ctx.prolog_type == 'constant':
            return Predicate (ctx.value)

        raise PrologRuntimeError ('Internal error: unknown context type "%s" stored in db.' % ctx.prolog_type)

    def _value_pt(self, value):
        if isinstance(value, StringLiteral):
            pt = 'string'
        elif isinstance(value, NumberLiteral):
            pt = 'number'
        elif isinstance(value, Predicate):
            if len(value.args)>0:
                raise PrologRuntimeError ('Only string/number literals and prolog constants can be stored in contexts, got: %s (%s %s).' % (repr(value), type(value), value.__class__))
            pt = 'constant'
        else:
            raise PrologRuntimeError ('Only string/number literals and prolog constants can be stored in contexts, got: %s (%s %s).' % (repr(value), type(value), value.__class__))
        return pt

    def _value_v(self, value):
        if isinstance(value, StringLiteral):
            v = value.s
        elif isinstance(value, NumberLiteral):
            v = unicode(value.f)
        elif isinstance(value, Predicate):
            if len(value.args)>0:
                raise PrologRuntimeError ('Only string/number literals and prolog constants can be stored in contexts, got: %s (%s %s).' % (repr(value), type(value), value.__class__))
            v = value.name
        else:
            raise PrologRuntimeError ('Only string/number literals and prolog constants can be stored in contexts, got: %s (%s %s).' % (repr(value), type(value), value.__class__))
        return v

    def write_context (self, name, key, value):

        v  = self._value_v(value)
        pt = self._value_pt(value)

        ctx = self.db.session.query(model.Context).filter(model.Context.name==name, model.Context.key==key).first()
        if not ctx:
            ctx = model.Context(name=name, key=key, value=v, default_value=v, prolog_type=pt)
            self.db.session.add(ctx)
        else:
            ctx.value       = v
            ctx.prolog_type = pt

    def set_context_default(self, name, key, value):

        v  = self._value_v(value)
        pt = self._value_pt(value)

        ctx = self.db.session.query(model.Context).filter(model.Context.name==name, model.Context.key==key).first()

        if not ctx:
            ctx = model.Context(name=name, key=key, value=v, default_value=v, prolog_type=pt)
            self.db.session.add(ctx)
        else:
            ctx.default_value = v
            ctx.prolog_type   = pt

    def reset_context(self, name):

        for ctx in self.db.session.query(model.Context).filter(model.Context.name==name).all():
            ctx.value = ctx.default_value
        
