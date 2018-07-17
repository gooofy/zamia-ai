#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2014, 2015, 2016, 2017 Guenter Bartsch
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

#
# fetch weather forecast data from OpenWeatherMap, generate prolog assertions from it
#

import os
import sys
import locale
import traceback
import codecs
import logging
import pytz
import json
import urllib2
import astral
import re

from urllib2              import HTTPError
from datetime             import datetime, timedelta
from tzlocal              import get_localzone
from nltools              import misc

WEATHER_DATA_MODULE = 'weather_data'
KELVIN              = 273.15
coord_matcher       = re.compile(r"Point\(([0-9.]+)\s([0-9.]+)\)")

def fetch_weather_forecast(kernal):

    config  = misc.load_config('.airc')
    api_key = config.get("weather", "api_key")

    logging.debug ('fetch_weather_forecast cronj ob, api key: %s' % api_key)

    sl = SourceLocation(fn='__internet__', col=0, line=0)

    #
    # resolve city ids, timezones
    #

    locations = {}

    # owmCityId(wdeLosAngeles, 5368361). 
    solutions = kernal.rt.search_predicate ('owmCityId', ['_1', '_2'])

    for s in solutions:

        location = s['_1'].name
        city_id  = int(s['_2'].f)

        # aiTimezone(wdeNewYorkCity, "America/New_York").
        solutions2 = kernal.rt.search_predicate ('aiTimezone', [location, '_1'])
        if len(solutions2)<1:
            continue
        timezone = solutions2[0]['_1'].s

        solutions2 = kernal.rt.search_predicate ('rdfsLabel', [location, 'en', '_1'])
        if len(solutions2)<1:
            continue
        label = solutions2[0]['_1'].s

        # wdpdCoordinateLocation(wdeBerlin, "Point(13.383333333 52.516666666)").
        solutions2 = kernal.rt.search_predicate ('wdpdCoordinateLocation', [location, '_1'])
        if len(solutions2)<1:
            continue
        m = coord_matcher.match(solutions2[0]['_1'].s)
        if not m:
            continue
        geo_lat  = float(m.group(2))
        geo_long = float(m.group(1))

        if not location in locations:
            locations[location] = {}
            locations[location]['city_id']  = city_id
            locations[location]['timezone'] = timezone
            locations[location]['label']    = label
            locations[location]['long']     = geo_long
            locations[location]['lat']      = geo_lat

    def mangle_label(label):
        return ''.join(map(lambda c: c if c.isalnum() else '', label))

    #
    # generate triples of weather and astronomical data
    #

    env = {}

    for location in locations:

        city_id   = locations[location]['city_id']
        timezone  = locations[location]['timezone']
        loc_label = mangle_label(locations[location]['label'])
        geo_lat   = locations[location]['lat']
        geo_long  = locations[location]['long']

        tz = pytz.timezone(timezone)

        ref_dt = datetime.now(tz).replace( hour        = 0,
                                           minute      = 0,
                                           second      = 0,
                                           microsecond = 0)

        logging.debug("%s %s" % ( location, ref_dt ) )

        #
        # sunrise / sunset
        #

        l = astral.Location()
        l.name      = 'name'
        l.region    = 'region'
        l.latitude  = geo_lat
        l.longitude = geo_long
        l.timezone  = timezone
        l.elevation = 0

        for day_offset in range(7):
            cur_date = (ref_dt + timedelta(days=day_offset)).date()

            sun = l.sun(date=cur_date, local=True)

            sun_const = u'aiUnlabeledSun%s%s' % (loc_label, cur_date.strftime('%Y%m%d'))

            env = do_retract(env, build_predicate('aiLocation', [sun_const, '_']))
            env = do_retract(env, build_predicate('aiDate',     [sun_const, '_']))
            env = do_retract(env, build_predicate('aiDawn',     [sun_const, '_']))
            env = do_retract(env, build_predicate('aiSunrise',  [sun_const, '_']))
            env = do_retract(env, build_predicate('aiNoon',     [sun_const, '_']))
            env = do_retract(env, build_predicate('aiSunset',   [sun_const, '_']))
            env = do_retract(env, build_predicate('aiDusk',     [sun_const, '_']))

            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiLocation', [sun_const, location])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiDate',     [sun_const, StringLiteral(cur_date.isoformat())])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiDawn',     [sun_const, StringLiteral(sun['dawn'].isoformat())])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiSunrise',  [sun_const, StringLiteral(sun['sunrise'].isoformat())])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiNoon',     [sun_const, StringLiteral(sun['noon'].isoformat())])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiSunset',   [sun_const, StringLiteral(sun['sunset'].isoformat())])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiDusk',     [sun_const, StringLiteral(sun['dusk'].isoformat())])))

            logging.debug ("%s %s %s -> %s" % (sun_const, cur_date, sun['sunrise'], sun['sunset']) )



        #
        # fetch json forecast data from OpenWeatherMap
        #

        url = 'http://api.openweathermap.org/data/2.5/forecast?id=%s&APPID=%s' % (city_id, api_key)

        data = json.load(urllib2.urlopen(url))

        if not 'list' in data:
            logging.error ('failed to fetch weather data for %s, got: %s' % (location, repr(data)))
            continue


        # print repr(data['list'])

        for fc in data['list']:

            dt_to   = datetime.strptime (fc['dt_txt'], '%Y-%m-%d %H:%M:%S')
            dt_to   = dt_to.replace(tzinfo=pytz.utc)

            dt_from = dt_to - timedelta(hours=3)

            city_id       = city_id
            temp_min      = fc['main']['temp_min']-KELVIN
            temp_max      = fc['main']['temp_max']-KELVIN
            code          = fc['weather'][0]['id']
            precipitation = float(fc['rain']['3h']) if 'rain' in fc and '3h' in fc['rain'] else 0.0
            icon          = fc['weather'][0]['icon']
            description   = fc['weather'][0]['description']
            clouds        = float(fc['clouds']['all'])

            fc_const = 'aiUnlabeledFc%s%s' % (loc_label, dt_from.strftime('%Y%m%d%H%M%S'))

            logging.debug ("%s on %s-%s city_id=%s" % (fc_const, dt_from, dt_to, city_id))

            # aiDescription(aiUnlabeledFcFreudental20161205180000, "clear sky").
            # aiDtEnd(aiUnlabeledFcFreudental20161205180000, "2016-12-05T21:00:00+00:00").
            # aiTempMin(aiUnlabeledFcFreudental20161205180000, -6.666).
            # aiIcon(aiUnlabeledFcFreudental20161205180000, "01n").
            # aiLocation(aiUnlabeledFcFreudental20161205180000, wdeFreudental).
            # aiDtStart(aiUnlabeledFcFreudental20161205180000, "2016-12-05T18:00:00+00:00").
            # aiClouds(aiUnlabeledFcFreudental20161205180000, 0.0).
            # aiPrecipitation(aiUnlabeledFcFreudental20161205180000, 0.0).
            # aiTempMax(aiUnlabeledFcFreudental20161205180000, -6.45).

            env = do_retract(env, build_predicate('aiDescription',   [fc_const, '_']))
            env = do_retract(env, build_predicate('aiDtEnd',         [fc_const, '_']))
            env = do_retract(env, build_predicate('aiTempMin',       [fc_const, '_']))
            env = do_retract(env, build_predicate('aiIcon',          [fc_const, '_']))
            env = do_retract(env, build_predicate('aiLocation',      [fc_const, '_']))
            env = do_retract(env, build_predicate('aiDtStart',       [fc_const, '_']))
            env = do_retract(env, build_predicate('aiClouds',        [fc_const, '_']))
            env = do_retract(env, build_predicate('aiPrecipitation', [fc_const, '_']))
            env = do_retract(env, build_predicate('aiTempMax',       [fc_const, '_']))

            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiLocation',      [fc_const, location])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiTempMin',       [fc_const, temp_min])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiTempMax',       [fc_const, temp_max])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiPrecipitation', [fc_const, precipitation])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiClouds',        [fc_const, clouds])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiIcon',          [fc_const, StringLiteral(icon)])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiDescription',   [fc_const, StringLiteral(description)])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiDtStart',       [fc_const, StringLiteral(dt_from.isoformat())])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiDtEnd',         [fc_const, StringLiteral(dt_to.isoformat())])))

    kernal.rt.apply_overlay (WEATHER_DATA_MODULE, env)

# if __name__ == "__main__":
# 
#     logging.basicConfig(level=logging.DEBUG)
# 
#     config = misc.load_config('.airc')
#     
#     # kb = AIKB()
#     # gn = u'http://ai.zamia.org/benchmark'
# 
#     # kb.register_prefix('ai', 'http://ai.zamia.org/kb/')
#     # kb.register_prefix('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
# 
#     fetch_weather_forecast (config, kb, gn)
# 
# 
#     # start_time = time.time()
#     # kb = AIKB()
#     # logging.debug ('AIKB init took %fs' % (time.time() - start_time))


