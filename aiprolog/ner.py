#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import logging

from nltools.tokenizer    import tokenize
from nltools.misc         import limit_str
from zamiaprolog.errors   import PrologRuntimeError
from zamiaprolog.logic    import Variable, NumberLiteral, StringLiteral, ListLiteral, Predicate

import model

MAX_NER_RESULTS = 5
 
ner_dict   = {} # lang -> class -> token -> entity -> [idx1, idx2, ...]
 
def _ner_learn(lang, cls, entities, labels):

    global ner_dict

    # import pdb; pdb.set_trace()

    if not lang in ner_dict:
        ner_dict[lang] = {}

    if not cls in ner_dict[lang]:
        ner_dict[lang][cls] = {}

    nd = ner_dict[lang][cls]

    for i, entity in enumerate(entities):

        label = labels[i]

        for j, token in enumerate(tokenize(label, lang=lang)):

            if not token in nd:
                nd[token] = {}

            if not entity in nd[token]:
                nd[token][entity] = set([])

            nd[token][entity].add(j)

            # logging.debug ('ner_learn: %4d %s %s: %s -> %s %s' % (i, entity, label, token, cls, lang))

    cnt = 0
    for token in nd:
        # import pdb; pdb.set_trace()
        # s1 = repr(nd[token])
        # s2 = limit_str(s1, 10)
        logging.debug ('ner_learn: nd[%-20s]=%s' % (token, limit_str(repr(nd[token]), 80)))
        cnt += 1
        if cnt > 10:
            break


    return True

def _ner(lang, cls, tstart, tend, tokens):

    global ner_dict

    nd = ner_dict[lang][cls]

    #
    # start scoring
    #

    max_scores = {}

    for tstart in range (tstart-1, tstart+2):
        if tstart <0:
            continue

        for tend in range (tend-1, tend+2):
            if tend > len(tokens):
                continue
  
            scores = {}

            for tidx in range(tstart, tend):

                toff = tidx-tstart

                # logging.debug('tidx: %d, toff: %d [%d - %d]' % (tidx, toff, tstart, tend))

                token = tokens[tidx]
                if not token in nd:
                    # logging.debug('token %s not in nd %s %s' % (repr(token), repr(lang), repr(cls)))
                    continue

                for entity in nd[token]:

                    if not entity in scores:
                        scores[entity] = 0.0

                    for eidx in nd[token][entity]:
                        points = 2.0-abs(eidx-toff)
                        if points>0:
                            scores[entity] += points

            logging.debug('scores: %s' % repr(scores))

            for entity in scores:
                if not entity in max_scores:
                    max_scores[entity] = scores[entity]
                    continue
                if scores[entity]>max_scores[entity]:
                    max_scores[entity] = scores[entity]

    res = []
    cnt = 0

    # for entity in max_scores:

    for entity, max_score in sorted(max_scores.iteritems(), key=lambda x: x[1], reverse=True):

        res.append((entity, max_score))

        cnt += 1
        if cnt > MAX_NER_RESULTS:
            break

    return res
# 
# def ner_best(ner_res, ias):
#     # FIXME: provide hook(s) for scoring functions
#     return ner_res[0]
# 
# def builtin_ner_learn (g, pe):
# 
#     """ ner_learn (+Lang, +Cat, +Entity, +Label) """
# 
#     pe._trace ('CALLED BUILTIN ner_learn', g)
# 
#     pred = g.terms[g.inx]
#     args = pred.args
#     if len(args) != 4:
#         raise PrologRuntimeError('ner_learn: 4 args expected.', g.location)
# 
#     arg_Lang  = pe.prolog_get_constant (args[0], g.env, g.location)
#     arg_Cat   = pe.prolog_get_constant (args[1], g.env, g.location)
#     arg_Ent   = pe.prolog_get_constant (args[2], g.env, g.location)
#     arg_Label = pe.prolog_get_string   (args[3], g.env, g.location)
# 
#     # import pdb; pdb.set_trace()
# 
#     ner_learn(arg_Lang, arg_Cat, [arg_Ent], [arg_Label])
# 
#     return True

def _build_ner_dict(pe):

    data = {}

    for nerd in pe.db.session.query(model.NERData).all():

        if not nerd.lang in data:
            data[nerd.lang] = {}

        if not nerd.cls in data[nerd.lang]:
            data[nerd.lang][nerd.cls] = ([],[])
           
        data[nerd.lang][nerd.cls][0].append(nerd.entity)
        data[nerd.lang][nerd.cls][1].append(nerd.label)

    for lang in data:
        for cls in data[lang]:
            _ner_learn (lang, cls, data[lang][cls][0], data[lang][cls][1])

def builtin_ner(g, pe):

    global ner_dict

    """ ner (+Lang, +Cat, +TS, +TE, +Tokens, -Entity, -Score) """

    pe._trace ('CALLED BUILTIN ner', g)

    pred = g.terms[g.inx]
    args = pred.args

    if len(args) != 7:
        raise PrologRuntimeError('ner: 7 args ( +Lang, +Cat, +TS, +TE, +Tokens, -Entity, -Score ) expected.', g.location)

    #
    # extract args, tokens
    #

    arg_Lang    = pe.prolog_get_constant(args[0], g.env, g.location)
    arg_Class   = pe.prolog_eval        (args[1], g.env, g.location)
    arg_TStart  = pe.prolog_get_int     (args[2], g.env, g.location)
    arg_TEnd    = pe.prolog_get_int     (args[3], g.env, g.location)
    arg_Tokens  = pe.prolog_get_list    (args[4], g.env, g.location)
    arg_Entity  = pe.prolog_get_variable(args[5], g.env, g.location)
    arg_Score   = pe.prolog_get_variable(args[6], g.env, g.location)

    # import pdb; pdb.set_trace()
    if not ner_dict:
        _build_ner_dict(pe)

    if not arg_Lang in ner_dict:
        raise PrologRuntimeError('ner: lang %s unknown.' % arg_Lang, g.location)

    tokens = map(lambda x: x.s, arg_Tokens.l)

    res = []
    if isinstance(arg_Class, Variable):

        for c in ner_dict[arg_Lang]:

            for entity, score in ner(arg_Lang, c, arg_TStart, arg_TEnd, tokens):

                r = { arg_Class.name : Predicate(c),
                      arg_Entity     : Predicate(entity),
                      arg_Score      : NumberLiteral(score) }
                res.append(r)

    else:

        if not arg_Class.name in ner_dict[arg_Lang]:
            raise PrologRuntimeError('ner: class %s unknown.' % arg_Class.name, g.location)

        for entity, score in _ner(arg_Lang, arg_Class.name, arg_TStart, arg_TEnd, tokens):
            r = { arg_Entity     : Predicate(entity),
                  arg_Score      : NumberLiteral(score) }
            res.append(r)


    return res


