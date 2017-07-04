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

from base.utils        import hears, says, nlp_base_self_address_s, rdf, entity_label, is_male, is_female
from base.conversation import nlp_base_sayagain_s, nlp_base_isaid_r, nlp_base_whatwasourtopic_s
from base.ner          import ner_learn

DEPENDS    = [ 'base' ]

#
# named entity recognition (NER)
#

# this will switch to much smaller training sets so we can keep 
# debug turn-around cycle times low
DEBUG_MODE = True

def ner_learn_humans(kernal, lang):

    entities = []
    labels = []

    for d in rdf (kernal, [('ENTITY', 'wdpd:InstanceOf', 'wde:Human'),
                           ('ENTITY', 'rdfs:label',      'LABEL')
                          ], distinct=True, filters=[ ('=', ('lang', 'LABEL'), lang) ]):

        entities.append(d['ENTITY'])
        labels.append(d['LABEL'])

    ner_learn(lang, 'human', entities, labels)

def init_module(kernal):
    ner_learn_humans(kernal, 'en')
    ner_learn_humans(kernal, 'de')


#
# utils
#

def nlp_f1_ent_pp(kernal, lang, ias, human):

    if lang=='en':
        if is_male(kernal, human):
            ias['f1_ent_pp3s'] = "he"
            ias['f1_ent_pp3o'] = "him"
        elif is_female(kernal, human):
            ias['f1_ent_pp3s'] = "she"
            ias['f1_ent_pp3o'] = "her"
        else:
            ias['f1_ent_pp3s'] = "it"
            ias['f1_ent_pp3o'] = "it"
            
    elif lang=='de':

        if is_male(kernal, human):
            ias['f1_ent_pp3s'] = "er"
            ias['f1_ent_pp3o'] = "ihn"
        elif is_female(kernal, human):
            ias['f1_ent_pp3s'] = "sie"
            ias['f1_ent_pp3o'] = "sie"
        else:
            ias['f1_ent_pp3s'] = "es"
            ias['f1_ent_pp3o'] = "es"

    else:
        raise Exception ('unsupported language: %s' % lang)

def nlp_f1_ent_human(kernal, lang, ias, human):

    ias['f1_entlabel'] = entity_label(kernal, lang, human)

    nlp_f1_ent_pp(kernal, lang, ias, human)




#
# datasets
#

def known_humans_data(lang, size):

    if DEBUG_MODE:
        return [ ('http://www.wikidata.org/entity/Q39829', 'Stephen King') ]

    else:
        if size == 'small':
            return [ ('http://www.wikidata.org/entity/Q39829', 'Stephen King'),
                     ('http://www.wikidata.org/entity/Q76',    'Barack Obama')]

        res = []

        for d in rdf (kernal, [('HUMAN', 'wdpd:InstanceOf', 'wde:Human'),
                               ('HUMAN', 'rdfs:label',      'LABEL')],
                               distinct=True, filters=[ ('=', ('lang', 'LABEL'), lang) ]):

            res.append ((d['HUMAN'], d['LABEL']))

#
# questions about humans known
#

def nlp_humans_doyouknow_s(lang, s, human_label):

    if lang == 'en':

        res = []

        res.extend(hears ('en', s, ['do you ', ['happen to',''], 'know', '$'], label=human_label))

    elif lang == 'de':

        res = []

        res.extend(hears ('de', s, ['kennst du', ['eigentlich',''], '$'], label=human_label))

    else:
        raise Exception ('unsupported language: %s' % lang)

    return res

def nlp_humans_doyouknow_r (lang, r):

    if lang == 'en':

        return [ 
                 says ('en', r, u'Sure I know %(f1_entlabel)s.'),
                 says ('en', r, u'Yes I know %(f1_entlabel)s.'),
                 says ('en', r, u'Sure I know %(f1_ent_pp3o)s.'),
                 says ('en', r, u'Yes I know %(f1_ent_pp3o)s.'),
               ] 

    elif lang == 'de':

        return [ 
                 says ('de', r, u'Klar kenne ich %(f1_entlabel)s.'),
                 says ('de', r, u'Ja ich kenne %(f1_entlabel)s.  '),
                 says ('de', r, u'Klar kenne ich %(f1_ent_pp3o)s.'),
                 says ('de', r, u'Ja ich kenne %(f1_ent_pp3o)s.  '),
               ]

    else:
        raise Exception ('unsupported language: %s' % lang)
    
def nlp_humans_doyouknow(kernal, res):

    # single-round training

    for lang in ['en', 'de']:
        for data in known_humans_data(lang, 'large'):
            for s1 in nlp_base_self_address_s(kernal, lang, []):
                for s2,tstart,tend in nlp_humans_doyouknow_s(lang, s1, data[1]):
                    g = [

                         "from base.ner import ner, ner_best",

                         "ner1res = ner('%s', ias, 'human', %d, %d)" % (lang, tstart, tend),

                         "ias['f1_type']        = 'question'",
                         "ias['f1_topic']       = 'familiarity'",

                         "ner1entity,ner1score = ner_best(ner1res, ias)",

                         "ias['f1_entclass']    = 'human'",
                         "ias['f1_ent']         = ner1entity",

                         "from humans import nlp_f1_ent_human",
                         "nlp_f1_ent_human(kernal, '%s', ias, ner1entity)" % lang,

                        ]
                    for r1 in nlp_humans_doyouknow_r(lang, []):
                        res.append((lang, [[], s2, g, r1]))


#
# birthplace and birtdate questions
#

def nlp_humans_whereborn_s(lang, s, human_label):

    if lang == 'en':

        res = []

        res.extend(hears ('en', s, [ [ "where", "in which town", "in which city"], ["was", "is"], "$", "born?" ], label=human_label))
        res.extend(hears ('en', s, [ "which is", [ "the birthplace", "the place of birth"], "of", "$" ], label=human_label))

    elif lang == 'de':

        res = []

        res.extend(hears ('de', s, [ ["wo", "in welcher Stadt", "an welchem Ort"], ["wurde", "ist"], ["eigentlich", ""], "$", "geboren?" ], label=human_label))
        res.extend(hears ('de', s, [ ["welches", "was"], "ist", ["der Geburtsort", "die Geburtsstadt"], "von", "$" ], label=human_label))

    else:
        raise Exception ('unsupported language: %s' % lang)

    return res

def nlp_humans_whereborn_r (lang, r):

    if lang == 'en':

        return [ 
                 says ('en', r, u'%(f1_entlabel)s was born in %(f1_loclabel)s.'),
                 says ('en', r, u'%(f1_ent_pp3s)s was born in %(f1_loclabel)s.'),
               ] 

    elif lang == 'de':

        return [ 
                 says ('de', r, u'%(f1_entlabel)s wurde in %(f1_loclabel)s geboren.'),
                 says ('de', r, u'%(f1_ent_pp3s)s wurde in %(f1_loclabel)s geboren.'),
               ]

    else:
        raise Exception ('unsupported language: %s' % lang)
  
def nlp_humans_whereborn(kernal, res):

    # single-round training

    for lang in ['en', 'de']:
        for data in known_humans_data(lang, 'large'):
            for s1 in nlp_base_self_address_s(kernal, lang, []):
                for s2,tstart,tend in nlp_humans_whereborn_s(lang, s1, data[1]):
                    g = [

                         "from base.ner import ner, ner_best",

                         "ner1res = ner('%s', ias, 'human', %d, %d)" % (lang, tstart, tend),

                         "ias['f1_type']        = 'question'",
                         "ias['f1_topic']       = 'birthplace'",

                         "ner1entity,ner1score = ner_best(ner1res, ias)",

                         "ias['f1_entclass']    = 'human'",
                         "ias['f1_ent']         = ner1entity",

                         "from humans import nlp_f1_ent_human",
                         "nlp_f1_ent_human(kernal, '%s', ias, ner1entity)" % lang,

                         "from base.utils import rdf, entity_label",
                         "data=rdf (kernal, [(ner1entity, 'wdpd:PlaceOfBirth', 'BIRTHPLACE')], distinct=True, limit=1)[0]",
                         "ias['f1_loc']         = data['BIRTHPLACE']",
                         
                         "ias['f1_loclabel'] = entity_label(kernal, '%s', data['BIRTHPLACE'])" % lang,
                        ]
                    for r1 in nlp_humans_whereborn_r(lang, []):
                        res.append((lang, [[], s2, g, r1]))

 
def nlp_humans_whenborn_s(lang, s, human_label):

    if lang == 'en':

        res = []

        res.extend(hears ('en', s, [ [ "when", "in which year"], ["was", "is"], "$", "born?" ], label=human_label))
        res.extend(hears ('en', s, [ ["when is", "on what day is"], "$", "birthday" ], label=human_label+"'s'"))

    elif lang == 'de':

        res = []

        res.extend(hears ('de', s, [ ["wann", "in welchem Jahr", "an welchem tag"], ["wurde", "ist"], ["eigentlich", ""], "$", "geboren?" ], label=human_label))
        res.extend(hears ('de', s, [ ["wann hat", "an welchem Tag hat"], ["eigentlich", ""], "$", "Geburtstag?" ], label=human_label))

    else:
        raise Exception ('unsupported language: %s' % lang)

    return res

def nlp_humans_whenborn_r (lang, r):

    if lang == 'en':

        return [ 
                 says ('en', r, u'%(f1_entlabel)s was born on %(f1_month_label)s %(f1_day)d, %(f1_year)d.'),
                 says ('en', r, u'%(f1_ent_pp3s)s was born on %(f1_month_label)s %(f1_day)d, %(f1_year)d.'),
               ] 

    elif lang == 'de':

        return [ 
                 says ('de', r, u'%(f1_entlabel)s wurde am %(f1_day_label)s %(f1_month_label)s %(f1_year)d geboren.'),
                 says ('de', r, u'%(f1_ent_pp3s)s wurde am %(f1_day_label)s %(f1_month_label)s %(f1_year)d geboren.'),
               ]

    else:
        raise Exception ('unsupported language: %s' % lang)
  
def nlp_humans_whenborn(kernal, res):

    # single-round training

    for lang in ['en', 'de']:
        for data in known_humans_data(lang, 'large'):
            for s1 in nlp_base_self_address_s(kernal, lang, []):
                for s2,tstart,tend in nlp_humans_whenborn_s(lang, s1, data[1]):
                    g = [

                         "from base.ner import ner, ner_best",

                         "ner1res = ner('%s', ias, 'human', %d, %d)" % (lang, tstart, tend),

                         "ias['f1_type']        = 'question'",
                         "ias['f1_topic']       = 'birthdate'",

                         "ner1entity,ner1score = ner_best(ner1res, ias)",

                         "ias['f1_entclass']    = 'human'",
                         "ias['f1_ent']         = ner1entity",

                         "from humans import nlp_f1_ent_human",
                         "nlp_f1_ent_human(kernal, '%s', ias, ner1entity)" % lang,

                         "from base.utils import rdf, entity_label",
                         "t=rdf (kernal, [(ner1entity, 'wdpd:DateOfBirth', 'BIRTHDATE')], distinct=True, limit=1)[0]['BIRTHDATE']",
                         
                         "ias['f1_day']         = t.day",
                         "ias['f1_month']       = t.month",
                         "ias['f1_year']        = t.year",

                         "from base.time import NLP_DAY_OF_THE_WEEK_LABEL, NLP_MONTH_LABEL",

                         "ias['f1_wday_label']  = NLP_DAY_OF_THE_WEEK_LABEL[ias['lang']][t.weekday()]",
                         "ias['f1_month_label'] = NLP_MONTH_LABEL[ias['lang']][t.month]",

                         "from num2words import num2words",

                         "ias['f1_day_label']   = num2words(t.day, ordinal=True, lang=ias['lang'])+'n'",
                        ]
                    for r1 in nlp_humans_whenborn_r(lang, []):
                        res.append((lang, [[], s2, g, r1]))
 
#
# multi-round / followup birthday/birthplace questions
#

# nlp_humans_g (LANG, followup, birthplace, G) :-
#     G is [
#         setz(ias(I, f1_type,     _), question),
#         setz(ias(I, f1_topic,    _), birthplace),
#         
#         ias(I, f1_ent, NER1ENTITY),
# 
#         nlp_f1_ent_human (LANG, I, NER1ENTITY),
# 
#         rdf (distinct, limit(1),
#              NER1ENTITY, wdpd:PlaceOfBirth, BIRTHPLACE),
#         setz(ias(I, f1_loc, _), BIRTHPLACE),
# 
#         entity_label(LANG, BIRTHPLACE, BPLABEL),
# 
#         setz(ias(I, f1_loclabel, _), BPLABEL)
#         ].
# 
# nlp_humans_s (en, followup, birthplace, S) :-
#     hears (en, S, [["and",""], ["where","in which town","in which city"] ] ).
# nlp_humans_s (de, followup, birthplace, S) :-
#     hears (de, S, [["und",""], ["wo","in welcher stadt","an welchem ort"]] ).
# nlp_humans_s (en, followup, birthplace, S) :-
#     not(debug_mode('humans')),
#     hears (en, S, [["and",""], ["where","in which town","in which city"], ["was","is"], ["she","he"], "born", ["again",""] ] ).
# nlp_humans_s (de, followup, birthplace, S) :-
#     not(debug_mode('humans')),
#     hears (de, S, [["und",""], ["wo","in welcher stadt","an welchem ort"], ["wurde","ist"], ["sie","er"], ["eigentlich",""], ["nochmal",""], "geboren" ] ).
# 
# nlp_humans_s (en, followup, birthplace, S) :-
#     not(debug_mode('humans')),
#     hears (en, S, [["and",""], "which", "is", ["the birthplace","place of birth"], "of", ["him","her"], ["again",""]]).
# nlp_humans_s (de, followup, birthplace, S) :-
#     not(debug_mode('humans')),
#     hears (de, S, [["und",""], "welches", "ist", ["eigentlich","nochmal",""], ["der Geburtsort","die Geburtsstadt"], "von", ["ihm","ihr"]] ).
# 
# 
# nlp_humans_g (LANG, followup, birthdate, G) :-
#     G is [
#         setz(ias(I, f1_type,     _), question),
#         setz(ias(I, f1_topic,    _), birthdate),
#         
#         ias(I, f1_ent, NER1ENTITY),
# 
#         nlp_f1_ent_human (LANG, I, NER1ENTITY),
# 
#         rdf (distinct, limit(1),
#              NER1ENTITY,   wdpd:DateOfBirth,  BIRTHDATE),
#         setz(ias(I, f1_time, _), BIRTHDATE),
# 
#         transcribe_date(LANG, dativ, BIRTHDATE, BDLABEL),
#         setz(ias(I, f1_timelabel, _), BDLABEL)
#         ].
# 
# nlp_humans_s (en, followup, birthdate, S) :-
#     hears (en, S, [["and",""], ["when","in which year"] ] ).
# nlp_humans_s (de, followup, birthdate, S) :-
#     hears (de, S, [["und",""], ["wann","in welchem Jahr"] ] ).
# nlp_humans_s (en, followup, birthdate, S) :-
#     not(debug_mode('humans')),
#     hears (en, S, [["and",""], ["when","in which year"], ["was","is"], ["she","he"], "born", ["again",""] ] ).
# nlp_humans_s (de, followup, birthdate, S) :-
#     not(debug_mode('humans')),
#     hears (de, S, [["und",""], ["wann","in welchem Jahr"], ["wurde","ist"], ["sie","er"], ["eigentlich",""], ["nochmal",""], "geboren" ] ).
# 
# nlp_humans_sgr(LANG, followup, TOPIC, S, G, R) :-
#     nlp_humans_s (LANG, followup, TOPIC, S),
#     nlp_humans_g (LANG, followup, TOPIC, G),
#     nlp_humans_r (LANG, TOPIC, R).
# 
# nlp_train('humans', en, [[], S1, G1, R1, [], S2, G2, R2]) :-
#     nlp_humans_sgr(en, small, start, TOPIC1, S1, G1, R1),
#     nlp_humans_sgr(en, followup, TOPIC2, S2, G2, R2).
# 
# nlp_train('humans', de, [[], S1, G1, R1, [], S2, G2, R2]) :-
#     nlp_humans_sgr(de, small, start, TOPIC1, S1, G1, R1),
#     nlp_humans_sgr(de, followup, TOPIC2, S2, G2, R2).
# 
# nlp_test('humans', en, 'multi1', [],
#          ['When was Stephen King born?', 'Stephen King was born on September 21, 1947.', [],
#           'and where?', 'Stephen King was born in Portland.', []]).
# 
# nlp_test('humans', de, 'multi2', [],
#          ['Wann wurde Stephen King geboren?', 'Stephen King wurde am einundzwanzigsten September 1947 geboren.', [],
#           'und wo?', 'Stephen King wurde in Portland geboren.', []]).

# nlp_test(en,
#          ivr(in('Where was Angela Merkel born?'),
#              out('angela merkel was born in barmbek-nord')),
#          ivr(in('What were we talking about?'),
#              out('angela merkels birthday')),
#          ivr(in('and where was she born again?'),
#              out('angela merkel was born in barmbek-nord'))).
# nlp_test(de,
#          ivr(in('Wo wurde Angela Merkel geboren?'),
#              out('angela merkel wurde in barmbek-nord geboren')),
#          ivr(in('Welches Thema hatten wir?'),
#              out('angela merkels geburtstag.')),
#          ivr(in('und wo wurde sie nochmal geboren?'),
#              out('angela merkel wurde in barmbek-nord geboren'))).
#

# nlp_test(en,
#          ivr(in('When was Angela Merkel born?'),
#              out('Angela Merkel was born on july seventeen, 1954.')),
#          ivr(in('What were we talking about?'),
#              out('angela merkels birthday')),
#          ivr(in('and when was she born?'),
#              out('Angela Merkel was born on july seventeen, 1954.')),
#          ivr(in('and where?'),
#              out('she was born in barmbek nord'))
#         ).
# 
# nlp_test(de,
#          ivr(in('Wann wurde Angela Merkel geboren?'),
#              out('Angela Merkel wurde am siebzehnten juli 1954 geboren.')),
#          ivr(in('Welches Thema hatten wir?'),
#              out('angela merkels geburtstag')),
#          ivr(in('und wann wurde sie nochmal geboren?'),
#              out('Angela Merkel wurde am siebzehnten juli 1954 geboren.')),
#          ivr(in('und wo?'),
#              out('Angela Merkel wurde in barmbek nord geboren.'))
#         ).

#
# if we don't know anything else, we can tell the user about the human's birthplace
#

def nlp_humans_whatabout_s(lang, s, human_label):

    if lang == 'en':

        res = []

        res.extend(hears ('en', s, [ [ "what about", "who is", "what is", "what do you know about", "what do you know of" ], "$" ], label=human_label))

    elif lang == 'de':

        res = []

        res.extend(hears ('de', s, [ [ "wer ist", "wer ist eigentlich", "was ist mit", "was ist eigentlich mit", "was weisst du über", "was weisst du eigentlich über" ], "$" ], label=human_label))

    else:
        raise Exception ('unsupported language: %s' % lang)

    return res

def nlp_humans_whatabout(kernal, res):

    # single-round training

    for lang in ['en', 'de']:
        for data in known_humans_data(lang, 'large'):
            for s1 in nlp_base_self_address_s(kernal, lang, []):
                for s2,tstart,tend in nlp_humans_whatabout_s(lang, s1, data[1]):
                    g = [

                         "from base.ner import ner, ner_best",

                         "ner1res = ner('%s', ias, 'human', %d, %d)" % (lang, tstart, tend),

                         "ias['f1_type']        = 'question'",
                         "ias['f1_topic']       = 'birthplace'",

                         "ner1entity,ner1score = ner_best(ner1res, ias)",

                         "ias['f1_entclass']    = 'human'",
                         "ias['f1_ent']         = ner1entity",

                         "from humans import nlp_f1_ent_human",
                         "nlp_f1_ent_human(kernal, '%s', ias, ner1entity)" % lang,

                         "from base.utils import rdf, entity_label",
                         "data=rdf (kernal, [(ner1entity, 'wdpd:PlaceOfBirth', 'BIRTHPLACE')], distinct=True, limit=1)[0]",
                         "ias['f1_loc']         = data['BIRTHPLACE']",
                         
                         "ias['f1_loclabel'] = entity_label(kernal, '%s', data['BIRTHPLACE'])" % lang,
                        ]
                    for r1 in nlp_humans_whereborn_r(lang, []):
                        res.append((lang, [[], s2, g, r1]))

def nlp_train (kernal):

    res = []

    nlp_humans_doyouknow(kernal, res)
    nlp_humans_whereborn(kernal, res)
    nlp_humans_whenborn(kernal, res)
    nlp_humans_whatabout(kernal, res)

    return res


def nlp_test (kernal):

    return [ ('de', 'know1',      [], ["Kennst Du Stephen King?", "Ja ich kenne Stephen King", []]),
             ('en', 'know2',      [], ["Do you know Stephen King?", "Sure I know Stephen King", []]),
             ('en', 'know3',      [], ["Do you know Stephen King?", "Sure I know him", []]), 
             ('en', 'whereborn1', [], ['Where was Stephen King born?', 'Stephen King was born in Portland.', []]),
             ('de', 'whereborn2', [], ['Wo wurde Stephen King geboren?', 'Stephen King wurde in Portland geboren.', []]),
             ('en', 'whenborn1',  [], ['When was Stephen King born?', 'Stephen King was born on September 21, 1947.', []]),
             ('de', 'whenborn2',  [], ['Wann wurde Stephen King geboren?', 'Stephen King wurde am einundzwanzigsten September 1947 geboren.', []]),
             ('en', 'whatabout1', [], ['What about Stephen King?', 'Stephen King was born in Portland.', []]),
             ('de', 'whatabout2', [], ['Was ist mit Stephen King?', 'Stephen King wurde in Portland geboren.', []]),
           ]

