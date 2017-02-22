#!/usr/bin/env python
# -*- coding: utf-8 -*- 

DEPENDS    = [ ]

PL_SOURCES = [
              'common-sense.pl',
             ]

KB_SOURCES = [
              'tz.n3',
              ('http://fragments.dbpedia.org/2016-04/en',
               ['dbr:Freudental',
                'dbr:Ludwigsburg',
                'dbr:Stuttgart',
                'dbr:Tallinn',
                'dbr:San_Francisco',
                'dbr:Los_Angeles',
                'dbr:New_York_City', 
                'dbr:London',
                'dbr:Paris',
                'dbr:Reykjavík',
                'dbr:Oberwiesenthal',
                'dbr:Arnstorf',
                'dbr:Hamburg',
                'dbr:Brackenheim',
                'dbr:Heilbronn',
                'dbr:Ludwigshafen',
                'http://dbpedia.org/resource/Blomberg,_North_Rhine-Westphalia',
                'dbr:Biberach_an_der_Riss',
                'http://dbpedia.org/resource/Washington,_D.C.',
                'http://dbpedia.org/resource/Fairbanks,_Alaska' 
               ]
              )
             ]

