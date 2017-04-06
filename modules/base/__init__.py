#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import rdflib

DEPENDS    = [ 'config' ]

PL_SOURCES = [
              'base.pl',
              'conversation.pl',
              'math.pl',
              'time.pl',
              'people.pl',
             ]

RDF_PREFIXES = {
                'rdf':     'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'rdfs':    'http://www.w3.org/2000/01/rdf-schema#',
                'ai':      'http://ai.zamia.org/kb/',
                'aiu':     'http://ai.zamia.org/kb/user/',
                'aiup':    'http://ai.zamia.org/kb/user/prop/',
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
                  'sws.geonames.org': 'http://data.linkeddatafragments.org/geonames',
                }

RDF_ALIASES = {
                u'wde:Human'                      : u'http://www.wikidata.org/entity/Q5',
                u'wde:Computer'                   : u'http://www.wikidata.org/entity/Q68',
                u'wde:AngelaMerkel'               : u'http://www.wikidata.org/entity/Q567',
                u'wde:GerhardSchröder'            : u'http://www.wikidata.org/entity/Q2530',
                u'wde:ProgrammingLanguage'        : u'http://www.wikidata.org/entity/Q9143',
                u'wde:ComputerScientist'          : u'http://www.wikidata.org/entity/Q82594',
                u'wde:HomeComputer'               : u'http://www.wikidata.org/entity/Q473708',
                u'wde:Female'                     : u'http://www.wikidata.org/entity/Q6581072',
                u'wde:Male'                       : u'http://www.wikidata.org/entity/Q6581097',
                u'wde:FemaleGivenName'            : u'http://www.wikidata.org/entity/Q11879590',
                u'wde:MaleGivenName'              : u'http://www.wikidata.org/entity/Q12308941',

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

    for proplabel, propid in [(u'PlaceOfBirth'                               , u'P19'),
                              (u'SexOrGender'                                , u'P21'),
                              (u'InstanceOf'                                 , u'P31'),
                              (u'PositionHeld'                               , u'P39'),
                              (u'Director'                                   , u'P57'),
                              (u'ScreenWriter'                               , u'P58'),
                              (u'Occupation'                                 , u'P106'),
                              (u'LocatedInTheAdministrativeTerritorialEntity', u'P131'),
                              (u'Genre'                                      , u'P136'),
                              (u'BasedOn'                                    , u'P144'),
                              (u'CastMember'                                 , u'P161'),
                              (u'DateOfBirth'                                , u'P569'),
                              (u'PublicationDate'                            , u'P577'),
                              (u'StartTime'                                  , u'P580'),
                              (u'EndTime'                                    , u'P582'),
                              (u'MainSubject'                                , u'P921'),
                              (u'Replaces'                                   , u'P1365'),
                              (u'ReplacedBy'                                 , u'P1366'),
                              (u'GeoNamesID'                                 , u'P1566'),
                             ]:

        RDF_ALIASES[prefix + ':' + proplabel] = iri + propid


KB_SOURCES = [

              # people

              (
                [ 
                  u'wde:AngelaMerkel', 
                  u'wde:GerhardSchröder',
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
                [
                
                  [('wdpd:GeoNamesID', lambda l: (rdflib.URIRef('ai:GeoNames'), rdflib.URIRef('http://sws.geonames.org/%s/' % l)))], 
                
                ]
              ),
              'tz.n3',
            ]

