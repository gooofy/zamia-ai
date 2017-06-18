#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import rdflib

from copy               import deepcopy

from nltools.tokenizer  import tokenize
from zamiaprolog.parser import NAME_CHARS
from zamiaprolog.logic  import Predicate, StringLiteral, ListLiteral
from ner                import builtin_ner_learn, builtin_ner

DEPENDS    = [ 'config' ]

PL_SOURCES = [
              'base.pl',
              'conversation.pl',
              'geo.pl',
              'math.pl',
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


KB_SOURCES = [

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

              'tz.n3',
            ]

def builtin_says(g, pe):

    """ says ( +Lang, ?List, +Str ) """

    pe._trace ('CALLED BUILTIN says', g)

    pred = g.terms[g.inx]
    args = pred.args

    if len(args) != 3:
        raise PrologRuntimeError('says: 3 args ( +Lang, ?List, +Str ) expected.', g.location)

    arg_Lang  = pe.prolog_get_constant(args[0], g.env, g.location)
    arg_List  = pe.prolog_get_variable(args[1], g.env, g.location)
    arg_Str   = pe.prolog_get_string(args[2], g.env, g.location)

    parts1 = arg_Str.split('%')
    cnt = 0

    l = []

    for p1 in parts1:

        o = 0

        if cnt > 0:
           
            o += 2

            while p1[o] != ')':
                o += 1

            var_name = p1[1:o]
            o += 1

            format_char = p1[o]
            l.append(Predicate('sayv', [ Predicate(arg_Lang), Predicate(var_name), Predicate(format_char) ]))

            o += 1

        parts2 = tokenize(p1[o:], lang=arg_Lang, keep_punctuation=True)

        for p2 in parts2:
            l.append(Predicate('say', [ Predicate(arg_Lang), StringLiteral(p2) ]))

        cnt += 1
    
    # if len(parts1)>2:
    #     import pdb; pdb.set_trace()

    if not arg_List in g.env:
        g.env[arg_List] = ListLiteral(l)
    else:
        l2 = deepcopy(g.env[arg_List].l)
        l2.extend(l)
        g.env[arg_List] = ListLiteral(l2)

    return True

def init_module(rt):

    rt.register_builtin ('ner_learn',    builtin_ner_learn)
    rt.register_builtin ('ner',          builtin_ner)
    rt.register_builtin ('says',         builtin_says)

