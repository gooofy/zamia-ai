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
from tzlocal import get_localzone # $ pip install tzlocal

from zamiaprolog.runtime import PrologRuntime
from zamiaprolog.errors  import PrologRuntimeError
from zamiaprolog.logic   import NumberLiteral, StringLiteral, ListLiteral

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

    v = pe.read_context(pe.context_name, key)
    if not v:
        return False

    # print u"builtin_context: %s -> %s" % (key, unicode(v.body))

    g.env[arg_v] = v.body[0]

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

    pe.add_utterance(arg_L, arg_S)

    return True

def builtin_eou(g, pe):

    pe._trace ('CALLED BUILTIN eou', g)

    pe.end_utterance()

    return True

def builtin_say_eou(g, pe):

    pe._trace ('CALLED BUILTIN say_eou', g)

    builtin_say(g, pe)
    builtin_eou(g, pe)

    return True

def builtin_action(g, pe):

    pe._trace ('CALLED BUILTIN action', g)

    pred = g.terms[g.inx]
    args = pred.args

    evaluated_args = map (lambda v: pe.prolog_eval(v, g.env), args)

    pe.add_action(evaluated_args)

    return True

def builtin_sparql_query(g, pe):

    pe._trace ('CALLED BUILTIN sparql_query', g)

    pred = g.terms[g.inx]
    args = pred.args
    if len(args) < 1:
        raise PrologRuntimeError('say: at least 1 argument expected.')

    query = pe.prolog_get_string(args[0], g.env)

    # logging.debug("builtin_sparql_query called, query: '%s'" % query)

    # run query

    result = pe.kb.query (query)

    # logging.debug("builtin_sparql_query result: '%s'" % repr(result))

    # turn result into lists of literals we can then bind to prolog variables

    res_map  = {} 
    res_vars = {} # variable idx -> variable name

    for binding in result:

        for v in binding.labels:

            l = binding[v]

            value    = unicode(l)

            if l.datatype:

                datatype = str(l.datatype)

                if datatype == 'http://www.w3.org/2001/XMLSchema#decimal':
                    value = NumberLiteral(float(value))
                elif datatype == 'http://www.w3.org/2001/XMLSchema#float':
                    value = NumberLiteral(float(value))
                elif datatype == 'http://www.w3.org/2001/XMLSchema#dateTime':
                    dt = dateutil.parser.parse(value)
                    value = NumberLiteral(time.mktime(dt.timetuple()))
                else:
                    raise PrologRuntimeError('sparql_query: unknown datatype %s .' % datatype)
           
            else:
                if l.value is None:
                    value = ListLiteral([])
                else:
                    value = StringLiteral(value)

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

    def __init__(self, db):

        super(AIPrologRuntime, self).__init__(db)

        # our knowledge base

        self.kb = HALKB()

        # contexts

        self.register_builtin('context',         builtin_context)
        self.register_builtin('set_context',     builtin_set_context)

        # TTS

        self.register_builtin('say',             builtin_say)
        self.register_builtin('eou',             builtin_eou)      # eou: End Of Utterance
        self.register_builtin('say_eou',         builtin_say_eou)
        self.utterance_buffer = []

        # actions

        self.register_builtin('action',          builtin_action)

        # sparql
        self.register_builtin('sparql_query',    builtin_sparql_query)

    def set_context_name(self, context_name):
        self.context_name = context_name

    def reset_utterances(self):
        self.utterance_buffer = []

    def get_utterances(self):
        return self.utterance_buffer

    def add_utterance(self, lang, utterance):
        
        n = len(self.utterance_buffer)

        # do we have an open utterance?
        if n>0 and not self.utterance_buffer[n-1]['finished']:
            self.utterance_buffer[n-1]['utterance'] += ' ' + utterance
        else:
            self.utterance_buffer.append({'finished' : False, 
                                          'lang'     : lang,
                                          'utterance': utterance})
    def end_utterance(self):
        n = len(self.utterance_buffer)
        if n>0:
            self.utterance_buffer[n-1]['finished'] = True

    def reset_actions(self):
        self.actions = []

    def add_action(self, args):
        self.actions.append(args)

    def get_actions(self):
        return self.actions
    #
    # manage stored contexts in db
    #

    def read_context (self, name, key):

        ctx = self.db.session.query(model.Context).filter(model.Context.name==name, model.Context.key==key).first()
        if not ctx:
            return None

        return self.parser.parse_line_clause_body(ctx.value)

    def write_context (self, name, key, value):

        v = unicode(value)

        ctx = self.db.session.query(model.Context).filter(model.Context.name==name, model.Context.key==key).first()
        if not ctx:
            ctx = model.Context(name=name, key=key, value=v, default_value=v)
            self.db.session.add(ctx)
        else:
            ctx.value = v

    def set_context_default(self, name, key, value):

        ctx = self.db.session.query(model.Context).filter(model.Context.name==name, model.Context.key==key).first()

        if not ctx:
            ctx = model.Context(name=name, key=key, value=value, default_value=value)
            self.db.session.add(ctx)
        else:
            ctx.default_value = value

    def reset_context(self, name):

        for ctx in self.db.session.query(model.Context).filter(model.Context.name==name).all():
            ctx.value = ctx.default_value
        

