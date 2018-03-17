#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017, 2018 Guenter Bartsch
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
import urllib2
import pytz
import json

from datetime             import datetime, timedelta
from nltools              import misc

import weather
import base

DEPENDS = [ 'base', 'config', 'dialog' ]
KELVIN  = 273.15

def get_time_span (cdt, ts):
    if ts == 'weatherNearFuture':
        if cdt.hour < 18:
            return base.get_time_span(cdt, 'today')
        return base.get_time_span(cdt, 'tomorrow')
    return base.get_time_span(cdt, ts)

def get_time_label(c, cdt, ts):
    if ts == 'weatherNearFuture':
        if cdt.hour < 18:
            if c.lang == 'de':
                return 'heute'
            return 'today'
        if c.lang == 'de':
            return 'morgen'
        return 'tomorrow'
    return base.get_time_label(c, ts)


#     def time_label(CT, de, weatherNearFuture, "heute"):
#         before_evening(CT)
#     def time_label(CT, en, weatherNearFuture, "tomorrow"):
#         after_evening(CT)
#     def time_label(CT, de, weatherNearFuture, "morgen"):
#         after_evening(CT)

def get_api_key():

    config = misc.load_config('.airc')
    return config.get('weather', 'api_key')


def fetch_weather_data (c, cdt, loc, ts):

    if c.test_mode:
        # fixed mock data for our tests
        return {'code': 500, 
                'clouds': 30.0, 
                'description': u'mostly clear skies', 
                'temp_max': 4.0, 
                'temp_min': -8.0, 
                'precipitation': 0.7031249999999999, 
                'icon': u'02n'}

    ts, te = get_time_span(cdt, ts)

    api_key = get_api_key()

    city_id = c.kernal.prolog_query_one('owmCityId(%s, CITY_ID).' % loc)
    if not city_id:
        return None

    url = 'http://api.openweathermap.org/data/2.5/forecast?id=%s&APPID=%s' % (city_id, api_key)

    data = json.load(urllib2.urlopen(url))

    if not 'list' in data:
        logging.error ('failed to fetch weather data for %s, got: %s' % (location, repr(data)))
        return None

    res = {
           'temp_min'      :  100000.0,
           'temp_max'      : -100000.0,
           'code'          : '',
           'precipitation' : 0.0,
           'icon'          : '',
           'description'   : '',
           'clouds'        : ''
          }

    cnt = 0.0

    for fc in data['list']:

        dt_to   = datetime.strptime (fc['dt_txt'], '%Y-%m-%d %H:%M:%S')
        dt_to   = dt_to.replace(tzinfo=pytz.utc)

        dt_from = dt_to - timedelta(hours=3)

        if (dt_from > te) or (dt_to < ts):
            continue

        temp_min      = fc['main']['temp_min']-KELVIN
        if temp_min < res['temp_min']:
            res['temp_min'] = temp_min
        temp_max      = fc['main']['temp_max']-KELVIN
        if temp_max > res['temp_max']:
            res['temp_max'] = temp_max
        res['precipitation'] += float(fc['rain']['3h']) if 'rain' in fc and '3h' in fc['rain'] else 0.0
        res['code']          = fc['weather'][0]['id']
        res['icon']          = fc['weather'][0]['icon']
        res['description']   = fc['weather'][0]['description']
        res['clouds']        = float(fc['clouds']['all'])

        cnt += 1.0
    
    if cnt:
        res['precipitation'] /= cnt

    return res

def get_data(k):

    weather.get_data(k)

