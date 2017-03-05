#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from kb_weather import fetch_weather_forecast

DEPENDS = [ 'base' ]

PL_SOURCES = [
              'weather.pl',
             ]

KB_SOURCES = [
              'weather_base.n3',
              'weather_test.n3',
             ]

CRONJOBS   = [
              ( 'fetch_forecast', 4 * 60 * 60, fetch_weather_forecast),
             ]

