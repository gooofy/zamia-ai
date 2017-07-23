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
from rdf                  import rdf

#
# very basic utilities
#

def hears(lang, s, txt, label=None):

    if isinstance (txt, basestring):
        s1 = copy(s)
        s1.extend(tokenize(txt, lang=lang))
        return s1

    # import pdb; pdb.set_trace()

    todo = [(txt, 0, [], None, None)]

    done   = []

    while todo:

        # print repr(todo)

        l, pos, res, tstart, tend = todo.pop()

        if pos >= len(l):
            if label:
                done.append((res, tstart, tend))
            else:
                done.append(res)
            continue

        e = l[pos]
        if isinstance(e, basestring):

            if label and e=='$':
                tstart = len(res)
                tokens = tokenize(label, lang=lang)
                tend = tstart + len(tokens)
            else:
                tokens = tokenize(e, lang=lang)

            res = copy(res)
            res.extend(tokens)
            todo.append((l, pos+1, res, tstart, tend))

        else:

            for e2 in e:
                tokens = tokenize(e2, lang=lang)
                res2 = copy(res)
                res2.extend(tokens)
                todo.append((l, pos+1, res2, tstart, tend))

    start = s

    res = []

    if label:

        for d, tstart, tend in done:

            r = deepcopy(start)

            for token in d:
                r.append(token)

            res.append ((r, tstart, tend))

    else:
        for d in done:

            r = deepcopy(start)

            for token in d:
                r.append(token)

            res.append (r)

    return res

def says (lang, r, txt, actions=None, bor=False):

    r1 = copy(r)
    # for t in tokenize(txt, lang=lang):
    #     r1.append(u"say('%s', '%s')" % (lang, t))

    if bor:
        r1.append(u"r_bor(ias)")

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
            r1.append(u"r_sayv(ias, '%s', '%s')" % (var_name, format_char))

            o += 1

        parts2 = tokenize(p1[o:], lang=lang, keep_punctuation=True)

        for p2 in parts2:
            r1.append(u"r_say(ias, u'%s')" % p2.replace("'", "\\'"))

        cnt += 1
   
    if actions:
        for a in actions:
            r1.append(u"r_action(ias, %s)" % repr(a))

    return r1

def r_say (ias, s):

    r = ias['resp']

    if len(r)==0:
        r.append([])

    r[len(r)-1].append(s)

    # print "r_say (%s) called -> %s" % (s, repr(r[len(r)-1]))

def r_bor (ias):
    ias['resp'].append([])

def nlp_add_round(res, lang, question, answer):

    s = hears(lang, [], question)
    
    r = says (lang, [], answer, bor=True)

    res.append((lang, [[], s, r]))

    return res


#
# wikidata / rdf related utils
#

def entity_label(kernal, lang, entity):


    res = rdf (kernal, [(entity, 'rdfs:label', 'LABEL')], 
               distinct=True, limit=1, filters=[ ('=', ('lang', 'LABEL'), lang) ])

    if len(res)!=1:
        # try the english label instead
        res = rdf (kernal, [(entity, 'rdfs:label', 'LABEL')], 
                   distinct=True, limit=1, filters=[ ('=', ('lang', 'LABEL'), 'en') ])
        if len(res)!=1:
            # import pdb; pdb.set_trace()
            print 'warning: no label found for %s' % entity
            return 'unknown'

    # print "entity_label: %s -> %s" % (entity, repr(res))
    return res[0]['LABEL']

# is_entity(ENTITY) :-
#     rdf (limit(1), ENTITY, rdfs:label, LABEL).
 
# humans / persons
 
# is_human(ENTITY) :- rdf (ENTITY, wdpd:InstanceOf, wde:Human).
 
def is_male(kernal, entity):
    return len( rdf (kernal, [('ENTITY', 'wdpd:SexOrGender', 'wde:Male')]))>0
def is_female(kernal, entity):
    return len( rdf (kernal, [('ENTITY', 'wdpd:SexOrGender', 'wde:Female')]))>0

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


