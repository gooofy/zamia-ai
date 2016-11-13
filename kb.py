#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016 Guenter Bartsch
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
# HAL's central, semantic web based knowledge base
#
# current implementation: virtuoso universal server hosted mirror of DBPedia + extensions
#

import sys
import re
import os
import codecs
import json
from time import time

import requests
from requests.auth import HTTPDigestAuth

import utils
import model

#
# common prefixes we use in our queries
#

COMMON_PREFIXES = {
            'rdf':     'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs':    'http://www.w3.org/2000/01/rdf-schema#',
            'weather': 'http://hal.zamia.org/weather/',
            'dbo':     'http://dbpedia.org/ontology/',
            'dbr':     'http://dbpedia.org/resource/',
            'dbp':     'http://dbpedia.org/property/',
            'xml':     'http://www.w3.org/XML/1998/namespace',
            'xsd':     'http://www.w3.org/2001/XMLSchema#',
    }

class HALKB(object):

    def __init__(self):

        #
        # get config
        #

        self.endpoint      = model.config.get("kb", "endpoint")
        user               = model.config.get("kb", "user")
        passwd             = model.config.get("kb", "passwd")
      
        #
        # prepare our lightweight sparql wrapper
        #

        self.query_prefixes = ''.join(map(lambda k: "PREFIX %s: <%s>\n" % (k, COMMON_PREFIXES[k]), COMMON_PREFIXES))
        self.auth           = HTTPDigestAuth(user, passwd)

    def sparql(self, query):

        query  = self.query_prefixes + query
        # print query

        response = requests.post(
          self.endpoint,
          # data    = '',
          params  = {'query': query},
          headers = {"accept": "application/sparql-results+json"},
          auth   = self.auth
        )
        return response

    def query(self, query):

        response = self.sparql(query)

        return json.loads(response.text.decode("utf-8"))



if __name__ == "__main__":

    kb = HALKB()

    query = """
               INSERT DATA {
                   GRAPH <http://hal.zamia.org>
                   { 
                       weather:fc_Fairbanks__Alaska_20161112_morning weather:location <http://dbpedia.org/resource/Fairbanks,_Alaska> .
                       weather:fc_Fairbanks__Alaska_20161112_morning weather:temp_min -30 .
                       weather:fc_Fairbanks__Alaska_20161112_morning weather:temp_max -20 .
                   }
                }
            """
    print kb.sparql(query)

    query = """
            WITH <http://hal.zamia.org>
            DELETE { weather:fc_Fairbanks__Alaska_20161112_morning ?p ?v }
            WHERE { weather:fc_Fairbanks__Alaska_20161112_morning ?p ?v }
            """
    print kb.sparql(query)


    # query = """
    #        SELECT DISTINCT ?location ?cityid ?timezone ?label
    #        WHERE {
    #           ?location weather:cityid ?cityid .
    #           ?location weather:timezone ?timezone .
    #           ?location rdfs:label ?label .
    #           FILTER(LANGMATCHES(LANG(?label), "en")) .
    #        }"""
    query = """
           SELECT DISTINCT ?p ?v ?g
           WHERE {
              GRAPH ?g { weather:fc_Fairbanks__Alaska_20161112_morning ?p ?v }.
           }"""

    r = kb.query(query)

    for b in r['results']['bindings']:
        print repr(b)


