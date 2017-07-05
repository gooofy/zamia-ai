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

#
# hello
#

def nlp_greetings_hello_s(lang, s):

    if lang == 'en':

        res = []

        res.extend(hears ('en', s, ['greetings']))
        res.extend(hears ('en', s, ['good morning']))
        res.extend(hears ('en', s, ['hello']))
        res.extend(hears ('en', s, ['hallo']))
        res.extend(hears ('en', s, ['hi']))
        res.extend(hears ('en', s, ['good day']))
        res.extend(hears ('en', s, ['morning']))
        res.extend(hears ('en', s, ['good evening']))
        res.extend(hears ('en', s, ['good night']))
        res.extend(hears ('en', s, ['Cooee']))
        res.extend(hears ('en', s, ['Cooey']))
        res.extend(hears ('en', s, ['hi there']))

    elif lang == 'de':

        res = []

        res.extend(hears ('de', s, ['grüß dich']))
        res.extend(hears ('de', s, ['hallo']))
        res.extend(hears ('de', s, ['hi']))
        res.extend(hears ('de', s, ['guten morgen']))
        res.extend(hears ('de', s, ['guten tag']))
        res.extend(hears ('de', s, ['guten abend']))
        res.extend(hears ('de', s, ['guten nachmittag']))
        res.extend(hears ('de', s, ['gute nacht']))
        res.extend(hears ('de', s, ['schönen guten morgen']))
        res.extend(hears ('de', s, ['schönen guten tag']))
        res.extend(hears ('de', s, ['schönen guten abend']))
        res.extend(hears ('de', s, ['schönen guten nachmittag']))
        res.extend(hears ('de', s, ['gute nacht']))
        res.extend(hears ('de', s, ['tag']))
        res.extend(hears ('de', s, ['morgen']))
        res.extend(hears ('de', s, ['huhu']))

    else:
        raise Exception ('unsupported language: %s' % lang)

    return res

def nlp_greetings_hello_r(lang, r):

    if lang == 'en':

        return [ 
                 says ('en', r, u'Hello!'    , actions = [['attention', 'on']]),
                 says ('en', r, u'Hi!'       , actions = [['attention', 'on']]),
                 says ('en', r, u'Greetings!', actions = [['attention', 'on']]),
                 says ('en', r, u'Hey!'      , actions = [['attention', 'on']]),
               ] 

    elif lang == 'de':

        return [ 
                 says ('de', r, u'Hallo!'    , actions = [['attention', 'on']]),
                 says ('de', r, u'Hi!'       , actions = [['attention', 'on']]),
                 says ('de', r, u'Grüß Dich!', actions = [['attention', 'on']]),
                 says ('de', r, u'Hey!'      , actions = [['attention', 'on']]),
               ]

    else:
        raise Exception ('unsupported language: %s' % lang)
    
def nlp_greetings_hello(kernal, res):

    # single-round training

    for lang in ['en', 'de']:
        for s1_1 in nlp_base_self_address_s(kernal, lang, []):
            for s1_2 in nlp_greetings_hello_s(lang, s1_1):
                for r1 in nlp_greetings_hello_r(lang, []):
                    res.append((lang, [[], s1_2, [], r1]))

    return res

#
# bye
#

def nlp_greetings_goodbye_s(lang, s):

    if lang == 'en':

        res = []

        res.extend(hears ('en', s, ['goodbye']))
        res.extend(hears ('en', s, ['bye']))
        res.extend(hears ('en', s, ['ciao']))
        res.extend(hears ('en', s, ['so long']))
        res.extend(hears ('en', s, ['bye for now']))
        res.extend(hears ('en', s, ['see ya']))
        res.extend(hears ('en', s, ['see you later']))
        res.extend(hears ('en', s, ['till next time']))

    elif lang == 'de':

        res = []

        res.extend(hears ('de', s, ['auf wiedersehen']))
        res.extend(hears ('de', s, ['tschüss']))
        res.extend(hears ('de', s, ['ciao']))
        res.extend(hears ('de', s, ['ade']))
        res.extend(hears ('de', s, ['bye']))
        res.extend(hears ('de', s, ['cu']))
        res.extend(hears ('de', s, ['bis bald']))
        res.extend(hears ('de', s, ['bis zum nächsten mal']))

    else:
        raise Exception ('unsupported language: %s' % lang)

    return res

def nlp_greetings_goodbye_r(lang, r):

    if lang == 'en':

        return [ 
                 says ('en', r, u'Bye'             , actions = [['attention', 'off']]),
                 says ('en', r, u'So long'         , actions = [['attention', 'off']]),
                 says ('en', r, u'See you later'   , actions = [['attention', 'off']]),
                 says ('en', r, u'Bye for now'     , actions = [['attention', 'off']]),
               ] 

    elif lang == 'de':

        return [ 
                 says ('de', r, u'Ade'             , actions = [['attention', 'off']]),
                 says ('de', r, u'Tschüss'         , actions = [['attention', 'off']]),
                 says ('de', r, u'Bis bald'        , actions = [['attention', 'off']]),
                 says ('de', r, u'Ciao'            , actions = [['attention', 'off']]),
               ]

    else:
        raise Exception ('unsupported language: %s' % lang)
    
def nlp_greetings_goodbye(kernal, res):

    # single-round training

    for lang in ['en', 'de']:
        for s1_1 in nlp_greetings_goodbye_s(lang, []):
            for s1_2 in nlp_base_self_address_s(kernal, lang, s1_1):
                for r1 in nlp_greetings_goodbye_r(lang, []):
                    res.append((lang, [[], s1_2, [], r1]))

    return res


#
# howdy
#
 
def nlp_greetings_howdy_s(lang, s):

    if lang == 'en':

        res = []

        res.extend(hears ('en', s, [["how are you","howdy","how do you do","how are you feeling"], ["today",""], "?"]))

    elif lang == 'de':

        res = []

        res.extend(hears ('de', s, [["wie geht es dir","wie gehts","was geht","wie fühlst du dich"], ["heute",""], "?"]))

    else:
        raise Exception ('unsupported language: %s' % lang)

    return res

def nlp_greetings_howdy_r(lang, r):

    if lang == 'en':

        return [ 
                 says ('en', r, u'Great, thanks. How do you feel today?'),
                 says ('en', r, u'Very well - and you?'),
                 says ('en', r, u'I am doing great, how are you doing?'),
                 says ('en', r, u'Great as always!'),
                 says ('en', r, u'Thanks for asking, I am doing fine. How about you?'),
               ] 

    elif lang == 'de':

        return [ 
                 says ('de', r, u'Sehr gut, danke. Und selber?'),
                 says ('de', r, u'Gut, danke. Wie geht es Dir?'),
                 says ('de', r, u'Mir geht es prima, und Dir?'),
                 says ('de', r, u'Mir geht es gut, und selber?'),
                 says ('de', r, u'Super, wie immer!'),
                 says ('de', r, u'Gut, danke der Nachfrage. Wie geht es Dir?'),
               ]

    else:
        raise Exception ('unsupported language: %s' % lang)

def nlp_greetings_howdy(kernal, res):

    # single-round training

    for lang in ['en', 'de']:
        for s1_1 in nlp_base_self_address_s(kernal, lang, []):
            for s1_2 in nlp_greetings_howdy_s(lang, s1_1):
                for r1 in nlp_greetings_howdy_r(lang, []):
                    res.append((lang, [[], s1_2, [], r1]))

    return res

def nlp_smalltalk_greetings_train(kernal, res):

    res = []

    nlp_greetings_hello(kernal, res)
    nlp_greetings_goodbye(kernal, res)
    nlp_greetings_howdy(kernal, res)

    return res

def nlp_smalltalk_greetings_test(kernal, res):

    res.extend([ 
                ('en', 'hello1',   [], ["Hi!",                        "hello!",             [['attention', 'on']]]),
                ('de', 'hello2',   [], ["Hallo!",                     "hallo!",             [['attention', 'on']]]),
                ('en', 'goodbye1', [], ["Bye!",                       "Bye!",               [['attention', 'off']]]),
                ('de', 'goodbye2', [], ["Tschüss Computer!",          "Tschüss!",           [['attention', 'off']]]),
                ('en', 'howdy1',   [], ["Computer, how are you?",     "very well and you?", []]),
                ('de', 'howdy2',   [], ["Computer, wie geht es Dir?", "Super, wie immer!",  []]),
               ])
