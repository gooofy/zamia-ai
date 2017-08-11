#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from num2words         import num2words
from zamiaprolog.logic import StringLiteral
from base.ner          import builtin_ner_learn, builtin_ner
from base.utils        import builtin_say

DEPENDS    = [ 'config' ]

AIP_SOURCES = ['time.aip', 'conversation.aip']

# NLP_DAY_OF_THE_WEEK_LABEL = {
#     'en': { 0: 'Monday',
#             1: 'Tuesday',
#             2: 'Wednesday',
#             3: 'Thursday',
#             4: 'Friday',
#             5: 'Saturday',
#             6: 'Sunday'},
# 
#     'de': { 0: 'Montag',
#             1: 'Dienstag',
#             2: 'Mittwoch',
#             3: 'Donnerstag',
#             4: 'Freitag',
#             5: 'Samstag',
#             6: 'Sonntag'} }
# 
# 
# NLP_MONTH_LABEL = {
#     'en': { 1: 'January',
#             2: 'February',
#             3: 'March',
#             4: 'April',
#             5: 'May',
#             6: 'June',
#             7: 'July',
#             8: 'August',
#             9: 'September',
#            10: 'October',
#            11: 'November',
#            12: 'December'},
# 
#     'de': { 1: 'Januar',
#             2: 'Februar',
#             3: 'März',
#             4: 'April',
#             5: 'Mai',
#             6: 'Juni',
#             7: 'Juli',
#             8: 'August',
#             9: 'September',
#            10: 'Oktober',
#            11: 'November',
#            12: 'Dezember'}}

def builtin_transcribe_number (g, pe):

    """ transcribe_number (+Lang, +Case, +N, -N_SCRIPT) """

    pe._trace ('CALLED BUILTIN transcribe_number', g)

    # import pdb; pdb.set_trace()

    pred = g.terms[g.inx]
    args = pred.args
    if len(args) != 4:
        raise PrologRuntimeError('transcribe_number: 4 args expected.', g.location)

    arg_Lang  = pe.prolog_get_constant (args[0], g.env, g.location)
    arg_Case  = pe.prolog_get_constant (args[1], g.env, g.location)
    arg_N     = pe.prolog_get_int      (args[2], g.env, g.location)
    arg_NSCR  = pe.prolog_get_variable (args[3], g.env, g.location)

    if arg_Case == 'nominative':
        res  = num2words(arg_N, ordinal=False, lang=arg_Lang)
    elif arg_Case == 'ordinal':
        res  = num2words(arg_N, ordinal=True, lang=arg_Lang)
    elif arg_Case == 'ordgen':
        res  = num2words(arg_N, ordinal=True, lang=arg_Lang)
        if arg_Lang == 'de':
            res += u'n'
    else:
        raise PrologRuntimeError('transcribe_number: case "%s" not recognized.' % arg_Case, g.location)

    g.env[arg_NSCR] = StringLiteral(res)

    return True

# def builtin_transcribe_date (g, pe):
# 
#     """ transcribe_date (+Lang, +Case, +TS, -TS_SCRIPT) """
# 
#     pe._trace ('CALLED BUILTIN transcribe_date', g)
# 
#     import pdb; pdb.set_trace()
# 
#     pred = g.terms[g.inx]
#     args = pred.args
#     if len(args) != 4:
#         raise PrologRuntimeError('transcribe_date: 4 args expected.', g.location)
# 
#     arg_Lang  = pe.prolog_get_constant (args[0], g.env, g.location)
#     arg_Case  = pe.prolog_get_constant (args[1], g.env, g.location)
#     arg_TS    = pe.prolog_get_string   (args[2], g.env, g.location)
#     arg_TSCR  = pe.prolog_get_variable (args[3], g.env, g.location)
# 
# 
# 
# 
#     g.env[arg_TSCR] = StringLiteral(res)
# 
#     return True

def init_module(kernal):

    # kernal.rt.register_builtin ('transcribe_date', builtin_transcribe_date)   # transcribe_date (+Lang, +Case, +TS, -TS_SCRIPT)
    kernal.rt.register_builtin ('transcribe_number', builtin_transcribe_number) # transcribe_number (+Lang, +Case, +N, -N_SCRIPT)
    kernal.rt.register_builtin ('ner_learn',         builtin_ner_learn)         # ner_learn (+Lang, +Cat, +Entity, +Label)
    kernal.rt.register_builtin ('ner',               builtin_ner)               # ner (+Lang, +Cat, +TS, +TE, +Tokens, -Entity, -Score)
    kernal.rt.register_builtin ('say',               builtin_say)               # say (+C, +Str)

