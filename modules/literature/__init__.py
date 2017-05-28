#!/usr/bin/env python
# -*- coding: utf-8 -*- 

DEPENDS    = [ 'base', 'humans' ]

PL_SOURCES = [
              'literature.pl'
             ]

# FIXME: this needs lots of work / expansion

RDF_ALIASES = {
                u'wde:Novel2001ASpaceOdyssey'     : u'http://www.wikidata.org/entity/Q835341',
                u'wde:NovelNeuromancer'           : u'http://www.wikidata.org/entity/Q662029',
                u'wde:NovelTheStand'              : u'http://www.wikidata.org/entity/Q149552',
              }

KB_SOURCES = [

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
            ]

