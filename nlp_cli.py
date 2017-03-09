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
# consolidated shell for all prolog/nlp/kb related operations
#

import os
import sys
import traceback
import codecs
import logging
import cmdln
import random
import time

import psycopg2

import model

from nlp_kernal import NLPKernal

DEFAULT_LOGLEVEL   = logging.INFO
RDF_LIB_DUMP_PATH  = 'data/HALKB.n3'

class NLPCli(cmdln.Cmdln):

    name = "nlp_cli"

    def __init__(self):
       
        cmdln.Cmdln.__init__(self)

        self.kernal = NLPKernal()

    @cmdln.option("-l", "--clean-logic", dest="clean_logic", action="store_true",
           help="clean predicates from logicdb")
    @cmdln.option("-k", "--clean-kb", dest="clean_kb", action="store_true",
           help="clean kb graph")
    @cmdln.option("-d", "--clean-discourses", dest="clean_discourses", action="store_true",
           help="clean discourses")
    @cmdln.option("-c", "--clean-cronjobs", dest="clean_cronjobs", action="store_true",
           help="clean cronjob db entries")
    @cmdln.option("-a", "--clean-all", dest="clean_all", action="store_true",
           help="clean everything (logicdb, kb graph and discourses)")
    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    def do_clean(self, subcmd, opts, *paths):
        """${cmd_name}: clean module related data

        ${cmd_usage}
        ${cmd_option_list}
        """

        if len(paths)==0:
            logging.error ('specify at least one module name or "all" to clean all modules')
            return

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        else:
            logging.getLogger().setLevel(logging.INFO)

        self.kernal.clean(paths, opts.clean_all, opts.clean_logic, opts.clean_discourses, 
                                 opts.clean_cronjobs, opts.clean_kb)


        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    def do_kb_import(self, subcmd, opts, *paths):
        """${cmd_name}: import module kb

        ${cmd_usage}
        ${cmd_option_list}
        """

        if len(paths)==0:
            logging.error ('specify at least one module name or "all" to load all modules')
            return

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        self.kernal.import_kb_multi(paths)

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    
    @cmdln.option ("-o", "--output-file", dest="outfn", type = "str", default=RDF_LIB_DUMP_PATH,
           help="export filename, default: %s" % RDF_LIB_DUMP_PATH)
    @cmdln.option ("-m", "--module", dest="module", type = "str", default='all',
           help="module to export, default: all")
    @cmdln.option ("-f", "--format", dest="format", type = "str", default='n3',
           help="export format, default: n3")

    def do_kb_export(self, subcmd, opts, *paths):
        """${cmd_name}: export KB graph(s) to file

        ${cmd_usage}
        ${cmd_option_list}
        """

        if opts.module == 'all':
            self.kernal.kb.dump(opts.outfn, format=opts.format)
        else:
            graph = self.kernal._module_graph_name(opts.module)
            self.kernal.kb.dump_graph(graph, opts.outfn, format=opts.format)

        logging.info( "%s written." % opts.outfn)

    def do_kb_search(self, subcmd, opts, *paths):
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
                logging.info("%s %s %s" % (node, row['r'], row['n']))

            query = u"""
                     SELECT ?r ?n
                     WHERE {
                            ?n ?r %s .
                     }
                     """ % node

            qres = self.kb.query(query)

            for row in qres:
                logging.info("%s %s %s" % (row['n'], row['r'], node))

    @cmdln.option ("-f", "--file", action="store_true", dest="from_file",
                   help="argument(s) represent(s) file name(s) to read sparql from")
    @cmdln.option ("-s", "--sql", dest="sql", action="store_true",
                   help="log SQL statements")
    @cmdln.option ("-v", "--verbose", dest="verbose", action="store_true",
                   help="verbose logging")
    def do_kb_query(self, subcmd, opts, *paths):
        """${cmd_name}: run sparql query

        ${cmd_usage}
        ${cmd_option_list}
        """

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        if opts.sql:
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

        for a in paths:

            if opts.from_file:
                with codecs.open(a, 'r', 'utf8') as f:
                    query = f.read()
            else:
                query = a

            logging.debug ('running query...')
            start_time = time.time()

            qres = self.kernal.kb.query(query)

            logging.debug ('query done. took %fs' % (time.time()-start_time))

            logging.debug ('sparql query result: %s' % str(qres))
            logging.debug ('sparql query bindings: %s' % repr(qres.bindings))
            # print repr(qres.bindings)

            for binding in qres.bindings:

                # print repr(binding.labels)

                s = ''

                for var in binding:
                     s += u'%s=%s ' % (unicode(var), repr(binding[var]))
                logging.info(s)
        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)

    @cmdln.option ("-f", "--file", action="store_true", dest="from_file",
                   help="argument(s) represent(s) file name(s) to read sparql from")
    def do_kb_update(self, subcmd, opts, *paths):
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

    @cmdln.option("-g", "--trace", dest="run_trace", action="store_true",
           help="enable tracing")
    @cmdln.option("-u", "--print-utterances", dest="print_utterances", action="store_true",
           help="print generated utterances")
    @cmdln.option("-t", "--tests", dest="run_tests", action="store_true",
           help="run tests")
    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    def do_compile(self, subcmd, opts, *paths):
        """${cmd_name}: compile module(s)

        ${cmd_usage}
        ${cmd_option_list}
        """

        if len(paths)==0:
            logging.error ('specify at least one module name')
            return

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.debug('verbose logging enabled.')
        else:
            logging.getLogger().setLevel(logging.INFO)

        self.kernal.compile_module_multi (paths, opts.run_trace, opts.run_tests, opts.print_utterances)

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    @cmdln.option("-f", "--force", dest="force", action="store_true",
           help="force cronjob to run even if it is not due to")
    def do_cron(self, subcmd, opts, *paths):
        """${cmd_name}: run module(s) cronjobs

        ${cmd_usage}
        ${cmd_option_list}
        """

        if len(paths)==0:
            logging.error ('specify at least one module name')
            return

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        self.kernal.run_cronjobs_multi(paths, opts.force)

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option ("-n", "--num-steps", dest="num_steps", type = "int", default=50000,
           help="number of training steps, default: 50000")
    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    def do_train(self, subcmd, opts, *paths):
        """${cmd_name}: train tensorflow model

        ${cmd_usage}
        ${cmd_option_list}
        """

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        self.kernal.train (opts.num_steps)

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    def do_chat(self, subcmd, opts, *paths):
        """${cmd_name}: chat with model in natural language

        ${cmd_usage}
        ${cmd_option_list}
        """

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        self.kernal.setup_tf_model(True, True)

        while True:

            line = raw_input ('nlp> ')

            if line == 'quit' or line == 'exit':
                break

            utts, actions = self.kernal.process_line(line)

            if len(utts)>0:
                print "SAY", random.choice(utts)['utterance']

            for action in actions:
                print "ACTION", action

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option ("-d", "--dict", dest="dictfn", type = "str", default=None,
           help="dictionary to use to detect unknown words, default: none")
    # @cmdln.option ("-m", "--module", dest="module", type = "str", default='all',
    #        help="extract utterances from specific module only, default: all modules")
    @cmdln.option ("-n", "--num-utterances", dest="num_utterances", type = "int", default=0,
           help="number of utterances to extract, default: 0 (all)")
    def do_utterances(self, subcmd, opts, *paths):
        """${cmd_name}: get sample or all utterances from DB

        ${cmd_usage}
        ${cmd_option_list}
        """

        self.kernal.dump_utterances(opts.num_utterances, opts.dictfn)


#
# init terminal
#

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

#
# logging
#

logging.basicConfig(level=DEFAULT_LOGLEVEL)
logging.getLogger("requests").setLevel(logging.WARNING)

#
# run cli
#

ncli = NLPCli()
sys.exit(ncli.main(loop=cmdln.LOOP_IF_EMPTY))

