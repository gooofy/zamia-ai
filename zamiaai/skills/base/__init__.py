#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging

from num2words         import num2words

DEPENDS    = [ 'config' ]

PL_SOURCES = ['utils.pl']

# wikidata utils in python

def transcribe_number (n, lang, flx):

    if flx == 'nominative':
        return num2words(n, ordinal=False, lang=lang)
    elif flx == 'ordinal':
        return num2words(n, ordinal=True, lang=lang)
    elif flx == 'ordgen':
        res = num2words(n, ordinal=True, lang=lang)
        if lang == 'de':
            res += u'n'
        return res
    else:
        raise Exception('transcribe_number: flx "%s" not recognized.' % flx)

def transcribe_time(dt, lang):

    h12 = dt.hour if dt.hour < 13 else dt.hour - 12

    if lang == 'en':
        if dt.minute == 0:
            return u"exactly %d o'clock" % h12
        elif dt.minute == 1:
            return u"one minute past %d" % h12
        elif dt.minute == 15:
            return u"a quarter past %d" % h12
        elif dt.minute == 30:
            return u"half past %d" % h12

        return u"%d minutes past %d" % (dt.minute, h12)

    if dt.minute == 0:
        return u"genau %d Uhr" % h12
    elif dt.minute == 1:
        return u"eine Minute nach %d" % h12
    elif dt.minute == 15:
        return u"viertel nach %d" % h12
    elif dt.minute == 30:
        return u"eine halbe Stunde nach %d" % h12

    return u"%d Minuten nach %d" % (dt.minute, h12)

def get_time_span (cdt, ts):
    if ts == 'today':
        return cdt.replace(hour= 0, minute= 0, second= 0, microsecond=0), \
               cdt.replace(hour=23, minute=59, second=59, microsecond=0)

    if ts == 'tomorrow':
        return cdt.replace(day=cdt.day+1, hour= 0, minute= 0, second= 0, microsecond=0), \
               cdt.replace(day=cdt.day+1, hour=23, minute=59, second=59, microsecond=0)

    if ts == 'dayAfterTomorrow':
        return cdt.replace(day=cdt.day+2, hour= 0, minute= 0, second= 0, microsecond=0), \
               cdt.replace(day=cdt.day+2, hour=23, minute=59, second=59, microsecond=0)

    if ts == 'nextThreeDays':
        return cdt.replace(day=cdt.day, hour= 0, minute= 0, second= 0, microsecond=0), \
               cdt.replace(day=cdt.day+3, hour=23, minute=59, second=59, microsecond=0)

def get_time_label(c, ts):

    if c.lang == 'de':
        if ts == 'today':
            return u"heute"
        elif ts == 'tomorrow':
            return u"morgen"
        elif ts == 'dayAfterTomorrow':
            return u"übermorgen"
        elif ts == 'nextThreeDays':
            return u"in den nächsten drei Tagen"

    if ts == 'today':
        return u"today"
    elif ts == 'tomorrow':
        return u"tomorrow"
    elif ts == 'dayAfterTomorrow':
        return u"day after tomorrow"
    elif ts == 'nextThreeDays':
        return u"in the next three days"

    raise Exception ('unknown timespec %s' % repr(ts))

month_label_en = { 1 : 'january',
                   2 : 'february',
                   3 : 'march',
                   4 : 'april',
                   5 : 'may',
                   6 : 'june',
                   7 : 'july',
                   8 : 'august',
                   9 : 'september',
                  10 : 'october',
                  11 : 'november',
                  12 : 'december'}

month_label_de = { 1 : 'januar',
                   2 : 'februar',
                   3 : 'märz',
                   4 : 'april',
                   5 : 'mai',
                   6 : 'juni',
                   7 : 'juli',
                   8 : 'august',
                   9 : 'september',
                  10 : 'oktober',
                  11 : 'november',
                  12 : 'dezember'}

def transcribe_month(m, lang):
    if lang == 'en':
        return month_label_en[m]
    elif lang == 'de':
        return month_label_de[m]
    raise Exception ('FIXME: lang %d not implemented yet.' % lang)

weekday_en = { 0: 'Monday',
               1: 'Tuesday',
               2: 'Wednesday',
               3: 'Thursday',
               4: 'Friday',
               5: 'Saturday',
               6: 'Sunday'}

weekday_de = { 0: 'Montag',
               1: 'Dienstag',
               2: 'Mittwoch',
               3: 'Donnerstag',
               4: 'Freitag',
               5: 'Samstag',
               6: 'Sonntag'}

def transcribe_wday_ts (dt, lang):

    wd = dt.weekday()
    if lang=='en':
        return weekday_en[wd]
    elif lang=='de':
        return weekday_de[wd]
    raise Exception ('FIXME: lang %d not implemented yet.' % lang)
 
def transcribe_date(dt, lang, flx):
    if lang == 'en':
        if flx == 'dativ':
            ds = transcribe_number(dt.day, 'en', 'nominative')
            ms = transcribe_month(dt.month, 'en')
            return u'%s %s, %s' % (ms, ds, dt.year)
        else:
            raise Exception ('FIXME: not implemented yet.')

    elif lang == 'de':
        if flx == 'dativ':
            ds = transcribe_number(dt.day, 'de', 'ordgen')
            ms = transcribe_month(dt.month, 'de')
            return u'%s %s %s' % (ds, ms, dt.year)
        else:
            raise Exception ('FIXME: not implemented yet.')

def get_data(k):

    k.dte.macro('en', 'timespec', {'TIME' : 'today'           , 'LABEL' : u'today'})
    k.dte.macro('en', 'timespec', {'TIME' : 'tomorrow'        , 'LABEL' : u'tomorrow'})
    k.dte.macro('en', 'timespec', {'TIME' : 'dayAfterTomorrow', 'LABEL' : u'the day after tomorrow'})
    k.dte.macro('en', 'timespec', {'TIME' : 'nextThreeDays'   , 'LABEL' : u'the next three days'})
    
    k.dte.macro('de', 'timespec', {'TIME' : 'today'           , 'LABEL' : u'heute'})
    k.dte.macro('de', 'timespec', {'TIME' : 'tomorrow'        , 'LABEL' : u'morgen'})
    k.dte.macro('de', 'timespec', {'TIME' : 'dayAfterTomorrow', 'LABEL' : u'übermorgen'})
    k.dte.macro('de', 'timespec', {'TIME' : 'nextThreeDays'   , 'LABEL' : u'die nächsten drei Tage'})

