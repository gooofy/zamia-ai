#!/usr/bin/env python
# -*- coding: utf-8 -*- 

DEPENDS    = [ ]

PL_SOURCES = [
              'geo.pl',
              'people.pl',
              'time.pl',
             ]

KB_SOURCES = [
              'tz.n3',

              # people

              (
                [ 
                  ('wdpd:PositionHeld', 'wde:FederalChancellorOfGermany'),
                  ('wdpd:PositionHeld', 'wde:PresidentOfGermany'),
                  # ('wdpd:Occupation',   'wde:ComputerScientist'),
                  #u'wde:AngelaMerkel', 
                  #u'wde:GerhardSchröder',
                ],
                [
                  ['wdpd:PlaceOfBirth'], 
                  ['wdp:PositionHeld','*']
                ]
              ),

              # places

              (
                [
                  u'wde:Freudental',
                  u'wde:Ludwigsburg',
                  u'wde:Stuttgart',
                  u'wde:Tallinn',
                  u'wde:SanFrancisco',
                  u'wde:LosAngeles',
                  u'wde:NewYorkCity',
                  u'wde:London',
                  u'wde:Paris',
                  u'wde:Reykjavík',
                  u'wde:Oberwiesenthal'
                  u'wde:Arnstorf',
                  u'wde:Hamburg',
                  u'wde:Brackenheim',
                  u'wde:Heilbronn',
                  u'wde:Ludwigshafen',
                  u'wde:BiberachRiss',
                  u'wde:BlombergNRW',
                  u'wde:WashingtonDC',
                  u'wde:Fairbanks',
                ],
                [[]]
              )
            ]
