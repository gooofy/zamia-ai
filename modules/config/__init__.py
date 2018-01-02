#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from xsbprolog import xsb_hl_query

DEPENDS     = [ 'data' ]

PL_SOURCES  = [
               'config'
              ]

def get_data(kernal):

    #
    # name / self address utils
    #
    
    # macro(en, my_forename, W) :- forename (self, en, W).
    # macro(de, my_forename, W) :- forename (self, de, W).
  
    for soln in xsb_hl_query('forename', ['self', 'L', 'W']):
        kernal.dte.macro(soln['L'], 'my_forename', soln)
 
    # macro(en, self_address, L) :- forename (self, en, L), str_append(L, ', ').
    # macro(en, self_address, L) :- L is "".
    # macro(de, self_address, L) :- forename (self, de, L), str_append(L, ', ').
    # macro(de, self_address, L) :- L is "".
    
    for soln in xsb_hl_query('forename', ['self', 'L', 'W']):
        kernal.dte.macro(soln['L'], 'self_address', {'W': soln['W'] + ', '})
    kernal.dte.macro('en', 'self_address', {'W': ''})
    kernal.dte.macro('de', 'self_address', {'W': ''})

