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
#
# generate n3 of given names
#

import codecs

from nltools import misc

misc.init_app ('gen_names')

def mangle_name(name):

    res = u''
    for c in name:
        if c.isalpha():
            res += c

    return res

with codecs.open('old/names/head.n3', 'r', 'utf8') as f:
    for line in f:
        print line.strip()

print

with codecs.open('old/names/german-female.txt', 'r', 'utf8') as f:

    for line in f:

        parts = line.split(' ')
        name = parts[0]

        print u'hal:FemaleGivenName%s   rdfs:label "%s"@en;' % (mangle_name(name), name)
        print u'                        rdfs:label "%s"@de;' % name
        print u'                        wdpd:P31       wde:Q11879590; # instanceof femaleGivenName'
        print u'                        wdpd:P21       wde:Q6581072 . # gender female'

        print


with codecs.open('old/names/german-male.txt', 'r', 'utf8') as f:

    for line in f:

        parts = line.split(' ')
        name = parts[0]

        print u'hal:MaleGivenName%s     rdfs:label "%s"@en;' % (mangle_name(name), name)
        print u'                        rdfs:label "%s"@de;' % name
        print u'                        wdpd:P31       wde:Q12308941; # instanceof maleGivenName'
        print u'                        wdpd:P21       wde:Q6581097 . # gender male'
# modules/base/__init__.py:                u'wde:Female'                     : u'http://www.wikidata.org/entity/Q6581072',
# modules/base/__init__.py:                u'wde:Male'                       : u'http://www.wikidata.org/entity/Q6581097',

        print



