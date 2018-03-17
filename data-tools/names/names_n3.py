#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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



