#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017 Guenter Bartsch
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

from copy                 import deepcopy, copy
from nltools.tokenizer    import tokenize
from zamiaprolog.logic    import NumberLiteral, StringLiteral, ListLiteral, Literal, Variable, Predicate, Clause, SourceLocation
from zamiaprolog.builtins import do_gensym, do_assertz, do_retract
from zamiaprolog.errors   import PrologRuntimeError

#
# very basic utilities
#

def builtin_say (g, pe):

    """ say (+C, +Str) """

    pe._trace ('CALLED BUILTIN say', g)

    pred = g.terms[g.inx]
    args = pred.args
    if len(args) != 2:
        raise PrologRuntimeError('say: 2 args (+C, +Str) expected.', g.location)

    arg_C     = pe.prolog_eval         (args[0], g.env, g.location)
    arg_Str   = pe.prolog_get_string   (args[1], g.env, g.location)

    # figure out language from context

    solutions = pe.search_predicate('lang', [arg_C, 'L'], env=g.env)

    if len(solutions)<1:
        import pdb; pdb.set_trace()
        raise PrologRuntimeError('say: internal error: failed to determine language.', g.location)

    lang = solutions[0]['L'].name

    parts = []
    for p1 in arg_Str.split('{'):
        for p2 in p1.split('}'):
            parts.append(p2)

    res = {}
    cnt = 0
    for part in parts:

        if cnt % 2 == 1:

            subparts = part.split(',')

            if len(subparts)!=2:
                self.report_error ('variable string "%s" not recognized .' % repr(part))

            var_s = subparts[0]
            fmt_s = subparts[1]

            var_v = pe.prolog_eval (Variable(var_s), g.env, g.location)
            
            if isinstance(var_v, StringLiteral):
                v = var_v.s
            else:
                v = unicode(var_v)

            if fmr_s == 'd':
                v = unicode(int(v))
            elif fmt_s == 'f':
                v = unicode(float(v))

            res = do_assertz (g.env, Clause ( Predicate('c_say', [arg_C, StringLiteral(v)]) , location=g.location), res=res)

        else:

            for t in tokenize(part, lang=lang, keep_punctuation=True):
                res = do_assertz (g.env, Clause ( Predicate('c_say', [arg_C, StringLiteral(t)]) , location=g.location), res=res)
        cnt += 1


    return [res]


# FIXME: remove old code below

# def hears(lang, s, txt, label=None):
# 
#     if isinstance (txt, basestring):
#         s1 = copy(s)
#         s1.extend(tokenize(txt, lang=lang))
#         return s1
# 
#     # import pdb; pdb.set_trace()
# 
#     todo = [(txt, 0, [], None, None)]
# 
#     done   = []
# 
#     while todo:
# 
#         # print repr(todo)
# 
#         l, pos, res, tstart, tend = todo.pop()
# 
#         if pos >= len(l):
#             if label:
#                 done.append((res, tstart, tend))
#             else:
#                 done.append(res)
#             continue
# 
#         e = l[pos]
#         if isinstance(e, basestring):
# 
#             if label and e=='$':
#                 tstart = len(res)
#                 tokens = tokenize(label, lang=lang)
#                 tend = tstart + len(tokens)
#             else:
#                 tokens = tokenize(e, lang=lang)
# 
#             res = copy(res)
#             res.extend(tokens)
#             todo.append((l, pos+1, res, tstart, tend))
# 
#         else:
# 
#             for e2 in e:
#                 tokens = tokenize(e2, lang=lang)
#                 res2 = copy(res)
#                 res2.extend(tokens)
#                 todo.append((l, pos+1, res2, tstart, tend))
# 
#     start = s
# 
#     res = []
# 
#     if label:
# 
#         for d, tstart, tend in done:
# 
#             r = deepcopy(start)
# 
#             for token in d:
#                 r.append(token)
# 
#             res.append ((r, tstart, tend))
# 
#     else:
#         for d in done:
# 
#             r = deepcopy(start)
# 
#             for token in d:
#                 r.append(token)
# 
#             res.append (r)
# 
#     return res


# #
# # wikidata related utils
# #
# 
# def entity_label(kernal, lang, entity):
# 
# 
#     res = rdf (kernal, [(entity, 'rdfs:label', 'LABEL')], 
#                distinct=True, limit=1, filters=[ ('=', ('lang', 'LABEL'), lang) ])
# 
#     if len(res)!=1:
#         # try the english label instead
#         res = rdf (kernal, [(entity, 'rdfs:label', 'LABEL')], 
#                    distinct=True, limit=1, filters=[ ('=', ('lang', 'LABEL'), 'en') ])
#         if len(res)!=1:
#             # import pdb; pdb.set_trace()
#             print 'warning: no label found for %s' % entity
#             return 'unknown'
# 
#     # print "entity_label: %s -> %s" % (entity, repr(res))
#     return res[0]['LABEL']
# 
# # is_entity(ENTITY) :-
# #     rdf (limit(1), ENTITY, rdfs:label, LABEL).
#  
# # humans / persons
#  
# # is_human(ENTITY) :- rdf (ENTITY, wdpd:InstanceOf, wde:Human).
#  
# def is_male(kernal, entity):
#     return len( rdf (kernal, [('ENTITY', 'wdpd:SexOrGender', 'wde:Male')]))>0
# def is_female(kernal, entity):
#     return len( rdf (kernal, [('ENTITY', 'wdpd:SexOrGender', 'wde:Female')]))>0
# 
# # entity_gender(ENTITY, GENDER) :- is_male(ENTITY), GENDER is male.
# # entity_gender(ENTITY, GENDER) :- is_female(ENTITY), GENDER is female.
 
