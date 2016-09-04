#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2014, 2015, 2016 Guenter Bartsch
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
# generate HAL-Prolog code from weather forecast data in hal DB
#

import os
import sys
import locale
import ConfigParser
from os.path import expanduser
from optparse import OptionParser
import traceback

from datetime import datetime, timedelta
import pytz
import json
import urllib2
from tzlocal import get_localzone

import psycopg2

import model

WEATHERFN = 'data/dst/weather-dynamic.pl'
TEMP_OFFSET = 3.0

class Forecast(object):

    def __init__(self, dt, temp_min, temp_max, code, precipitation, icon, description, clouds):

        self.dt            = dt
        self.temp_min      = temp_min
        self.temp_max      = temp_max
        self.code          = code
        self.precipitation = precipitation
        self.icon          = icon
        self.description   = description
        self.clouds        = clouds

    def __str__(self):
        return "Forecast (dt=%s, temp_min=%d, temp_max=%d, code=%s, icon=%s, description=%s, clouds=%d)" % (self.dt, 
                                                                                    self.temp_min, 
                                                                                    self.temp_max, 
                                                                                    self.code,
                                                                                    self.icon, 
                                                                                    self.description,
                                                                                    self.clouds)


def get_timestamps ():

    # timestamps we're interested in:

    dt = datetime.now(get_localzone()).replace(tzinfo=pytz.utc)

    dts = [
              # today 0
              (dt + timedelta(days=0)).replace (hour= 9, minute=0, second=0, microsecond=0),
              (dt + timedelta(days=0)).replace (hour=15, minute=0, second=0, microsecond=0),
              (dt + timedelta(days=0)).replace (hour=21, minute=0, second=0, microsecond=0),
              (dt + timedelta(days=1)).replace (hour= 3, minute=0, second=0, microsecond=0),

              # tomorrow 4
              (dt + timedelta(days=1)).replace (hour= 9, minute=0, second=0, microsecond=0),
              (dt + timedelta(days=1)).replace (hour=15, minute=0, second=0, microsecond=0),
              (dt + timedelta(days=1)).replace (hour=21, minute=0, second=0, microsecond=0),
              (dt + timedelta(days=2)).replace (hour= 3, minute=0, second=0, microsecond=0),

              # day after tomorrow 8
              (dt + timedelta(days=2)).replace (hour= 9, minute=0, second=0, microsecond=0),
              (dt + timedelta(days=2)).replace (hour=15, minute=0, second=0, microsecond=0),
              (dt + timedelta(days=2)).replace (hour=21, minute=0, second=0, microsecond=0),
              (dt + timedelta(days=3)).replace (hour= 3, minute=0, second=0, microsecond=0),

              # + 3 days 12
              (dt + timedelta(days=3)).replace (hour= 9, minute=0, second=0, microsecond=0),
              (dt + timedelta(days=3)).replace (hour=15, minute=0, second=0, microsecond=0),
              (dt + timedelta(days=3)).replace (hour=21, minute=0, second=0, microsecond=0),
              (dt + timedelta(days=4)).replace (hour= 3, minute=0, second=0, microsecond=0),

              # + 4 days 16
              # (dt + timedelta(days=4)).replace (hour= 9, minute=0, second=0, microsecond=0),
              # (dt + timedelta(days=4)).replace (hour=15, minute=0, second=0, microsecond=0),
              # (dt + timedelta(days=4)).replace (hour=21, minute=0, second=0, microsecond=0),
              # (dt + timedelta(days=5)).replace (hour= 3, minute=0, second=0, microsecond=0),
        ]

    return dts

#
# load config, set up global variables
#

db_server  = model.config.get("weather", "dbserver")
db_name    = model.config.get("weather", "dbname")
db_user    = model.config.get("weather", "dbuser")
db_pass    = model.config.get("weather", "dbpass")
city_pred  = model.config.get("weather", "city_pred")

#
# init terminal
#

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

#
# connect to DB
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# main
#

# timestamps we're interested in:
dts = get_timestamps()

forecasts = []

for dt in dts:

    # print dt

    # print "SELECT temp_min, temp_max, code, precipitation, icon, description, clouds FROM weather_forecast WHERE dt=%s" % dt

    cur.execute ("SELECT temp_min, temp_max, code, precipitation, icon, description, clouds FROM weather_forecast WHERE dt=%s", (dt,))

    row = cur.fetchone()

    # print row
    
    fc = Forecast (dt            = dt, 
                   temp_min      = float(row[0]),
                   temp_max      = float(row[1]),
                   code          = row[2],
                   precipitation = float(row[3]),
                   icon          = row[4],
                   description   = row[5],
                   clouds        = float(row[6]))

    # print "FC   %s" % (str(fc))
    forecasts.append(fc)


#
# dump prolog code
#

dt_today = datetime.now(get_localzone()).replace(tzinfo=pytz.utc)

def make_dt (days, hour):
    global dt_today

    return (dt_today + timedelta(days=days)).replace (hour= hour, minute=0, second=0, microsecond=0)



forecast_slices = {
    'today'                    : (forecasts[ 0: 3], make_dt(0,  0), make_dt(1,  0)),
    'todayMorning'             : (forecasts[ 0: 1], make_dt(0,  0), make_dt(0, 12)),
    'todayAfternoon'           : (forecasts[ 1: 2], make_dt(0, 12), make_dt(0, 18)),
    'todayEvening'             : (forecasts[ 2: 3], make_dt(0, 18), make_dt(1,  0)),

    'tomorrow'                 : (forecasts[ 4: 7], make_dt(1,  0), make_dt(2,  0)),
    'tomorrowMorning'          : (forecasts[ 4: 5], make_dt(1,  0), make_dt(1, 12)),
    'tomorrowAfternoon'        : (forecasts[ 5: 6], make_dt(1, 12), make_dt(1, 18)),
    'tomorrowEvening'          : (forecasts[ 6: 7], make_dt(1, 18), make_dt(2,  0)),

    'dayAfterTomorrow'         : (forecasts[ 8:11], make_dt(2,  0), make_dt(3,  0)),
    'dayAfterTomorrowMorning'  : (forecasts[ 8: 9], make_dt(2,  0), make_dt(2, 12)),
    'dayAfterTomorrowAfternoon': (forecasts[ 9:10], make_dt(2, 12), make_dt(2, 18)),
    'dayAfterTomorrowEvening'  : (forecasts[10:11], make_dt(2, 18), make_dt(3,  0)),
    
    'nextThreeDays'            : (forecasts[ 4:15], make_dt(1,  0), make_dt(4,  0)),
    }

def myCap(s):
    return s[0].capitalize() + s[1:]

iconDesc = {
    "01" : "weatherCondClearSky",
    "02" : "weatherCondFewClouds",
    "03" : "weatherCondScatteredClouds",
    "04" : "weatherCondBrokenClouds",
    "09" : "weatherCondShowerRain",
    "10" : "weatherCondRain",
    "11" : "weatherCondThunderstorm",
    "13" : "weatherCondSnow",
    "50" : "weatherCondMist",
}

with open(WEATHERFN, 'w') as weatherf:

    weatherf.write ("% prolog\n")
    weatherf.write ("\n")
    weatherf.write ("%! module weather-dynamic\n")
    weatherf.write ("\n")

    for span in forecast_slices:

        event_id = 'eWeather'+myCap(city_pred)+myCap(span)

        icon          = '01d.png'
        temp_min      = 200.0
        temp_max      = -200.0
        precipitation = 0.0
        clouds        = 0.0
        num           = 0

        for fc in forecast_slices[span][0]:

            if fc.icon > icon:
                icon = fc.icon
            if fc.temp_min < temp_min:
                temp_min = fc.temp_min
            if fc.temp_max > temp_max:
                temp_max = fc.temp_max
            precipitation += fc.precipitation
            clouds        += fc.clouds
            num += 1

        clouds = clouds / float(num)

        dt_start = forecast_slices[span][1]
        dt_end   = forecast_slices[span][2]

        weatherf.write ("%\n")
        weatherf.write ("%% %s\n" % span)
        weatherf.write ("%\n")

        # weatherf.write ("startTime(%s,X) :- date_time_stamp(date(%d,%d,%d,%d,%d,%d,'local'),X)." % (span, dt_start.year, dt_start.month,
        #                                                                                   dt_start.day, dt_start.hour, 
        #                                                                                   dt_start.minute,
        #                                                                                   dt_start.second))
        # weatherf.write ("endTime(%s,X) :- date_time_stamp(date(%d,%d,%d,%d,%d,%d,'local'),X)." % (span, dt_end.year, dt_end.month,
        #                                                                                   dt_end.day, dt_end.hour, 
        #                                                                                   dt_end.minute,
        #                                                                                   dt_end.second))
        weatherf.write ("time(%s,%s).\n" % (event_id, span))
        weatherf.write ("place(%s,%s).\n" % (event_id, city_pred))
        weatherf.write ("weatherDesc(%s,%s).\n" % (event_id, iconDesc[icon[0:2]]))
        weatherf.write ("tempMin(%s,%s).\n" % (event_id, temp_min + TEMP_OFFSET))
        weatherf.write ("tempMax(%s,%s).\n" % (event_id, temp_max + TEMP_OFFSET))
        weatherf.write ("precipitation(%s,%s).\n" % (event_id, precipitation))
        weatherf.write ("cloudiness(%s,%s).\n" % (event_id, clouds))
        weatherf.write ("\n")

print "%s written." % WEATHERFN
print

