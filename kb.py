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
# current implementation: small excerpts from DBPedia plus some extensions stored in a local RDFLib Graph
#

import sys
import re
import os
import codecs
import json
from time import time

import requests
from requests.auth import HTTPDigestAuth

import rdflib

import utils
import model

# our sleepycat graph store

RDF_LIB_STORE_PATH = 'data/dst/HALRDFLibStore'
RDF_LIB_DUMP_PATH  = 'data/dst/HALKB.n3'

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
            'geo':     'http://www.opengis.net/ont/geosparql#',
            'geo1':    'http://www.w3.org/2003/01/geo/wgs84_pos#',
            'geof':    'http://www.opengis.net/def/function/geosparql/',
    }

#
# essentially we have two graphs: dbpedia subset + our own entries
#

GRAPHS = [ 'http://dbpedia.org', 'http://hal.zamia.org' ]

class HALKB(object):

    def __init__(self):

        #
        # prepare our lightweight sparql wrapper
        #

        self.query_prefixes = ''.join(map(lambda k: "PREFIX %s: <%s>\n" % (k, COMMON_PREFIXES[k]), COMMON_PREFIXES))

        #
        # set up graph store
        #

        self.graph = rdflib.ConjunctiveGraph('Sleepycat')
        self.graph.open(RDF_LIB_STORE_PATH, create = True)

        # Bind a few prefix/namespace pairs for more readable output

        for c in GRAPHS:
            g = self.graph.get_context(c)
            for p in COMMON_PREFIXES:
                g.bind(p, rdflib.Namespace(COMMON_PREFIXES[p]))

    def clear_graph(self, context):
        query = """
                CLEAR GRAPH <%s>
                """ % (context)
        self.sparql(query)

    def dump(self, fn=RDF_LIB_DUMP_PATH):

        # print
        # print 'dump', fn
        # print
        # print list(self.graph.contexts())

        self.graph.serialize(destination=fn, format='n3')

    def dump_graph(self, context, fn, format='n3'):

        g = self.graph.get_context(context)

        g.serialize(destination=fn, format='n3')

    def parse (self, context, format, data):
        g = self.graph.get_context(context)
        g.parse(format=format, data=data)

    def parse_file (self, context, format, fn):
        g = self.graph.get_context(context)
        g.parse(fn, format=format)

    #
    # local sparql queries
    #

    def sparql(self, query):

        query  = self.query_prefixes + query

        return self.graph.update(query)

    def query(self, query):

        query  = self.query_prefixes + query

        return self.graph.query(query)

    #
    # remote sparql utilities
    #

    def remote_sparql(self, endpoint, query, user=None, passwd=None, response_format='application/sparql-results+json'):

        if user:
            auth   = HTTPDigestAuth(user, passwd)
        else:
            auth   = None

        query  = self.query_prefixes + query
        # print query

        response = requests.post(
          endpoint,
          # data    = '',
          params  = {'query': query},
          headers = {"accept": response_format},
          auth    = auth
        )
        return response

    def remote_query(self, endpoint, query, user=None, passwd=None):

        response = self.remote_sparql(endpoint, query, user=user, passwd=passwd)

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
    kb.sparql(query)

