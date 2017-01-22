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
import imp
import time
import cmdln
import random

from sqlalchemy.orm import sessionmaker
import psycopg2

import tensorflow as tf

import model

from kb import HALKB, RDF_LIB_DUMP_PATH
from prolog_compiler import PrologCompiler
from logicdb import LogicDB
from nltools import misc
from nlp_model import NLPModel
from nlp_engine import NLPEngine

GRAPH_PREFIX       = 'http://hal.zamia.org/kb/'

DEFAULT_LOGLEVEL   = logging.INFO

class NLPCli(cmdln.Cmdln):

    name = "nlp_cli"

    def __init__(self):
       
        cmdln.Cmdln.__init__(self)

        self.config = misc.load_config('.nlprc')

        #
        # database
        #

        Session = sessionmaker(bind=model.engine)
        self.session = Session()

        #
        # logic DB
        #

        self.db = LogicDB(self.session)

        #
        # knowledge base
        #

        self.kb = HALKB()

        #
        # module management, setup
        #

        self.modules  = {}
        s = self.config.get('semantics', 'modules')
        self.all_modules = map (lambda s: s.strip(), s.split(','))

        for mn2 in self.all_modules:
            self.load_module (mn2)

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

        for module_name in paths:

            if opts.clean_logic or opts.clean_all:
                logging.info('cleaning logic for %s...' % module_name)
                if module_name == 'all':
                    self.db.clear_all_modules()
                else:
                    self.db.clear_module(module_name)

            if opts.clean_discourses or opts.clean_all:
                logging.info('cleaning discourses for %s...' % module_name)
                if module_name == 'all':
                    self.session.query(model.Discourse).delete()
                else:
                    self.session.query(model.Discourse).filter(model.Discourse.module==module_name).delete()

            if opts.clean_cronjobs or opts.clean_all:
                logging.info('cleaning cronjobs for %s...' % module_name)
                if module_name == 'all':
                    self.session.query(model.Cronjob).delete()
                else:
                    self.session.query(model.Cronjob).filter(model.Cronjob.module==module_name).delete()

            if opts.clean_kb or opts.clean_all:
                logging.info('cleaning kb for %s...' % module_name)
                if module_name == 'all':
                    self.kb.clear_all_graphs()
                else:
                    graph = self._module_graph_name(module_name)
                    self.kb.clear_graphs(graph)

        self.session.commit()

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    def load_module (self, module_name):

        if module_name in self.modules:
            return self.modules[module_name]

        logging.debug("loading module '%s'" % module_name)

        fp, pathname, description = imp.find_module(module_name, ['modules'])

        # print fp, pathname, description

        m = None

        try:
            m = imp.load_module(module_name, fp, pathname, description)

            self.modules[module_name] = m

            # print m
            # print getattr(m, '__all__', None)

            # for name in dir(m):
            #     print name

            for m2 in getattr (m, 'DEPENDS'):
                self.load_module(m2)

            if hasattr(m, 'CRONJOBS'):

                # update cronjobs in db

                old_cronjobs = set()
                for cronjob in self.session.query(model.Cronjob).filter(model.Cronjob.module==module_name):
                    old_cronjobs.add(cronjob.name)

                new_cronjobs = set()
                for name, interval, f in getattr (m, 'CRONJOBS'):

                    logging.debug ('registering cronjob %s' %name)

                    cj = self.session.query(model.Cronjob).filter(model.Cronjob.module==module_name, model.Cronjob.name==name).first()
                    if not cj:
                        cj = model.Cronjob(module=module_name, name=name, last_run=0)
                        self.session.add(cj)

                    cj.interval = interval
                    new_cronjobs.add(cj.name)

                for cjn in old_cronjobs:
                    if cjn in new_cronjobs:
                        continue
                    self.session.query(model.Cronjob).filter(model.Cronjob.module==module_name, model.Cronjob.name==cjn).delete()

                self.session.commit()

        except:
            logging.error(traceback.format_exc())

        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()

        return m

    def _module_graph_name (self, module_name):
        return GRAPH_PREFIX + module_name

    def import_kb (self, module_name):

        graph = self._module_graph_name(module_name)

        self.kb.register_graph(graph)

        self.kb.clear_graph(graph)

        m = self.modules[module_name]

        for kb_entry in getattr (m, 'KB_SOURCES'):

            if isinstance(kb_entry, basestring):
        
                kb_pathname = 'modules/%s/%s' % (module_name, kb_entry)

                logging.info('importing %s ...' % kb_pathname)
                
                self.kb.parse_file(graph, 'n3', kb_pathname)

            else:

                endpoint, nodes = kb_entry

                logging.info('importing nodes from %s...' % endpoint)

                for node in nodes:

                    logging.debug('importing %s from %s...' % (node, endpoint))

                    query = u"""
                             CONSTRUCT {
                                %s ?r ?n .
                             }
                             WHERE {
                                %s ?r ?n .
                             }
                             """ % (node, node)

                    res = self.kb.remote_sparql(endpoint, query, response_format='text/n3')

                    logging.debug("importing %s ?r ?n from %s: %d bytes." % (node, endpoint, len(res.text)))

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
                    logging.debug("importing ?n ?r %s from %s: %d bytes" % (node, endpoint, len(res.text)))

                    self.kb.parse(context=graph, format='n3', data=res.text)

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

        for module_name in paths:

            if module_name == 'all':

                for mn2 in self.all_modules:
                    self.load_module (mn2)
                    self.import_kb (mn2)

            else:

                self.load_module (module_name)

                self.import_kb (module_name)

        self.session.commit()

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
            self.kb.dump(opts.outfn, format=opts.format)
        else:
            graph = self._module_graph_name(opts.module)
            self.kb.dump_graph(graph, opts.outfn, format=opts.format)

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
    def do_kb_query(self, subcmd, opts, *paths):
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

                s = ''

                for var in binding:
                     s += u'%s=%s ' % (unicode(var), unicode(binding[var]))
                logging.info(s)

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

    def compile_module (self, module_name, trace=False, run_tests=False):

        m = self.modules[module_name]

        compiler = PrologCompiler (self.session, trace, run_tests)

        for pl_fn in getattr (m, 'PL_SOURCES'):
            
            pl_pathname = 'modules/%s/%s' % (module_name, pl_fn)

            compiler.do_compile (pl_pathname, module_name)

    @cmdln.option("-g", "--trace", dest="run_trace", action="store_true",
           help="enable tracing")
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
        else:
            logging.getLogger().setLevel(logging.INFO)

        for module_name in paths:

            if module_name == 'all':

                for mn2 in self.all_modules:
                    self.load_module (mn2)
                    self.compile_module (mn2, opts.run_trace, opts.run_tests)

            else:
                self.load_module (module_name)
                self.compile_module (module_name, opts.run_trace, opts.run_tests)

        self.session.commit()

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    def run_cronjobs (self, module_name, force=False):

        m = self.modules[module_name]
        if not hasattr(m, 'CRONJOBS'):
            return

        graph = self._module_graph_name(module_name)

        self.kb.register_graph(graph)

        for name, interval, f in getattr (m, 'CRONJOBS'):

            cronjob = self.session.query(model.Cronjob).filter(model.Cronjob.module==module_name, model.Cronjob.name==name).first()

            t = time.time()

            next_run = cronjob.last_run + interval

            if force or t > next_run:

                logging.debug ('running cronjob %s' %name)
                f (self.config, self.kb)

                cronjob.last_run = t

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

        for module_name in paths:

            if module_name == 'all':

                for mn2 in self.all_modules:
                    self.load_module (mn2)
                    self.run_cronjobs (mn2, force=opts.force)

            else:
                self.load_module (module_name)
                self.run_cronjobs (module_name, force=opts.force)

        self.session.commit()

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option ("-n", "--num-steps", dest="num_steps", type = "int", default=5000,
           help="number of training steps, default: 5000")
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

        nlp_model = NLPModel(self.session)
        nlp_model.train(opts.num_steps)

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

        #
        # setup nlp engine, tensorflow session
        #

        # setup config to use BFC allocator
        config = tf.ConfigProto()  
        config.gpu_options.allocator_type = 'BFC'

        with tf.Session(config=config) as tf_session:
            nlp_engine = NLPEngine(self.db, self.session, tf_session)

            while True:

                line = raw_input ('nlp> ')

                if line == 'quit' or line == 'exit':
                    break

                utts, actions = nlp_engine.process_line(line)

                if len(utts)>0:
                    print "SAY", random.choice(utts)['utterance']

                for action in actions:
                    print "ACTION", action

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

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

