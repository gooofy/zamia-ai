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

from tzlocal import get_localzone # $ pip install tzlocal
import dateutil.parser
from datetime import datetime
from copy import copy
from nltools.tokenizer import tokenize

from base.utils import hears, says, nlp_base_self_address_s
from base.conversation import nlp_base_sayagain_s, nlp_base_isaid_r, nlp_base_whatwasourtopic_s

DEPENDS    = [ 'config', 'base' ]

DEBUG_MODE = False

localzone = get_localzone()

nlp_dt_train_time_ts_small = [

    datetime(2017,  6, 12,  6, 30, tzinfo=localzone),
    datetime(2017,  2,  8, 13, 15, tzinfo=localzone)
    
    ]

def nlp_dt_train_time_ts():

    if DEBUG_MODE:
        dataset = nlp_dt_train_time_ts_small
    else:
        dataset = []
        for h in range(24):
            for m in range(60):
                dataset.append(datetime(2017,  6, 12,  h,  m, tzinfo=localzone))

    return dataset

NLP_DT_TIME_S = {'en': [ "do you know what time it is",
                         "what time is it",
                         "what's the time?"],
                 'de': [ "weißt du wie spät es ist",
                         "wieviel uhr ist es",
                         "wieviel uhr haben wir",
                         "wie spät ist es" ]}

def nlp_dt_time_s(lang, s):

    res = []
    for txt in NLP_DT_TIME_S[lang]:
        res.append(hears (lang, s, txt))

    return res

def nlp_base_time_r(lang, r, t_h, t_m):

    if lang == 'en':

        if t_m == 1:
            return  [ says ('en', r, "one minute past %(f1_hour)d") ]
        elif t_m == 15:
            return  [ says ('en', r, "a quarter past %(f1_hour)d") ]
        elif t_m == 30:
            return  [ says ('en', r, "half past %(f1_hour)d") ]
        else:
            return  [ says ('en', r, "%(f1_minute)d minutes past %(f1_hour)d") ]

    elif lang == 'de':

        if t_m == 1:
            return  [ says ('de', r, "eine Minute nach %(f1_hour)d") ]
        elif t_m == 15:
            return  [ says ('de', r, "viertel nach %(f1_hour)d") ]
        elif t_m == 30:
            return  [ says ('de', r, "eine halbe Stunde nach %(f1_hour)d") ]
        else:
            return  [ says ('de', r, "%(f1_minute)d Minuten nach %(f1_hour)d") ]

    else:
        raise Exception ('unsupported language "%s"' % lang)

NLP_DT_TIME_R = {'en' : [ "It is", 
                          "It is now", 
                          "The time is", 
                          "The time is now" ],
                 'de' : [ "Es ist", 
                          "Es ist jetzt", 
                          "Wir haben es ", 
                          "Die Uhrzeit ist " ]}


def nlp_dt_time_r(lang, r, t_h, t_m):
    
    res = []

    for txt in NLP_DT_TIME_R[lang]:
        r1 = says(lang, r, txt)
        for r2 in nlp_base_time_r(lang, r1, t_h, t_m):
            res.append(r2)
               
    return res
               
def nlp_dt_topic_time_r (lang, r):

    if lang == 'en':

        return [ says ('en', r, 'We were talking about the time'),
                 says ('en', r, 'The time was our topic') ]

    elif lang == 'de':

        return [ says ('de', r, 'Wir haben über die Zeit gesprochen'),
                 says ('de', r, 'Die Uhrzeit war unser Thema'),
               ] 

    else:
        raise Exception ('unsupported language: %s' % lang)

def nlp_dt_en_start_time(kernal, res):

    g = [

        "t = ias['currentTime']",

        "ias['f1_type']  = 'question'",
        "ias['f1_topic'] = 'time'",

        "t_h12 = t.hour if t.hour<13 else t.hour-12",

        "ias['f1_hour']   = t_h12",
        "ias['f1_minute'] = t.minute",

        ]

    # single-round training

    for ts in nlp_dt_train_time_ts():

        p1 = [ "import dateutil.parser ; ias['currentTime'] = dateutil.parser.parse('%s')" % ts.isoformat() ]

        for lang in ['en', 'de']:
            s = []
            for s1 in nlp_base_self_address_s(kernal, lang, s):
                for s2 in nlp_dt_time_s(lang, s1):

                    r = []
                    for r1 in nlp_dt_time_r(lang, r, ts.hour, ts.minute):
                        res.append((lang, [p1, s2, g, r1]))

    # multi-round / followup

    for ts in nlp_dt_train_time_ts_small:

        p1 = [ "import dateutil.parser ; ias['currentTime'] = dateutil.parser.parse('%s')" % ts.isoformat() ]

        for lang in ['en', 'de']:
            s1_1 = []
            for s1_2 in nlp_base_self_address_s(kernal, lang, s1_1):
                for s1_2 in nlp_dt_time_s(lang, s1_1):

                    for r1 in nlp_dt_time_r(lang, [], ts.hour, ts.minute):

                        for s2 in nlp_base_whatwasourtopic_s(lang, []):
                            for r2 in nlp_dt_topic_time_r(lang, []):
                                res.append((lang, [p1, s1_2, g, r1, p1, s2, [], r2]))

                        for s2 in nlp_base_sayagain_s(lang, []):
                            for r2_1 in nlp_base_isaid_r(lang, []):
                                for r2_2 in nlp_dt_time_r(lang, r2_1, ts.hour, ts.minute):
                                    res.append((lang, [p1, s1_2, g, r1, p1, s2, [], r2_2]))


#
# date questions
#

nlp_dt_train_date_ts_small = [

    datetime(2017,  6, 12,  6, 30, tzinfo=localzone),
    datetime(2017,  2,  8, 13, 15, tzinfo=localzone)
    
    ]

def nlp_dt_train_date_ts():

    if DEBUG_MODE:
        dataset = nlp_dt_train_date_ts_small
    else:
        dataset = []
        for d in range(31):
            dataset.append(datetime(2017,  1, d+1, 10,  0, tzinfo=localzone))
        for d in range(28):
            dataset.append(datetime(2017,  2, d+1, 10,  0, tzinfo=localzone))
        for d in range(31):
            dataset.append(datetime(2017,  3, d+1, 10,  0, tzinfo=localzone))
        for d in range(30):
            dataset.append(datetime(2017,  4, d+1, 10,  0, tzinfo=localzone))
        for d in range(31):
            dataset.append(datetime(2017,  5, d+1, 10,  0, tzinfo=localzone))
        for d in range(30):
            dataset.append(datetime(2017,  6, d+1, 10,  0, tzinfo=localzone))
        for d in range(31):
            dataset.append(datetime(2017,  7, d+1, 10,  0, tzinfo=localzone))
        for d in range(31):
            dataset.append(datetime(2017,  8, d+1, 10,  0, tzinfo=localzone))
        for d in range(30):
            dataset.append(datetime(2017,  9, d+1, 10,  0, tzinfo=localzone))
        for d in range(31):
            dataset.append(datetime(2017, 10, d+1, 10,  0, tzinfo=localzone))
        for d in range(30):
            dataset.append(datetime(2017, 11, d+1, 10,  0, tzinfo=localzone))
        for d in range(31):
            dataset.append(datetime(2017, 12, d+1, 10,  0, tzinfo=localzone))

    return dataset

def nlp_dt_date_s(lang, s):

    if lang == 'en':

        res = []

        res.extend(hears ('en', s, ['do you know what', ['day','date'], 'it is', ['today','']]))
        res.extend(hears ('en', s, ['what', ['date','day'], 'is it', ['today','']]))
        res.extend(hears ('en', s, ["what's the date", ['today','']]))

    elif lang == 'de':

        res = []

        res.extend(hears ('de', s, ['weisst du', ['welchen tag', 'welches datum'], 'wir', ['heute',''], 'haben']))
        res.extend(hears ('de', s, [['welchen tag','welches datum'], 'haben wir', ['heute','']]))
        res.extend(hears ('de', s, ['was ist heute für ein', ['tag','datum']]))
        res.extend(hears ('de', s, ['welchen haben wir heute']))

    else:
        raise Exception ('unsupported language: %s' % lang)

    return res

def nlp_dt_date_r (lang, r):

    if lang == 'en':

        return [ says ('en', r, u'The date is %(f1_wday_label)s %(f1_month_label)s %(f1_day)d, %(f1_year)d'),
                 says ('en', r, u'Today is %(f1_wday_label)s %(f1_month_label)s %(f1_day)d, %(f1_year)d'),
               ] 

    elif lang == 'de':

        return [ says ('de', r, u'Das Datum ist %(f1_wday_label)s der %(f1_day_label)s %(f1_month_label)s %(f1_year)d'),
                 says ('de', r, u'Heute ist %(f1_wday_label)s der %(f1_day_label)s %(f1_month_label)s %(f1_year)d'),
               ]

    else:
        raise Exception ('unsupported language: %s' % lang)
    
def nlp_dt_topic_date_r (lang, r):

    if lang == 'en':

        return [ says ('en', r, 'We were talking about the date'),
                 says ('en', r, 'The date was our topic') ]

    elif lang == 'de':

        return [ says ('de', r, 'Wir haben über das Datum gesprochen'),
                 says ('de', r, 'Das Datum war unser Thema'),
               ] 

    else:
        raise Exception ('unsupported language: %s' % lang)

def nlp_dt_en_start_date(kernal, res):

    g = [

        "t = ias['currentTime']",

        "ias['f1_type']        = 'question'",
        "ias['f1_topic']       = 'date'",

        "ias['f1_day']         = t.day",
        "ias['f1_month']       = t.month",
        "ias['f1_year']        = t.year",

        "from base.time import NLP_DAY_OF_THE_WEEK_LABEL, NLP_MONTH_LABEL",

        "ias['f1_wday_label']  = NLP_DAY_OF_THE_WEEK_LABEL[ias['lang']][t.weekday()]",
        "ias['f1_month_label'] = NLP_MONTH_LABEL[ias['lang']][t.month]",

        "from num2words import num2words",

        "ias['f1_day_label']   = num2words(t.day, ordinal=True, lang=ias['lang'])",


        ]

    # single-round training

    for ts in nlp_dt_train_date_ts():

        p1 = [ "import dateutil.parser ; ias['currentTime'] = dateutil.parser.parse('%s')" % ts.isoformat() ]

        for lang in ['en', 'de']:
            s = []
            for s1 in nlp_base_self_address_s(kernal, lang, s):
                for s2 in nlp_dt_date_s(lang, s1):
                    for r1 in nlp_dt_date_r(lang, []):
                        res.append((lang, [p1, s2, g, r1]))

    # multi-round / followup

    for ts in nlp_dt_train_date_ts_small:

        p1 = [ "import dateutil.parser ; ias['currentTime'] = dateutil.parser.parse('%s')" % ts.isoformat() ]

        for lang in ['en', 'de']:
            s1_1 = []
            for s1_2 in nlp_base_self_address_s(kernal, lang, s1_1):
                for s1_2 in nlp_dt_date_s(lang, s1_1):

                    for r1 in nlp_dt_date_r(lang, []):

                        for s2 in nlp_base_whatwasourtopic_s(lang, []):
                            for r2 in nlp_dt_topic_date_r(lang, []):
                                res.append((lang, [p1, s1_2, g, r1, p1, s2, [], r2]))

                        for s2 in nlp_base_sayagain_s(lang, []):
                            for r2_1 in nlp_base_isaid_r(lang, []):
                                for r2_2 in nlp_dt_date_r(lang, r2_1):
                                    res.append((lang, [p1, s1_2, g, r1, p1, s2, [], r2_2]))

def nlp_train (kernal):

    res = []

    nlp_dt_en_start_time(kernal, res)
    nlp_dt_en_start_date(kernal, res)

    return res

def nlp_test (kernal):

    p1 = [ "import dateutil.parser ; ias['currentTime'] = dateutil.parser.parse('2017-06-12T06:30:00+01:00')" ]
    p2 = [ "import dateutil.parser ; ias['currentTime'] = dateutil.parser.parse('2017-02-08T13:15:00+01:00')" ]

    return [ ('en', 'time1', p1, ["what time is it", "It is half past 6.", []]),
             ('en', 'time2', p2, ["what time is it", "It is a quarter past 1.", []]),
             ('en', 'time3', p2, ["what time is it", "It is a quarter past 1.", [], "huh?", "I said it is a quarter past 1.", []]),
             ('en', 'time3', p2, ["what time is it", "It is a quarter past 1.", [], "what was our topic?", "We were talking about the time.", []]),
             ('de', 'time4', p1, ["wie spät ist es", "Es ist eine halbe Stunde nach 6.", []]),
             ('de', 'time5', p2, ["wie spät ist es", "Es ist viertel nach 1.", []]),
             ('de', 'time6', p2, ["wie spät ist es", "Es ist viertel nach 1.", [], "was?", "Ich sagte es ist viertel nach eins.", []]),
             ('de', 'time6', p2, ["wie spät ist es", "Es ist viertel nach 1.", [], "worüber haben wir gesprochen?", "Die Uhrzeit war unser Thema.", []]),
             ('en', 'date1', p1, ["what date is it", "The date is Monday June 12, 2017.", []]),
             ('en', 'date2', p2, ["what date is it", "The date is Wednesday February 8, 2017", []]),
             ('en', 'date3', p2, ["what date is it", "The date is Wednesday February 8, 2017", [], "huh?", "I said The date is Wednesday February 8, 2017.", []]),
             ('en', 'date3', p2, ["what date is it", "The date is Wednesday February 8, 2017", [], "what was our topic?", "We were talking about the date.", []]),
             ('de', 'date4', p1, ["Welchen Tag haben wir heute?", "Heute ist Montag der zwölfte Juni 2017", []]),
             ('de', 'date5', p2, ["Welchen Tag haben wir heute?", "Heute ist Mittwoch der achte Februar 2017", []]),
             ('de', 'date6', p2, ["Welchen Tag haben wir heute?", "Heute ist Mittwoch der achte Februar 2017", [],
             "was?", "Ich sagte Heute ist Mittwoch der achte Februar 2017.", []]),
             ('de', 'date6', p2, ["Welchen Tag haben wir heute?", "Heute ist Mittwoch der achte Februar 2017", [], "worüber haben wir gesprochen?", "Das Datum war unser Thema.", []]),
           ]

