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

DEPENDS    = [ 'base' ]

AIP_SOURCES = [ 'humans.aip' ]

#
# FIXME: port code to AI-Prolog
#

# from base.utils        import hears, says, nlp_base_self_address_s, rdf, entity_label, is_male, is_female
# from base.conversation import nlp_base_sayagain_s, nlp_base_isaid_r, nlp_base_whatwasourtopic_s
# from base.ner          import ner_learn

# #
# # named entity recognition (NER)
# #
# 
# # this will switch to much smaller training sets so we can keep 
# # debug turn-around cycle times low
# DEBUG_MODE  = False
# 
# MULTI_ROUND_MOD = 97
# 
# def ner_learn_humans(kernal, lang):
# 
#     entities = []
#     labels = []
# 
#     for d in rdf (kernal, [('ENTITY', 'wdpd:InstanceOf', 'wde:Human'),
#                            ('ENTITY', 'rdfs:label',      'LABEL')
#                           ], distinct=True, filters=[ ('=', ('lang', 'LABEL'), lang) ]):
# 
#         entities.append(d['ENTITY'])
#         labels.append(d['LABEL'])
#         # print "NER %3d Human? %s %s" % (len(labels), d['ENTITY'], d['LABEL'])
# 
#     ner_learn(lang, 'human', entities, labels)
# 
# def init_module(kernal):
#     ner_learn_humans(kernal, 'en')
#     ner_learn_humans(kernal, 'de')
# 
# 
# #
# # utils
# #
# 
# def nlp_f1_ent_pp(kernal, lang, ias, human):
# 
#     if lang=='en':
#         if is_male(kernal, human):
#             ias['f1_ent_pp3s'] = "he"
#             ias['f1_ent_pp3o'] = "him"
#         elif is_female(kernal, human):
#             ias['f1_ent_pp3s'] = "she"
#             ias['f1_ent_pp3o'] = "her"
#         else:
#             ias['f1_ent_pp3s'] = "it"
#             ias['f1_ent_pp3o'] = "it"
#             
#     elif lang=='de':
# 
#         if is_male(kernal, human):
#             ias['f1_ent_pp3s'] = "er"
#             ias['f1_ent_pp3o'] = "ihn"
#         elif is_female(kernal, human):
#             ias['f1_ent_pp3s'] = "sie"
#             ias['f1_ent_pp3o'] = "sie"
#         else:
#             ias['f1_ent_pp3s'] = "es"
#             ias['f1_ent_pp3o'] = "es"
# 
#     else:
#         raise Exception ('unsupported language: %s' % lang)
# 
# def nlp_f1_ent_human(kernal, lang, ias, human):
# 
#     ias['f1_entlabel'] = entity_label(kernal, lang, human)
# 
#     nlp_f1_ent_pp(kernal, lang, ias, human)
# 
# 
# 
# 
# #
# # datasets
# #
# 
# def known_humans_data(kernal, lang, size):
# 
#     if DEBUG_MODE:
#         return [ ('http://www.wikidata.org/entity/Q39829', 'Stephen King') ]
# 
#     else:
#         if size == 'small':
#             return [ ('http://www.wikidata.org/entity/Q39829', 'Stephen King'),
#                      ('http://www.wikidata.org/entity/Q76',    'Barack Obama')]
# 
#         res = []
# 
#         for d in rdf (kernal, [('HUMAN',      'wdpd:InstanceOf',   'wde:Human'),
#                                ('HUMAN',      'rdfs:label',        'LABEL'),
#                                ('HUMAN',      'wdpd:PlaceOfBirth', 'BIRTHPLACE'),
#                                ('BIRTHPLACE', 'rdfs:label',        'BP_LABEL')],
#                                distinct=True, 
#                                limit=100,
#                                filters=[ ('=', ('lang', 'LABEL'), lang) ]):
# 
#             # print "%3d Human? %s %s" % (len(res), d['HUMAN'], d['LABEL'])
# 
#             res.append ((d['HUMAN'], d['LABEL']))
#         return res
# 
# #
# # followup birthday/birthplace questions
# #
# 
# def nlp_humans_whereborn_followup_s(lang, s):
# 
#     if lang == 'en':
# 
#         res = []
# 
#         res.extend(hears ('en', s, [["and",""], ["where","in which town","in which city"]]))
#         res.extend(hears ('en', s, [["and",""], ["where","in which town","in which city"], ["was","is"], ["she","he"], "born", ["again",""]]))
#         res.extend(hears ('en', s, [["and",""], "which", "is", ["the birthplace","place of birth"], "of", ["him","her"], ["again",""]]))
# 
#     elif lang == 'de':
# 
#         res = []
# 
#         res.extend(hears ('de', s, [["und",""], ["wo","in welcher stadt","an welchem ort"] ]))
#         res.extend(hears ('de', s, [["und",""], ["wo","in welcher stadt","an welchem ort"], ["wurde","ist"], ["sie","er"], ["eigentlich",""], ["nochmal",""], "geboren" ]))
#         res.extend(hears ('de', s, [["und",""], "welches", "ist", ["eigentlich","nochmal",""], ["der Geburtsort","die Geburtsstadt"], "von", ["ihm","ihr"] ]))
# 
#     else:
#         raise Exception ('unsupported language: %s' % lang)
# 
#     return res
# 
# def nlp_humans_whereborn_followup_g():
#     return [
# 
#          "ias['f1_type']        = 'question'",
#          "ias['f1_topic']       = 'birthplace'",
# 
#          "ner1entity = ias['f1_ent']",
# 
#          "from humans import nlp_f1_ent_human",
#          "nlp_f1_ent_human(kernal, ias['lang'], ias, ner1entity)",
# 
#          "from base.utils import rdf, entity_label",
#          "data=rdf (kernal, [(ner1entity, 'wdpd:PlaceOfBirth', 'BIRTHPLACE')], distinct=True, limit=1)[0]",
#          "ias['f1_loc']         = data['BIRTHPLACE']",
#          
#          "ias['f1_loclabel'] = entity_label(kernal, ias['lang'], data['BIRTHPLACE'])",
#         ]
# 
# 
# def nlp_humans_whenborn_followup_s(lang, s):
# 
#     if lang == 'en':
# 
#         res = []
# 
#         res.extend(hears ('en', s, [["and",""], ["when","in which year"] ]))
#         res.extend(hears ('en', s, [["and",""], ["when","in which year"], ["was","is"], ["she","he"], "born", ["again",""] ]))
# 
#     elif lang == 'de':
# 
#         res = []
# 
#         res.extend(hears ('de', s, [["und",""], ["wann","in welchem Jahr"] ]))
#         res.extend(hears ('de', s, [["und",""], ["wann","in welchem Jahr"], ["wurde","ist"], ["sie","er"], ["eigentlich",""], ["nochmal",""], "geboren" ]))
# 
#     else:
#         raise Exception ('unsupported language: %s' % lang)
# 
#     return res
# 
# def nlp_humans_whenborn_followup_g():
#     return [
# 
#          "ias['f1_type']        = 'question'",
#          "ias['f1_topic']       = 'birthdate'",
# 
#          "ner1entity = ias['f1_ent']",
# 
#          "from base.utils import rdf, entity_label",
#          "t=rdf (kernal, [(ner1entity, 'wdpd:DateOfBirth', 'BIRTHDATE')], distinct=True, limit=1)[0]['BIRTHDATE']",
#          
#          "ias['f1_day']         = t.day",
#          "ias['f1_month']       = t.month",
#          "ias['f1_year']        = t.year",
# 
#          "from base.time import NLP_DAY_OF_THE_WEEK_LABEL, NLP_MONTH_LABEL",
# 
#          "ias['f1_wday_label']  = NLP_DAY_OF_THE_WEEK_LABEL[ias['lang']][t.weekday()]",
#          "ias['f1_month_label'] = NLP_MONTH_LABEL[ias['lang']][t.month]",
# 
#          "from num2words import num2words",
# 
#          "ias['f1_day_label']   = num2words(t.day, ordinal=True, lang=ias['lang'])+'n'",
#         ]
# 
# #
# # questions about humans known
# #
# 
# def nlp_humans_doyouknow_s(lang, s, human_label):
# 
#     if lang == 'en':
# 
#         res = []
# 
#         res.extend(hears ('en', s, ['do you ', ['happen to',''], 'know', '$'], label=human_label))
# 
#     elif lang == 'de':
# 
#         res = []
# 
#         res.extend(hears ('de', s, ['kennst du', ['eigentlich',''], '$'], label=human_label))
# 
#     else:
#         raise Exception ('unsupported language: %s' % lang)
# 
#     return res
# 
# def nlp_humans_doyouknow_r (lang, r):
# 
#     if lang == 'en':
# 
#         return [ 
#                  says ('en', r, u'Sure I know %(f1_entlabel)s.'),
#                  says ('en', r, u'Yes I know %(f1_entlabel)s.'),
#                  says ('en', r, u'Sure I know %(f1_ent_pp3o)s.'),
#                  says ('en', r, u'Yes I know %(f1_ent_pp3o)s.'),
#                ] 
# 
#     elif lang == 'de':
# 
#         return [ 
#                  says ('de', r, u'Klar kenne ich %(f1_entlabel)s.'),
#                  says ('de', r, u'Ja ich kenne %(f1_entlabel)s.  '),
#                  says ('de', r, u'Klar kenne ich %(f1_ent_pp3o)s.'),
#                  says ('de', r, u'Ja ich kenne %(f1_ent_pp3o)s.  '),
#                ]
# 
#     else:
#         raise Exception ('unsupported language: %s' % lang)
#     
# def nlp_humans_doyouknow_g(tstart, tend):
#     return [
# 
#          "from base.ner import ner, ner_best",
# 
#          "ner1res = ner(ias['lang'], ias, 'human', %d, %d)" % (tstart, tend),
# 
#          "ias['f1_type']        = 'question'",
#          "ias['f1_topic']       = 'familiarity'",
# 
#          "ner1entity,ner1score = ner_best(ner1res, ias)",
# 
#          "ias['f1_entclass']    = 'human'",
#          "ias['f1_ent']         = ner1entity",
# 
#          "from humans import nlp_f1_ent_human",
#          "nlp_f1_ent_human(kernal, ias['lang'], ias, ner1entity)",
# 
#         ]
# 
# 
# 
# def nlp_humans_doyouknow(kernal, res):
# 
#     # single-round training
# 
#     for lang in ['en', 'de']:
#         for data in known_humans_data(kernal, lang, 'large'):
#             for s1_1 in nlp_base_self_address_s(kernal, lang, []):
#                 for s1_2,tstart,tend in nlp_humans_doyouknow_s(lang, s1_1, data[1]):
#                     g1 = nlp_humans_doyouknow_g(tstart, tend)
#                     for r1 in nlp_humans_doyouknow_r(lang, []):
#                         res.append((lang, [[], s1_2, g1, r1]))
# 
#     # multi-round training
# 
#     cnt = 0
# 
#     for lang in ['en', 'de']:
#         for data in known_humans_data(kernal, lang, 'small'):
#             for s1_1 in nlp_base_self_address_s(kernal, lang, []):
#                 for s1_2,tstart,tend in nlp_humans_doyouknow_s(lang, s1_1, data[1]):
#                     g1 = nlp_humans_doyouknow_g(tstart, tend)
#                     for r1 in nlp_humans_doyouknow_r(lang, []):
# 
#                         for s2 in nlp_base_whatwasourtopic_s(lang, []):
#                             for r2 in nlp_humans_topic_r(lang, []):
#                                 cnt += 1
#                                 if cnt % MULTI_ROUND_MOD == 0:
#                                     res.append((lang, [[], s1_2, g1, r1, [], s2, [], r2]))
# 
#                         for s2 in nlp_base_sayagain_s(lang, []):
#                             for r2_1 in nlp_base_isaid_r(lang, []):
#                                 for r2_2 in nlp_humans_doyouknow_r(lang, r2_1):
#                                     cnt += 1
#                                     if cnt % MULTI_ROUND_MOD == 0:
#                                         res.append((lang, [[], s1_2, g1, r1, [], s2, [], r2_2]))
# 
#                         g2 = nlp_humans_whenborn_followup_g()
#                         for s2 in nlp_humans_whenborn_followup_s(lang, []):
#                             for r2 in nlp_humans_whenborn_r(lang, []):
#                                 cnt += 1
#                                 if cnt % MULTI_ROUND_MOD == 0:
#                                     res.append((lang, [[], s1_2, g1, r1, [], s2, g2, r2]))
# 
#                         g2 = nlp_humans_whereborn_followup_g()
#                         for s2 in nlp_humans_whereborn_followup_s(lang, []):
#                             for r2 in nlp_humans_whereborn_r(lang, []):
#                                 cnt += 1
#                                 if cnt % MULTI_ROUND_MOD == 0:
#                                     res.append((lang, [[], s1_2, g1, r1, [], s2, g2, r2]))
# 
#                         res.append((lang, [[], s1_2, g1, r1]))
# 
# #
# # birthplace and birtdate questions
# #
# 
# def nlp_humans_whereborn_s(lang, s, human_label):
# 
#     if lang == 'en':
# 
#         res = []
# 
#         res.extend(hears ('en', s, [ [ "where", "in which town", "in which city"], ["was", "is"], "$", "born?" ], label=human_label))
#         res.extend(hears ('en', s, [ "which is", [ "the birthplace", "the place of birth"], "of", "$" ], label=human_label))
# 
#     elif lang == 'de':
# 
#         res = []
# 
#         res.extend(hears ('de', s, [ ["wo", "in welcher Stadt", "an welchem Ort"], ["wurde", "ist"], ["eigentlich", ""], "$", "geboren?" ], label=human_label))
#         res.extend(hears ('de', s, [ ["welches", "was"], "ist", ["der Geburtsort", "die Geburtsstadt"], "von", "$" ], label=human_label))
# 
#     else:
#         raise Exception ('unsupported language: %s' % lang)
# 
#     return res
# 
# def nlp_humans_whereborn_r (lang, r):
# 
#     if lang == 'en':
# 
#         return [ 
#                  says ('en', r, u'%(f1_entlabel)s was born in %(f1_loclabel)s.'),
#                  says ('en', r, u'%(f1_ent_pp3s)s was born in %(f1_loclabel)s.'),
#                ] 
# 
#     elif lang == 'de':
# 
#         return [ 
#                  says ('de', r, u'%(f1_entlabel)s wurde in %(f1_loclabel)s geboren.'),
#                  says ('de', r, u'%(f1_ent_pp3s)s wurde in %(f1_loclabel)s geboren.'),
#                ]
# 
#     else:
#         raise Exception ('unsupported language: %s' % lang)
#   
# def nlp_humans_whereborn_g (tstart, tend):
#     return [
# 
#          "from base.ner import ner, ner_best",
# 
#          "ner1res = ner(ias['lang'], ias, 'human', %d, %d)" % (tstart, tend),
# 
#          "ias['f1_type']        = 'question'",
#          "ias['f1_topic']       = 'birthplace'",
# 
#          "ner1entity,ner1score = ner_best(ner1res, ias)",
# 
#          "ias['f1_entclass']    = 'human'",
#          "ias['f1_ent']         = ner1entity",
# 
#          "from humans import nlp_f1_ent_human",
#          "nlp_f1_ent_human(kernal, ias['lang'], ias, ner1entity)",
# 
#          "from base.utils import rdf, entity_label",
#          "data=rdf (kernal, [(ner1entity, 'wdpd:PlaceOfBirth', 'BIRTHPLACE')], distinct=True, limit=1)[0]",
#          "ias['f1_loc']         = data['BIRTHPLACE']",
#          
#          "ias['f1_loclabel'] = entity_label(kernal, ias['lang'], data['BIRTHPLACE'])",
#         ]
# 
# def nlp_humans_whereborn(kernal, res):
# 
#     # single-round training
# 
#     for lang in ['en', 'de']:
#         for data in known_humans_data(kernal, lang, 'large'):
#             for s1_1 in nlp_base_self_address_s(kernal, lang, []):
#                 for s1_2,tstart,tend in nlp_humans_whereborn_s(lang, s1_1, data[1]):
#                     g1 =  nlp_humans_whereborn_g (tstart, tend)
#                     for r1 in nlp_humans_whereborn_r(lang, []):
#                         res.append((lang, [[], s1_2, g1, r1]))
# 
#     # multi-round training
# 
#     cnt = 0
# 
#     for lang in ['en', 'de']:
#         for data in known_humans_data(kernal, lang, 'small'):
#             for s1_1 in nlp_base_self_address_s(kernal, lang, []):
#                 for s1_2,tstart,tend in nlp_humans_whereborn_s(lang, s1_1, data[1]):
#                     g1 =  nlp_humans_whereborn_g (tstart, tend)
#                     for r1 in nlp_humans_whereborn_r(lang, []):
# 
#                         for s2 in nlp_base_whatwasourtopic_s(lang, []):
#                             for r2 in nlp_humans_topic_r(lang, []):
#                                 cnt += 1
#                                 if cnt % MULTI_ROUND_MOD == 0:
#                                     res.append((lang, [[], s1_2, g1, r1, [], s2, [], r2]))
# 
#                         for s2 in nlp_base_sayagain_s(lang, []):
#                             for r2_1 in nlp_base_isaid_r(lang, []):
#                                 for r2_2 in nlp_humans_whereborn_r(lang, r2_1):
#                                     cnt += 1
#                                     if cnt % MULTI_ROUND_MOD == 0:
#                                         res.append((lang, [[], s1_2, g1, r1, [], s2, [], r2_2]))
# 
#                         g2 = nlp_humans_whenborn_followup_g()
#                         for s2 in nlp_humans_whenborn_followup_s(lang, []):
#                             for r2 in nlp_humans_whenborn_r(lang, []):
#                                 cnt += 1
#                                 if cnt % MULTI_ROUND_MOD == 0:
#                                     res.append((lang, [[], s1_2, g1, r1, [], s2, g2, r2]))
# 
# 
# def nlp_humans_whenborn_s(lang, s, human_label):
# 
#     if lang == 'en':
# 
#         res = []
# 
#         res.extend(hears ('en', s, [ [ "when", "in which year"], ["was", "is"], "$", "born?" ], label=human_label))
#         res.extend(hears ('en', s, [ ["when is", "on what day is"], "$", "birthday" ], label=human_label+"'s'"))
# 
#     elif lang == 'de':
# 
#         res = []
# 
#         res.extend(hears ('de', s, [ ["wann", "in welchem Jahr", "an welchem tag"], ["wurde", "ist"], ["eigentlich", ""], "$", "geboren?" ], label=human_label))
#         res.extend(hears ('de', s, [ ["wann hat", "an welchem Tag hat"], ["eigentlich", ""], "$", "Geburtstag?" ], label=human_label))
# 
#     else:
#         raise Exception ('unsupported language: %s' % lang)
# 
#     return res
# 
# def nlp_humans_whenborn_r (lang, r):
# 
#     if lang == 'en':
# 
#         return [ 
#                  says ('en', r, u'%(f1_entlabel)s was born on %(f1_month_label)s %(f1_day)d, %(f1_year)d.'),
#                  says ('en', r, u'%(f1_ent_pp3s)s was born on %(f1_month_label)s %(f1_day)d, %(f1_year)d.'),
#                ] 
# 
#     elif lang == 'de':
# 
#         return [ 
#                  says ('de', r, u'%(f1_entlabel)s wurde am %(f1_day_label)s %(f1_month_label)s %(f1_year)d geboren.'),
#                  says ('de', r, u'%(f1_ent_pp3s)s wurde am %(f1_day_label)s %(f1_month_label)s %(f1_year)d geboren.'),
#                ]
# 
#     else:
#         raise Exception ('unsupported language: %s' % lang)
#   
# def nlp_humans_whenborn_g(tstart, tend):
#     return [
# 
#          "from base.ner import ner, ner_best",
# 
#          "ner1res = ner(ias['lang'], ias, 'human', %d, %d)" % (tstart, tend),
# 
#          "ias['f1_type']        = 'question'",
#          "ias['f1_topic']       = 'birthdate'",
# 
#          "ner1entity,ner1score = ner_best(ner1res, ias)",
# 
#          "ias['f1_entclass']    = 'human'",
#          "ias['f1_ent']         = ner1entity",
# 
#          "from humans import nlp_f1_ent_human",
#          "nlp_f1_ent_human(kernal, ias['lang'], ias, ner1entity)",
# 
#          "from base.utils import rdf, entity_label",
#          "t=rdf (kernal, [(ner1entity, 'wdpd:DateOfBirth', 'BIRTHDATE')], distinct=True, limit=1)[0]['BIRTHDATE']",
#          
#          "ias['f1_day']         = t.day",
#          "ias['f1_month']       = t.month",
#          "ias['f1_year']        = t.year",
# 
#          "from base.time import NLP_DAY_OF_THE_WEEK_LABEL, NLP_MONTH_LABEL",
# 
#          "ias['f1_wday_label']  = NLP_DAY_OF_THE_WEEK_LABEL[ias['lang']][t.weekday()]",
#          "ias['f1_month_label'] = NLP_MONTH_LABEL[ias['lang']][t.month]",
# 
#          "from num2words import num2words",
# 
#          "ias['f1_day_label']   = num2words(t.day, ordinal=True, lang=ias['lang'])+'n'",
#         ]
# 
# def nlp_humans_whenborn(kernal, res):
# 
#     # single-round training
# 
#     for lang in ['en', 'de']:
#         for data in known_humans_data(kernal, lang, 'large'):
#             for s1_1 in nlp_base_self_address_s(kernal, lang, []):
#                 for s1_2,tstart,tend in nlp_humans_whenborn_s(lang, s1_1, data[1]):
#                     g1 = nlp_humans_whenborn_g(tstart, tend)
#                     for r1 in nlp_humans_whenborn_r(lang, []):
#                         res.append((lang, [[], s1_2, g1, r1]))
# 
#     # multi-round training
# 
#     cnt = 0
# 
#     for lang in ['en', 'de']:
#         for data in known_humans_data(kernal, lang, 'small'):
#             for s1_1 in nlp_base_self_address_s(kernal, lang, []):
#                 for s1_2,tstart,tend in nlp_humans_whenborn_s(lang, s1_1, data[1]):
#                     g1 = nlp_humans_whenborn_g(tstart, tend)
#                     for r1 in nlp_humans_whenborn_r(lang, []):
#                         for s2 in nlp_base_whatwasourtopic_s(lang, []):
#                             for r2 in nlp_humans_topic_r(lang, []):
#                                 cnt += 1
#                                 if cnt % MULTI_ROUND_MOD == 0:
#                                     res.append((lang, [[], s1_2, g1, r1, [], s2, [], r2]))
# 
#                         for s2 in nlp_base_sayagain_s(lang, []):
#                             for r2_1 in nlp_base_isaid_r(lang, []):
#                                 for r2_2 in nlp_humans_whenborn_r(lang, r2_1):
#                                     cnt += 1
#                                     if cnt % MULTI_ROUND_MOD == 0:
#                                         res.append((lang, [[], s1_2, g1, r1, [], s2, [], r2_2]))
# 
#                         g2 = nlp_humans_whereborn_followup_g()
#                         for s2 in nlp_humans_whereborn_followup_s(lang, []):
#                             for r2 in nlp_humans_whereborn_r(lang, []):
#                                 cnt += 1
#                                 if cnt % MULTI_ROUND_MOD == 0:
#                                     res.append((lang, [[], s1_2, g1, r1, [], s2, g2, r2]))
#  
# #
# # if we don't know anything else, we can tell the user about the human's birthplace
# #
# 
# def nlp_humans_whatabout_s(lang, s, human_label):
# 
#     if lang == 'en':
# 
#         res = []
# 
#         res.extend(hears ('en', s, [ [ "what about", "who is", "what is", "what do you know about", "what do you know of" ], "$" ], label=human_label))
# 
#     elif lang == 'de':
# 
#         res = []
# 
#         res.extend(hears ('de', s, [ [ "wer ist", "wer ist eigentlich", "was ist mit", "was ist eigentlich mit", "was weisst du über", "was weisst du eigentlich über" ], "$" ], label=human_label))
# 
#     else:
#         raise Exception ('unsupported language: %s' % lang)
# 
#     return res
# 
# def nlp_humans_whatabout_g(lang, tstart, tend):
#     return [
# 
#          "from base.ner import ner, ner_best",
# 
#          "ner1res = ner('%s', ias, 'human', %d, %d)" % (lang, tstart, tend),
# 
#          "ias['f1_type']        = 'question'",
#          "ias['f1_topic']       = 'birthplace'",
# 
#          "ner1entity,ner1score = ner_best(ner1res, ias)",
# 
#          "ias['f1_entclass']    = 'human'",
#          "ias['f1_ent']         = ner1entity",
# 
#          "from humans import nlp_f1_ent_human",
#          "nlp_f1_ent_human(kernal, '%s', ias, ner1entity)" % lang,
# 
#          "from base.utils import rdf, entity_label",
#          "data=rdf (kernal, [(ner1entity, 'wdpd:PlaceOfBirth', 'BIRTHPLACE')], distinct=True, limit=1)[0]",
#          "ias['f1_loc']         = data['BIRTHPLACE']",
#          
#          "ias['f1_loclabel'] = entity_label(kernal, '%s', data['BIRTHPLACE'])" % lang,
#         ]
# 
# def nlp_humans_topic_r (lang, r):
# 
#     if lang == 'en':
# 
#         return [ 
#                  says ('en', r, u'we were talking about %(f1_entlabel)s.'),
#                  says ('en', r, u'our topic was %(f1_entlabel)s.'),
#                ] 
# 
#     elif lang == 'de':
# 
#         return [ 
#                  says ('de', r, u'wir haben über %(f1_entlabel)s gesprochen.'),
#                  says ('de', r, u'unser thema war %(f1_entlabel)s.'),
#                ]
# 
#     else:
#         raise Exception ('unsupported language: %s' % lang)
#   
# def nlp_humans_whatabout(kernal, res):
# 
#     # single-round training
# 
#     for lang in ['en', 'de']:
#         for data in known_humans_data(kernal, lang, 'large'):
#             for s1 in nlp_base_self_address_s(kernal, lang, []):
#                 for s2,tstart,tend in nlp_humans_whatabout_s(lang, s1, data[1]):
#                     g = nlp_humans_whatabout_g(lang, tstart, tend)
#                     for r1 in nlp_humans_whereborn_r(lang, []):
#                         res.append((lang, [[], s2, g, r1]))
# 
# 
#     # multi-round training
# 
#     cnt = 0
# 
#     for lang in ['en', 'de']:
#         for data in known_humans_data(kernal, lang, 'small'):
#             for s1_1 in nlp_base_self_address_s(kernal, lang, []):
#                 for s1_2,tstart,tend in nlp_humans_whatabout_s(lang, s1_1, data[1]):
#                     g1 = nlp_humans_whatabout_g(lang, tstart, tend)
#                     for r1 in nlp_humans_whereborn_r(lang, []):
# 
#                         for s2 in nlp_base_whatwasourtopic_s(lang, []):
#                             for r2 in nlp_humans_topic_r(lang, []):
#                                 cnt += 1
#                                 if cnt % MULTI_ROUND_MOD == 0:
#                                     res.append((lang, [[], s1_2, g1, r1, [], s2, [], r2]))
# 
#                         for s2 in nlp_base_sayagain_s(lang, []):
#                             for r2_1 in nlp_base_isaid_r(lang, []):
#                                 for r2_2 in nlp_humans_whereborn_r(lang, r2_1):
#                                     cnt += 1
#                                     if cnt % MULTI_ROUND_MOD == 0:
#                                         res.append((lang, [[], s1_2, g1, r1, [], s2, [], r2_2]))
# 
#                         g2 = nlp_humans_whenborn_followup_g()
#                         for s2 in nlp_humans_whenborn_followup_s(lang, []):
#                             for r2 in nlp_humans_whenborn_r(lang, []):
#                                 cnt += 1
#                                 if cnt % MULTI_ROUND_MOD == 0:
#                                     res.append((lang, [[], s1_2, g1, r1, [], s2, g2, r2]))
# 
#                         g2 = nlp_humans_whereborn_followup_g()
#                         for s2 in nlp_humans_whereborn_followup_s(lang, []):
#                             for r2 in nlp_humans_whereborn_r(lang, []):
#                                 cnt += 1
#                                 if cnt % MULTI_ROUND_MOD == 0:
#                                     res.append((lang, [[], s1_2, g1, r1, [], s2, g2, r2]))
# 
# 
# def nlp_train (kernal):
# 
#     res = []
# 
#     nlp_humans_doyouknow(kernal, res)
#     nlp_humans_whereborn(kernal, res)
#     nlp_humans_whenborn(kernal, res)
#     nlp_humans_whatabout(kernal, res)
# 
#     return res
# 
# 
# def nlp_test (kernal):
# 
#     return [ ('de', 'know1',      [], ["Kennst Du Stephen King?", "Ja ich kenne Stephen King", []]),
#              ('en', 'know2',      [], ["Do you know Stephen King?", "Sure I know Stephen King", []]),
#              ('en', 'know3',      [], ["Do you know Stephen King?", "Sure I know him", []]), 
# 
#              # ('de', 'know4',      [], ["Kennst Du Stephen King?", "Ja ich kenne Stephen King", [], "und an welchem ort wurde er geboren?", 'Stephen King wurde in Portland geboren.', []]),
#              # ('de', 'know5',      [], ["Computer, Kennst Du Stephen King?", "Ja ich kenne Stephen King", [], "und in welchem jahr wurde er eigentlich geboren?", 'Stephen King wurde am einundzwanzigsten September 1947 geboren.', []]),
#              # ('de', 'know6',      [], ["Kennst Du Stephen King?", "Ja ich kenne Stephen King", [], "wie bitte?", 'Ich sagte Ja ich kenne Stephen King.', []]),
#              # ('de', 'know7',      [], ["Kennst Du Stephen King?", "Ja ich kenne Stephen King", [], "was war unser thema?", 'Unser Thema war Stephen King', []]),
# 
#              # ('en', 'know8',      [], ["Do you know Stephen King?", "Sure I know him", [], "where was he born?", 'Stephen King was born in Portland.', []]), 
#              # ('en', 'know9',      [], ["Do you know Stephen King?", "Sure I know him", [], "when was he born?", 'Stephen King was born on September 21, 1947.', []]), 
#              # ('en', 'know10',     [], ["Do you know Stephen King?", "Sure I know him", [], "huh?", 'I said Sure I know him', []]), 
#              # ('en', 'know11',     [], ["Do you know Stephen King?", "Sure I know him", [], "what was our topic?", 'We were talking about Stephen King.', []]), 
# 
#              ('en', 'whereborn1', [], ['Where was Stephen King born?', 'Stephen King was born in Portland.', []]),
#              # ('en', 'whereborn2', [], ['Where was Stephen King born?', 'Stephen King was born in Portland.', [], "and when?", "Stephen King was born September 21, 1947.", []]),
#              # ('en', 'whereborn3', [], ['Where was Stephen King born?', 'Stephen King was born in Portland.', [], "huh?", "I said Stephen King was born in Portland.", []]),
#              # ('en', 'whereborn4', [], ['Where was Stephen King born?', 'Stephen King was born in Portland.', [], "what was our topic?", "We were talking about Stephen King.", []]),
# 
#              ('de', 'whereborn5', [], ['Wo wurde Stephen King geboren?', 'Stephen King wurde in Portland geboren.', []]),
#              # ('de', 'whereborn6', [], ['Wo wurde Stephen King geboren?', 'Stephen King wurde in Portland geboren.', [], "und wann?", "Stephen King wurde am einundzwanzigsten September 1947 geboren.", []]),
#              # ('de', 'whereborn7', [], ['Wo wurde Stephen King geboren?', 'Stephen King wurde in Portland geboren.', [], "wie bitte?", "Ich sagte Stephen King wurde in Portland geboren.", []]),
#              # ('de', 'whereborn8', [], ['Wo wurde Stephen King geboren?', 'Stephen King wurde in Portland geboren.', [], "was war unser Thema?", "Unser Thema war Stephen King", []]),
# 
#              ('en', 'whenborn1',  [], ['When was Stephen King born?', 'Stephen King was born on September 21, 1947.', []]),
#              # ('en', 'whenborn2',  [], ['When was Stephen King born?', 'Stephen King was born on September 21, 1947.', [], 'and where?', 'Stephen King was born in Portland.', []]),
#              # ('en', 'whenborn3',  [], ['When was Stephen King born?', 'Stephen King was born on September 21, 1947.', [], 'huh?', 'I said Stephen King was born on September 21, 1947.', []]),
#              # ('en', 'whenborn4',  [], ['When was Stephen King born?', 'Stephen King was born on September 21, 1947.', [], 'what was our topic?', 'We were talking about Stephen King.', []]),
# 
#              ('de', 'whenborn5',  [], ['Wann wurde Stephen King geboren?', 'Stephen King wurde am einundzwanzigsten September 1947 geboren.', []]),
#              # ('de', 'whenborn6',  [], ['Wann wurde Stephen King geboren?', 'Stephen King wurde am einundzwanzigsten September 1947 geboren.', [], 'und wo?', 'Stephen King wurde in Portland geboren.', []]),
#              # ('de', 'whenborn7',  [], ['Wann wurde Stephen King geboren?', 'Stephen King wurde am einundzwanzigsten September 1947 geboren.', [], 'wie bitte?', 'ich sagte Stephen King wurde am einundzwanzigsten September 1947 geboren.', []]),
#              # ('de', 'whenborn8',  [], ['Wann wurde Stephen King geboren?', 'Stephen King wurde am einundzwanzigsten September 1947 geboren.', [], 'was war unser Thema?', 'Unser Thema war Stephen King', []]),
# 
#              ('en', 'whatabout1', [], ['What about Stephen King?', 'Stephen King was born in Portland.', []]),
#              ('de', 'whatabout2', [], ['Was ist mit Stephen King?', 'Stephen King wurde in Portland geboren.', []]),
#              # ('en', 'whatabout3', [], ['What about Stephen King?', 'Stephen King was born in Portland.', [], "huh?", "I said Stephen King was born in Portland.", []]),
#              # ('de', 'whatabout4', [], ['Was ist mit Stephen King?', 'Stephen King wurde in Portland geboren.', [], "wie bitte?", "Ich sagte Stephen King wurde in Portland geboren.", []]),
#              # ('en', 'whatabout5', [], ['What about Stephen King?', 'Stephen King was born in Portland.', [], "what was our topic", "We were talking about Stephen King", []]),
#              # ('de', 'whatabout6', [], ['Was ist mit Stephen King?', 'Stephen King wurde in Portland geboren.', [], "worüber haben wir gesprochen?", "Unser Thema war Stephen King", []]),
#              # ('en', 'whatabout7', [], ['What about Stephen King?', 'Stephen King was born in Portland.', [], "when was he born?", "Stephen King was born on September 21, 1947.", []]),
#              # ('de', 'whatabout8', [], ['Was ist mit Stephen King?', 'Stephen King wurde in Portland geboren.', [], "und wann wurde er geboren?", "Stephen King wurde am einundzwanzigsten September 1947 geboren.", []]),
#              # ('en', 'whatabout9', [], ['What about Stephen King?', 'Stephen King was born in Portland.', [], "and where?", "Stephen King was born in Portland.", []]),
#              # ('de', 'whatabout10',[], ['Was ist mit Stephen King?', 'Stephen King wurde in Portland geboren.', [], "und wo?", "Stephen King wurde in Portland geboren.", []]),
#            ]

