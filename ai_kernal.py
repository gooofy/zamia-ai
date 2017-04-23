#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016, 2017 Guenter Bartsch
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
# ai kernal, central hub for all the other components to hook into
#
# natural language -> [ tokenizer ] -> tokens -> [ seq2seq model ] -> prolog -> [ prolog engine ] -> say/action preds
#

import os
import sys
import logging
import traceback
import imp
import time
import random
import codecs
import rdflib

import numpy as np

from sqlalchemy.orm import sessionmaker
import model

from zamiaprolog.logicdb import LogicDB
from zamiaprolog.logic   import StringLiteral, ListLiteral, NumberLiteral, SourceLocation
from zamiaprolog.errors  import PrologError
from aiprolog.pl2rdf     import pl_literal_to_rdf
from aiprolog.runtime    import AIPrologRuntime, CONTEXT_GRAPH_NAME, USER_PREFIX, CURIN, KB_PREFIX, DEFAULT_USER, \
                                TEST_USER, TEST_TIME
from aiprolog.parser     import AIPrologParser

from kb import AIKB
from nltools import misc
from nltools.tokenizer import tokenize

class AIKernal(object):

    def __init__(self):

        self.config = misc.load_config('.airc')

        #
        # database
        #

        Session = sessionmaker(bind=model.engine)
        self.session = Session()

        #
        # logic DB
        #

        self.db = LogicDB(model.url)

        #
        # knowledge base
        #

        self.kb = AIKB()

        #
        # TensorFlow (deferred, as tf can take quite a bit of time to set up)
        #

        self.tf_session = None
        self.nlp_model  = None

        #
        # module management, setup
        #

        self.modules  = {}
        s = self.config.get('semantics', 'modules')
        self.all_modules = map (lambda s: s.strip(), s.split(','))

        #
        # prolog environment setup
        #

        self.prolog_rt = AIPrologRuntime(self.db, self.kb)
        self.parser    = AIPrologParser()


    # FIXME: this will work only on the first call
    def setup_tf_model (self, forward_only, load_model, ini_fn):

        if not self.tf_session:

            import tensorflow as tf

            # setup config to use BFC allocator
            config = tf.ConfigProto()  
            config.gpu_options.allocator_type = 'BFC'

            self.tf_session = tf.Session(config=config)

        if not self.nlp_model:

            from nlp_model import NLPModel

            self.nlp_model = NLPModel(self.session, ini_fn)

            if load_model:

                self.nlp_model.load_dicts()

                # we need the inverse dict to reconstruct the output from tensor

                self.inv_output_dict = {v: k for k, v in self.nlp_model.output_dict.iteritems()}

                self.tf_model = self.nlp_model.create_tf_model(self.tf_session, forward_only = forward_only) 
                self.tf_model.batch_size = 1

                self.nlp_model.load_model(self.tf_session)


    def clean (self, module_names, clean_all, clean_logic, clean_discourses, 
                                   clean_cronjobs, clean_kb):

        for module_name in module_names:

            if clean_logic or clean_all:
                logging.info('cleaning logic for %s...' % module_name)
                if module_name == 'all':
                    self.db.clear_all_modules()
                else:
                    self.db.clear_module(module_name)

            if clean_discourses or clean_all:
                logging.info('cleaning discourses for %s...' % module_name)
                if module_name == 'all':
                    self.session.query(model.DiscourseRound).delete()
                else:
                    self.session.query(model.DiscourseRound).filter(model.DiscourseRound.module==module_name).delete()

            if clean_cronjobs or clean_all:
                logging.info('cleaning cronjobs for %s...' % module_name)
                if module_name == 'all':
                    self.session.query(model.Cronjob).delete()
                else:
                    self.session.query(model.Cronjob).filter(model.Cronjob.module==module_name).delete()

            if clean_kb or clean_all:
                logging.info('cleaning kb for %s...' % module_name)
                if module_name == 'all':
                    self.kb.clear_all_graphs()
                else:
                    graph = self._module_graph_name(module_name)
                    self.kb.clear_graph(graph)

        self.session.commit()

    def load_module (self, module_name, run_init=False, run_trace=False):

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
                self.load_module(m2, run_init=run_init, run_trace=run_trace)

            if hasattr(m, 'RDF_PREFIXES'):
                prefixes = getattr(m, 'RDF_PREFIXES')
                for prefix in prefixes:
                    self.kb.register_prefix(prefix, prefixes[prefix])

            if hasattr(m, 'LDF_ENDPOINTS'):
                endpoints = getattr(m, 'LDF_ENDPOINTS')
                for endpoint in endpoints:
                    self.kb.register_endpoint(endpoint, endpoints[endpoint])

            if hasattr(m, 'RDF_ALIASES'):
                aliases = getattr(m, 'RDF_ALIASES')
                for alias in aliases:
                    self.kb.register_alias(alias, aliases[alias])

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

            if run_init:
                gn = rdflib.Graph(identifier=CONTEXT_GRAPH_NAME)
                self.kb.remove((CURIN, None, None, gn))

                quads = [ ( CURIN, KB_PREFIX+u'user', DEFAULT_USER, gn) ]

                self.kb.addN_resolve(quads)

                prolog_s = u'init(\'%s\')' % (module_name)
                c = self.parser.parse_line_clause_body(prolog_s)

                self.prolog_rt.set_trace(run_trace)

                self.prolog_rt.reset_actions()
            
                solutions = self.prolog_rt.search(c)

                # import pdb; pdb.set_trace()
            
                actions = self.prolog_rt.get_actions()
                for action in actions:
                    self.prolog_rt.execute_builtin_actions(action)


        except:
            logging.error(traceback.format_exc())

        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()

        return m

    def _module_graph_name (self, module_name):
        return KB_PREFIX + module_name

    def import_kb (self, module_name):

        graph = self._module_graph_name(module_name)

        self.kb.register_graph(graph)

        # disabled to enable incremental kb updates self.kb.clear_graph(graph)

        m = self.modules[module_name]

        # import LDF first as it is incremental

        res_paths = []
        for kb_entry in getattr (m, 'KB_SOURCES'):
            if not isinstance(kb_entry, basestring):
                res_paths.append(kb_entry)

        if len(res_paths)>0:
            logging.info('mirroring from LDF endpoints, target graph: %s ...' % graph)
            quads = self.kb.ldf_mirror(res_paths, graph)

        # now import files, if any

        for kb_entry in getattr (m, 'KB_SOURCES'):
            if isinstance(kb_entry, basestring):
                kb_pathname = 'modules/%s/%s' % (module_name, kb_entry)
                logging.info('importing %s ...' % kb_pathname)
                self.kb.parse_file(graph, 'n3', kb_pathname)


    def import_kb_multi (self, module_names):

        for module_name in module_names:

            if module_name == 'all':

                for mn2 in self.all_modules:
                    self.load_module (mn2)
                    self.import_kb (mn2)

            else:

                self.load_module (module_name)

                self.import_kb (module_name)

        self.session.commit()

    def compile_module (self, module_name, trace=False, print_utterances=False, warn_level=0):

        m = self.modules[module_name]

        logging.debug('parsing sources of module %s (print_utterances: %s) ...' % (module_name, print_utterances))

        compiler = AIPrologParser (trace=trace, print_utterances=print_utterances, warn_level=warn_level)

        compiler.clear_module(module_name, self.db)

        for pl_fn in getattr (m, 'PL_SOURCES'):
            
            pl_pathname = 'modules/%s/%s' % (module_name, pl_fn)

            logging.debug('   parsing %s ...' % pl_pathname)
            compiler.compile_file (pl_pathname, module_name, self.db, self.kb)

    def compile_module_multi (self, module_names, run_trace=False, print_utterances=False, warn_level=0):

        for module_name in module_names:

            if module_name == 'all':

                for mn2 in self.all_modules:
                    self.load_module (mn2)
                    self.compile_module (mn2, run_trace, print_utterances, warn_level)

            else:
                self.load_module (module_name)
                self.compile_module (module_name, run_trace, print_utterances, warn_level)

        self.session.commit()

    def process_input (self, utterance, utt_lang, user_uri, test_mode=False, trace=False):

        """ process user input, return action(s) """

        gn = rdflib.Graph(identifier=CONTEXT_GRAPH_NAME)

        tokens = tokenize(utterance, utt_lang)

        self.kb.remove((CURIN, None, None, gn))

        sl = SourceLocation('<input>', 0, 0)

        quads = [ ( CURIN, KB_PREFIX+u'user',      user_uri,                                            gn),
                  ( CURIN, KB_PREFIX+u'utterance', utterance,                                           gn),
                  ( CURIN, KB_PREFIX+u'uttLang',   utt_lang,                                            gn),
                  ( CURIN, KB_PREFIX+u'tokens',    pl_literal_to_rdf(ListLiteral(tokens), self.kb, sl), gn)
                  ]

        if test_mode:
            quads.append( ( CURIN, KB_PREFIX+u'currentTime', pl_literal_to_rdf(NumberLiteral(TEST_TIME), self.kb, sl), gn ) )
        else:
            quads.append( ( CURIN, KB_PREFIX+u'currentTime', pl_literal_to_rdf(NumberLiteral(time.time()), self.kb, sl), gn ) )
   
        self.kb.addN_resolve(quads)

        self.prolog_rt.reset_actions()
        self.prolog_rt.set_trace(trace)

        if test_mode:

            prolog_s = None

            for dr in self.db.session.query(model.DiscourseRound).filter(model.DiscourseRound.inp==utterance, 
                                                                         model.DiscourseRound.lang==utt_lang):
            
                prolog_s = ','.join(dr.resp.split(';'))

                logging.info("test tokens=%s prolog_s=%s" % (repr(tokens), prolog_s) )
                
            if not prolog_s:
                logging.error('test utterance %s not found!' % utterance)
                return []

        else:

            x = self.nlp_model.compute_x(utterance)

            logging.debug("x: %s -> %s" % (utterance, x))

            # which bucket does it belong to?
            bucket_id = min([b for b in xrange(len(self.nlp_model.buckets)) if self.nlp_model.buckets[b][0] > len(x)])

            # get a 1-element batch to feed the sentence to the model
            encoder_inputs, decoder_inputs, target_weights = self.tf_model.get_batch( {bucket_id: [(x, [])]}, bucket_id )

            # print "encoder_inputs, decoder_inputs, target_weights", encoder_inputs, decoder_inputs, target_weights

            # get output logits for the sentence
            _, _, output_logits = self.tf_model.step(self.tf_session, encoder_inputs, decoder_inputs, target_weights, bucket_id, True)

            logging.debug("output_logits: %s" % repr(output_logits))

            # this is a greedy decoder - outputs are just argmaxes of output_logits.
            outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]

            # print "outputs", outputs

            preds = map (lambda o: self.inv_output_dict[o], outputs)
            logging.debug("preds: %s" % repr(preds))

            prolog_s = ''

            do_and = True

            # import pdb; pdb.set_trace()

            for p in preds:

                if p[0] == '_':
                    continue # skip _EOS

                if p == u'or':
                    do_and = False
                    continue

                if len(prolog_s)>0:
                    if do_and:
                        prolog_s += ', '
                    else:
                        prolog_s += '; '
                prolog_s += p

                do_and = True

            logging.debug('?- %s' % prolog_s)

        abufs = []

        c = self.parser.parse_line_clause_body(prolog_s)
        # logging.debug( "Parse result: %s" % c)

        # logging.debug( "Searching for c: %s" % c )

        solutions = self.prolog_rt.search(c)

        # if len(solutions) == 0:
        #     raise PrologError ('nlp_test: %s no solution found.' % clause.location)

        # print "round %d utterances: %s" % (round_num, repr(prolog_rt.get_utterances())) 

        abufs = self.prolog_rt.get_actions()

        return abufs

    def do_eliza (self, utterance, utt_lang, trace=False):

        """ produce eliza-style response """

        logging.info ('producing ELIZA-style response for input %s' % utterance)

        self.prolog_rt.reset_actions()
        self.prolog_rt.set_trace(trace)

        c = self.parser.parse_line_clause_body('answer(dodge_question, %s)' % utt_lang)
        solutions = self.prolog_rt.search(c)
        abufs = self.prolog_rt.get_actions()

        return abufs


    def test_module (self, module_name, trace=False):

        logging.info('running tests of module %s ...' % (module_name))

        gn = rdflib.Graph(identifier=CONTEXT_GRAPH_NAME)

        for nlpt in self.db.session.query(model.NLPTest).filter(model.NLPTest.module==module_name):

            # import pdb; pdb.set_trace()
        
            # test setup predicate for this module

            self.kb.remove((CURIN, None, None, gn))

            quads = [ ( CURIN, KB_PREFIX+u'user', TEST_USER, gn) ]

            self.kb.addN_resolve(quads)

            prolog_s = u'test_setup(\'%s\')' % (module_name)
            c = self.parser.parse_line_clause_body(prolog_s)

            self.prolog_rt.set_trace(trace)

            self.prolog_rt.reset_actions()
        
            solutions = self.prolog_rt.search(c)

            actions = self.prolog_rt.get_actions()
            for action in actions:
                self.prolog_rt.execute_builtin_actions(action)

            # extract test rounds, look up matching discourse_rounds, execute them

            clause = self.parser.parse_line_clause_body(nlpt.test_src)
            clause.location = nlpt.location
            logging.debug( "Parse result: %s (%s)" % (clause, clause.__class__))

            args = clause.body.args
            lang = args[0].name

            round_num = 0
            for ivr in args[1:]:

                if ivr.name != 'ivr':
                    raise PrologError ('nlp_test: ivr predicate args expected.')

                test_in = ''
                test_out = ''
                test_actions = []

                for e in ivr.args:

                    if e.name == 'in':
                        test_in = ' '.join(tokenize(e.args[0].s, lang))
                    elif e.name == 'out':
                        test_out = ' '.join(tokenize(e.args[0].s, lang))
                    elif e.name == 'action':
                        test_actions.append(e.args)
                    else:
                        raise PrologError (u'nlp_test: ivr predicate: unexpected arg: ' + unicode(e))
                   
                logging.info("nlp_test: %s round %d test_in     : %s" % (clause.location, round_num, test_in) )
                logging.info("nlp_test: %s round %d test_out    : %s" % (clause.location, round_num, test_out) )
                logging.info("nlp_test: %s round %d test_actions: %s" % (clause.location, round_num, test_actions) )

                # execute all matching clauses, collect actions

                # FIXME: nlp_test should probably let the user specify a user
                action_buffers = self.process_input (test_in, lang, TEST_USER, test_mode=True, trace=trace)

                # check actual actions vs expected ones
                matching_abuf = None
                for abuf in action_buffers:

                    logging.info("nlp_test: %s round %d %s" % (clause.location, round_num, repr(abuf)) )

                    # check utterance

                    actual_out = u''
                    utt_lang   = u'en'
                    for action in abuf['actions']:
                        p = action[0].name
                        if p == 'say':
                            utt_lang = unicode(action[1])
                            actual_out += u' ' + unicode(action[2])

                    if len(test_out) > 0:
                        if len(actual_out)>0:
                            actual_out = u' '.join(tokenize(actual_out, utt_lang))
                        if actual_out != test_out:
                            logging.info("nlp_test: %s round %d UTTERANCE MISMATCH." % (clause.location, round_num))
                            continue # no match

                    logging.info("nlp_test: %s round %d UTTERANCE MATCHED!" % (clause.location, round_num))

                    # check actions

                    if len(test_actions)>0:

                        # import pdb; pdb.set_trace()

                        # print repr(test_actions)

                        actions_matched = True
                        for action in test_actions:
                            for act in abuf['actions']:
                                # print "    check action match: %s vs %s" % (repr(action), repr(act))
                                if action == act:
                                    break
                            if action != act:
                                actions_matched = False
                                break

                        if not actions_matched:
                            logging.info("nlp_test: %s round %d ACTIONS MISMATCH." % (clause.location, round_num))
                            continue

                        logging.info("nlp_test: %s round %d ACTIONS MATCHED!" % (clause.location, round_num))

                    matching_abuf = abuf
                    break

                if not matching_abuf:
                    raise PrologError (u'nlp_test: %s round %d no matching abuf found.' % (clause.location, round_num))
               
                self.prolog_rt.execute_builtin_actions(matching_abuf)

                round_num += 1

        logging.info('running tests of module %s complete!' % (module_name))

    def run_tests_multi (self, module_names, run_trace=False):

        for module_name in module_names:

            if module_name == 'all':

                for mn2 in self.all_modules:
                    self.load_module (mn2, run_init=True, run_trace=run_trace)
                    self.test_module (mn2, run_trace)

            else:
                self.load_module (module_name, run_init=True, run_trace=run_trace)
                self.test_module (module_name, run_trace)


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
                f (self.config, self.kb, graph)

                cronjob.last_run = t

    def run_cronjobs_multi (self, module_names, force, run_trace=False):

        for module_name in module_names:

            if module_name == 'all':

                for mn2 in self.all_modules:
                    self.load_module (mn2, run_init=True, run_trace=run_trace)
                    self.run_cronjobs (mn2, force=force)

            else:
                self.load_module (module_name, run_init=True, run_trace=run_trace)
                self.run_cronjobs (module_name, force=force)

        self.session.commit()

    def train (self, ini_fn):

        self.setup_tf_model (False, False, ini_fn)
        self.nlp_model.train()


    def dump_utterances (self, num_utterances, dictfn, lang, module):

        dic = None
        if dictfn:
            dic = set()
            with codecs.open(dictfn, 'r', 'utf8') as dictf:
                for line in dictf:
                    parts = line.strip().split(';')
                    if len(parts) != 2:
                        continue
                    dic.add(parts[0])

        all_utterances = []

        req = self.session.query(model.DiscourseRound).filter(model.DiscourseRound.lang==lang)

        if module and module != 'all':
            req = req.filter(model.DiscourseRound.module==module)

        for dr in req:

            if not dic:
                all_utterances.append(dr.inp)
            else:

                # is at least one word not covered by our dictionary?

                unk = False
                for t in tokenize(dr.inp):
                    if not t in dic:
                        # print u"unknown word: %s in %s" % (t, dr.inp)
                        unk = True
                        dic.add(t)
                        break
                if not unk:
                    continue

                all_utterances.append(dr.inp)

        utts = set()

        if num_utterances > 0:

            while (len(utts) < num_utterances):

                i = random.randrange(0, len(all_utterances))
                utts.add(all_utterances[i])

        else:
            for utt in all_utterances:
                utts.add(utt)
                
        for utt in utts:
            print utt



