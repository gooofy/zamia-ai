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
# fetch weather forecast data from OpenWeatherMap, generate and store triples
#

import os
import sys
import locale
import traceback
import codecs
import logging

from urllib2 import HTTPError
from datetime import datetime, timedelta
import pytz
import json
import urllib2
from tzlocal import get_localzone
import astral

from kb import HALKB

import model

KELVIN          = 273.15

def fetch_weather_forecast(config, kb):

    api_key    = config.get("weather", "api_key")

    #
    # fetch city ids, timezones
    #

    locations = {}

    logging.debug("fetching city ids, timezones from kb...")

    query = """
            SELECT DISTINCT ?location ?cityid ?timezone ?label ?long ?lat
                   WHERE {
                      ?location hal:cityid ?cityid .
                      ?location hal:timezone ?timezone .
                      ?location rdfs:label ?label .
                      ?location geo1:long ?long .
                      ?location geo1:lat ?lat .
                      FILTER(LANGMATCHES(LANG(?label), "en")) .
            }
            """

    try:
        results = kb.query(query)

        # print repr(results)

        for row in results:

            # print repr(row)
            #         print(result["label"]["value"])

            location = row['location']
            city_id  = int(row['cityid'])
            timezone = str(row['timezone'])
            label    = unicode(row['label'])
            geo_lat  = float(row['lat'])
            geo_long = float(row['long'])

            if not location in locations:
                locations[location] = {}
                locations[location]['city_id']  = city_id
                locations[location]['timezone'] = timezone
                locations[location]['label']    = label
                locations[location]['long']     = geo_long
                locations[location]['lat']      = geo_lat

                logging.debug("   %-30s %-20s %7d %+12.6f %+12.6f" % (label, timezone, int(city_id), float(geo_long), float(geo_lat)))

    except HTTPError:

        logging.error('HTTPError')

        traceback.print_exc()

    def mangle_uri(label):
        return ''.join(map(lambda c: c if c.isalnum() else '_', label))

    #
    # generate triples of weather and astronomical data
    #

    for location in locations:

        city_id   = locations[location]['city_id']
        timezone  = locations[location]['timezone']
        loc_label = mangle_uri(locations[location]['label'])
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

            sun_uri = 'hal:sun_%s_%s' % (loc_label, cur_date.strftime('%Y%m%d'))

            query = """
                    INSERT DATA {
                       GRAPH <http://hal.zamia.org>
                       { 
                           %s hal:location <%s> .
                           %s hal:date "%s"^^xsd:date .
                           %s hal:dawn "%s"^^xsd:dateTime   .
                           %s hal:sunrise "%s"^^xsd:dateTime   .
                           %s hal:noon "%s"^^xsd:dateTime   .
                           %s hal:sunset "%s"^^xsd:dateTime   .
                           %s hal:dusk "%s"^^xsd:dateTime   .
                       }
                    }
                    """ % ( sun_uri, location, \
                            sun_uri, cur_date.isoformat(), \
                            sun_uri, sun['dawn'].isoformat(), \
                            sun_uri, sun['sunrise'].isoformat(), \
                            sun_uri, sun['noon'].isoformat(), \
                            sun_uri, sun['sunset'].isoformat(), \
                            sun_uri, sun['dusk'].isoformat())

            # print query

            kb.sparql(query)

            logging.debug ("astral %s %s %s -> %s" % (location, cur_date.isoformat(), sun['sunrise'], sun['sunset']) )

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

            logging.debug ("forecast %s on %s-%s city_id=%s" % (location, dt_from, dt_to, city_id))

            fc_uri = 'hal:fc_%s_%s' % (loc_label, dt_from.strftime('%Y%m%d_%H%M%S'))

            query = """
                    WITH <http://hal.zamia.org>
                    DELETE { %s ?p ?v }
                    WHERE { %s ?p ?v }
                    """ % (fc_uri, fc_uri)

            # print query
            kb.sparql(query)

            query = """
                    INSERT DATA {
                       GRAPH <http://hal.zamia.org>
                       { 
                           %s hal:location <%s> .
                           %s hal:temp_min      "%f"^^xsd:float .
                           %s hal:temp_max      "%f"^^xsd:float .
                           %s hal:precipitation "%f"^^xsd:float .
                           %s hal:clouds        "%f"^^xsd:float .
                           %s hal:icon "%s" .
                           %s hal:description "%s" .
                           %s hal:dt_start "%s"^^xsd:dateTime .
                           %s hal:dt_end "%s"^^xsd:dateTime .
                       }
                    }
                    """ % ( fc_uri, location, fc_uri, temp_min, fc_uri, temp_max, \
                            fc_uri, precipitation, fc_uri, clouds, fc_uri, icon,  \
                            fc_uri, description, fc_uri, dt_from.isoformat(), fc_uri, dt_to.isoformat())

            # print query
            result = kb.sparql(query)

