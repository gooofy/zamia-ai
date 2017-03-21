#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import rdflib

DEPENDS    = [ 'base' ]

PL_SOURCES = [
              'politics.pl',
             ]

RDF_ALIASES = {
                u'wde:PresidentOfGermany'         : u'http://www.wikidata.org/entity/Q25223',
                u'wde:FederalChancellorOfGermany' : u'http://www.wikidata.org/entity/Q4970706',
              }

KB_SOURCES = [

              # people

              (
                [ 
                  ('wdpd:PositionHeld', 'wde:FederalChancellorOfGermany'),
                  ('wdpd:PositionHeld', 'wde:PresidentOfGermany'),
                ],
                [
                  ['wdpd:PlaceOfBirth'], 
                  ['wdp:PositionHeld','*']
                ]
              ),

            ]

