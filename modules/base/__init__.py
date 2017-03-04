#!/usr/bin/env python
# -*- coding: utf-8 -*- 

DEPENDS    = [ ]

PL_SOURCES = [
              'geo.pl',
              'people.pl',
              'time.pl',
             ]

RDF_PREFIXES = {
                'rdf':     'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'rdfs':    'http://www.w3.org/2000/01/rdf-schema#',
                'hal':     'http://hal.zamia.org/kb/',
                'dbo':     'http://dbpedia.org/ontology/',
                'dbr':     'http://dbpedia.org/resource/',
                'dbp':     'http://dbpedia.org/property/',
                'xml':     'http://www.w3.org/XML/1998/namespace',
                'xsd':     'http://www.w3.org/2001/XMLSchema#',
                'geo':     'http://www.opengis.net/ont/geosparql#',
                'geo1':    'http://www.w3.org/2003/01/geo/wgs84_pos#',
                'geof':    'http://www.opengis.net/def/function/geosparql/',
                'owl':     'http://www.w3.org/2002/07/owl#',
                'schema':  'http://schema.org/',
                'wde':     'http://www.wikidata.org/entity/',
                'wdes':    'http://www.wikidata.org/entity/statement',
                'wdpd':    'http://www.wikidata.org/prop/direct/',
                'wdps':    'http://www.wikidata.org/prop/statement/',
                'wdpq':    'http://www.wikidata.org/prop/qualifier/',
                'wdp':     'http://www.wikidata.org/prop/',
               }

LDF_ENDPOINTS = {
                  'www.wikidata.org': 'https://query.wikidata.org/bigdata/ldf',
                }

RDF_ALIASES = {
                u'wde:Human'                      : u'http://www.wikidata.org/entity/Q5',
                u'wde:AngelaMerkel'               : u'http://www.wikidata.org/entity/Q567',
                u'wde:GerhardSchröder'            : u'http://www.wikidata.org/entity/Q2530',
                u'wde:PresidentOfGermany'         : u'http://www.wikidata.org/entity/Q25223',
                u'wde:ComputerScientist'          : u'http://www.wikidata.org/entity/Q82594',
                u'wde:FederalChancellorOfGermany' : u'http://www.wikidata.org/entity/Q4970706',
                u'wde:Female'                     : u'http://www.wikidata.org/entity/Q6581072',
                u'wde:Male'                       : u'http://www.wikidata.org/entity/Q6581097',

                u'wde:Freudental'                 : u'http://www.wikidata.org/entity/Q61656',
                u'wde:Ludwigsburg'                : u'http://www.wikidata.org/entity/Q622',
                u'wde:Stuttgart'                  : u'http://www.wikidata.org/entity/Q1022',
                u'wde:Tallinn'                    : u'http://www.wikidata.org/entity/Q1770',
                u'wde:SanFrancisco'               : u'http://www.wikidata.org/entity/Q62',
                u'wde:LosAngeles'                 : u'http://www.wikidata.org/entity/Q65',
                u'wde:NewYorkCity'                : u'http://www.wikidata.org/entity/Q60',
                u'wde:London'                     : u'http://www.wikidata.org/entity/Q84',
                u'wde:Paris'                      : u'http://www.wikidata.org/entity/Q90',
                u'wde:Reykjavík'                  : u'http://www.wikidata.org/entity/Q1764',
                u'wde:Oberwiesenthal'             : u'http://www.wikidata.org/entity/Q57926',
                u'wde:Arnstorf'                   : u'http://www.wikidata.org/entity/Q582608',
                u'wde:Hamburg'                    : u'http://www.wikidata.org/entity/Q1055',
                u'wde:Brackenheim'                : u'http://www.wikidata.org/entity/Q53751',
                u'wde:Heilbronn'                  : u'http://www.wikidata.org/entity/Q715',
                u'wde:Ludwigshafen'               : u'http://www.wikidata.org/entity/Q2910',
                u'wde:BiberachRiss'               : u'http://www.wikidata.org/entity/Q16069',
                u'wde:BlombergNRW'                : u'http://www.wikidata.org/entity/Q168646',
                u'wde:WashingtonDC'               : u'http://www.wikidata.org/entity/Q61',
                u'wde:Fairbanks'                  : u'http://www.wikidata.org/entity/Q79638',
              }

# wikidata properties

for prefix, iri in [('wdpd',    'http://www.wikidata.org/prop/direct/'),
                    ('wdps',    'http://www.wikidata.org/prop/statement/'),
                    ('wdpq',    'http://www.wikidata.org/prop/qualifier/'),
                    ('wdp',     'http://www.wikidata.org/prop/')]:

    for proplabel, propid in [(u'PlaceOfBirth'               , u'P19'),
                              (u'SexOrGender'                , u'P21'),
                              (u'InstanceOf'                 , u'P31'),
                              (u'PositionHeld'               , u'P39'),
                              (u'Occupation'                 , u'P106'),
                              (u'StartTime'                  , u'P580'),
                              (u'EndTime'                    , u'P582'), ]:

        RDF_ALIASES[prefix + ':' + proplabel] = iri + propid


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

