#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import rdflib
from tzlocal import get_localzone # $ pip install tzlocal
import dateutil.parser
from datetime import datetime
from copy import copy
from nltools.tokenizer import tokenize

from base import hears, says

DEPENDS    = [ 'config', 'base' ]

DEBUG_MODE = True

NLP_BASE_SELF_ADDRESS_S = {'en': ['hal', 'computer', ''],
                           'de': ['hal', 'computer', '']}

def nlp_base_self_address_s(lang, s):

    res = []
    for txt in NLP_BASE_SELF_ADDRESS_S[lang]:
        res.append(hears (lang, s, txt))

    return res


# def nlp_greetings_s (res, s, nextf):
#     for txt in ['greetings','good morning','hello','hallo','hi','good day','morning','good evening','good night','Cooee','Cooey','hi there']:
#         s1 = hears(res, s, txt, nextf)
#         
# res=[]
# self_address(res, [], [nlp_greetings_s])
# print res

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
               

def nlp_dt_en_start_time(res):

    g = [

        "t = ias['currentTime']",

        "ias['f1_type']  = 'question'",
        "ias['f1_topic'] = 'time'",

        "t_h12 = t.hour if t.hour<13 else t.hour-12",

        "ias['f1_hour']   = t_h12",
        "ias['f1_minute'] = t.minute",

        ]

    for ts in nlp_datetime_train_time_ts():

        p1 = [ "import dateutil.parser ; ias['currentTime'] = dateutil.parser.parse('%s')" % ts.isoformat() ]

        for lang in ['en', 'de']:
            s = []
            for s1 in nlp_base_self_address_s(lang, s):
                for s2 in nlp_dt_time_s(lang, s1):

                    r = []
                    for r1 in nlp_dt_r(lang, r, ts.hour, ts.minute):
                        res.append((lang, [p1, s2, g, r1]))


def nlp_train (kernal):

    res = []

    nlp_dt_en_start_time(res)

    return res

def nlp_test (kernal):

    p1 = [ "import dateutil.parser ; ias['currentTime'] = dateutil.parser.parse('2017-06-12T06:30:00+01:00')" ]
    p2 = [ "import dateutil.parser ; ias['currentTime'] = dateutil.parser.parse('2017-06-12T13:15:00+01:00')" ]

    return [ ('en', 'time1', p1, ["what time is it", "It is half past 6.", []]),
             ('en', 'time2', p2, ["what time is it", "It is a quarter past 1.", []]),
             ('de', 'time3', p1, ["wie spät ist es", "Es ist eine halbe Stunde nach 6.", []]),
             ('de', 'time4', p2, ["wie spät ist es", "Es ist viertel nach 1.", []]) ]

