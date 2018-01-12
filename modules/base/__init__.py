#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import logging

from num2words         import num2words
from zamiaprolog.logic import StringLiteral

DEPENDS    = [ 'config' ]

PL_SOURCES = ['time.pl', 'utils.pl']

def transcribe_time_en(dt):

    h12 = dt.hour if dt.hour < 13 else dt.hour - 12

    if dt.minute == 0:
        return u"exactly %d o'clock" % h12
    elif dt.minute == 1:
        return u"one minute past %d" % h12
    elif dt.minute == 15:
        return u"a quarter past %d" % h12
    elif dt.minute == 30:
        return u"half past %d" % h12

    return u"%d minutes past %d" % (dt.minute, h12)

def transcribe_time_de(dt):

    h12 = dt.hour if dt.hour < 13 else dt.hour - 12

    if dt.minute == 0:
        return u"genau %d Uhr" % h12
    elif dt.minute == 1:
        return u"eine Minute nach %d" % h12
    elif dt.minute == 15:
        return u"viertel nach %d" % h12
    elif dt.minute == 30:
        return u"eine halbe Stunde nach %d" % h12

    return u"%d Minuten nach %d" % (dt.minute, h12)

# FIXME: port to python

# def builtin_transcribe_number (g, pe):
# 
#     """ transcribe_number (+Lang, +Case, +N, -N_SCRIPT) """
# 
#     pe._trace ('CALLED BUILTIN transcribe_number', g)
# 
#     # import pdb; pdb.set_trace()
# 
#     pred = g.terms[g.inx]
#     args = pred.args
#     if len(args) != 4:
#         raise PrologRuntimeError('transcribe_number: 4 args expected.', g.location)
# 
#     arg_Lang  = pe.prolog_get_constant (args[0], g.env, g.location)
#     arg_Case  = pe.prolog_get_constant (args[1], g.env, g.location)
#     arg_N     = pe.prolog_get_int      (args[2], g.env, g.location)
#     arg_NSCR  = pe.prolog_get_variable (args[3], g.env, g.location)
# 
#     if arg_Case == 'nominative':
#         res  = num2words(arg_N, ordinal=False, lang=arg_Lang)
#     elif arg_Case == 'ordinal':
#         res  = num2words(arg_N, ordinal=True, lang=arg_Lang)
#     elif arg_Case == 'ordgen':
#         res  = num2words(arg_N, ordinal=True, lang=arg_Lang)
#         if arg_Lang == 'de':
#             res += u'n'
#     else:
#         raise PrologRuntimeError('transcribe_number: case "%s" not recognized.' % arg_Case, g.location)
# 
#     g.env[arg_NSCR] = StringLiteral(res)
# 
#     return True
# 
# def init_module(kernal):
# 
#     # kernal.rt.register_builtin ('transcribe_date', builtin_transcribe_date)   # transcribe_date (+Lang, +Case, +TS, -TS_SCRIPT)
#     kernal.rt.register_builtin ('transcribe_number',  builtin_transcribe_number) # transcribe_number (+Lang, +Case, +N, -N_SCRIPT)
#     # kernal.rt.register_builtin ('ner_learn',         builtin_ner_learn)         # ner_learn (+Lang, +Cat, +Entity, +Label)
#     kernal.rt.register_builtin ('say',               builtin_say)               # say (+C, +Str)

