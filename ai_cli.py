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

from six.moves            import input

from zamiaprolog.builtins import ASSERT_OVERLAY_VAR_NAME
from zamiaprolog.logic    import Predicate
from zamiaprolog.runtime  import PROLOG_LOGGER_NAME
from zamiaprolog.errors   import PrologError, PrologRuntimeError
from aiprolog.runtime     import USER_PREFIX
from zamiaai.ai_kernal    import AIKernal
from zamiaai              import model
from nltools              import misc

DEFAULT_LOGLEVEL   = logging.INFO
CLI_MODULE        = '__cli__'

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
                num_tests, num_fails = self.kernal.run_tests_multi (paths, run_trace=opts.run_trace, test_name=opts.test_name)

                if num_fails:
                    logging.error('%d test(s) failed out of %d test(s) run.' % (num_fails, num_tests))
                else:
                    logging.info('all %d test(s) worked!' % num_tests)

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
            num_tests, num_fails = self.kernal.run_tests_multi (paths, run_trace=opts.run_trace, test_name=opts.test_name)
            if num_fails:
                logging.error('%d test(s) failed out of %d test(s) run.' % (num_fails, num_tests))
            else:
                logging.info('all %d test(s) worked!' % num_tests)

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

    @cmdln.option("-i", "--incremental", dest="incremental", action="store_true",
           help="incremental training (load previously saved variables)")
    @cmdln.option("-n", "--num-steps", dest="num_steps", type = "int", default=100000,
           help="number of steps to train for, default: 100000")
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

        self.kernal.train (paths[0], opts.num_steps, opts.incremental)

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option("-g", "--trace", dest="run_trace", action="store_true",
           help="enable prolog tracing")
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

        user_uri    = USER_PREFIX + opts.username
        cur_context = None

        while True:

            line = input ('ai> ')

            if line == 'quit' or line == 'exit':
                break

            try:
                score, resps, actions, solutions, cur_context = self.kernal.process_input(line, self.kernal.nlp_model.lang, user_uri, run_trace=opts.run_trace, prev_ctx = cur_context)

                for idx in range (len(resps)):
                    logging.debug('[%05d] %s ' % (score, u' '.join(resps[idx])))

                # if we have multiple responses, pick one at random

                if len(resps)>0:

                    idx = random.randint(0, len(resps)-1)

                    # apply DB overlay, if any
                    ovl = solutions[idx].get(ASSERT_OVERLAY_VAR_NAME)
                    if ovl:
                        # logging.info(str(ovl))
                        # import pdb; pdb.set_trace()
                        ovl.do_apply(CLI_MODULE, self.kernal.db, commit=True)

                    acts = actions[idx]
                    for action in acts:
                        logging.debug("ACTION %s" % repr(action))

                    resp = resps[idx]
                    logging.info('RESP: [%05d] %s ' % (score, u' '.join(resp)))

                    # import pdb; pdb.set_trace()
                            
            except Exception as e:
                logging.error(traceback.format_exc())

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


    @cmdln.option ("-l", "--lang", dest="lang", type = "str", default='en',
           help="language, default: en")
    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    def do_align(self, subcmd, opts, *paths):
        """${cmd_name}: align utterance(s) to db modules

        ${cmd_usage}
        ${cmd_option_list}
        """

        if len(paths) != 1:
            raise Exception ("one argument (utterance or file name) expected")

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        # collect utterances from paths

        utterances = []
        for uttfn in paths:
            with codecs.open(uttfn, 'r', 'utf8') as uttf:
                for line in uttf:
                    utterances.append(line.strip())

        self.kernal.align_utterances(opts.lang, utterances)




#
# init terminal
#

misc.init_app('ai_cli')

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

