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

from urllib2          import HTTPError
from datetime         import datetime, timedelta
import pytz
import json
import urllib2
import rdflib

from rdflib.namespace import XSD
from tzlocal          import get_localzone

from nltools          import misc
from kb               import HALKB

import astral
import model

KELVIN          = 273.15

def fetch_weather_forecast(config, kb, graph_name):

    api_key    = config.get("weather", "api_key")
    graph      = rdflib.Graph(identifier=graph_name)

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
                      ?location hal:GeoNames ?gid .
                      ?gid <http://www.w3.org/2003/01/geo/wgs84_pos#long> ?long .
                      ?gid <http://www.w3.org/2003/01/geo/wgs84_pos#lat> ?lat .
                      FILTER(lang(?label) = 'en') .
            }
            """

    # query = """
    #         SELECT DISTINCT ?location ?cityid ?timezone
    #         WHERE {
    #            ?location hal:cityid ?cityid .
    #            ?location hal:timezone ?timezone .
    #         }
    #         """

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

    quads = []

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

            sun_uri = u'hal:sun_%s_%s' % (loc_label, cur_date.strftime('%Y%m%d'))

            kb.remove ((sun_uri, None, None, graph))

            quads.append(( sun_uri, u'hal:location', location, graph ))
            quads.append(( sun_uri, u'hal:date',     rdflib.Literal(cur_date, datatype=XSD.date), graph ))
            quads.append(( sun_uri, u'hal:dawn',     rdflib.Literal(sun['dawn'], datatype=XSD.dateTime), graph ))
            quads.append(( sun_uri, u'hal:sunrise',  rdflib.Literal(sun['sunrise'], datatype=XSD.dateTime), graph ))
            quads.append(( sun_uri, u'hal:noone',    rdflib.Literal(sun['noon'], datatype=XSD.dateTime), graph ))
            quads.append(( sun_uri, u'hal:sunset',   rdflib.Literal(sun['sunset'], datatype=XSD.dateTime), graph ))
            quads.append(( sun_uri, u'hal:dusk',     rdflib.Literal(sun['dusk'], datatype=XSD.dateTime), graph ))

            logging.debug ("astral %s %s %s -> %s" % (location, cur_date, sun['sunrise'], sun['sunset']) )

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

            kb.remove ((fc_uri, None, None, graph))

            quads.append(( fc_uri, u'hal:location',      location, graph ))
            quads.append(( fc_uri, u'hal:temp_min',      rdflib.Literal(unicode(temp_min), datatype=XSD.float), graph ))
            quads.append(( fc_uri, u'hal:temp_max',      rdflib.Literal(unicode(temp_max), datatype=XSD.float), graph ))
            quads.append(( fc_uri, u'hal:precipitation', rdflib.Literal(unicode(precipitation), datatype=XSD.float), graph ))
            quads.append(( fc_uri, u'hal:clouds',        rdflib.Literal(unicode(clouds), datatype=XSD.float), graph ))

            quads.append(( fc_uri, u'hal:icon',          rdflib.Literal(icon), graph ))
            quads.append(( fc_uri, u'hal:description',   rdflib.Literal(description), graph ))

            quads.append(( fc_uri, u'hal:dt_start',      rdflib.Literal(dt_from, datatype=XSD.dateTime), graph ))
            quads.append(( fc_uri, u'hal:dt_end',        rdflib.Literal(dt_to, datatype=XSD.dateTime), graph ))

        # break


        # logging.debug(repr(quads))

    # import pdb; pdb.set_trace()

    kb.addN_resolve(quads)

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    config = misc.load_config('.nlprc')
    
    kb = HALKB()
    gn = u'http://hal.zamia.org/benchmark'

    kb.register_prefix('hal', 'http://hal.zamia.org/kb/')
    kb.register_prefix('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')

    fetch_weather_forecast (config, kb, gn)


    # start_time = time.time()
    # kb = HALKB()
    # logging.debug ('HALKB init took %fs' % (time.time() - start_time))


