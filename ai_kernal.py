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
from zamiaprolog.errors  import PrologError
from aiprolog.runtime    import AIPrologRuntime
from aiprolog.parser     import AIPrologParser

from kb import HALKB
from nltools import misc
from nltools.tokenizer import tokenize

GRAPH_PREFIX       = u'http://hal.zamia.org/kb/'

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

        self.kb = HALKB()

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

        for mn2 in self.all_modules:
            self.load_module (mn2)

        #
        # prolog environment setup
        #

        self.prolog_rt = AIPrologRuntime(self.db, self.kb)
        self.parser    = AIPrologParser()


    # FIXME: this will work only on the first call
    def setup_tf_model (self, forward_only, load_model):

        if not self.tf_session:

            import tensorflow as tf

            # setup config to use BFC allocator
            config = tf.ConfigProto()  
            config.gpu_options.allocator_type = 'BFC'

            self.tf_session = tf.Session(config=config)

        if not self.nlp_model:

            from nlp_model import NLPModel

            self.nlp_model = NLPModel(self.session)

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

    def compile_module (self, module_name, trace=False, run_tests=False, print_utterances=False, warn_level=0):

        m = self.modules[module_name]

        logging.debug('parsing sources of module %s (print_utterances: %s) ...' % (module_name, print_utterances))

        compiler = AIPrologParser (trace=trace, run_tests=run_tests, print_utterances=print_utterances, warn_level=warn_level)

        compiler.clear_module(module_name, self.db)

        for pl_fn in getattr (m, 'PL_SOURCES'):
            
            pl_pathname = 'modules/%s/%s' % (module_name, pl_fn)

            logging.debug('   parsing %s ...' % pl_pathname)
            compiler.compile_file (pl_pathname, module_name, self.db, self.kb)

    def compile_module_multi (self, module_names, run_trace=False, run_tests=False, print_utterances=False, warn_level=0):

        for module_name in module_names:

            if module_name == 'all':

                for mn2 in self.all_modules:
                    self.load_module (mn2)
                    self.compile_module (mn2, run_trace, run_tests, print_utterances, warn_level)

            else:
                self.load_module (module_name)
                self.compile_module (module_name, run_trace, run_tests, print_utterances, warn_level)

        self.session.commit()

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

    def run_cronjobs_multi (self, module_names, force):

        for module_name in module_names:

            if module_name == 'all':

                for mn2 in self.all_modules:
                    self.load_module (mn2)
                    self.run_cronjobs (mn2, force=force)

            else:
                self.load_module (module_name)
                self.run_cronjobs (module_name, force=force)

        self.session.commit()

    def train (self, num_steps):

        self.setup_tf_model (False, False)
        self.nlp_model.train(num_steps)


    def process_line(self, line):

        self.setup_tf_model (True, True)
        from nlp_model import BUCKETS

        x = self.nlp_model.compute_x(line)

        logging.debug("x: %s -> %s" % (line, x))

        # which bucket does it belong to?
        bucket_id = min([b for b in xrange(len(BUCKETS)) if BUCKETS[b][0] > len(x)])

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

        for p in preds:

            if p[0] == '_':
                continue # skip _EOS

            if len(prolog_s)>0:
                prolog_s += ', '
            prolog_s += p

        logging.debug('?- %s' % prolog_s)

        try:
            c = self.parser.parse_line_clause_body(prolog_s)
            logging.debug( "Parse result: %s" % c)

            self.prolog_rt.reset_actions()

            self.prolog_rt.search(c)

            abufs = self.prolog_rt.get_actions()

            # if we have multiple abufs, pick one at random

            if len(abufs)>0:

                abuf = random.choice(abufs)

                self.prolog_rt.execute_builtin_actions(abuf)

                self.db.commit()

                return abuf

        except PrologError as e:

            logging.error("*** ERROR: %s" % e)

        return None

    def dump_utterances (self, num_utterances, dictfn):

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

        for dr in self.session.query(model.DiscourseRound):

            if not dic:
                all_utterances.append(dr.inp)
            else:

                # is at least one word not covered by our dictionary?

                unk = False
                for t in tokenize(dr.inp):
                    if not t in dic:
                        # print u"unknown word: %s in %s" % (t, dr.inp)
                        unk = True
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



