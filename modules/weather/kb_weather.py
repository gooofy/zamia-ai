#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2014, 2015, 2016, 2017 Guenter Bartsch
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
from zamiaprolog.builtins import do_assertz, do_retract
from zamiaprolog.logic    import build_predicate, Clause, SourceLocation

WEATHER_DATA_MODULE = 'weather_data'
KELVIN              = 273.15
coord_matcher       = re.compile(r"Point\(([0-9.]+)\s([0-9.]+)\)")

def fetch_weather_forecast(kernal):

    api_key    = kernal.config.get("weather", "api_key")

    logging.info ('fetch_weather_forecast cronj ob, api key: %s' % api_key)

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

    for location in locations:

        env = {}

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

        logging.info("%s %s" % ( location, ref_dt ) )

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
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiDate',     [sun_const, cur_date.isoformat()])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiDawn',     [sun_const, sun['dawn'].isoformat()])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiSunrise',  [sun_const, sun['sunrise'].isoformat()])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiNoon',     [sun_const, sun['noon'].isoformat()])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiSunset',   [sun_const, sun['sunset'].isoformat()])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiDusk',     [sun_const, sun['dusk'].isoformat()])))

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
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiIcon',          [fc_const, icon])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiDescription',   [fc_const, description])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiDtStart',       [fc_const, dt_from.isoformat()])))
            env = do_assertz(env, Clause(location=sl, head=build_predicate('aiDtEnd',         [fc_const, dt_to.isoformat()])))

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


