#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import rdflib

DEPENDS    = [ 'base', 'config', 'humans' ]

PL_SOURCES = [
              'tech.pl',
             ]

RDF_ALIASES = {
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

KB_SOURCES = [

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
            ]

