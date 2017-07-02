#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from tzlocal import get_localzone # $ pip install tzlocal
import dateutil.parser
from datetime import datetime
from copy import copy
from nltools.tokenizer import tokenize

from base.utils import hears, says, nlp_base_self_address_s
from base.conversation import nlp_base_sayagain_s, nlp_base_isaid_r, nlp_base_whatwasourtopic_s

DEPENDS    = [ 'config', 'base' ]

DEBUG_MODE = True

localzone = get_localzone()

nlp_datetime_train_time_ts_small = [

    datetime(2017,  6, 12,  6, 30, tzinfo=localzone),
    datetime(2017,  6, 12, 13, 15, tzinfo=localzone)
    
    ]

def nlp_datetime_train_time_ts():

    if DEBUG_MODE:
        dataset = nlp_datetime_train_time_ts_small
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


def nlp_dt_r(lang, r, t_h, t_m):
    
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

    for ts in nlp_datetime_train_time_ts():

        p1 = [ "import dateutil.parser ; ias['currentTime'] = dateutil.parser.parse('%s')" % ts.isoformat() ]

        for lang in ['en', 'de']:
            s = []
            for s1 in nlp_base_self_address_s(kernal, lang, s):
                for s2 in nlp_dt_time_s(lang, s1):

                    r = []
                    for r1 in nlp_dt_r(lang, r, ts.hour, ts.minute):
                        res.append((lang, [p1, s2, g, r1]))

    # multi-round / followup

    for ts in nlp_datetime_train_time_ts_small:

        p1 = [ "import dateutil.parser ; ias['currentTime'] = dateutil.parser.parse('%s')" % ts.isoformat() ]

        for lang in ['en', 'de']:
            s1_1 = []
            for s1_2 in nlp_base_self_address_s(kernal, lang, s1_1):
                for s1_2 in nlp_dt_time_s(lang, s1_1):

                    for r1 in nlp_dt_r(lang, [], ts.hour, ts.minute):

                        for s2 in nlp_base_whatwasourtopic_s(lang, []):
                            for r2 in nlp_dt_topic_time_r(lang, []):
                                res.append((lang, [p1, s1_2, g, r1, p1, s2, [], r2]))

                        for s2 in nlp_base_sayagain_s(lang, []):
                            for r2_1 in nlp_base_isaid_r(lang, []):
                                for r2_2 in nlp_dt_r(lang, r2_1, ts.hour, ts.minute):
                                    res.append((lang, [p1, s1_2, g, r1, p1, s2, [], r2_2]))


def nlp_train (kernal):

    res = []

    nlp_dt_en_start_time(kernal, res)

    return res

def nlp_test (kernal):

    p1 = [ "import dateutil.parser ; ias['currentTime'] = dateutil.parser.parse('2017-06-12T06:30:00+01:00')" ]
    p2 = [ "import dateutil.parser ; ias['currentTime'] = dateutil.parser.parse('2017-06-12T13:15:00+01:00')" ]

    return [ ('en', 'time1', p1, ["what time is it", "It is half past 6.", []]),
             ('en', 'time2', p2, ["what time is it", "It is a quarter past 1.", []]),
             ('en', 'time3', p2, ["what time is it", "It is a quarter past 1.", [], "huh?", "I said it is a quarter past 1.", []]),
             ('en', 'time3', p2, ["what time is it", "It is a quarter past 1.", [], "what was our topic?", "We were talking about the time.", []]),
             ('de', 'time4', p1, ["wie spät ist es", "Es ist eine halbe Stunde nach 6.", []]),
             ('de', 'time5', p2, ["wie spät ist es", "Es ist viertel nach 1.", []]),
             ('de', 'time6', p2, ["wie spät ist es", "Es ist viertel nach 1.", [], "was?", "Ich sagte es ist viertel nach eins.", []]),
             ('de', 'time6', p2, ["wie spät ist es", "Es ist viertel nach 1.", [], "worüber haben wir gesprochen?", "Die Uhrzeit war unser Thema.", []]),
           ]

