#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import logging
import rdflib
from rdflib.plugins.sparql.parserutils import CompValue

from zamiaprolog.errors  import PrologRuntimeError
from zamiaprolog.logic   import StringLiteral, NumberLiteral, Predicate, Clause, Variable
from zamiaprolog.runtime import do_assertz
from aiprolog.runtime    import build_algebra, CURIN, KB_PREFIX
from nltools.tokenizer   import tokenize
from nltools.misc        import limit_str
from aiprolog.pl2rdf     import rdf_to_pl

MAX_NER_RESULTS = 5

#     atom_chars(LANG, LSTR),
# 
#     rdf (distinct,
#          PERSON, wdpd:InstanceOf,   wde:Human,
#          PERSON, rdfs:label,        LABEL,
#          PERSON, wdpd:FamilyName,   FN,
#          FN,     rdfs:label,        FAMILY_NAME,
#          filter (lang(LABEL) = LSTR),
#          filter (lang(FAMILY_NAME) = LSTR)),
# 
#     tokenize (LANG, FAMILY_NAME, FN_TOKENS),
# 
#     NAME_TOKENS = FN_TOKENS.

ner_dict   = {} # lang -> class -> token -> entity -> [idx1, idx2, ...]

def builtin_ner_learn(g, pe):

    global ner_dict

    """ ner_learn ( +Lang, +Class, +Entity_List, +Label_List ) """

    pe._trace ('CALLED BUILTIN ner_learn', g)

    pred = g.terms[g.inx]
    args = pred.args

    if len(args) != 4:
        raise PrologRuntimeError('ner_learn: 4 args ( +Lang, +Class, +Entity_List, +Label_List ) expected.', g.location)

    arg_Lang        = pe.prolog_get_constant(args[0], g.env, g.location)
    arg_Class       = pe.prolog_get_constant(args[1], g.env, g.location)
    arg_Entity_List = pe.prolog_get_list(args[2], g.env, g.location)
    arg_Label_List  = pe.prolog_get_list(args[3], g.env, g.location)

    # import pdb; pdb.set_trace()

    if not arg_Lang in ner_dict:
        ner_dict[arg_Lang] = {}

    if not arg_Class in ner_dict[arg_Lang]:
        ner_dict[arg_Lang][arg_Class] = {}

    nd = ner_dict[arg_Lang][arg_Class]

    for i, entity in enumerate(arg_Entity_List.l):

        label = arg_Label_List.l[i]

        # logging.debug ('ner_learn: %4d %s %s' % (i, entity, label))

        for j, token in enumerate(tokenize(label.s, lang=arg_Lang)):

            if not token in nd:
                nd[token] = {}

            if not entity.s in nd[token]:
                nd[token][entity.s] = set([])

            nd[token][entity.s].add(j)

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

def _do_ner(g, pe, arg_Lang, arg_I, arg_Class, arg_TStart, arg_TEnd, arg_Entity) :

    global ner_dict

    nd = ner_dict[arg_Lang][arg_Class]

    tokens = pe.search_predicate('ias', [arg_I, 'tokens', 'TOKENS'], g.env)[0]['TOKENS'].l

    #
    # start scoring
    #

    max_scores = {}

    for tstart in range (arg_TStart-1, arg_TStart+2):
        if tstart <0:
            continue

        for tend in range (arg_TEnd-1, arg_TEnd+2):
            if tend > len(tokens):
                continue
  
            scores = {}

            for tidx in range(tstart, tend):

                toff = tidx-tstart

                logging.debug('tidx: %d, toff: %d [%d - %d]' % (tidx, toff, tstart, tend))

                token = tokens[tidx]
                if not token in nd:
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

        r = { arg_Entity: StringLiteral(entity) }

        clause = Clause (head=Predicate(name='ias', args=[arg_I, Predicate('score'), NumberLiteral(max_score)]), location=g.location)
        do_assertz(g.env, 'ias', clause, res=r)

        res.append(r)

        cnt += 1
        if cnt > MAX_NER_RESULTS:
            break

    return res

def builtin_ner(g, pe):

    global ner_dict

    """ ner ( +Lang, +I, ?Class, +TStart, +Tend, -Entity ) """

    pe._trace ('CALLED BUILTIN ner', g)

    pred = g.terms[g.inx]
    args = pred.args

    if len(args) != 6:
        raise PrologRuntimeError('ner: 6 args ( +Lang, +I, ?Class, +TStart, +Tend, -Entity ) expected.', g.location)

    #
    # extract args, tokens
    #

    arg_Lang    = pe.prolog_get_constant(args[0], g.env, g.location)
    arg_I       = pe.prolog_eval        (args[1], g.env, g.location)
    arg_Class   = pe.prolog_eval        (args[2], g.env, g.location)
    arg_TStart  = pe.prolog_get_int     (args[3], g.env, g.location)
    arg_TEnd    = pe.prolog_get_int     (args[4], g.env, g.location)
    arg_Entity  = pe.prolog_get_variable(args[5], g.env, g.location)

    if not arg_Lang in ner_dict:
        raise PrologRuntimeError('ner: lang %s unknown.' % arg_Lang, g.location)

    if isinstance(arg_Class, Variable):
        # import pdb; pdb.set_trace()

        res = []

        for c in ner_dict[arg_Lang]:

            rs = _do_ner(g, pe, arg_Lang, arg_I, c, arg_TStart, arg_TEnd, arg_Entity)
            for r in rs:

                r[arg_Class.name] = Predicate(c)
                res.append(r)

    else:

        if not arg_Class.name in ner_dict[arg_Lang]:
            raise PrologRuntimeError('ner: class %s unknown.' % arg_Class.name, g.location)

        res = _do_ner(g, pe, arg_Lang, arg_I, arg_Class.name, arg_TStart, arg_TEnd, arg_Entity)

            
    return res

