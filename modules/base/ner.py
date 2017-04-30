#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import logging
import rdflib
from rdflib.plugins.sparql.parserutils import CompValue

from zamiaprolog.errors import PrologRuntimeError
from zamiaprolog.logic  import StringLiteral, NumberLiteral
from aiprolog.runtime   import build_algebra, CURIN, KB_PREFIX
from nltools.tokenizer  import tokenize
from nltools.misc       import limit_str
from aiprolog.pl2rdf    import rdf_to_pl

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
ner_labels = {} # lang -> entity -> label

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

    if not arg_Lang in ner_dict:
        ner_dict[arg_Lang] = {}
    if not arg_Lang in ner_labels:
        ner_labels[arg_Lang] = {}

    if not arg_Class in ner_dict[arg_Lang]:
        ner_dict[arg_Lang][arg_Class] = {}

    nd = ner_dict[arg_Lang][arg_Class]
    nl = ner_labels[arg_Lang]

    for i, entity in enumerate(arg_Entity_List.l):

        label = arg_Label_List.l[i]

        nl[entity.s] = label.s

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

def builtin_ner(g, pe):

    global ner_dict

    """ ner ( +Lang, +Class, +TStart, +Tend, -Entity, -Label, -Score ) """

    pe._trace ('CALLED BUILTIN ner', g)

    pred = g.terms[g.inx]
    args = pred.args

    if len(args) != 7:
        raise PrologRuntimeError('ner: 7 args ( +Lang, +Class, +TStart, +Tend, -Entity, -Label, -Score ) expected.', g.location)

    #
    # extract args, tokens
    #

    arg_Lang        = pe.prolog_get_constant(args[0], g.env, g.location)
    arg_Class       = pe.prolog_get_constant(args[1], g.env, g.location)
    arg_TStart      = pe.prolog_get_int     (args[2], g.env, g.location)
    arg_TEnd        = pe.prolog_get_int     (args[3], g.env, g.location)
    arg_Entity      = pe.prolog_get_variable(args[4], g.env, g.location)
    arg_Label       = pe.prolog_get_variable(args[5], g.env, g.location)
    arg_Score       = pe.prolog_get_variable(args[6], g.env, g.location)

    base_score      = g.env[arg_Score].f if arg_Score in g.env else 0.0

    if not arg_Lang in ner_dict:
        raise PrologRuntimeError('ner: lang %s unknown.' % arg_Lang, g.location)
    if not arg_Lang in ner_labels:
        raise PrologRuntimeError('ner: lang %s unknown in labels.' % arg_Lang, g.location)

    if not arg_Class in ner_dict[arg_Lang]:
        raise PrologRuntimeError('ner: class %s unknown.' % arg_Class, g.location)

    nd = ner_dict[arg_Lang][arg_Class]
    nl = ner_labels[arg_Lang]

    quads = pe.kb.filter_quads ( s=CURIN, p=KB_PREFIX+u'tokens')

    tokens = rdf_to_pl(quads[0][2]).l

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
                        scores[entity] = base_score

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

        res.append({
                     arg_Entity: StringLiteral(entity), 
                     arg_Label : StringLiteral(nl[entity]), 
                     arg_Score : NumberLiteral(max_score)
                   })

        cnt += 1
        if cnt > MAX_NER_RESULTS:
            break

    return res


