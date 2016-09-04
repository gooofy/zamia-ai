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
# HAL-PROLOG builtin predicates
#

import sys
import datetime
import time
import pytz # $ pip install pytz
from tzlocal import get_localzone # $ pip install tzlocal

from logic import *
from prolog_engine import PrologRuntimeError, prolog_get_int, prolog_get_float, prolog_get_string, \
                          prolog_get_bool, prolog_get_variable, prolog_get_literal

def builtin_cmp_op(g, op):

    pred = g.clause.body[g.inx]
    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('cmp_op: 2 args expected.')

    a = prolog_get_float(args[0], g.env)
    b = prolog_get_float(args[1], g.env)

    res = op(a,b)

    logging.debug("builtin_cmp_op called, g: %s, a:%s, b:%s, res:%s" % (g, a, b, res))

    return res

def builtin_larger(g):           return builtin_cmp_op(g, lambda a,b: a>b)
def builtin_smaller(g):          return builtin_cmp_op(g, lambda a,b: a<b)
def builtin_smaller_or_equal(g): return builtin_cmp_op(g, lambda a,b: a<=b)
def builtin_larger_or_equal(g):  return builtin_cmp_op(g, lambda a,b: a>=b)
def builtin_non_equal(g):        return builtin_cmp_op(g, lambda a,b: a!=b)
def builtin_equal(g):            return builtin_cmp_op(g, lambda a,b: a==b)

def builtin_date_time_stamp(g):

    logging.debug( "builtin_date_time_stamp called, g: %s" % g)

    pred = g.clause.body[g.inx]
    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('date_time_stamp: 2 args expected.')

    if not isinstance(args[0], Predicate) or not args[0].name == 'date' or len(args[0].args) != 7:
        raise PrologRuntimeError('date_time_stamp: arg0: date structure expected.')

    arg_Y   = prolog_get_int(args[0].args[0], g.env)
    arg_M   = prolog_get_int(args[0].args[1], g.env)
    arg_D   = prolog_get_int(args[0].args[2], g.env)
    arg_H   = prolog_get_int(args[0].args[3], g.env)
    arg_Mn  = prolog_get_int(args[0].args[4], g.env)
    arg_S   = prolog_get_int(args[0].args[5], g.env)
    arg_TZ  = prolog_get_string(args[0].args[6], g.env)

    tz = get_localzone() if arg_TZ == 'local' else pytz.timezone(arg_TZ)

    if not isinstance(args[1], Variable):
        raise PrologRuntimeError('date_time_stamp: arg1: variable expected.')

    v = g.env.get(args[1].name)
    if v:
        raise PrologRuntimeError('date_time_stamp: arg1: variable already bound.')
    
    dt = datetime.datetime(arg_Y, arg_M, arg_D, arg_H, arg_Mn, arg_S, tzinfo=tz)
    g.env[args[1].name] = time.mktime(dt.timetuple())

    return True

def builtin_get_time(g):

    logging.debug( "builtin_get_time called, g: %s" % g)

    pred = g.clause.body[g.inx]
    args = pred.args
    if len(args) != 1:
        raise PrologRuntimeError('get_time: 1 arg expected.')

    arg_T   = prolog_get_variable(args[0], g.env)

    dt = datetime.datetime.now()
    g.env[arg_T] = NumberLiteral(time.mktime(dt.timetuple()))

    return True

def builtin_stamp_date_time(g):

    logging.debug ( "builtin_stamp_date_time called, g: %s" % g)

    pred = g.clause.body[g.inx]

    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('stamp_date_time: 2 args expected.')

    if not isinstance(args[1], Predicate) or not args[1].name == 'date' or len(args[1].args) != 7:
        raise PrologRuntimeError('stamp_date_time: arg1: date structure expected.')

    try:
        arg_Y   = prolog_get_variable(args[1].args[0], g.env)
        arg_M   = prolog_get_variable(args[1].args[1], g.env)
        arg_D   = prolog_get_variable(args[1].args[2], g.env)
        arg_H   = prolog_get_variable(args[1].args[3], g.env)
        arg_Mn  = prolog_get_variable(args[1].args[4], g.env)
        arg_S   = prolog_get_variable(args[1].args[5], g.env)
        arg_TZ  = prolog_get_string(args[1].args[6], g.env)

        tz = get_localzone() if arg_TZ == 'local' else pytz.timezone(arg_TZ)

        arg_TS  = prolog_get_float(args[0], g.env)

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

def builtin_say(g):

    logging.debug("builtin_say called, g: %s" % g)

    pred = g.clause.body[g.inx]
    args = pred.args
    if len(args) < 2:
        raise PrologRuntimeError('say: at least 2 args expected.')

    arg_L   = prolog_get_string(args[0], g.env)
    arg_F   = prolog_get_string(args[1], g.env)

    if len(args)>2:
        
        a = map(lambda x: prolog_get_literal(x, g.env), args[2:])

        print
        print "***** SAY(%s): %s" % (arg_L, arg_F % tuple(a))
        print

    else:

        print
        print "***** SAY(%s): %s" % (arg_L, arg_F)
        print

    return True

def register_builtins(engine):

    # arithmetic

    engine.register_builtin('>',    builtin_larger)
    engine.register_builtin('<',    builtin_smaller)
    engine.register_builtin('=<',   builtin_smaller_or_equal)
    engine.register_builtin('>=',   builtin_larger_or_equal)
    engine.register_builtin('=\\=', builtin_non_equal)
    engine.register_builtin('=:=',  builtin_equal)

    # time and date

    engine.register_builtin('date_time_stamp', builtin_date_time_stamp)
    engine.register_builtin('stamp_date_time', builtin_stamp_date_time)
    engine.register_builtin('get_time', builtin_get_time)

    # TTS

    engine.register_builtin('say', builtin_say)

