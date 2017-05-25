#!/usr/bin/env python
# -*- coding: utf-8 -*- 

DEPENDS    = [ 'base', 'config' ]

PL_SOURCES = [
              'media.pl',
             ]

RDF_ALIASES = {
                u'wde:B5aktuell'             : u'http://www.wikidata.org/entity/Q795291',
                u'wde:Deutschlandfunk'       : u'http://www.wikidata.org/entity/Q695328',
                u'wde:SWRAktuell'            : u'http://www.wikidata.org/entity/Q2208796',
                u'wde:SWR3'                  : u'http://www.wikidata.org/entity/Q2208789',
                u'wde:PowerHitRadio'         : u'http://www.wikidata.org/entity/Q12372710',
                u'wde:104.6RTL'              : u'http://www.wikidata.org/entity/Q166266',
              }

KB_SOURCES = [
              (
                [ 
                  u'wde:B5aktuell',
                  u'wde:Deutschlandfunk',
                  u'wde:SWRAktuell',
                  u'wde:SWR3',
                  u'wde:PowerHitRadio',
                  u'wde:104.6RTL', 
                ],
                [
                  [], 
                ]
              ),
              'slots.n3',
             ]

