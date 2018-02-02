#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
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
# consolidated shell for Zamia AI
#

import os
import sys
import traceback
import codecs
import logging
import cmdln
import random
import time
import readline
import atexit

from six.moves            import input

from zamiaai.ai_kernal    import AIKernal, AIContext, USER_PREFIX, LANGUAGES
from nltools              import misc
from xsbprolog            import xsb_hl_query_string

DEFAULT_LOGLEVEL   = logging.INFO
CLI_REALM          = '__cli__'

class AICli(cmdln.Cmdln):

    name = "ai_cli"

    def __init__(self):
       
        cmdln.Cmdln.__init__(self)

        self.config = misc.load_config('.airc')
        toplevel    = self.config.get('semantics', 'toplevel')
        xsb_root    = self.config.get('semantics', 'xsb_root')
        db_url      = self.config.get('db', 'url')

        self.kernal = AIKernal(db_url, xsb_root, toplevel)

    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    def do_clean(self, subcmd, opts, *module_names):
        """${cmd_name}: clean module related data

        ${cmd_usage}
        ${cmd_option_list}
        """

        if len(module_names)==0:
            logging.error ('specify at least one module name or "all" to clean all modules')
            return

        if len(module_names)==1 and module_names[0] == 'all':
            module_names = self.kernal.all_modules

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        else:
            logging.getLogger().setLevel(logging.INFO)

        self.kernal.clean(module_names)

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option("-g", "--trace", dest="run_trace", action="store_true",
           help="enable tracing when running tests")
    @cmdln.option("-t", "--test", dest="run_tests", action="store_true",
           help="run tests")
    @cmdln.option("-N", "--test-name", dest="test_name", type="str",
           help="run specific test only, default: all tests are run")
    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="enable verbose logging")
    def do_compile(self, subcmd, opts, *module_names):
        """${cmd_name}: compile module(s)

        ${cmd_usage}
        ${cmd_option_list}
        """

        if len(module_names)==0:
            logging.error ('specify at least one module name')
            return

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        try:
            self.kernal.compile_module_multi (module_names)

            if opts.run_tests:
                num_tests, num_fails = self.kernal.run_tests_multi (module_names, run_trace=opts.run_trace, test_name=opts.test_name)

                if num_fails:
                    logging.error('%d test(s) failed out of %d test(s) run.' % (num_fails, num_tests))
                else:
                    logging.info('all %d test(s) worked!' % num_tests)

        except:
            logging.error(traceback.format_exc())

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option("-g", "--trace", dest="run_trace", action="store_true",
           help="enable tracing")
    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    @cmdln.option("-N", "--test-name", dest="test_name", type="str",
           help="run specific test only, default: all tests are run")
    def do_test(self, subcmd, opts, *module_names):
        """${cmd_name}: run tests from module(s)

        ${cmd_usage}
        ${cmd_option_list}
        """

        if len(module_names)==0:
            logging.error ('specify at least one module name (or all to run tests from all modules)')
            return

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.debug('verbose logging enabled.')
        else:
            logging.getLogger().setLevel(logging.INFO)

        try:
            num_tests, num_fails = self.kernal.run_tests_multi (module_names, run_trace=opts.run_trace, test_name=opts.test_name)
            if num_fails:
                logging.error('%d test(s) failed out of %d test(s) run.' % (num_fails, num_tests))
            else:
                logging.info('all %d test(s) worked!' % num_tests)

        except PrologError as e:
            logging.error("*** ERROR: %s" % e)

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
    @cmdln.option("-l", "--lang", dest="lang", type = "str", default='en',
           help="language")
    @cmdln.option("-m", "--model", dest="model", type = "str", default=None,
           help="model to load, default: DB lookups only")
    @cmdln.option("-u", "--user", dest="username", type = "str", default="chat",
           help="username, default: chat")
    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    def do_chat(self, subcmd, opts, *models):
        """${cmd_name}: chat with model in natural language

        ${cmd_usage}
        ${cmd_option_list}
        """

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

        for mn2 in self.kernal.all_modules:
            self.kernal.consult_module (mn2)

        if opts.model:
            self.kernal.setup_tf_model('decode', True, opts.model)
            lang = self.kernal.nlp_model.lang
        else:
            lang = opts.lang

        user_uri = USER_PREFIX + opts.username
        ctx      = AIContext(user_uri, self.kernal.session, lang, CLI_REALM, self.kernal, test_mode=False)

        while True:

            line = input ('ai> ')

            if line == 'quit' or line == 'exit':
                break

            out, score, action, action_arg = self.kernal.process_input(ctx, line, lang, user_uri, run_trace=opts.run_trace)

            logging.info(u'RESP: [%6.1f] %s ' % (score, out))

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

    @cmdln.option ("-d", "--dict", dest="dictfn", type = "str", default=None,
           help="dictionary to use to detect unknown words, default: none")
    @cmdln.option ("-l", "--lang", dest="lang", type = "str", default='en',
           help="language, default: en")
    @cmdln.option ("-m", "--module", dest="module", type = "str", default='all',
           help="extract utterances from specific module only, default: all modules")
    @cmdln.option ("-n", "--num-utterances", dest="num_utterances", type = "int", default=0,
           help="number of utterances to extract, default: 0 (all)")
    def do_utterances(self, subcmd, opts):
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


    def do_prolog(self, subcmd, opts, *module_names):
        """${cmd_name}: open prolog shell for debugging

        ${cmd_usage}
        ${cmd_option_list}
        """

        if len(module_names) == 0:
            for mn2 in self.kernal.all_modules:
                self.kernal.consult_module (mn2)
        else:
            self.kernal.consult_module (module_names[0])

        histfile = os.path.join(os.path.expanduser("~"), ".xsb_hist")
        try:
            readline.read_history_file(histfile)
            # default history len is -1 (infinite), which may grow unruly
            readline.set_history_length(1000)
        except IOError:
            pass
        atexit.register(readline.write_history_file, histfile)

        while True:

            line = input ('prolog> ')

            if line == 'quit' or line == 'exit':
                break

            try:
                for res in xsb_hl_query_string(line):
                    logging.info('  %s' % repr(res))

            except Exception as e:
                logging.error(traceback.format_exc())

    @cmdln.option("-v", "--verbose", dest="verbose", action="store_true",
           help="verbose logging")
    def do_stats(self, subcmd, opts):
        """${cmd_name}: print DB statistics

        ${cmd_usage}
        ${cmd_option_list}
        """

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        else:
            logging.getLogger().setLevel(logging.INFO)

        stats = self.kernal.stats()

        totals = {}
        for m in stats:
            for lang in stats[m]:
                if not lang in totals:
                    totals[lang] = 0
                totals[lang] += stats[m][lang]

        stats2 = []

        for m in stats:

            s = '%-20s' % m

            for lang in LANGUAGES:
                s += '%3s:%9d (%5.1f%%)' % (lang, stats[m][lang], stats[m][lang]*100.0/totals[lang])
    
            stats2.append((s, stats[m]['en']))

        for t in sorted(stats2, key=lambda tup: tup[1]):
            logging.info(t[0])

        logging.getLogger().setLevel(DEFAULT_LOGLEVEL)

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

