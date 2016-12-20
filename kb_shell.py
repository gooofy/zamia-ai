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
# shell offering various import, query and update commands for working with HAL's knowlegde base
#

import os
import sys
import locale
import ConfigParser
from os.path import expanduser
from optparse import OptionParser
import traceback
import codecs
import rdflib

import cmdln

from kb import HALKB, RDF_LIB_DUMP_PATH

# public DBPedia endpoint

DBPEDIA_ENDPOINT   = 'http://dbpedia.org/sparql'

DEFAULT_GRAPH      = 'http://hal.zamia.org'


class KBShell(cmdln.Cmdln):

    name = "kb"

    def __init__(self):
        #super(KBShell, self).__init__()
       
        cmdln.Cmdln.__init__(self)

        #
        # knowledge base
        #

        self.kb = HALKB()

        self.graph    = DEFAULT_GRAPH
        self.endpoint = DBPEDIA_ENDPOINT


    def do_dump(self, subcmd, opts, *paths):
        """${cmd_name}: dump KB in N3 format

        ${cmd_usage}
        ${cmd_option_list}
        """
        # print "'svn %s' opts:  %s" % (subcmd, opts) 
        # print "'svn %s' paths: %s" % (subcmd, paths) 

        if len(paths)==0:
            fn = RDF_LIB_DUMP_PATH
        else:
            fn = paths[0]

        print "dumping to %s ..." % fn

        self.kb.dump(fn)

        print "%s written." % RDF_LIB_DUMP_PATH
        print


    def do_graph_set(self, subcmd, opts, *paths):
        """${cmd_name}: set graph to work on

        ${cmd_usage}
        ${cmd_option_list}
        """

        assert len(paths) == 1

        self.graph = paths[0]

        print "default graph set to", self.graph

    def do_graph_get(self, subcmd, opts, *paths):
        """${cmd_name}: get current graph name

        ${cmd_usage}
        ${cmd_option_list}
        """

        print self.graph

    def do_endpoint_set(self, subcmd, opts, *paths):
        """${cmd_name}: set endpoint to import from

        ${cmd_usage}
        ${cmd_option_list}
        """

        assert len(paths) == 1

        self.endpoint = paths[0]

        print "default endpoint set to %s" % self.endpoint

    def do_endpoint_get(self, subcmd, opts, *paths):
        """${cmd_name}: get current endpoint name

        ${cmd_usage}
        ${cmd_option_list}
        """

        print self.endpoint

    @cmdln.option ("-g", "--graph", dest="graph", type = "str",
           help="graph to work on")
    def do_graph_clear(self, subcmd, opts, *paths):
        """${cmd_name}: clear graph

        ${cmd_usage}
        ${cmd_option_list}
        """

        graph = opts.graph if opts.graph else self.graph

        self.kb.clear_graph(graph)

        print "graph %s cleared." % graph

    @cmdln.option ("-g", "--graph", dest="graph", type = "str",
           help="graph to work on")
    @cmdln.option ("-f", "--format", dest="format", type = "str", default='n3',
           help="import format, default: n3")
    def do_graph_import(self, subcmd, opts, *paths):
        """${cmd_name}: import graph from file(s)

        ${cmd_usage}
        ${cmd_option_list}
        """

        graph = opts.graph if opts.graph else self.graph

        for p in paths:
            print "importing %s -> %s, format %s" % (p, graph, opts.format)
            self.kb.parse_file(graph, opts.format, p)

        print

    @cmdln.option ("-g", "--graph", dest="graph", type = "str",
           help="graph to work on")
    @cmdln.option ("-f", "--format", dest="format", type = "str", default='n3',
           help="export format, default: n3")
    def do_graph_export(self, subcmd, opts, *paths):
        """${cmd_name}: export graph to file

        ${cmd_usage}
        ${cmd_option_list}
        """

        graph = opts.graph if opts.graph else self.graph

        assert len(paths) == 1
        p = paths[0]
        print "exporting %s -> %s, format %s" % (graph, p, opts.format)

        self.kb.dump_graph(graph, p, format=opts.format)

        print

    @cmdln.option ("-g", "--graph", dest="graph", type = "str",
           help="graph to work on")
    @cmdln.option ("-e", "--endpoint", dest="endpoint", type = "str",
           help="endpoint to import from")
    def do_endpoint_import(self, subcmd, opts, *paths):
        """${cmd_name}: import node(s) from endpoint

        ${cmd_usage}
        ${cmd_option_list}
        """

        graph    = opts.graph    if opts.graph else self.graph
        endpoint = opts.endpoint if opts.endpoint else self.endpoint

        for node in paths:
            query = u"""
                     CONSTRUCT {
                        %s ?r ?n .
                     }
                     WHERE {
                        %s ?r ?n .
                     }
                     """ % (node, node)

            res = self.kb.remote_sparql(endpoint, query, response_format='text/n3')

            print "importing %s ?r ?n from %s: %s" % (node, endpoint, res)

            self.kb.parse(context=graph, format='n3', data=res.text) 

            query = u"""
                     CONSTRUCT {
                        ?n ?r %s .
                     }
                     WHERE {
                        ?n ?r %s .
                     }
                     """ % (node, node)

            res = self.kb.remote_sparql(endpoint, query, response_format='text/n3')
            print "importing ?n ?r %s from %s: %s" % (node, endpoint, res)

            self.kb.parse(context=graph, format='n3', data=res.text)

        print


    def do_search(self, subcmd, opts, *paths):
        """${cmd_name}: search for triples 

        ${cmd_usage}
        ${cmd_option_list}
        """

        for node in paths:
            query = u"""
                     SELECT ?r ?n
                     WHERE {
                            %s ?r ?n .
                     }
                     """ % node

            qres = self.kb.query(query)

            for row in qres:
                print "%s %s %s" % (node, row['r'], row['n'])

            query = u"""
                     SELECT ?r ?n
                     WHERE {
                            ?n ?r %s .
                     }
                     """ % node

            qres = self.kb.query(query)

            for row in qres:
                print "%s %s %s" % (row['n'], row['r'], node)             

        print

    @cmdln.option ("-f", "--file", action="store_true", dest="from_file",
                   help="argument(s) represent(s) file name(s) to read sparql from")
    def do_query(self, subcmd, opts, *paths):
        """${cmd_name}: run sparql query

        ${cmd_usage}
        ${cmd_option_list}
        """

        for a in paths:

            if opts.from_file:
                with codecs.open(a, 'r', 'utf8') as f:
                    query = f.read()
            else:
                query = a

            qres = self.kb.query(query)

            # print repr(qres)
            # print repr(qres.bindings)

            for binding in qres.bindings:

                # print repr(binding.labels)

                for var in binding:
                    print u'%s=%s ' % (unicode(var), unicode(binding[var])),
                print

            # for row in qres:

            #     print row.labels
            #     print repr(row)

        print

    @cmdln.option ("-f", "--file", action="store_true", dest="from_file",
                   help="argument(s) represent(s) file name(s) to read sparql from")
    def do_update(self, subcmd, opts, *paths):
        """${cmd_name}: run sparql update

        ${cmd_usage}
        ${cmd_option_list}
        """

        for a in paths:

            if opts.from_file:
                with codecs.open(a, 'r', 'utf8') as f:
                    query = f.read()
            else:
                query = a

            qres = self.kb.sparql(query)

#
# init terminal
#

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

#
# run shell
#

kbs = KBShell()
sys.exit(kbs.main(loop=cmdln.LOOP_IF_EMPTY))

