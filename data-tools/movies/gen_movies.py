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
# look up IMDB top movies in wikidata
#

import sys
import codecs
import re
import requests
import urllib2
import urllib
from bs4 import BeautifulSoup

from nltools import misc

misc.init_app ('gen_movies')

WD_ENDPOINT = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?'

def remote_sparql(query, response_format='application/sparql-results+json'):

    url = WD_ENDPOINT + urllib.urlencode({'query': query})

    # print url

    response = requests.get(
      url,
      headers = {"accept": response_format},
    )
    return response

def lookup_movie(tt):

    query = """
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>
            SELECT DISTINCT ?movie ?imdb
            WHERE
            {
              ?movie wdt:P345 "%s". 
            }""" % tt

    res = remote_sparql(query)

    # print res, res.status_code, res.headers, res.text, res.json()

    if res.status_code == 200:

        data = res.json()

        movie = data[u'results'][u'bindings'][0][u'movie'][u'value']

        print "                  u'%s'," % movie


# lookup_movie("tt2096673")

request = urllib2.Request('http://www.imdb.com/chart/top')
opener = urllib2.build_opener()
html_doc = opener.open(request).read() 

# print html_doc

soup = BeautifulSoup(html_doc, 'html.parser')

#print(soup.prettify())

for link in soup.find_all('a'):

    href = link.get('href')

    if not href:
        continue

    # print href

    m = re.match(r"^/title/(tt\d+)/", href)
    if not m: 
        continue

    print "                  # movie: %s" % m.group(1)

    lookup_movie(m.group(1))

    # m = re.match(r"^http://www.onvista.de/index/([a-zA-Z0-9\-]+)$", href)
    # if not m:
    #     continue

sys.exit(0)

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



