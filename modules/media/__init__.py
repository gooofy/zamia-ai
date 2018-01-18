#!/usr/bin/env python
# -*- coding: utf-8 -*- 

DEPENDS    = [ 'base', 'config', 'dialog' ]

PL_SOURCES = [
               'slots.pl',
             ]

import media

def get_data(k):
    media.get_data(k)


