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

import rdflib

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
                u'wde:WikidataProperty'                                 : u'http://www.wikidata.org/entity/Q18616576',
                u'wde:TransitiveProperty'                               : u'http://www.wikidata.org/entity/Q18647515',
                u'wde:AsymmetricProperty'                               : u'http://www.wikidata.org/entity/Q18647519',
                u'wde:ReflexiveProperty'                                : u'http://www.wikidata.org/entity/Q18647521',
                u'wde:WikidatapropertyForTheRelationshipBetweenClasses' : u'http://www.wikidata.org/entity/Q28326461',

                u'wde:Human'                               : u'http://www.wikidata.org/entity/Q5',
                u'wde:Computer'                            : u'http://www.wikidata.org/entity/Q68',
                u'wde:Book'                                : u'http://www.wikidata.org/entity/Q571',
                u'wde:OperatingSystem'                     : u'http://www.wikidata.org/entity/Q9135',
                u'wde:ProgrammingLanguage'                 : u'http://www.wikidata.org/entity/Q9143',
                u'wde:Film'                                : u'http://www.wikidata.org/entity/Q11424',
                u'wde:PresidentOfTheUnitedStatesOfAmerica' : u'http://www.wikidata.org/entity/Q11696',
                u'wde:PresidentOfGermany'                  : u'http://www.wikidata.org/entity/Q25223',
                u'wde:Writer'                              : u'http://www.wikidata.org/entity/Q36180',
                u'wde:ComputerScientist'                   : u'http://www.wikidata.org/entity/Q82594',
                u'wde:HomeComputer'                        : u'http://www.wikidata.org/entity/Q473708',
                u'wde:FilmDirector'                        : u'http://www.wikidata.org/entity/Q2526255',
                u'wde:FederalChancellorOfGermany'          : u'http://www.wikidata.org/entity/Q4970706',
                u'wde:Female'                              : u'http://www.wikidata.org/entity/Q6581072',
                u'wde:Male'                                : u'http://www.wikidata.org/entity/Q6581097',
                u'wde:FemaleGivenName'                     : u'http://www.wikidata.org/entity/Q11879590',
                u'wde:MaleGivenName'                       : u'http://www.wikidata.org/entity/Q12308941',
                u'wde:MultitaskingOperatingSystem'         : u'http://www.wikidata.org/entity/Q28933706',

                u'wde:City'                                : u'http://www.wikidata.org/entity/Q515',
                u'wde:Capital'                             : u'http://www.wikidata.org/entity/Q5119',
                u'wde:Municipality'                        : u'http://www.wikidata.org/entity/Q15284',
                u'wde:GeographicRegion'                    : u'http://www.wikidata.org/entity/Q82794',
                u'wde:MunicipalityOfGermany'               : u'http://www.wikidata.org/entity/Q262166',
                u'wde:HumanSettlement'                     : u'http://www.wikidata.org/entity/Q486972',
                u'wde:BigCity'                             : u'http://www.wikidata.org/entity/Q1549591',
                u'wde:GeographicLocation'                  : u'http://www.wikidata.org/entity/Q2221906',
                u'wde:Location'                            : u'http://www.wikidata.org/entity/Q17334923',

                u'wde:AngelaMerkel'                        : u'http://www.wikidata.org/entity/Q567',
                u'wde:GerhardSchröder'                     : u'http://www.wikidata.org/entity/Q2530',
                u'wde:NiklausWirth'                        : u'http://www.wikidata.org/entity/Q92604',

                u'wde:DouglasAdams'                        : u'http://www.wikidata.org/entity/Q42',
                u'wde:JRRTolkien'                          : u'http://www.wikidata.org/entity/Q892',
                u'wde:DanBrown'                            : u'http://www.wikidata.org/entity/Q7345',
                u'wde:AlfredHitchcock'                     : u'http://www.wikidata.org/entity/Q7374',
                u'wde:NoamChomsky'                         : u'http://www.wikidata.org/entity/Q9049',
                u'wde:EdgarAllanPoe'                       : u'http://www.wikidata.org/entity/Q16867',
                u'wde:JKRowling'                           : u'http://www.wikidata.org/entity/Q34660',
                u'wde:StephenKing'                         : u'http://www.wikidata.org/entity/Q39829',
                u'wde:ArthurCClarke'                       : u'http://www.wikidata.org/entity/Q47087',
                u'wde:JohnGrisham'                         : u'http://www.wikidata.org/entity/Q106465',
                u'wde:MichaelCrichton'                     : u'http://www.wikidata.org/entity/Q172140',
                u'wde:WilliamGibson'                       : u'http://www.wikidata.org/entity/Q188987',
                u'wde:KenFollett'                          : u'http://www.wikidata.org/entity/Q210669',
                u'wde:NealStephenson'                      : u'http://www.wikidata.org/entity/Q312853',
                u'wde:ScottSigler'                         : u'http://www.wikidata.org/entity/Q3476305',

                u'wde:NewYorkCity'                         : u'http://www.wikidata.org/entity/Q60',
                u'wde:WashingtonDC'                        : u'http://www.wikidata.org/entity/Q61',
                u'wde:SanFrancisco'                        : u'http://www.wikidata.org/entity/Q62',
                u'wde:LosAngeles'                          : u'http://www.wikidata.org/entity/Q65',
                u'wde:London'                              : u'http://www.wikidata.org/entity/Q84',
                u'wde:Paris'                               : u'http://www.wikidata.org/entity/Q90',
                u'wde:Ludwigsburg'                         : u'http://www.wikidata.org/entity/Q622',
                u'wde:Heilbronn'                           : u'http://www.wikidata.org/entity/Q715',
                u'wde:Stuttgart'                           : u'http://www.wikidata.org/entity/Q1022',
                u'wde:Hamburg'                             : u'http://www.wikidata.org/entity/Q1055',
                u'wde:Reykjavík'                           : u'http://www.wikidata.org/entity/Q1764',
                u'wde:Tallinn'                             : u'http://www.wikidata.org/entity/Q1770',
                u'wde:Ludwigshafen'                        : u'http://www.wikidata.org/entity/Q2910',
                u'wde:BiberachRiss'                        : u'http://www.wikidata.org/entity/Q16069',
                u'wde:Brackenheim'                         : u'http://www.wikidata.org/entity/Q53751',
                u'wde:Oberwiesenthal'                      : u'http://www.wikidata.org/entity/Q57926',
                u'wde:Freudental'                          : u'http://www.wikidata.org/entity/Q61656',
                u'wde:Fairbanks'                           : u'http://www.wikidata.org/entity/Q79638',
                u'wde:Birenbach'                           : u'http://www.wikidata.org/entity/Q80455',
                u'wde:BlombergNRW'                         : u'http://www.wikidata.org/entity/Q168646',
                u'wde:Arnstorf'                            : u'http://www.wikidata.org/entity/Q582608',

                # literature

                u'wde:Novel2001ASpaceOdyssey'     : u'http://www.wikidata.org/entity/Q835341',
                u'wde:NovelNeuromancer'           : u'http://www.wikidata.org/entity/Q662029',
                u'wde:NovelTheStand'              : u'http://www.wikidata.org/entity/Q149552',

                # media

                u'wde:B5aktuell'             : u'http://www.wikidata.org/entity/Q795291',
                u'wde:Deutschlandfunk'       : u'http://www.wikidata.org/entity/Q695328',
                u'wde:SWRAktuell'            : u'http://www.wikidata.org/entity/Q2208796',
                u'wde:SWR3'                  : u'http://www.wikidata.org/entity/Q2208789',
                u'wde:PowerHitRadio'         : u'http://www.wikidata.org/entity/Q12372710',
                u'wde:104.6RTL'              : u'http://www.wikidata.org/entity/Q166266',

                # operating systems

                u'wde:Linux'                            : u'http://www.wikidata.org/entity/Q388',
                u'wde:MicrosoftWindows'                 : u'http://www.wikidata.org/entity/Q1406',
                u'wde:IBMOS2'                           : u'http://www.wikidata.org/entity/Q189794',
                u'wde:IBMZOS'                           : u'http://www.wikidata.org/entity/Q283705',
                u'wde:Solaris'                          : u'http://www.wikidata.org/entity/Q14646',
                u'wde:MSDOS'                            : u'http://www.wikidata.org/entity/Q47604',
                u'wde:Android'                          : u'http://www.wikidata.org/entity/Q94',
                u'wde:macOS'                            : u'http://www.wikidata.org/entity/Q14116',
                u'wde:iOS'                              : u'http://www.wikidata.org/entity/Q48493',
                u'wde:CPM'                              : u'http://www.wikidata.org/entity/Q219528',
                u'wde:Unix'                             : u'http://www.wikidata.org/entity/Q11368',

                # programming languages

                u'wde:C'                                : u'http://www.wikidata.org/entity/Q15777',
                u'wde:Java'                             : u'http://www.wikidata.org/entity/Q251',
                u'wde:Python'                           : u'http://www.wikidata.org/entity/Q28865',
                u'wde:Pascal'                           : u'http://www.wikidata.org/entity/Q81571',
                u'wde:BASIC'                            : u'http://www.wikidata.org/entity/Q42979',
                u'wde:TurboPascal'                      : u'http://www.wikidata.org/entity/Q473201',
                u'wde:Ruby'                             : u'http://www.wikidata.org/entity/Q161053',
                u'wde:HTML'                             : u'http://www.wikidata.org/entity/Q8811',
                u'wde:COBOL'                            : u'http://www.wikidata.org/entity/Q131140',
                u'wde:Fortran'                          : u'http://www.wikidata.org/entity/Q83303',
                u'wde:Perl'                             : u'http://www.wikidata.org/entity/Q42478',
                u'wde:Prolog'                           : u'http://www.wikidata.org/entity/Q163468',

                # home computers

                u'wde:CommodoreVIC20'                   : u'http://www.wikidata.org/entity/Q918232',
                u'wde:Commodore64'                      : u'http://www.wikidata.org/entity/Q99775',
                u'wde:CommodorePlus4'                   : u'http://www.wikidata.org/entity/Q868568',
                u'wde:Commodore128'                     : u'http://www.wikidata.org/entity/Q1115919',
                u'wde:CommodorePET'                     : u'http://www.wikidata.org/entity/Q946661',
                u'wde:TRS80'                            : u'http://www.wikidata.org/entity/Q610305',
                u'wde:Atari800'                         : u'http://www.wikidata.org/entity/Q4889765',
                u'wde:AtariST'                          : u'http://www.wikidata.org/entity/Q627302',
                u'wde:Altair8800'                       : u'http://www.wikidata.org/entity/Q223493',
                u'wde:Amiga'                            : u'http://www.wikidata.org/entity/Q100047',
                u'wde:AppleMacintosh'                   : u'http://www.wikidata.org/entity/Q75687',
                u'wde:AppleII'                          : u'http://www.wikidata.org/entity/Q3017175',
                u'wde:ZX81'                             : u'http://www.wikidata.org/entity/Q263250',
                u'wde:ZXSpectrum'                       : u'http://www.wikidata.org/entity/Q23882',
                u'wde:MSX'                              : u'http://www.wikidata.org/entity/Q853547',
                u'wde:TexasInstrumentsTI994A'           : u'http://www.wikidata.org/entity/Q454390',
                u'wde:AmstradCPC'                       : u'http://www.wikidata.org/entity/Q478829',

              }

# wikidata properties

for prefix, iri in [('wdpd',    'http://www.wikidata.org/prop/direct/'),
                    ('wdps',    'http://www.wikidata.org/prop/statement/'),
                    ('wdpq',    'http://www.wikidata.org/prop/qualifier/'),
                    ('wdp',     'http://www.wikidata.org/prop/')]:

    for proplabel, propid in [(u'PlaceOfBirth'                               , u'P19'),
                              (u'SexOrGender'                                , u'P21'),
                              (u'CountryOfCitizenship'                       , u'P27'),
                              (u'InstanceOf'                                 , u'P31'),
                              (u'PositionHeld'                               , u'P39'),
                              (u'Author'                                     , u'P50'),
                              (u'Director'                                   , u'P57'),
                              (u'ScreenWriter'                               , u'P58'),
                              (u'Occupation'                                 , u'P106'),
                              (u'LocatedIn'                                  , u'P131'),
                              (u'Genre'                                      , u'P136'),
                              (u'BasedOn'                                    , u'P144'),
                              (u'CastMember'                                 , u'P161'),
                              (u'SubclassOf'                                 , u'P279'),
                              (u'DateOfBirth'                                , u'P569'),
                              (u'PublicationDate'                            , u'P577'),
                              (u'StartTime'                                  , u'P580'),
                              (u'EndTime'                                    , u'P582'),
                              (u'FamilyName'                                 , u'P734'),
                              (u'GivenName'                                  , u'P735'),
                              (u'NotableWork'                                , u'P800'),
                              (u'MainSubject'                                , u'P921'),
                              (u'WorkLocation'                               , u'P937'),
                              (u'Replaces'                                   , u'P1365'),
                              (u'ReplacedBy'                                 , u'P1366'),
                              (u'GeoNamesID'                                 , u'P1566'),
                             ]:

        RDF_ALIASES[prefix + ':' + proplabel] = iri + propid


RES_PATHS = [

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
                  u'wde:Oberwiesenthal',
                  u'wde:Arnstorf',
                  u'wde:Hamburg',
                  u'wde:Brackenheim',
                  u'wde:Heilbronn',
                  u'wde:Ludwigshafen',
                  u'wde:BiberachRiss',
                  u'wde:BlombergNRW',
                  u'wde:WashingtonDC',
                  u'wde:Fairbanks',
                  u'wde:Birenbach',
                ],
                [
                  [('wdpd:GeoNamesID', lambda l: (rdflib.URIRef('ai:GeoNames'), rdflib.URIRef('http://sws.geonames.org/%s/' % l)))], 
                  ['wdpd:InstanceOf'],
                  ['wdpd:SubclassOf'],
                ]
              ),

              # people

              (
                [ 
                  u'wde:ArthurCClarke',
                  u'wde:NiklausWirth',
                  u'wde:DouglasAdams',
                  u'wde:JRRTolkien',
                  u'wde:DanBrown',
                  u'wde:AlfredHitchcock',
                  u'wde:NoamChomsky',
                  u'wde:EdgarAllanPoe',
                  u'wde:JKRowling',
                  u'wde:StephenKing',
                  u'wde:ArthurCClarke',
                  u'wde:JohnGrisham',
                  u'wde:MichaelCrichton',
                  u'wde:WilliamGibson',
                  u'wde:KenFollett',
                  u'wde:NealStephenson',
                  u'wde:ScottSigler',
                  ('wdpd:PositionHeld', 'wde:PresidentOfTheUnitedStatesOfAmerica'),
                  ('wdpd:PositionHeld', 'wde:FederalChancellorOfGermany'),
                  ('wdpd:PositionHeld', 'wde:PresidentOfGermany'),
                ],
                [
                  ['wdpd:PlaceOfBirth'], 
                  ['wdp:PositionHeld','*'],
                  ['wdpd:Genre'],
                  ['wdpd:CountryOfCitizenship'],
                  ['wdpd:Occupation'],
                  ['wdpd:NotableWork'],
                  ['wdpd:WorkLocation'],
                  ['wdpd:FamilyName'],
                  ['wdpd:GivenName'],
                  ['wdpd:InstanceOf'],
                  ['wdpd:SubclassOf'],
                ]
              ),

              # geo ontology

              (
                [
                  u'wde:City',
                  u'wde:Municipality',
                  u'wde:GeographicRegion',
                  u'wde:MunicipalityOfGermany',
                  u'wde:HumanSettlement',
                  u'wde:BigCity',
                  u'wde:GeographicLocation',
                  u'wde:Location',
                  u'wde:Capital',
                ],
                [
                  ['wdpd:SubclassOf'],
                  ['wdpd:InstanceOf'],
                ]
              ),

              # literature

              (
                [
                  u'wde:Novel2001ASpaceOdyssey',
                  u'wde:NovelNeuromancer',
                  u'wde:NovelTheStand',
                ],
                [
                  [u'wdpd:Genre'],
                  [u'wdpd:Author'],
                ]
              ),

              # media

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

              # operating systems

              (
                [ 
                  u'wde:Linux',
                  u'wde:MicrosoftWindows',
                  u'wde:IBMOS2',
                  u'wde:IBMZOS',
                  u'wde:Solaris',
                  u'wde:MSDOS',
                  u'wde:Android',
                  u'wde:macOS',
                  u'wde:iOS',
                  u'wde:CPM',
                  u'wde:Unix',
                  # ('wdpd:InstanceOf', 'wde:OperatingSystem'),
                  # ('wdpd:InstanceOf', 'wde:MultitaskingOperatingSystem'),
                ],
                [
                  [], 
                ]
              ),


              # programming languages

              (
                [ 
                  u'wde:C',
                  u'wde:Java',
                  u'wde:Python',
                  u'wde:Pascal',
                  u'wde:BASIC',
                  u'wde:TurboPascal',
                  u'wde:Ruby',
                  u'wde:HTML',
                  u'wde:COBOL',
                  u'wde:Fortran',
                  u'wde:Perl',
                  u'wde:Prolog',
                  # ('wdpd:InstanceOf', 'wde:ProgrammingLanguage'),
                ],
                [
                  [], 
                ]
              ),

              # home computers
              (
                [ 
                  u'wde:CommodoreVIC20',
                  u'wde:Commodore64',
                  u'wde:CommodorePlus4',
                  u'wde:Commodore128',
                  u'wde:CommodorePET',
                  u'wde:TRS80',
                  u'wde:Atari800',
                  u'wde:AtariST',
                  u'wde:Altair8800',
                  u'wde:Amiga',
                  u'wde:AppleMacintosh',
                  u'wde:AppleII',
                  u'wde:ZX81',
                  u'wde:ZXSpectrum',
                  u'wde:MSX',
                  u'wde:TexasInstrumentsTI994A',
                  u'wde:AmstradCPC',
                  # ('wdpd:InstanceOf', 'wde:HomeComputer'),
                ],
                [
                  ['wdpd:Manufacturer'], 
                ]
              ),

              # properties, ontology

              (
                [
                  u'wde:WikidataProperty',
                  u'wde:TransitiveProperty',
                  u'wde:AsymmetricProperty',
                  u'wde:ReflexiveProperty',
                  u'wde:WikidatapropertyForTheRelationshipBetweenClasses',
                  u'wde:Writer',
                  u'wde:FilmDirector',
                  u'wde:OperatingSystem',
                  u'wde:MultitaskingOperatingSystem',
                ],
                [
                  ['wdpd:SubclassOf'],
                  ['wdpd:InstanceOf'],
                ]
              ),

              # top 250 movies from IMDB as of 2017/03/16

              (
                [
                  # movie: tt0111161
                  u'http://www.wikidata.org/entity/Q172241',
                  # movie: tt0111161
                  u'http://www.wikidata.org/entity/Q172241',
                  # movie: tt0068646
                  u'http://www.wikidata.org/entity/Q47703',
                  # movie: tt0068646
                  u'http://www.wikidata.org/entity/Q47703',
                  # movie: tt0071562
                  u'http://www.wikidata.org/entity/Q184768',
                  # movie: tt0071562
                  u'http://www.wikidata.org/entity/Q184768',
                  # movie: tt0468569
                  u'http://www.wikidata.org/entity/Q163872',
                  # movie: tt0468569
                  u'http://www.wikidata.org/entity/Q163872',
                  # movie: tt0050083
                  u'http://www.wikidata.org/entity/Q2345',
                  # movie: tt0050083
                  u'http://www.wikidata.org/entity/Q2345',
                  # movie: tt0108052
                  u'http://www.wikidata.org/entity/Q483941',
                  # movie: tt0108052
                  u'http://www.wikidata.org/entity/Q483941',
                  # movie: tt0110912
                  u'http://www.wikidata.org/entity/Q104123',
                  # movie: tt0110912
                  u'http://www.wikidata.org/entity/Q104123',
                  # movie: tt0167260
                  u'http://www.wikidata.org/entity/Q131074',
                  # movie: tt0167260
                  u'http://www.wikidata.org/entity/Q131074',
                  # movie: tt0060196
                  u'http://www.wikidata.org/entity/Q41483',
                  # movie: tt0060196
                  u'http://www.wikidata.org/entity/Q41483',
                  # movie: tt0137523
                  u'http://www.wikidata.org/entity/Q190050',
                  # movie: tt0137523
                  u'http://www.wikidata.org/entity/Q190050',
                  # movie: tt0120737
                  u'http://www.wikidata.org/entity/Q127367',
                  # movie: tt0120737
                  u'http://www.wikidata.org/entity/Q127367',
                  # movie: tt0080684
                  u'http://www.wikidata.org/entity/Q181795',
                  # movie: tt0080684
                  u'http://www.wikidata.org/entity/Q181795',
                  # movie: tt0109830
                  u'http://www.wikidata.org/entity/Q134773',
                  # movie: tt0109830
                  u'http://www.wikidata.org/entity/Q134773',
                  # movie: tt1375666
                  u'http://www.wikidata.org/entity/Q25188',
                  # movie: tt1375666
                  u'http://www.wikidata.org/entity/Q25188',
                  # movie: tt0167261
                  u'http://www.wikidata.org/entity/Q164963',
                  # movie: tt0167261
                  u'http://www.wikidata.org/entity/Q164963',
                  # movie: tt0073486
                  u'http://www.wikidata.org/entity/Q171669',
                  # movie: tt0073486
                  u'http://www.wikidata.org/entity/Q171669',
                  # movie: tt0099685
                  u'http://www.wikidata.org/entity/Q42047',
                  # movie: tt0099685
                  u'http://www.wikidata.org/entity/Q42047',
                  # movie: tt0133093
                  u'http://www.wikidata.org/entity/Q83495',
                  # movie: tt0133093
                  u'http://www.wikidata.org/entity/Q83495',
                  # movie: tt0047478
                  u'http://www.wikidata.org/entity/Q189540',
                  # movie: tt0047478
                  u'http://www.wikidata.org/entity/Q189540',
                  # movie: tt0076759
                  u'http://www.wikidata.org/entity/Q17738',
                  # movie: tt0076759
                  u'http://www.wikidata.org/entity/Q17738',
                  # movie: tt0317248
                  u'http://www.wikidata.org/entity/Q220741',
                  # movie: tt0317248
                  u'http://www.wikidata.org/entity/Q220741',
                  # movie: tt0114369
                  u'http://www.wikidata.org/entity/Q190908',
                  # movie: tt0114369
                  u'http://www.wikidata.org/entity/Q190908',
                  # movie: tt0102926
                  u'http://www.wikidata.org/entity/Q133654',
                  # movie: tt0102926
                  u'http://www.wikidata.org/entity/Q133654',
                  # movie: tt0038650
                  u'http://www.wikidata.org/entity/Q204191',
                  # movie: tt0038650
                  u'http://www.wikidata.org/entity/Q204191',
                  # movie: tt0114814
                  u'http://www.wikidata.org/entity/Q132351',
                  # movie: tt0114814
                  u'http://www.wikidata.org/entity/Q132351',
                  # movie: tt0118799
                  u'http://www.wikidata.org/entity/Q19355',
                  # movie: tt0118799
                  u'http://www.wikidata.org/entity/Q19355',
                  # movie: tt0110413
                  u'http://www.wikidata.org/entity/Q484675',
                  # movie: tt0110413
                  u'http://www.wikidata.org/entity/Q484675',
                  # movie: tt0245429
                  u'http://www.wikidata.org/entity/Q155653',
                  # movie: tt0245429
                  u'http://www.wikidata.org/entity/Q155653',
                  # movie: tt0120815
                  u'http://www.wikidata.org/entity/Q165817',
                  # movie: tt0120815
                  u'http://www.wikidata.org/entity/Q165817',
                  # movie: tt0064116
                  u'http://www.wikidata.org/entity/Q168154',
                  # movie: tt0064116
                  u'http://www.wikidata.org/entity/Q168154',
                  # movie: tt0120586
                  u'http://www.wikidata.org/entity/Q208572',
                  # movie: tt0120586
                  u'http://www.wikidata.org/entity/Q208572',
                  # movie: tt0816692
                  u'http://www.wikidata.org/entity/Q13417189',
                  # movie: tt0816692
                  u'http://www.wikidata.org/entity/Q13417189',
                  # movie: tt0034583
                  u'http://www.wikidata.org/entity/Q132689',
                  # movie: tt0034583
                  u'http://www.wikidata.org/entity/Q132689',
                  # movie: tt0021749
                  u'http://www.wikidata.org/entity/Q238211',
                  # movie: tt0021749
                  u'http://www.wikidata.org/entity/Q238211',
                  # movie: tt0054215
                  u'http://www.wikidata.org/entity/Q163038',
                  # movie: tt0054215
                  u'http://www.wikidata.org/entity/Q163038',
                  # movie: tt0120689
                  u'http://www.wikidata.org/entity/Q208263',
                  # movie: tt0120689
                  u'http://www.wikidata.org/entity/Q208263',
                  # movie: tt1675434
                  u'http://www.wikidata.org/entity/Q595',
                  # movie: tt1675434
                  u'http://www.wikidata.org/entity/Q595',
                  # movie: tt0027977
                  u'http://www.wikidata.org/entity/Q45602',
                  # movie: tt0027977
                  u'http://www.wikidata.org/entity/Q45602',
                  # movie: tt0082971
                  u'http://www.wikidata.org/entity/Q174284',
                  # movie: tt0082971
                  u'http://www.wikidata.org/entity/Q174284',
                  # movie: tt0047396
                  u'http://www.wikidata.org/entity/Q34414',
                  # movie: tt0047396
                  u'http://www.wikidata.org/entity/Q34414',
                  # movie: tt0253474
                  u'http://www.wikidata.org/entity/Q150804',
                  # movie: tt0253474
                  u'http://www.wikidata.org/entity/Q150804',
                  # movie: tt0407887
                  u'http://www.wikidata.org/entity/Q172975',
                  # movie: tt0407887
                  u'http://www.wikidata.org/entity/Q172975',
                  # movie: tt0103064
                  u'http://www.wikidata.org/entity/Q170564',
                  # movie: tt0103064
                  u'http://www.wikidata.org/entity/Q170564',
                  # movie: tt0088763
                  u'http://www.wikidata.org/entity/Q91540',
                  # movie: tt0088763
                  u'http://www.wikidata.org/entity/Q91540',
                  # movie: tt2582802
                  u'http://www.wikidata.org/entity/Q15648198',
                  # movie: tt2582802
                  u'http://www.wikidata.org/entity/Q15648198',
                  # movie: tt0172495
                  u'http://www.wikidata.org/entity/Q128518',
                  # movie: tt0172495
                  u'http://www.wikidata.org/entity/Q128518',
                  # movie: tt0209144
                  u'http://www.wikidata.org/entity/Q190525',
                  # movie: tt0209144
                  u'http://www.wikidata.org/entity/Q190525',
                  # movie: tt0078788
                  u'http://www.wikidata.org/entity/Q182692',
                  # movie: tt0078788
                  u'http://www.wikidata.org/entity/Q182692',
                  # movie: tt0482571
                  u'http://www.wikidata.org/entity/Q46551',
                  # movie: tt0482571
                  u'http://www.wikidata.org/entity/Q46551',
                  # movie: tt0110357
                  u'http://www.wikidata.org/entity/Q36479',
                  # movie: tt0110357
                  u'http://www.wikidata.org/entity/Q36479',
                  # movie: tt0078748
                  u'http://www.wikidata.org/entity/Q103569',
                  # movie: tt0078748
                  u'http://www.wikidata.org/entity/Q103569',
                  # movie: tt3315342
                  u'http://www.wikidata.org/entity/Q24053263',
                  # movie: tt3315342
                  u'http://www.wikidata.org/entity/Q24053263',
                  # movie: tt0057012
                  u'http://www.wikidata.org/entity/Q105702',
                  # movie: tt0057012
                  u'http://www.wikidata.org/entity/Q105702',
                  # movie: tt0043014
                  u'http://www.wikidata.org/entity/Q193570',
                  # movie: tt0043014
                  u'http://www.wikidata.org/entity/Q193570',
                  # movie: tt0032553
                  u'http://www.wikidata.org/entity/Q109116',
                  # movie: tt0032553
                  u'http://www.wikidata.org/entity/Q109116',
                  # movie: tt0095765
                  u'http://www.wikidata.org/entity/Q464032',
                  # movie: tt0095765
                  u'http://www.wikidata.org/entity/Q464032',
                  # movie: tt0405094
                  u'http://www.wikidata.org/entity/Q153882',
                  # movie: tt0405094
                  u'http://www.wikidata.org/entity/Q153882',
                  # movie: tt0095327
                  u'http://www.wikidata.org/entity/Q274520',
                  # movie: tt0095327
                  u'http://www.wikidata.org/entity/Q274520',
                  # movie: tt0050825
                  u'http://www.wikidata.org/entity/Q747936',
                  # movie: tt0050825
                  u'http://www.wikidata.org/entity/Q747936',
                  # movie: tt1853728
                  u'http://www.wikidata.org/entity/Q571032',
                  # movie: tt1853728
                  u'http://www.wikidata.org/entity/Q571032',
                  # movie: tt0081505
                  u'http://www.wikidata.org/entity/Q186341',
                  # movie: tt0081505
                  u'http://www.wikidata.org/entity/Q186341',
                  # movie: tt0910970
                  u'http://www.wikidata.org/entity/Q104905',
                  # movie: tt0910970
                  u'http://www.wikidata.org/entity/Q104905',
                  # movie: tt0169547
                  u'http://www.wikidata.org/entity/Q25139',
                  # movie: tt0169547
                  u'http://www.wikidata.org/entity/Q25139',
                  # movie: tt1345836
                  u'http://www.wikidata.org/entity/Q189330',
                  # movie: tt1345836
                  u'http://www.wikidata.org/entity/Q189330',
                  # movie: tt0119698
                  u'http://www.wikidata.org/entity/Q186572',
                  # movie: tt0119698
                  u'http://www.wikidata.org/entity/Q186572',
                  # movie: tt0090605
                  u'http://www.wikidata.org/entity/Q104814',
                  # movie: tt0090605
                  u'http://www.wikidata.org/entity/Q104814',
                  # movie: tt0364569
                  u'http://www.wikidata.org/entity/Q475693',
                  # movie: tt0364569
                  u'http://www.wikidata.org/entity/Q475693',
                  # movie: tt0087843
                  u'http://www.wikidata.org/entity/Q206388',
                  # movie: tt0087843
                  u'http://www.wikidata.org/entity/Q206388',
                  # movie: tt3783958
                  u'http://www.wikidata.org/entity/Q20856802',
                  # movie: tt3783958
                  u'http://www.wikidata.org/entity/Q20856802',
                  # movie: tt0051201
                  u'http://www.wikidata.org/entity/Q196977',
                  # movie: tt0051201
                  u'http://www.wikidata.org/entity/Q196977',
                  # movie: tt0082096
                  u'http://www.wikidata.org/entity/Q62730',
                  # movie: tt0082096
                  u'http://www.wikidata.org/entity/Q62730',
                  # movie: tt0033467
                  u'http://www.wikidata.org/entity/Q24815',
                  # movie: tt0033467
                  u'http://www.wikidata.org/entity/Q24815',
                  # movie: tt0053125
                  u'http://www.wikidata.org/entity/Q223139',
                  # movie: tt0053125
                  u'http://www.wikidata.org/entity/Q223139',
                  # movie: tt0052357
                  u'http://www.wikidata.org/entity/Q202548',
                  # movie: tt0052357
                  u'http://www.wikidata.org/entity/Q202548',
                  # movie: tt0086190
                  u'http://www.wikidata.org/entity/Q181803',
                  # movie: tt0086190
                  u'http://www.wikidata.org/entity/Q181803',
                  # movie: tt0105236
                  u'http://www.wikidata.org/entity/Q72962',
                  # movie: tt0105236
                  u'http://www.wikidata.org/entity/Q72962',
                  # movie: tt0112573
                  u'http://www.wikidata.org/entity/Q162729',
                  # movie: tt0112573
                  u'http://www.wikidata.org/entity/Q162729',
                  # movie: tt0022100
                  u'http://www.wikidata.org/entity/Q127021',
                  # movie: tt0022100
                  u'http://www.wikidata.org/entity/Q127021',
                  # movie: tt0180093
                  u'http://www.wikidata.org/entity/Q487181',
                  # movie: tt0180093
                  u'http://www.wikidata.org/entity/Q487181',
                  # movie: tt0211915
                  u'http://www.wikidata.org/entity/Q484048',
                  # movie: tt0211915
                  u'http://www.wikidata.org/entity/Q484048',
                  # movie: tt0066921
                  u'http://www.wikidata.org/entity/Q181086',
                  # movie: tt0066921
                  u'http://www.wikidata.org/entity/Q181086',
                  # movie: tt0986264
                  u'http://www.wikidata.org/entity/Q1043614',
                  # movie: tt0986264
                  u'http://www.wikidata.org/entity/Q1043614',
                  # movie: tt0075314
                  u'http://www.wikidata.org/entity/Q47221',
                  # movie: tt0075314
                  u'http://www.wikidata.org/entity/Q47221',
                  # movie: tt0056172
                  u'http://www.wikidata.org/entity/Q228186',
                  # movie: tt0056172
                  u'http://www.wikidata.org/entity/Q228186',
                  # movie: tt0036775
                  u'http://www.wikidata.org/entity/Q478209',
                  # movie: tt0036775
                  u'http://www.wikidata.org/entity/Q478209',
                  # movie: tt0338013
                  u'http://www.wikidata.org/entity/Q208269',
                  # movie: tt0338013
                  u'http://www.wikidata.org/entity/Q208269',
                  # movie: tt0056592
                  u'http://www.wikidata.org/entity/Q177922',
                  # movie: tt0056592
                  u'http://www.wikidata.org/entity/Q177922',
                  # movie: tt0086879
                  u'http://www.wikidata.org/entity/Q190956',
                  # movie: tt0086879
                  u'http://www.wikidata.org/entity/Q190956',
                  # movie: tt0435761
                  u'http://www.wikidata.org/entity/Q187278',
                  # movie: tt0435761
                  u'http://www.wikidata.org/entity/Q187278',
                  # movie: tt0093058
                  u'http://www.wikidata.org/entity/Q243439',
                  # movie: tt0093058
                  u'http://www.wikidata.org/entity/Q243439',
                  # movie: tt5074352
                  u'http://www.wikidata.org/entity/Q20762668',
                  # movie: tt5074352
                  u'http://www.wikidata.org/entity/Q20762668',
                  # movie: tt0070735
                  u'http://www.wikidata.org/entity/Q62665',
                  # movie: tt0070735
                  u'http://www.wikidata.org/entity/Q62665',
                  # movie: tt0062622
                  u'http://www.wikidata.org/entity/Q103474',
                  # movie: tt0062622
                  u'http://www.wikidata.org/entity/Q103474',
                  # movie: tt0045152
                  u'http://www.wikidata.org/entity/Q309153',
                  # movie: tt0045152
                  u'http://www.wikidata.org/entity/Q309153',
                  # movie: tt0114709
                  u'http://www.wikidata.org/entity/Q171048',
                  # movie: tt0114709
                  u'http://www.wikidata.org/entity/Q171048',
                  # movie: tt0040522
                  u'http://www.wikidata.org/entity/Q172837',
                  # movie: tt0040522
                  u'http://www.wikidata.org/entity/Q172837',
                  # movie: tt0476735
                  u'http://www.wikidata.org/entity/Q797577',
                  # movie: tt0476735
                  u'http://www.wikidata.org/entity/Q797577',
                  # movie: tt0012349
                  u'http://www.wikidata.org/entity/Q374172',
                  # movie: tt0012349
                  u'http://www.wikidata.org/entity/Q374172',
                  # movie: tt0361748
                  u'http://www.wikidata.org/entity/Q153723',
                  # movie: tt0361748
                  u'http://www.wikidata.org/entity/Q153723',
                  # movie: tt0208092
                  u'http://www.wikidata.org/entity/Q335160',
                  # movie: tt0208092
                  u'http://www.wikidata.org/entity/Q335160',
                  # movie: tt0071853
                  u'http://www.wikidata.org/entity/Q25043',
                  # movie: tt0071853
                  u'http://www.wikidata.org/entity/Q25043',
                  # movie: tt1187043
                  u'http://www.wikidata.org/entity/Q229633',
                  # movie: tt1187043
                  u'http://www.wikidata.org/entity/Q229633',
                  # movie: tt0119488
                  u'http://www.wikidata.org/entity/Q339876',
                  # movie: tt0119488
                  u'http://www.wikidata.org/entity/Q339876',
                  # movie: tt0059578
                  u'http://www.wikidata.org/entity/Q153677',
                  # movie: tt0059578
                  u'http://www.wikidata.org/entity/Q153677',
                  # movie: tt0086250
                  u'http://www.wikidata.org/entity/Q47075',
                  # movie: tt0086250
                  u'http://www.wikidata.org/entity/Q47075',
                  # movie: tt2106476
                  u'http://www.wikidata.org/entity/Q32303',
                  # movie: tt2106476
                  u'http://www.wikidata.org/entity/Q32303',
                  # movie: tt0053604
                  u'http://www.wikidata.org/entity/Q270510',
                  # movie: tt0053604
                  u'http://www.wikidata.org/entity/Q270510',
                  # movie: tt0119217
                  u'http://www.wikidata.org/entity/Q193835',
                  # movie: tt0119217
                  u'http://www.wikidata.org/entity/Q193835',
                  # movie: tt0042876
                  u'http://www.wikidata.org/entity/Q135465',
                  # movie: tt0042876
                  u'http://www.wikidata.org/entity/Q135465',
                  # movie: tt1832382
                  u'http://www.wikidata.org/entity/Q640561',
                  # movie: tt1832382
                  u'http://www.wikidata.org/entity/Q640561',
                  # movie: tt0097576
                  u'http://www.wikidata.org/entity/Q185658',
                  # movie: tt0097576
                  u'http://www.wikidata.org/entity/Q185658',
                  # movie: tt0017136
                  u'http://www.wikidata.org/entity/Q151599',
                  # movie: tt0017136
                  u'http://www.wikidata.org/entity/Q151599',
                  # movie: tt0042192
                  u'http://www.wikidata.org/entity/Q200299',
                  # movie: tt0042192
                  u'http://www.wikidata.org/entity/Q200299',
                  # movie: tt0055630
                  u'http://www.wikidata.org/entity/Q20475',
                  # movie: tt0055630
                  u'http://www.wikidata.org/entity/Q20475',
                  # movie: tt0372784
                  u'http://www.wikidata.org/entity/Q166262',
                  # movie: tt0372784
                  u'http://www.wikidata.org/entity/Q166262',
                  # movie: tt1049413
                  u'http://www.wikidata.org/entity/Q174811',
                  # movie: tt1049413
                  u'http://www.wikidata.org/entity/Q174811',
                  # movie: tt0053291
                  u'http://www.wikidata.org/entity/Q190086',
                  # movie: tt0053291
                  u'http://www.wikidata.org/entity/Q190086',
                  # movie: tt0040897
                  u'http://www.wikidata.org/entity/Q251559',
                  # movie: tt0040897
                  u'http://www.wikidata.org/entity/Q251559',
                  # movie: tt0105695
                  u'http://www.wikidata.org/entity/Q104137',
                  # movie: tt0105695
                  u'http://www.wikidata.org/entity/Q104137',
                  # movie: tt0363163
                  u'http://www.wikidata.org/entity/Q152857',
                  # movie: tt0363163
                  u'http://www.wikidata.org/entity/Q152857',
                  # movie: tt0081398
                  u'http://www.wikidata.org/entity/Q220780',
                  # movie: tt0081398
                  u'http://www.wikidata.org/entity/Q220780',
                  # movie: tt0095016
                  u'http://www.wikidata.org/entity/Q105598',
                  # movie: tt0095016
                  u'http://www.wikidata.org/entity/Q105598',
                  # movie: tt0041959
                  u'http://www.wikidata.org/entity/Q271830',
                  # movie: tt0041959
                  u'http://www.wikidata.org/entity/Q271830',
                  # movie: tt0118849
                  u'http://www.wikidata.org/entity/Q339804',
                  # movie: tt0118849
                  u'http://www.wikidata.org/entity/Q339804',
                  # movie: tt0113277
                  u'http://www.wikidata.org/entity/Q42198',
                  # movie: tt0113277
                  u'http://www.wikidata.org/entity/Q42198',
                  # movie: tt0057115
                  u'http://www.wikidata.org/entity/Q110354',
                  # movie: tt0057115
                  u'http://www.wikidata.org/entity/Q110354',
                  # movie: tt0071315
                  u'http://www.wikidata.org/entity/Q644987',
                  # movie: tt0071315
                  u'http://www.wikidata.org/entity/Q644987',
                  # movie: tt0457430
                  u'http://www.wikidata.org/entity/Q216006',
                  # movie: tt0457430
                  u'http://www.wikidata.org/entity/Q216006',
                  # movie: tt0044741
                  u'http://www.wikidata.org/entity/Q152105',
                  # movie: tt0044741
                  u'http://www.wikidata.org/entity/Q152105',
                  # movie: tt0060107
                  u'http://www.wikidata.org/entity/Q503046',
                  # movie: tt0060107
                  u'http://www.wikidata.org/entity/Q503046',
                  # movie: tt2096673
                  u'http://www.wikidata.org/entity/Q6144664',
                  # movie: tt2096673
                  u'http://www.wikidata.org/entity/Q6144664',
                  # movie: tt0096283
                  u'http://www.wikidata.org/entity/Q39571',
                  # movie: tt0096283
                  u'http://www.wikidata.org/entity/Q39571',
                  # movie: tt0089881
                  u'http://www.wikidata.org/entity/Q565231',
                  # movie: tt0089881
                  u'http://www.wikidata.org/entity/Q565231',
                  # movie: tt0047296
                  u'http://www.wikidata.org/entity/Q211372',
                  # movie: tt0047296
                  u'http://www.wikidata.org/entity/Q211372',
                  # movie: tt3170832
                  u'http://www.wikidata.org/entity/Q18703032',
                  # movie: tt3170832
                  u'http://www.wikidata.org/entity/Q18703032',
                  # movie: tt0015864
                  u'http://www.wikidata.org/entity/Q214723',
                  # movie: tt0015864
                  u'http://www.wikidata.org/entity/Q214723',
                  # movie: tt1305806
                  u'http://www.wikidata.org/entity/Q748851',
                  # movie: tt1305806
                  u'http://www.wikidata.org/entity/Q748851',
                  # movie: tt0050212
                  u'http://www.wikidata.org/entity/Q188718',
                  # movie: tt0050212
                  u'http://www.wikidata.org/entity/Q188718',
                  # movie: tt0083658
                  u'http://www.wikidata.org/entity/Q184843',
                  # movie: tt0083658
                  u'http://www.wikidata.org/entity/Q184843',
                  # movie: tt0347149
                  u'http://www.wikidata.org/entity/Q29011',
                  # movie: tt0347149
                  u'http://www.wikidata.org/entity/Q29011',
                  # movie: tt0031679
                  u'http://www.wikidata.org/entity/Q866120',
                  # movie: tt0031679
                  u'http://www.wikidata.org/entity/Q866120',
                  # movie: tt0050976
                  u'http://www.wikidata.org/entity/Q217189',
                  # movie: tt0050976
                  u'http://www.wikidata.org/entity/Q217189',
                  # movie: tt0120735
                  u'http://www.wikidata.org/entity/Q851095',
                  # movie: tt0120735
                  u'http://www.wikidata.org/entity/Q851095',
                  # movie: tt1255953
                  u'http://www.wikidata.org/entity/Q1212650',
                  # movie: tt1255953
                  u'http://www.wikidata.org/entity/Q1212650',
                  # movie: tt0055031
                  u'http://www.wikidata.org/entity/Q309545',
                  # movie: tt0055031
                  u'http://www.wikidata.org/entity/Q309545',
                  # movie: tt0112641
                  u'http://www.wikidata.org/entity/Q220910',
                  # movie: tt0112641
                  u'http://www.wikidata.org/entity/Q220910',
                  # movie: tt0268978
                  u'http://www.wikidata.org/entity/Q164103',
                  # movie: tt0268978
                  u'http://www.wikidata.org/entity/Q164103',
                  # movie: tt2119532
                  u'http://www.wikidata.org/entity/Q21010856',
                  # movie: tt2119532
                  u'http://www.wikidata.org/entity/Q21010856',
                  # movie: tt0080678
                  u'http://www.wikidata.org/entity/Q272860',
                  # movie: tt0080678
                  u'http://www.wikidata.org/entity/Q272860',
                  # movie: tt0050986
                  u'http://www.wikidata.org/entity/Q239756',
                  # movie: tt0050986
                  u'http://www.wikidata.org/entity/Q239756',
                  # movie: tt0116231
                  u'http://www.wikidata.org/entity/Q635848',
                  # movie: tt0116231
                  u'http://www.wikidata.org/entity/Q635848',
                  # movie: tt0434409
                  u'http://www.wikidata.org/entity/Q5890',
                  # movie: tt0434409
                  u'http://www.wikidata.org/entity/Q5890',
                  # movie: tt0993846
                  u'http://www.wikidata.org/entity/Q1392744',
                  # movie: tt0993846
                  u'http://www.wikidata.org/entity/Q1392744',
                  # movie: tt0017925
                  u'http://www.wikidata.org/entity/Q850159',
                  # movie: tt0017925
                  u'http://www.wikidata.org/entity/Q850159',
                  # movie: tt1291584
                  u'http://www.wikidata.org/entity/Q1415964',
                  # movie: tt1291584
                  u'http://www.wikidata.org/entity/Q1415964',
                  # movie: tt0018455
                  u'http://www.wikidata.org/entity/Q431093',
                  # movie: tt0018455
                  u'http://www.wikidata.org/entity/Q431093',
                  # movie: tt1280558
                  u'http://www.wikidata.org/entity/Q2151097',
                  # movie: tt1280558
                  u'http://www.wikidata.org/entity/Q2151097',
                  # movie: tt0117951
                  u'http://www.wikidata.org/entity/Q109135',
                  # movie: tt0117951
                  u'http://www.wikidata.org/entity/Q109135',
                  # movie: tt1205489
                  u'http://www.wikidata.org/entity/Q126699',
                  # movie: tt1205489
                  u'http://www.wikidata.org/entity/Q126699',
                  # movie: tt0046912
                  u'http://www.wikidata.org/entity/Q496255',
                  # movie: tt0046912
                  u'http://www.wikidata.org/entity/Q496255',
                  # movie: tt0118715
                  u'http://www.wikidata.org/entity/Q337078',
                  # movie: tt0118715
                  u'http://www.wikidata.org/entity/Q337078',
                  # movie: tt0077416
                  u'http://www.wikidata.org/entity/Q201674',
                  # movie: tt0077416
                  u'http://www.wikidata.org/entity/Q201674',
                  # movie: tt0405508
                  u'http://www.wikidata.org/entity/Q924135',
                  # movie: tt0405508
                  u'http://www.wikidata.org/entity/Q924135',
                  # movie: tt0019254
                  u'http://www.wikidata.org/entity/Q51520',
                  # movie: tt0019254
                  u'http://www.wikidata.org/entity/Q51520',
                  # movie: tt0116282
                  u'http://www.wikidata.org/entity/Q222720',
                  # movie: tt0116282
                  u'http://www.wikidata.org/entity/Q222720',
                  # movie: tt0031381
                  u'http://www.wikidata.org/entity/Q2875',
                  # movie: tt0031381
                  u'http://www.wikidata.org/entity/Q2875',
                  # movie: tt0046438
                  u'http://www.wikidata.org/entity/Q26060',
                  # movie: tt0046438
                  u'http://www.wikidata.org/entity/Q26060',
                  # movie: tt0266543
                  u'http://www.wikidata.org/entity/Q132863',
                  # movie: tt0266543
                  u'http://www.wikidata.org/entity/Q132863',
                  # movie: tt0167404
                  u'http://www.wikidata.org/entity/Q183063',
                  # movie: tt0167404
                  u'http://www.wikidata.org/entity/Q183063',
                  # movie: tt0084787
                  u'http://www.wikidata.org/entity/Q210756',
                  # movie: tt0084787
                  u'http://www.wikidata.org/entity/Q210756',
                  # movie: tt0477348
                  u'http://www.wikidata.org/entity/Q183081',
                  # movie: tt0477348
                  u'http://www.wikidata.org/entity/Q183081',
                  # movie: tt0061512
                  u'http://www.wikidata.org/entity/Q684150',
                  # movie: tt0061512
                  u'http://www.wikidata.org/entity/Q684150',
                  # movie: tt0032976
                  u'http://www.wikidata.org/entity/Q204212',
                  # movie: tt0032976
                  u'http://www.wikidata.org/entity/Q204212',
                  # movie: tt0892769
                  u'http://www.wikidata.org/entity/Q373096',
                  # movie: tt0892769
                  u'http://www.wikidata.org/entity/Q373096',
                  # movie: tt0266697
                  u'http://www.wikidata.org/entity/Q165325',
                  # movie: tt0266697
                  u'http://www.wikidata.org/entity/Q165325',
                  # movie: tt0469494
                  u'http://www.wikidata.org/entity/Q244315',
                  # movie: tt0469494
                  u'http://www.wikidata.org/entity/Q244315',
                  # movie: tt0758758
                  u'http://www.wikidata.org/entity/Q269912',
                  # movie: tt0758758
                  u'http://www.wikidata.org/entity/Q269912',
                  # movie: tt0978762
                  u'http://www.wikidata.org/entity/Q1128756',
                  # movie: tt0978762
                  u'http://www.wikidata.org/entity/Q1128756',
                  # movie: tt2267998
                  u'http://www.wikidata.org/entity/Q14920425',
                  # movie: tt2267998
                  u'http://www.wikidata.org/entity/Q14920425',
                  # movie: tt0091251
                  u'http://www.wikidata.org/entity/Q1130395',
                  # movie: tt0091251
                  u'http://www.wikidata.org/entity/Q1130395',
                  # movie: tt0079470
                  u'http://www.wikidata.org/entity/Q24953',
                  # movie: tt0079470
                  u'http://www.wikidata.org/entity/Q24953',
                  # movie: tt0025316
                  u'http://www.wikidata.org/entity/Q208632',
                  # movie: tt0025316
                  u'http://www.wikidata.org/entity/Q208632',
                  # movie: tt0374887
                  u'http://www.wikidata.org/entity/Q262778',
                  # movie: tt0374887
                  u'http://www.wikidata.org/entity/Q262778',
                  # movie: tt1130884
                  u'http://www.wikidata.org/entity/Q210364',
                  # movie: tt1130884
                  u'http://www.wikidata.org/entity/Q210364',
                  # movie: tt0091763
                  u'http://www.wikidata.org/entity/Q190643',
                  # movie: tt0091763
                  u'http://www.wikidata.org/entity/Q190643',
                  # movie: tt0395169
                  u'http://www.wikidata.org/entity/Q223884',
                  # movie: tt0395169
                  u'http://www.wikidata.org/entity/Q223884',
                  # movie: tt1979320
                  u'http://www.wikidata.org/entity/Q1768437',
                  # movie: tt1979320
                  u'http://www.wikidata.org/entity/Q1768437',
                  # movie: tt0074958
                  u'http://www.wikidata.org/entity/Q572165',
                  # movie: tt0074958
                  u'http://www.wikidata.org/entity/Q572165',
                  # movie: tt0073707
                  u'http://www.wikidata.org/entity/Q949228',
                  # movie: tt0073707
                  u'http://www.wikidata.org/entity/Q949228',
                  # movie: tt3011894
                  u'http://www.wikidata.org/entity/Q16672466',
                  # movie: tt3011894
                  u'http://www.wikidata.org/entity/Q16672466',
                  # movie: tt0046268
                  u'http://www.wikidata.org/entity/Q465773',
                  # movie: tt0046268
                  u'http://www.wikidata.org/entity/Q465773',
                  # movie: tt0242519
                  u'http://www.wikidata.org/entity/Q5732486',
                  # movie: tt0242519
                  u'http://www.wikidata.org/entity/Q5732486',
                  # movie: tt0092005
                  u'http://www.wikidata.org/entity/Q494722',
                  # movie: tt0092005
                  u'http://www.wikidata.org/entity/Q494722',
                  # movie: tt0107207
                  u'http://www.wikidata.org/entity/Q304074',
                  # movie: tt0107207
                  u'http://www.wikidata.org/entity/Q304074',
                  # movie: tt1895587
                  u'http://www.wikidata.org/entity/Q18154496',
                  # movie: tt1895587
                  u'http://www.wikidata.org/entity/Q18154496',
                  # movie: tt0053198
                  u'http://www.wikidata.org/entity/Q162331',
                  # movie: tt0053198
                  u'http://www.wikidata.org/entity/Q162331',
                  # movie: tt1392190
                  u'http://www.wikidata.org/entity/Q1757288',
                  # movie: tt1392190
                  u'http://www.wikidata.org/entity/Q1757288',
                  # movie: tt2024544
                  u'http://www.wikidata.org/entity/Q3023357',
                  # movie: tt2024544
                  u'http://www.wikidata.org/entity/Q3023357',
                  # movie: tt0064115
                  u'http://www.wikidata.org/entity/Q232000',
                  # movie: tt0064115
                  u'http://www.wikidata.org/entity/Q232000',
                  # movie: tt2278388
                  u'http://www.wikidata.org/entity/Q3521099',
                  # movie: tt2278388
                  u'http://www.wikidata.org/entity/Q3521099',
                  # movie: tt0052618
                  u'http://www.wikidata.org/entity/Q180098',
                  # movie: tt0052618
                  u'http://www.wikidata.org/entity/Q180098',
                  # movie: tt0405159
                  u'http://www.wikidata.org/entity/Q184255',
                  # movie: tt0405159
                  u'http://www.wikidata.org/entity/Q184255',
                  # movie: tt0060827
                  u'http://www.wikidata.org/entity/Q695255',
                  # movie: tt0060827
                  u'http://www.wikidata.org/entity/Q695255',
                  # movie: tt0033870
                  u'http://www.wikidata.org/entity/Q221462',
                  # movie: tt0033870
                  u'http://www.wikidata.org/entity/Q221462',
                  # movie: tt0245712
                  u'http://www.wikidata.org/entity/Q474098',
                  # movie: tt0245712
                  u'http://www.wikidata.org/entity/Q474098',
                  # movie: tt2488496
                  u'http://www.wikidata.org/entity/Q6074',
                  # movie: tt2488496
                  u'http://www.wikidata.org/entity/Q6074',
                  # movie: tt0050783
                  u'http://www.wikidata.org/entity/Q18405',
                  # movie: tt0050783
                  u'http://www.wikidata.org/entity/Q18405',
                  # movie: tt0109117
                  u'http://www.wikidata.org/entity/Q283481',
                  # movie: tt0109117
                  u'http://www.wikidata.org/entity/Q283481',
                  # movie: tt0107290
                  u'http://www.wikidata.org/entity/Q167726',
                  # movie: tt0107290
                  u'http://www.wikidata.org/entity/Q167726',
                  # movie: tt0093779
                  u'http://www.wikidata.org/entity/Q506418',
                  # movie: tt0093779
                  u'http://www.wikidata.org/entity/Q506418',
                  # movie: tt0353969
                  u'http://www.wikidata.org/entity/Q488169',
                  # movie: tt0353969
                  u'http://www.wikidata.org/entity/Q488169',
                  # movie: tt1028532
                  u'http://www.wikidata.org/entity/Q59249',
                  # movie: tt1028532
                  u'http://www.wikidata.org/entity/Q59249',
                  # movie: tt0079944
                  u'http://www.wikidata.org/entity/Q200437',
                  # movie: tt0079944
                  u'http://www.wikidata.org/entity/Q200437',
                  # movie: tt0087544
                  u'http://www.wikidata.org/entity/Q8885676',
                  # movie: tt0087544
                  u'http://www.wikidata.org/entity/Q8885676',
                  # movie: tt0120382
                  u'http://www.wikidata.org/entity/Q214801',
                  # movie: tt0120382
                  u'http://www.wikidata.org/entity/Q214801',
                  # movie: tt0112471
                  u'http://www.wikidata.org/entity/Q659609',
                  # movie: tt0112471
                  u'http://www.wikidata.org/entity/Q659609',
                  # movie: tt0032551
                  u'http://www.wikidata.org/entity/Q676039',
                  # movie: tt0032551
                  u'http://www.wikidata.org/entity/Q676039',
                  # movie: tt0052311
                  u'http://www.wikidata.org/entity/Q778161',
                  # movie: tt0052311
                  u'http://www.wikidata.org/entity/Q778161',
                  # movie: tt0075686
                  u'http://www.wikidata.org/entity/Q233464',
                  # movie: tt0075686
                  u'http://www.wikidata.org/entity/Q233464',
                  # movie: tt0075148
                  u'http://www.wikidata.org/entity/Q188652',
                  # movie: tt0075148
                  u'http://www.wikidata.org/entity/Q188652',
                  # movie: tt1201607
                  u'http://www.wikidata.org/entity/Q232009',
                  # movie: tt1201607
                  u'http://www.wikidata.org/entity/Q232009',
                  # movie: tt0083987
                  u'http://www.wikidata.org/entity/Q202211',
                  # movie: tt0083987
                  u'http://www.wikidata.org/entity/Q202211',
                  # movie: tt0246578
                  u'http://www.wikidata.org/entity/Q426828',
                  # movie: tt0246578
                  u'http://www.wikidata.org/entity/Q426828',
                  # movie: tt0046911
                  u'http://www.wikidata.org/entity/Q739046',
                  # movie: tt0046911
                  u'http://www.wikidata.org/entity/Q739046',
                  # movie: tt1392214
                  u'http://www.wikidata.org/entity/Q3404003',
                  # movie: tt1392214
                  u'http://www.wikidata.org/entity/Q3404003',
                  # movie: tt0440963
                  u'http://www.wikidata.org/entity/Q107226',
                  # movie: tt0440963
                  u'http://www.wikidata.org/entity/Q107226',
                  # movie: tt0198781
                  u'http://www.wikidata.org/entity/Q187726',
                  # movie: tt0198781
                  u'http://www.wikidata.org/entity/Q187726',
                  # movie: tt0264464
                  u'http://www.wikidata.org/entity/Q208108',
                  # movie: tt0264464
                  u'http://www.wikidata.org/entity/Q208108',
                  # movie: tt0088247
                  u'http://www.wikidata.org/entity/Q162255',
                  # movie: tt0088247
                  u'http://www.wikidata.org/entity/Q162255',
                  # movie: tt0056801
                  u'http://www.wikidata.org/entity/Q12018',
                  # movie: tt0056801
                  u'http://www.wikidata.org/entity/Q12018',
                  # movie: tt0032138
                  u'http://www.wikidata.org/entity/Q193695',
                  # movie: tt0032138
                  u'http://www.wikidata.org/entity/Q193695',
                  # movie: tt0107048
                  u'http://www.wikidata.org/entity/Q488655',
                  # movie: tt0107048
                  u'http://www.wikidata.org/entity/Q488655',
                  # movie: tt0114746
                  u'http://www.wikidata.org/entity/Q175038',
                  # movie: tt0114746
                  u'http://www.wikidata.org/entity/Q175038',
                  # movie: tt0113247
                  u'http://www.wikidata.org/entity/Q466101',
                  # movie: tt0113247
                  u'http://www.wikidata.org/entity/Q466101',
                  # movie: tt0072684
                  u'http://www.wikidata.org/entity/Q471716',
                  # movie: tt0072684
                  u'http://www.wikidata.org/entity/Q471716',
                  # movie: tt4430212
                  u'http://www.wikidata.org/entity/Q19824636',
                  # movie: tt4430212
                  u'http://www.wikidata.org/entity/Q19824636',
                  # movie: tt0073195
                  u'http://www.wikidata.org/entity/Q189505',
                  # movie: tt0073195
                  u'http://www.wikidata.org/entity/Q189505',
                  # movie: tt0338564
                  u'http://www.wikidata.org/entity/Q714057',
                  # movie: tt0338564
                  u'http://www.wikidata.org/entity/Q714057',
                  # movie: tt0074896
                  u'http://www.wikidata.org/entity/Q588464',
                  # movie: tt0074896
                  u'http://www.wikidata.org/entity/Q588464',
                  # movie: tt0036868
                  u'http://www.wikidata.org/entity/Q645094',
                  # movie: tt0036868
                  u'http://www.wikidata.org/entity/Q645094',
                  # movie: tt2948356
                  u'http://www.wikidata.org/entity/Q15270647',
                  # movie: tt2948356
                  u'http://www.wikidata.org/entity/Q15270647',
                  # movie: tt0058946
                  u'http://www.wikidata.org/entity/Q784812',
                  # movie: tt0058946
                  u'http://www.wikidata.org/entity/Q784812',
                  # movie: tt0072890
                  u'http://www.wikidata.org/entity/Q458656',
                  # movie: tt0072890
                  u'http://www.wikidata.org/entity/Q458656',
                  # movie: tt1454029
                  u'http://www.wikidata.org/entity/Q204374',
                  # movie: tt1454029
                  u'http://www.wikidata.org/entity/Q204374',
                  # movie: tt1954470
                  u'http://www.wikidata.org/entity/Q16248515',
                  # movie: tt1954470
                  u'http://www.wikidata.org/entity/Q16248515',
                  # movie: tt0044079
                  u'http://www.wikidata.org/entity/Q499639',
                  # movie: tt0044079
                  u'http://www.wikidata.org/entity/Q499639',
                  # movie: tt0325980
                  u'http://www.wikidata.org/entity/Q46717',
                  # movie: tt0325980
                  u'http://www.wikidata.org/entity/Q46717',
                  # movie: tt0169102
                  u'http://www.wikidata.org/entity/Q843949',
                  # movie: tt0169102
                  u'http://www.wikidata.org/entity/Q843949',
                  # movie: tt0056687
                  u'http://www.wikidata.org/entity/Q26644',
                  # movie: tt0056687
                  u'http://www.wikidata.org/entity/Q26644',
                  # movie: tt0401792
                  u'http://www.wikidata.org/entity/Q192115',
                  # movie: tt0401792
                  u'http://www.wikidata.org/entity/Q192115',
                ],
                [
                  [u'wdpd:Genre'],
                  [u'wdpd:BasedOn'],
                  [u'wdpd:Director'],
                  [u'wdpd:MainSubject'],
                  # [u'wdpd:ScreenWriter'],
                  # [u'wdpd:CastMember'],
                ]
              ),
            ]

