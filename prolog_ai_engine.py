#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016 Guenter Bartsch
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
# HAL-Prolog engine with builtin predicates for AI use
#

import sys
import datetime
import dateutil.parser
import time
import pytz # $ pip install pytz
from tzlocal import get_localzone # $ pip install tzlocal

from logic import *
from prolog_engine import PrologEngine, PrologRuntimeError

from kb import HALKB

def builtin_cmp_op(g, op, pe):

    pred = g.clause.body[g.inx]
    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('cmp_op: 2 args expected.')

    a = pe.prolog_get_float(args[0], g.env)
    b = pe.prolog_get_float(args[1], g.env)

    res = op(a,b)

    if pe.trace:
        logging.info("builtin_cmp_op called, a=%s, b=%s, res=%s" % (a, b, res))

    return res

def builtin_larger(g, pe):           return builtin_cmp_op(g, lambda a,b: a>b  ,pe)
def builtin_smaller(g, pe):          return builtin_cmp_op(g, lambda a,b: a<b  ,pe)
def builtin_smaller_or_equal(g, pe): return builtin_cmp_op(g, lambda a,b: a<=b ,pe)
def builtin_larger_or_equal(g, pe):  return builtin_cmp_op(g, lambda a,b: a>=b ,pe)
def builtin_non_equal(g, pe):        return builtin_cmp_op(g, lambda a,b: a!=b ,pe)
def builtin_equal(g, pe):            return builtin_cmp_op(g, lambda a,b: a==b ,pe)

def builtin_date_time_stamp(g, pe):

    # logging.debug( "builtin_date_time_stamp called, g: %s" % g)
    pe._trace ('CALLED BUILTIN date_time_stamp', g)

    pred = g.clause.body[g.inx]
    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('date_time_stamp: 2 args expected.')

    if not isinstance(args[0], Predicate) or not args[0].name == 'date' or len(args[0].args) != 7:
        raise PrologRuntimeError('date_time_stamp: arg0: date structure expected.')

    arg_Y   = pe.prolog_get_int(args[0].args[0], g.env)
    arg_M   = pe.prolog_get_int(args[0].args[1], g.env)
    arg_D   = pe.prolog_get_int(args[0].args[2], g.env)
    arg_H   = pe.prolog_get_int(args[0].args[3], g.env)
    arg_Mn  = pe.prolog_get_int(args[0].args[4], g.env)
    arg_S   = pe.prolog_get_int(args[0].args[5], g.env)
    arg_TZ  = pe.prolog_get_string(args[0].args[6], g.env)

    #if pe.trace:
    #    print "BUILTIN date_time_stamp called, Y=%s M=%s D=%s H=%s Mn=%s S=%s TZ=%s" % ( str(arg_Y), str(arg_M), str(arg_D), str(arg_H), str(arg_Mn), str(arg_S), str(arg_TZ))

    tz = get_localzone() if arg_TZ == 'local' else pytz.timezone(arg_TZ)

    if not isinstance(args[1], Variable):
        raise PrologRuntimeError('date_time_stamp: arg1: variable expected.')

    v = g.env.get(args[1].name)
    if v:
        raise PrologRuntimeError('date_time_stamp: arg1: variable already bound.')
    
    dt = datetime.datetime(arg_Y, arg_M, arg_D, arg_H, arg_Mn, arg_S, tzinfo=tz)
    g.env[args[1].name] = NumberLiteral(time.mktime(dt.timetuple()))

    return True

def builtin_get_time(g, pe):

    pe._trace ('CALLED BUILTIN get_time', g)

    pred = g.clause.body[g.inx]
    args = pred.args
    if len(args) != 1:
        raise PrologRuntimeError('get_time: 1 arg expected.')

    arg_T   = pe.prolog_get_variable(args[0], g.env)

    dt = datetime.datetime.now()
    g.env[arg_T] = NumberLiteral(time.mktime(dt.timetuple()))

    return True

def builtin_stamp_date_time(g, pe):

    pe._trace ('CALLED BUILTIN stamp_date_time', g)

    pred = g.clause.body[g.inx]

    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('stamp_date_time: 2 args expected.')

    if not isinstance(args[1], Predicate) or not args[1].name == 'date' or len(args[1].args) != 7:
        raise PrologRuntimeError('stamp_date_time: arg1: date structure expected.')

    try:
        arg_Y   = pe.prolog_get_variable(args[1].args[0], g.env)
        arg_M   = pe.prolog_get_variable(args[1].args[1], g.env)
        arg_D   = pe.prolog_get_variable(args[1].args[2], g.env)
        arg_H   = pe.prolog_get_variable(args[1].args[3], g.env)
        arg_Mn  = pe.prolog_get_variable(args[1].args[4], g.env)
        arg_S   = pe.prolog_get_variable(args[1].args[5], g.env)
        arg_TZ  = pe.prolog_get_string(args[1].args[6], g.env)

        tz = get_localzone() if arg_TZ == 'local' else pytz.timezone(arg_TZ)

        arg_TS  = pe.prolog_get_float(args[0], g.env)

        dt = datetime.datetime.fromtimestamp(arg_TS, tz)

        g.env[arg_Y]  = NumberLiteral(dt.year)
        g.env[arg_M]  = NumberLiteral(dt.month)
        g.env[arg_D]  = NumberLiteral(dt.day)
        g.env[arg_H]  = NumberLiteral(dt.hour)
        g.env[arg_Mn] = NumberLiteral(dt.minute)
        g.env[arg_S]  = NumberLiteral(dt.second)

    except PrologRuntimeError:
        return False

    return True

def builtin_sub_string(g, pe):

    pe._trace ('CALLED BUILTIN sub_string', g)

    pred = g.clause.body[g.inx]
    args = pred.args
    if len(args) != 5:
        raise PrologRuntimeError('sub_string: 5 args expected.')

    arg_String    = pe.prolog_get_string(args[0], g.env)
    arg_Before    = pe.prolog_eval(args[1], g.env)
    arg_Length    = pe.prolog_eval(args[2], g.env) 
    arg_After     = pe.prolog_eval(args[3], g.env)  
    arg_SubString = pe.prolog_eval(args[4], g.env)  

    # FIXME: implement other variants
    if arg_Before:
        if not isinstance (arg_Before, NumberLiteral):
            raise PrologRuntimeError('sub_string: arg_Before: Number expected, %s found instead.' % arg_Before.__class__)
        before = int(arg_Before.f)
        
        if arg_Length:

            if not isinstance (arg_Length, NumberLiteral):
                raise PrologRuntimeError('sub_string: arg_Length: Number expected, %s found instead.' % arg_Length.__class__)
            length = int(arg_Length.f)

            if arg_After:
                raise PrologRuntimeError('sub_string: FIXME: arg_After required to be a variable for now.')
            else:

                var_After = pe.prolog_get_variable(args[3], g.env)
                if var_After != '_':
                    g.env[var_After] = NumberLiteral(len(arg_String) - before - length)

                if arg_SubString:
                    raise PrologRuntimeError('sub_string: FIXME: arg_SubString required to be a variable for now.')
                else:
                    var_SubString = pe.prolog_get_variable(args[4], g.env)

                    if var_SubString != '_':
                        g.env[var_SubString] = StringLiteral(arg_String[before:before + length])

        else:
            raise PrologRuntimeError('sub_string: FIXME: arg_Length required to be a literal for now.')
    else:
        raise PrologRuntimeError('sub_string: FIXME: arg_Before required to be a literal for now.')
        
    return True

def builtin_context(g, pe):

    pe._trace ('CALLED BUILTIN context', g)

    pred = g.clause.body[g.inx]
    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('context: 2 args expected.')

    key     = args[0].name
    arg_v   = pe.prolog_get_variable(args[1], g.env)

    v = pe.db.read_context(pe.context_name, key)
    if not v:
        return False

    # print u"builtin_context: %s -> %s" % (key, unicode(v.body))

    g.env[arg_v] = v.body[0]

    return True

def builtin_set_context(g, pe):

    pe._trace ('CALLED BUILTIN set_context', g)

    pred = g.clause.body[g.inx]
    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('context: 2 args expected.')

    key   = args[0].name
    value = pe.prolog_eval(args[1], g.env)

    # print u"builtin_set_context: %s -> %s" % (key, unicode(value))
    pe.db.write_context(pe.context_name, key, value)

    return True

def builtin_say(g, pe):

    pe._trace ('CALLED BUILTIN say', g)

    pred = g.clause.body[g.inx]
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

    pred = g.clause.body[g.inx]
    args = pred.args

    evaluated_args = map (lambda v: pe.prolog_eval(v, g.env), args)

    pe.add_action(evaluated_args)

    return True

def builtin_sparql_query(g, pe):

    pe._trace ('CALLED BUILTIN sparql_query', g)

    pred = g.clause.body[g.inx]
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

#
# functions
#

def builtin_format_str(pred, env, pe):

    pe._trace_fn ('CALLED FUNCTION format_str', env)

    args  = pred.args
    arg_F = pe.prolog_get_string(args[0], env)

    if len(args)>1:
        
        a = map(lambda x: pe.prolog_get_literal(x, env), args[1:])

        f_str = arg_F % tuple(a)

    else:

        f_str = arg_F

    return StringLiteral(f_str)

def builtin_isoformat(pred, env, pe):

    pe._trace_fn ('CALLED FUNCTION isoformat', env)

    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('isoformat: 2 args expected.')

    arg_TS  = pe.prolog_get_float (args[0], env)
    arg_TZ  = pe.prolog_get_string(args[1], env)

    tz = get_localzone() if arg_TZ == 'local' else pytz.timezone(arg_TZ)

    dt = datetime.datetime.fromtimestamp(arg_TS, tz)

    return StringLiteral(dt.isoformat())

def _builtin_list_lambda (pred, env, pe, l):

    args = pred.args
    if len(args) != 1:
        raise PrologRuntimeError('list builtin fn: 1 arg expected.')

    arg_list = pe.prolog_get_list (args[0], env)

    res = reduce(l, arg_list.l)
    return res, arg_list.l
    # if isinstance(res, (int, float)):
    #     return NumberLiteral(res)
    # else:
    #     return StringLiteral(unicode(res))

def builtin_list_max(pred, env, pe):

    pe._trace_fn ('CALLED FUNCTION list_max', env)

    return _builtin_list_lambda (pred, env, pe, lambda x, y: x if x > y else y)[0]

def builtin_list_min(pred, env, pe):

    pe._trace_fn ('CALLED FUNCTION list_min', env)

    return _builtin_list_lambda (pred, env, pe, lambda x, y: x if x < y else y)[0]

def builtin_list_sum(pred, env, pe):

    pe._trace_fn ('CALLED FUNCTION list_sum', env)

    return _builtin_list_lambda (pred, env, pe, lambda x, y: x + y)[0]

def builtin_list_avg(pred, env, pe):

    pe._trace_fn ('CALLED FUNCTION list_avg', env)

    l_sum, l = _builtin_list_lambda (pred, env, pe, lambda x, y: x + y)

    assert len(l)>0
    return l_sum / NumberLiteral(float(len(l)))


class PrologAIEngine(PrologEngine):

    def __init__(self, db):

        super(PrologAIEngine, self).__init__(db)

        # our knowledge base

        self.kb = HALKB()

        # arithmetic

        self.register_builtin('>',               builtin_larger)
        self.register_builtin('<',               builtin_smaller)
        self.register_builtin('=<',              builtin_smaller_or_equal)
        self.register_builtin('>=',              builtin_larger_or_equal)
        self.register_builtin('=\\=',            builtin_non_equal)
        self.register_builtin('=:=',             builtin_equal)

        # strings

        self.register_builtin('sub_string',      builtin_sub_string)

        # time and date

        self.register_builtin('date_time_stamp', builtin_date_time_stamp)
        self.register_builtin('stamp_date_time', builtin_stamp_date_time)
        self.register_builtin('get_time',        builtin_get_time)

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

        #
        # builtin functions
        #

        self.register_builtin_function ('format_str', builtin_format_str)
        self.register_builtin_function ('isoformat',  builtin_isoformat)

        # lists

        self.register_builtin_function ('list_max',   builtin_list_max)
        self.register_builtin_function ('list_min',   builtin_list_min)
        self.register_builtin_function ('list_sum',   builtin_list_sum)
        self.register_builtin_function ('list_avg',   builtin_list_avg)


    def set_context_name(self, context_name):
        self.context_name = context_name

    def reset_context(self):
        self.db.reset_context(self.context_name)

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

