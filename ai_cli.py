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
# consolidated shell for all prolog/ai/kb related operations
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

from zamiaprolog.logic   import Predicate
from zamiaprolog.runtime import PROLOG_LOGGER_NAME
from aiprolog.runtime    import USER_PREFIX
from zamiaprolog.errors  import PrologError, PrologRuntimeError
from ai_kernal           import AIKernal
from nltools             import misc

DEFAULT_LOGLEVEL   = logging.INFO
RDF_LIB_DUMP_PATH  = 'data/AIKB.n3'

class AICli(cmdln.Cmdln):

    name = "ai_cli"

    def __init__(self):
       
        cmdln.Cmdln.__init__(self)

        self.kernal = AIKernal()

    @cmdln.option("-l", "--clean-logic", dest="clean_logic", action="store_true",
           help="clean predicates from logicdb")
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
                                 opts.clean_cronjobs)


        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option("-g", "--trace", dest="run_trace", action="store_true",
           help="enable tracing when running tests")
    @cmdln.option("-t", "--test", dest="run_tests", action="store_true",
           help="run tests")
    @cmdln.option("-N", "--test-name", dest="test_name", type="str",
           help="run specific test only, default: all tests are run")
    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="enable verbose logging")
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

        try:
            self.kernal.compile_module_multi (paths)

            if opts.run_tests:
                self.kernal.run_tests_multi (paths, run_trace=opts.run_trace, test_name=opts.test_name)

        except PrologError as e:
            logging.error("*** ERROR: %s" % e)

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)
        logging.getLogger(PROLOG_LOGGER_NAME).setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option("-g", "--trace", dest="run_trace", action="store_true",
           help="enable tracing")
    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    @cmdln.option("-N", "--test-name", dest="test_name", type="str",
           help="run specific test only, default: all tests are run")
    def do_test(self, subcmd, opts, *paths):
        """${cmd_name}: run tests from module(s)

        ${cmd_usage}
        ${cmd_option_list}
        """

        if len(paths)==0:
            logging.error ('specify at least one module name (or all to run tests from all modules)')
            return

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.debug('verbose logging enabled.')
        else:
            logging.getLogger().setLevel(logging.INFO)

        try:
            self.kernal.run_tests_multi (paths, run_trace=opts.run_trace, test_name=opts.test_name)
        except PrologError as e:
            logging.error("*** ERROR: %s" % e)

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    @cmdln.option("-g", "--trace", dest="run_trace", action="store_true",
           help="enable prolog tracing")
    @cmdln.option("-f", "--force", dest="force", action="store_true",
           help="force cronjob to run even if it is not due to")
    def do_cron(self, subcmd, opts, *paths):
        """${cmd_name}: run module(s) cronjobs

        ${cmd_usage}
        ${cmd_option_list}
        """

        if len(paths)==0:
            logging.error ('specify at least one module name (or "all" to run all module cronjobs)')
            return

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        self.kernal.run_cronjobs_multi(paths, opts.force, run_trace=opts.run_trace)

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    def do_train(self, subcmd, opts, *paths):
        """${cmd_name}: train tensorflow model

        ${cmd_usage}
        ${cmd_option_list}
        """

        if len(paths) != 1:
            raise Exception ("You need to specify exactly one model ini file")

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        self.kernal.train (paths[0])

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option ("-u", "--user", dest="username", type = "str", default="chat",
           help="username, default: chat")
    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    @cmdln.option ("-s", "--global-step", dest="global_step", type = "int", default=0,
           help="global step to load, default: 0 (latest)")
    def do_chat(self, subcmd, opts, *paths):
        """${cmd_name}: chat with model in natural language

        ${cmd_usage}
        ${cmd_option_list}
        """

        if len(paths) != 1:
            raise Exception ("You need to specify exactly one model ini file")

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        for mn2 in self.kernal.all_modules:
            self.kernal.load_module (mn2)
            self.kernal.init_module (mn2)

        self.kernal.setup_tf_model('decode', True, paths[0], global_step=opts.global_step)

        user_uri = USER_PREFIX + opts.username

        while True:

            line = raw_input ('ai> ')

            if line == 'quit' or line == 'exit':
                break

            try:
                abufs = self.kernal.process_input(line, self.kernal.nlp_model.lang, user_uri, test_mode=False)

                for abuf in abufs:
                    logging.debug ("abuf: %s" % repr(abuf))

                # if we have multiple abufs, pick one at random

                if len(abufs)>0:

                    abuf = random.choice(abufs)

                    self.kernal.prolog_rt.execute_builtin_actions(abuf)

                    self.kernal.db.commit()

                    for action in abuf['actions']:
                        p = action[0]
                        if not isinstance(p, Predicate):
                            continue
                        if p.name == 'say': 
                            print "SAY", action[2]
                        else:
                            print "ACTION", action
                            
            except Exception as e:
                logging.error(traceback.format_exc())

                abufs = self.kernal.do_eliza(line, self.kernal.nlp_model.lang, trace=opts.run_trace)

                abuf = random.choice(abufs)

                for action in abuf['actions']:
                    p = action[0]
                    if not isinstance(p, Predicate):
                        continue
                    if p.name == 'say': 
                        print "SAY", action[2]

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option ("-d", "--dict", dest="dictfn", type = "str", default=None,
           help="dictionary to use to detect unknown words, default: none")
    @cmdln.option ("-l", "--lang", dest="lang", type = "str", default='en',
           help="language, default: en")
    @cmdln.option ("-m", "--module", dest="module", type = "str", default='all',
           help="extract utterances from specific module only, default: all modules")
    @cmdln.option ("-n", "--num-utterances", dest="num_utterances", type = "int", default=0,
           help="number of utterances to extract, default: 0 (all)")
    def do_utterances(self, subcmd, opts, *paths):
        """${cmd_name}: get sample or all utterances from DB

        ${cmd_usage}
        ${cmd_option_list}
        """

        self.kernal.dump_utterances(opts.num_utterances, opts.dictfn, opts.lang, opts.module)


#
# init terminal
#

misc.init_app('ai_cli')

# reload(sys)
# sys.setdefaultencoding('utf-8')
# sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

#
# logging
#

logging.basicConfig(level=DEFAULT_LOGLEVEL)
logging.getLogger("requests").setLevel(logging.WARNING)

#
# run cli
#

aicli = AICli()
sys.exit(aicli.main(loop=cmdln.LOOP_IF_EMPTY))

