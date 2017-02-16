#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017 Guenter Bartsch
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
import logging
import json
import traceback
import time
import requests
from requests.auth import HTTPDigestAuth

import rdflib

from nltools import misc
from sparqlalchemy.sparqlalchemy import SPARQLAlchemyStore

# # our sleepycat graph store
# 
# RDF_LIB_STORE_PATH = 'data/dst/HALRDFLibStore'

#
# common prefixes we use in our queries
#

COMMON_PREFIXES = {
            'rdf':     'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs':    'http://www.w3.org/2000/01/rdf-schema#',
            'hal':     'http://hal.zamia.org/kb/',
            'dbo':     'http://dbpedia.org/ontology/',
            'dbr':     'http://dbpedia.org/resource/',
            'dbp':     'http://dbpedia.org/property/',
            'xml':     'http://www.w3.org/XML/1998/namespace',
            'xsd':     'http://www.w3.org/2001/XMLSchema#',
            'geo':     'http://www.opengis.net/ont/geosparql#',
            'geo1':    'http://www.w3.org/2003/01/geo/wgs84_pos#',
            'geof':    'http://www.opengis.net/def/function/geosparql/',
            'schema':  'http://schema.org/',
    }

#
# essentially we have two graphs: dbpedia subset + our own entries
#

class HALKB(object):

    def __init__(self):

        #
        # prepare our lightweight sparql wrapper
        #

        self.query_prefixes = ''.join(map(lambda k: "PREFIX %s: <%s>\n" % (k, COMMON_PREFIXES[k]), COMMON_PREFIXES))

        #
        # set up graph store
        #

        config = misc.load_config('.nlprc')

        # DB, SPARQLAlchemyStore

        db_url = config.get('db', 'url')

        self.sas = SPARQLAlchemyStore(db_url, 'halkb', echo=False)


    def register_graph(self, c):

        raise Exception ('FIXME: implement dump functions in sparqlalchemy')

        # # Bind a few prefix/namespace pairs for more readable output

        # g = self.graph.get_context(c)
        # for p in COMMON_PREFIXES:
        #     g.bind(p, rdflib.Namespace(COMMON_PREFIXES[p]))

    def close (self):
        # self.graph.close()
        pass

    def clear_graph(self, context):
        self.sas.clear_graph(context)
        # query = """
        #         CLEAR GRAPH <%s>
        #         """ % (context)
        # self.sparql(query)

    def clear_all_graphs (self):
        self.sas.clear_all_graphs()

    def dump(self, fn, format='n3'):

        raise Exception ('FIXME: implement dump functions in sparqlalchemy')
        # print
        # print 'dump', fn
        # print
        # print list(self.graph.contexts())

        # self.graph.serialize(destination=fn, format=format)

    def dump_graph(self, context, fn, format='n3'):

        raise Exception ('FIXME: implement dump functions in sparqlalchemy')
        # g = self.graph.get_context(context)

        # g.serialize(destination=fn, format='n3')

    def parse (self, context, format, data):

        self.sas.parse(format=format, data=data, context=context)


    def parse_file (self, context, format, fn):
        self.sas.parse(fn, format=format, context=context)

    #
    # local sparql queries
    #

    def sparql(self, query):

        raise Exception ('FIXME: sparql update queries not implemented yet.')

        # query  = self.query_prefixes + query

        # return self.graph.update(query)

    def query(self, query):

        query  = self.query_prefixes + query

        return self.sas.query(query)

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

    logging.basicConfig(level=logging.DEBUG)

    gn = u'http://hal.zamia.org/benchmark'

    start_time = time.time()
    kb = HALKB()
    logging.debug ('HALKB init took %fs' % (time.time() - start_time))

    start_time = time.time()
    kb.clear_graph(gn)
    logging.debug ('HALKB clear graph took %fs' % (time.time() - start_time))

    # query = """
    #            INSERT DATA {
    #                GRAPH <http://hal.zamia.org/benchmark>
    #                { 
    #                    hal:fc_Fairbanks__Alaska_20161112_morning hal:location <http://dbpedia.org/resource/Fairbanks,_Alaska> .
    #                    hal:fc_Fairbanks__Alaska_20161112_morning hal:temp_min -30 .
    #                    hal:fc_Fairbanks__Alaska_20161112_morning hal:temp_max -20 .
    #                }
    #             }
    #         """
    # start_time = time.time()
    # kb.sparql(query)
    # logging.debug ('HALKB sparql() took %fs' % (time.time() - start_time))

    # generate lots of n3 data, for parser benchmarking

    n3data = '@prefix hal: <http://hal.zamia.org/kb/> .\n'
    for i in range (1000):
        n3data += 'hal:n%d hal:bench hal:m%d .\n' % (i, i)

    # print n3data

    print 'HALKB parsing...'
    start_time = time.time()
    kb.parse (gn, 'n3', n3data)
    logging.debug ('HALKB parse() took %fs' % (time.time() - start_time))

    print 'HALKB parsing (again)...'
    start_time = time.time()
    kb.parse (gn, 'n3', n3data)
    logging.debug ('HALKB parse() took %fs' % (time.time() - start_time))

    start_time = time.time()
    kb.close()
    logging.debug ('HALKB close() took %fs' % (time.time() - start_time))

