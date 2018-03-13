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
# Use LDF endpoints for sourcing triples, mirror them into a memory RDFLib store, dump in N3 format
#

import os
import sys
import traceback
import codecs
import logging
import time
import urllib
import requests
import rdflib

from optparse import OptionParser
from urlparse import urlparse

from nltools  import misc
from config   import RDF_PREFIXES, LDF_ENDPOINTS, RDF_ALIASES, RES_PATHS

DEBUG_LIMIT = 0
# DEBUG_LIMIT = 23

CACHE_PATH    = 'cache'
CACHE_MAX_AGE = 7 * 24 * 60 * 60 # 7 days

class LDFMirror(object):
    """
    Helper class for mirroring triples from LDF endpoints
    """

    def __init__ (self, graph, endpoints, aliases, prefixes):
        """
        Create new endpoint mirror helper

        graph     -- target RDFLib graph
                    
        endpoints -- dict mapping host names to LDF endpoints, e.g. 
                     {
                         'www.wikidata.org': 'https://query.wikidata.org/bigdata/ldf',
                     }
        aliases   -- dict mapping resource aliases to IRIs, e.g.
                     {
                          u'wde:Female' : u'http://www.wikidata.org/entity/Q6581072',
                          u'wde:Male'   : u'http://www.wikidata.org/entity/Q6581097',
                     }
        prefixes  -- dict mapping aliases to IRIs, e.g.
                     {
                          'dbo' : 'http://dbpedia.org/ontology/',
                          'dbr' : 'http://dbpedia.org/resource/',
                          'dbp' : 'http://dbpedia.org/property/',
                     }
        """

        self.graph     = graph
        self.endpoints = endpoints
        self.aliases   = aliases
        self.prefixes  = prefixes

    def _find_endpoint (self, resource):
        parsed_uri = urlparse(resource)
        if parsed_uri.netloc in self.endpoints:
            return self.endpoints[parsed_uri.netloc]
        return None

    def resolve_shortcuts (self, resource):

        if isinstance(resource, rdflib.URIRef):
            return rdflib.URIRef(self.resolve_shortcuts(unicode(resource)))

        #
        # apply aliases
        #

        if resource in self.aliases:
            return self.aliases[resource]

        #
        # apply prefixes
        #

        for pfx in self.prefixes:
            prefix = pfx + ':'
            if resource.startswith(prefix):
                resource = self.prefixes[pfx] + resource[len(prefix):]
                break

        return resource

    def _fetch_ldf (self, s=None, p=None, o=None):

        triples = []

        params   = {}
        endpoint = None
        label    = None
        if s:
            params['subject']   = s
            endpoint = self._find_endpoint(s)
            label=unicode(s)
        if p:
            params['predicate'] = p
            if not endpoint:
                endpoint = self._find_endpoint(p)
            if not label:
                label=unicode(p)
        if o:
            params['object']    = o
            if not endpoint:
                endpoint = self._find_endpoint(o)
            if not label:
                label=unicode(o)

        if not endpoint:
            return triples

        # logging.info ("LDF: *** fetching from endpoint %s" % endpoint)

        url = endpoint + '?' + urllib.urlencode(params)

        if not label:
            label = '<unknown>'

        cache_fn = '%s/%s.n3' % (CACHE_PATH, url.replace('/', '_'))

        use_cache = os.path.exists(cache_fn)
        if use_cache:
            st  = os.stat(cache_fn)
            age = time.time() - st.st_mtime
            if age > CACHE_MAX_AGE:
                use_cache = False

        if use_cache:

            with codecs.open(cache_fn, 'r', 'utf8') as cache_f:
                memg = rdflib.Graph()
                memg.parse(source=cache_f, format='n3')
                for s2,p2,o2 in memg.triples((rdflib.URIRef(s) if s else None, 
                                              rdflib.URIRef(p) if p else None, 
                                              rdflib.URIRef(o) if o else None )):

                    # print english labels as we come across them to make mirroring log less boring
                    if isinstance(o2, rdflib.term.Literal) \
                        and unicode(p2) == u'http://www.w3.org/2000/01/rdf-schema#label' \
                        and o2.language == u'en':
                        # logging.info (u'LDF:   fetched LABEL(en)=%s' % o2)
                        label = o2

                    # logging.debug ('quad: %s %s %s' % (s2,p2,o2))
                    triples.append((s2,p2,o2))

        else:

            while True:

                response = requests.get(
                  url,
                  headers = {"accept": 'text/turtle'},
                )

                # logging.debug ('%s response: %d' % (url, response.status_code))
                # for h in response.headers:
                #     logging.debug ('   header %s: %s' % (h, response.headers[h]))

                if response.status_code != 200:
                    break

                # extract triples

                memg = rdflib.Graph()
                memg.parse(data=response.text, format='turtle')
              
                for s2,p2,o2 in memg.triples((rdflib.URIRef(s) if s else None, 
                                              rdflib.URIRef(p) if p else None, 
                                              rdflib.URIRef(o) if o else None )):

                    # print english labels as we come across them to make mirroring log less boring
                    if isinstance(o2, rdflib.term.Literal) \
                        and unicode(p2) == u'http://www.w3.org/2000/01/rdf-schema#label' \
                        and o2.language == u'en':
                        # logging.info (u'LDF:   fetched LABEL(en)=%s' % o2)
                        label = o2

                    # logging.debug ('quad: %s %s %s' % (s2,p2,o2))
                    triples.append((s2,p2,o2))

                # paged resource?
                url = None
                for s2,p2,o2 in memg.triples((None, rdflib.URIRef('http://www.w3.org/ns/hydra/core#nextPage'), None )):
                    url = str(o2)
                    # logging.debug ('got next page url: %s, %d triples so far' % (url, len(triples)))
                for s2,p2,o2 in memg.triples((None, rdflib.URIRef('http://www.w3.org/ns/hydra/core#next'), None )):
                    # logging.debug ('got next page ref: %s' % repr(o))
                    url = str(o2)
                    # logging.debug ('got next page url: %s, %d triples so far' % (url, len(triples)))

                if not url:
                    break

            with codecs.open(cache_fn, 'w', 'utf8') as cache_f:
                memg = rdflib.Graph()
                for t in triples:
                    memg.add(t)

                cache_f.write(memg.serialize(format='n3'))

        if use_cache:
            cache_str = 'CACHED'
        else:
            cache_str = 'FETCH '

        logging.info (u'LDF: %8.1fs %5d:%5d %s %s' % (time.time() - self.start_time, len(self.done), len(self.todo), cache_str, label[:40]))
        return triples

    def mirror (self, res_paths):
        """ 
        mirror triples from endpoints according to resource paths specified in res_paths.

        Each resource path is a tuple consisting of a list of start resources and a list
        of patterns describing which edges to follow.

        A very simple example of a resource path may consist of just a start resource, e.g.

        ( [ u'wde:AngelaMerkel' ], [ [] ] )

        this would mirror the resource u'wde:AngelaMerkel' with all its direct properties but
        not recurse into the graph at all. Imagine we'd also be interested in her birth place
        and statements about positions held we could specify paths:

        ( [ u'wde:AngelaMerkel' ], [ ['wdpd:PlaceOfBirth'], ['wdp:PositionHeld','*'] ] )

        this would mirror all properties of her birth place as well as recurse into all
        wdp:PositionHeld statements and further down to any resource linked from there.

        Lastly, we can also specify basic graph patterns for start points. Using this feature,
        we could mirror all federal chancellors of Germany using this resource path specification:

        ( [ ('wdpd:PositionHeld', 'wde:FederalChancellorOfGermany') ], [ ['wdpd:PlaceOfBirth'], ['wdp:PositionHeld','*'] ] )

        """


        self.start_time = time.time()

        self.todo = []
        self.done = set()

        for res_path in res_paths:

            resolved_paths = map( 
                               lambda p: 
                                 map( 
                                   lambda p: (self.resolve_shortcuts(p[0]), p[1]) if type(p) is tuple else
                                   self.resolve_shortcuts(p), p), res_path[1])

            for resource in res_path[0]:

                if isinstance(resource, basestring):
                    rs = [ self.resolve_shortcuts (resource) ]
                else:
                    rs = []
                    for t in self._fetch_ldf(p=self.resolve_shortcuts(resource[0]), 
                                             o=self.resolve_shortcuts(resource[1])):
                        rs.append(t[0])
          
                for r in rs:
                    for resolved_path in resolved_paths:
                        # import pdb; pdb.set_trace()

                        logging.debug ('adding task: %s %s' % (r, repr(resolved_path)))
                        self.todo.append((rdflib.URIRef(r), resolved_path))
               
        while len(self.todo)>0:

            resource, path = self.todo.pop()

            todo_new = set()

            # fetch resources from LDF only once

            if resource in self.done:
                triples = list(self.graph.triples((resource, None, None)))
                # logging.debug (u'LDF:                       DONE, %d triples' % len(triples))
                do_add = False

            else:

                triples = self._fetch_ldf (s=resource)
                self.done.add(resource)
                do_add = True

            # transformations

            if len(path)>0:
                res_filter = path[0]

                if type(res_filter) is tuple:
                    pred, f = res_filter

                    for t in triples:

                        s = t[0]
                        p = t[1]
                        o = t[2]

                        if unicode(p) != pred:
                            continue

                        np, no = f(o)

                        np = self.resolve_shortcuts(np)

                        if do_add:
                            triples.append ((s, np, no))

                        res_filter = unicode(np)

            if do_add:
                for t in triples:
                    self.graph.add(t)

            if len(path)>0:

                new_path   = path[1:]

                for t in triples:

                    if len(t)<3:
                        logging.error('triple of 2?! %s' % repr(t))
                        continue

                    s = t[0]
                    p = t[1]
                    o = t[2]

                    if not isinstance(o, rdflib.URIRef):
                        continue

                    # logging.debug ('LDF   checking %s %s' % (p, o))

                    if res_filter == '*' or res_filter == unicode(p):

                        # import pdb; pdb.set_trace()

                        task = (o, new_path)

                        # logging.debug ('LDF   adding new task: %s' % repr(task))
                        self.todo.append(task)



class LDFMirrorP2E(LDFMirror):
    """
    Like LDFMirror but fetches property entities as well
    """

    def __init__ (self, graph, endpoints, aliases, prefixes, p2e_mapper ):
        """
        Create new endpoint mirror helper with P2E (propert to entity mapping) support
        Like LDFMirror but fetches property entities as well.

        graph     -- target RDFLib graph
                    
        endpoints -- dict mapping host names to LDF endpoints, e.g. 
                     {
                         'www.wikidata.org': 'https://query.wikidata.org/bigdata/ldf',
                     }

        p2emapper -- function that will be called on each property for entity mapping
                     wikidata example:
                         def p2e_mapper(p):
                             if p.startswith('http://www.wikidata.org/prop/direct/'):
                                 return 'http://www.wikidata.org/entity/' + p[36:]
                             if p.startswith('http://www.wikidata.org/prop/'):
                                 return 'http://www.wikidata.org/entity/' + p[29:]
                             return None
        """

        self.p2e_mapper = p2e_mapper
        
        super (LDFMirrorP2E, self).__init__(graph, endpoints, aliases, prefixes)

    def get_all_predicates(self, limit=0):

        preds = set()

        for t in self.graph:
            if t[1] in preds:
                continue
            preds.add(t[1])

        return preds

    def mirror (self, res_paths):

        super (LDFMirrorP2E, self).mirror(res_paths)

        preds = self.get_all_predicates()

        pred_ents = set()
        for p in preds:
            pe = self.p2e_mapper(p)
            if pe:
                pred_ents.add(pe)

        # call mirror() again on list of property entities to ensure those
        # are present in our mirrored dataset as well

        res_list = []
        cnt      = 0
        for pe in sorted (pred_ents):
            res_list.append(pe)
            cnt += 1
            if DEBUG_LIMIT and (DEBUG_LIMIT <= cnt):
                break

        logging.info ('**** ADDED %d PROPERTY ENTITIES TO MIRROR ****' % cnt)

        super (LDFMirrorP2E, self).mirror([(res_list, [[]])])

def p2e_mapper(p):
    if p.startswith('http://www.wikidata.org/prop/direct/'):
        return 'http://www.wikidata.org/entity/' + p[36:]
    if p.startswith('http://www.wikidata.org/qualifier/'):
        return 'http://www.wikidata.org/entity/' + p[34:]
    if p.startswith('http://www.wikidata.org/prop/statement/'):
        return 'http://www.wikidata.org/entity/' + p[39:]
    if p.startswith('http://www.wikidata.org/prop/'):
        return 'http://www.wikidata.org/entity/' + p[29:]
    return None

DEFAULT_OUTPUT='foo.n3'

#
# init, cmdline
#

misc.init_app('ldfmirror')

parser = OptionParser("usage: %prog [options]")

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")
parser.add_option ("-o", "--output", dest="outputfn", type = "string", default=DEFAULT_OUTPUT,
                   help="output file, default: %s" % DEFAULT_OUTPUT)

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)


outputfn = options.outputfn

#
# main
#

g = rdflib.Graph()

mirror = LDFMirrorP2E (g, LDF_ENDPOINTS, RDF_ALIASES, RDF_PREFIXES, p2e_mapper )

mirror.mirror (RES_PATHS)

logging.info ('writing %s...' % outputfn)
with codecs.open(outputfn, 'w', 'utf8') as outputf:
    outputf.write(g.serialize(format='n3'))

logging.info ('%s written.' % outputfn)

