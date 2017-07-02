#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from copy                 import deepcopy, copy

from nltools.tokenizer    import tokenize
from rdf                  import rdf

#
# very basic utilities
#

def hears(lang, s, txt):
    s1 = copy(s)
    s1.extend(tokenize(txt, lang=lang))
    return s1

def says (lang, r, txt):
    r1 = copy(r)
    # for t in tokenize(txt, lang=lang):
    #     r1.append(u"say('%s', '%s')" % (lang, t))

    parts1 = txt.split('%')
    cnt = 0

    l = []

    for p1 in parts1:

        o = 0

        if cnt > 0:
           
            o += 2

            while p1[o] != ')':
                o += 1

            var_name = p1[1:o]
            o += 1

            format_char = p1[o]
            r1.append(['sayv', lang, var_name, format_char])

            o += 1

        parts2 = tokenize(p1[o:], lang=lang, keep_punctuation=True)

        for p2 in parts2:
            r1.append(['say', lang, p2])

        cnt += 1
    
    return r1

#
# wikidata / rdf related utils
#
 
# entity_label(LANG, ENTITY, LABEL) :-
#     atom_chars(LANG, LSTR),
#     rdf (distinct,
#          ENTITY, rdfs:label, LABEL,
#          filter (lang(LABEL) = LSTR)).
# 
# is_entity(ENTITY) :-
#     rdf (limit(1), ENTITY, rdfs:label, LABEL).
 
# humans / persons
 
# is_human(ENTITY) :- rdf (ENTITY, wdpd:InstanceOf, wde:Human).
 
# is_male(ENTITY) :- rdf (ENTITY, wdpd:SexOrGender, wde:Male).
# is_female(ENTITY) :- rdf (ENTITY, wdpd:SexOrGender, wde:Female). 
 
# entity_gender(ENTITY, GENDER) :- is_male(ENTITY), GENDER is male.
# entity_gender(ENTITY, GENDER) :- is_female(ENTITY), GENDER is female.
 
#
# score/action utilities (hears/says are implemented in python now)
#
 
# scorez(I, SCORE) :- assertz(ias(I, score, SCORE)).
# 
# acts(R, ACTION) :- list_append(R, ACTION).
 
#
# some self address NLP macros
#
 
def nlp_base_self_address_s(kernal, lang, s):

    res = [s]
    for d in rdf (kernal, [('aiu:self', 'ai:forename', 'LABEL')], distinct=True, filters=[ ('=', ('lang', 'LABEL'), lang) ]):
        res.append(hears (lang, s, d['LABEL']))

    return res

# ne: not empty
 
def nlp_base_self_address_ne_s(kernal, lang, s):

    res = []
    for d in rdf (kernal, [('aiu:self', 'ai:forename', 'LABEL')], distinct=True, filters=[ ('=', ('lang', 'LABEL'), lang) ]):
        res.append(hears (lang, s, d['LABEL']))

    return res

#
# nlp helper for simple input->response training samples
#
 
# nlp_train(MODULE, LANG, [[], S1, [], R1]) :-
#     nlp_gens(MODULE, LANG, INP, RESP),
#     hears (LANG, S1, INP),
#     says (LANG, R1, RESP).


