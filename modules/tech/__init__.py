#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import rdflib

DEPENDS    = [ 'base', 'config' ]

PL_SOURCES = [
              'tech.pl',
             ]

KB_SOURCES = [

              # programming languages

              (
                [ 
                  ('wdpd:InstanceOf', 'wde:ProgrammingLanguage'),
                ],
                [
                  [], 
                ]
              ),

              # home computers
              (
                [ 
                  ('wdpd:InstanceOf', 'wde:HomeComputer'),
                ],
                [
                  ['wdpd:Manufacturer'], 
                ]
              ),
            ]

