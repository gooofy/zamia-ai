#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Guenter Bartsch
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

import logging
import dateutil.parser

from zamiaprolog.errors import PrologRuntimeError
from zamiaprolog.logic  import StringLiteral, NumberLiteral
from kb_weather         import fetch_weather_forecast

DEPENDS = [ 'base', 'config' ]

AIP_SOURCES = [
               'weather_test.aip', 'weather.aip',
              ]

CRONJOBS   = [
              ( 'fetch_forecast', 4 * 60 * 60, fetch_weather_forecast),
             ]

# % all weather events that affect a given timespan
# wev_timespan (C, TIMESPAN, WEV) :-
# 
#     time_span (C:time, TIMESPAN, TSTART, TEND),
# 
#     aiDtStart(WEV, WEV_TSTART),
#     aiDtEnd(WEV, WEV_END),
# 
#     or ( and ( >= (WEV_TSTART, TSTART), =< (WEV_TEND, TEND)),
#          and ( >= (WEV_TSTART, TSTART), 
# 
# weather_data (C, PLACE, TIMESPAN, CODE, PREC, TEMP_MIN, TEMP_MAX, CLOUDS) :-
# 
# 
#     findall (WEV, and ( >=(TSTART, aiDtStart (WEV, WEV_TSTART)
# 
#     aiDtStart(aiUnlabeledFcFreudental20161206000000, "2016-12-06T00:00:00+00:00").
#     aiTempMin(aiUnlabeledFcFreudental20161206000000, -7.344).
#     aiIcon(aiUnlabeledFcFreudental20161206000000, "01n").
#     aiDtEnd(aiUnlabeledFcFreudental20161206000000, "2016-12-06T03:00:00+00:00").
#     aiPrecipitation(aiUnlabeledFcFreudental20161206000000, 0.0).
#     aiTempMax(aiUnlabeledFcFreudental20161206000000, -7.27).
#     aiLocation(aiUnlabeledFcFreudental20161206000000, wdeFreudental).
#     aiDescription(aiUnlabeledFcFreudental20161206000000, "clear sky").
#     aiClouds(aiUnlabeledFcFreudental20161206000000, 0.0).


def builtin_weather_data (g, pe):

    """ weather_data (PLACE, TSTART, TEND, CODE, PREC, TEMP_MIN, TEMP_MAX, CLOUDS) """

    pe._trace ('CALLED BUILTIN weather_data', g)

    # import pdb; pdb.set_trace()

    pred = g.terms[g.inx]
    args = pred.args
    if len(args) != 8:
        raise PrologRuntimeError('weather_data: expected 8 args, %d args found.' % len(args), g.location)

    arg_Place     = pe.prolog_eval         (args[0], g.env, g.location)
    arg_TStart    = pe.prolog_get_string   (args[1], g.env, g.location)
    arg_TEnd      = pe.prolog_get_string   (args[2], g.env, g.location)

    tstart = dateutil.parser.parse(arg_TStart)
    tend   = dateutil.parser.parse(arg_TEnd)

    arg_code      = pe.prolog_get_variable (args[3], g.env, g.location)
    arg_prec      = pe.prolog_get_variable (args[4], g.env, g.location)
    arg_temp_min  = pe.prolog_get_variable (args[5], g.env, g.location)
    arg_temp_max  = pe.prolog_get_variable (args[6], g.env, g.location)
    arg_clouds    = pe.prolog_get_variable (args[7], g.env, g.location)

    wevs = pe.search_predicate('weather_events', [arg_Place, '_1', '_2', '_3', '_4', '_5', '_6', '_7'])

    cnt      = 0
    code     = ''
    prec     = 0.0
    temp_min = 10000.0
    temp_max = -10000.0
    clouds   = 0.0

    for wev in wevs:

        wev_tstart     = dateutil.parser.parse(wev['_1'].s)
        wev_tend       = dateutil.parser.parse(wev['_2'].s)

        if (wev_tstart > tend) or (wev_tend < tstart):
            # logging.info ('ignoring wev %s' % repr(wev))
            # import pdb; pdb.set_trace()
            continue

        wev_code       = wev['_3'].s[:2]
        wev_prec       = wev['_4'].f
        wev_temp_min   = wev['_5'].f 
        wev_temp_max   = wev['_6'].f 
        wev_clouds     = wev['_7'].f 
        
        if wev_temp_min < temp_min:
            temp_min = wev_temp_min
        if wev_temp_max > temp_max:
            temp_max = wev_temp_max
        if wev_code > code:
            code = wev_code
        prec += wev_prec
        clouds += wev_clouds

        cnt += 1

    if cnt == 0:
        raise PrologRuntimeError('weather_data: no data found.', g.location)

    prec   /= float(cnt)
    clouds /= float(cnt)

    g.env[arg_code]     = StringLiteral(code)
    g.env[arg_prec]     = NumberLiteral(prec)
    g.env[arg_temp_min] = NumberLiteral(temp_min)
    g.env[arg_temp_max] = NumberLiteral(temp_max)
    g.env[arg_clouds]   = NumberLiteral(clouds)

    return True

def init_module(kernal):

    kernal.rt.register_builtin ('weather_data', builtin_weather_data) # weather_data (+C, +Str)

