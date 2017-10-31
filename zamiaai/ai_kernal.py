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
# natural language -> [ tokenizer ] -> tokens -> [ seq2seq model ] -> AIProlog -> [ Context ] -> actions/says
#

from __future__ import print_function

import os
import sys
import logging
import traceback
import imp
import time
import random
import codecs
import datetime
import pytz
import json

import numpy as np

from six                    import viewitems
from tzlocal                import get_localzone # $ pip install tzlocal
from copy                   import deepcopy, copy
from sqlalchemy.orm         import sessionmaker
from six                    import text_type
from scipy.spatial.distance import cosine
from threading              import RLock, Lock

from zamiaai                import model

from aiprolog.runtime       import AIPrologRuntime, USER_PREFIX, DEFAULT_USER
from aiprolog.parser        import AIPrologParser
from zamiaprolog.logicdb    import LogicDB
from zamiaprolog.builtins   import do_gensym, do_assertz, ASSERT_OVERLAY_VAR_NAME
from zamiaprolog.logic      import Clause, Predicate, StringLiteral, NumberLiteral, ListLiteral, Literal, SourceLocation, \
                                   json_to_prolog, prolog_to_json
from zamiaprolog.errors     import PrologRuntimeError
from nltools                import misc
from nltools.tokenizer      import tokenize
from nltools.tts            import TTS
from kaldisimple.nnet3      import KaldiNNet3OnlineModel, KaldiNNet3OnlineDecoder

TEST_USER          = USER_PREFIX + u'Test'
TEST_TIME          = datetime.datetime(2016,12,6,13,28,6,tzinfo=get_localzone()).isoformat()
TEST_MODULE        = '__test__'

def avg_feature_vector(words, model, num_features, index2word_set):
    #function to average all words vectors in a given paragraph
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0

    for word in words:
        if word in index2word_set:
            nwords = nwords+1
            featureVec = np.add(featureVec, model[word])

    if nwords > 0:
        featureVec = np.divide(featureVec, nwords)
    return featureVec

class AIKernal(object):

    def __init__(self, load_all_modules=False):

        self.config = misc.load_config('.airc')

        #
        # database
        #

        Session = sessionmaker(bind=model.engine)
        self.session = Session()

        #
        # TensorFlow (deferred, as tf can take quite a bit of time to set up)
        #

        self.tf_session = None
        self.nlp_model  = None

        #
        # module management, setup
        #

        self.modules             = {}
        self.initialized_modules = set()
        s = self.config.get('semantics', 'modules')
        self.all_modules         = list(map (lambda s: s.strip(), s.split(',')))
        sys.path.append('modules')

        #
        # AIProlog parser, runtime
        #

        db_url          = self.config.get('db', 'url')
        self.db         = LogicDB(db_url)
        self.aip_parser = AIPrologParser(self)
        self.rt         = AIPrologRuntime(self.db)
        self.dummyloc   = SourceLocation ('<rt>')

        #
        # alignment / word2vec (on-demand model loading)
        #
        self.w2v_model          = None
        self.w2v_lang           = None
        self.w2v_all_utterances = []

        #
        # load modules, if requested
        #
        if load_all_modules:
            for mn2 in self.all_modules:
                self.load_module (mn2)
                self.init_module (mn2)

    # FIXME: this will work only on the first call
    def setup_tf_model (self, mode, load_model, ini_fn, global_step=0):

        if not self.tf_session:

            import tensorflow as tf

            # setup config to use BFC allocator
            config = tf.ConfigProto()  
            # config.gpu_options.allocator_type = 'BFC'

            self.tf_session = tf.Session(config=config)

        if not self.nlp_model:

            from nlp_model import NLPModel

            self.nlp_model = NLPModel(self.session, ini_fn, global_step = global_step)

            if load_model:

                self.nlp_model.load_dicts()

                # we need the inverse dict to reconstruct the output from tensor

                self.inv_output_dict = {v: k for k, v in viewitems(self.nlp_model.output_dict)}

                self.tf_model = self.nlp_model.create_tf_model(self.tf_session, mode = mode) 
                self.tf_model.batch_size = 1

                self.tf_model.restore(self.tf_session, self.nlp_model.model_fn)


    def clean (self, module_names, clean_all, clean_logic, clean_discourses, 
                                   clean_cronjobs):

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

        self.session.commit()

    def load_module (self, module_name):

        if module_name in self.modules:
            return self.modules[module_name]

        logging.debug("loading module '%s'" % module_name)

        # fp, pathname, description = imp.find_module(module_name, ['modules'])
        fp, pathname, description = imp.find_module(module_name)

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

            if hasattr(m, 'init_module'):
                initializer = getattr(m, 'init_module')
                initializer(self)

        except:
            logging.error('failed to load module "%s"' % module_name)
            logging.error(traceback.format_exc())
            sys.exit(1)

        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()

        return m

    def init_module (self, module_name, run_trace=False):

        if module_name in self.initialized_modules:
            return

        logging.debug("initializing module '%s'" % module_name)

        self.initialized_modules.add(module_name)

        m = self.load_module(module_name)

        if not m:
            raise Exception ('init_module: module "%s" not found.' % module_name)

        for m2 in getattr (m, 'DEPENDS'):
            self.init_module(m2)

        prolog_s = u'init(\'%s\')' % (module_name)
        c = self.aip_parser.parse_line_clause_body(prolog_s)

        self.rt.set_trace(run_trace)

        solutions = self.rt.search(c)

    def compile_module (self, module_name):

        m = self.modules[module_name]

        # clear module, delete old NLP training data

        self.db.clear_module(module_name, commit=True)
        self.session.query(model.TrainingData).filter(model.TrainingData.module==module_name).delete()
        self.session.query(model.TestCase).filter(model.TestCase.module==module_name).delete()
        self.session.query(model.NERData).filter(model.NERData.module==module_name).delete()

        # extract new training data for this module

        train_ds = []
        tests    = []
        ner      = {}

        if hasattr(m, 'nlp_train'):

            # training_data_cnt = 0

            logging.info ('module %s python training data extraction...' % module_name)

            nlp_train = getattr(m, 'nlp_train')
            train_ds.extend(nlp_train(self))

        if hasattr(m, 'nlp_test'):

            logging.info ('module %s python test case extraction...' % module_name)

            nlp_test = getattr(m, 'nlp_test')
            nlp_tests = nlp_test(self)
            tests.extend(nlp_tests)

        if hasattr(m, 'AIP_SOURCES'):

            logging.info ('module %s AIP training data extraction...' % module_name)

            for inputfn in m.AIP_SOURCES:
                ds, ts, ne = self.aip_parser.compile_file('modules/%s/%s' % (module_name, inputfn), module_name)

                train_ds.extend(ds)
                tests.extend(ts)

                for lang in ne:
                    if not lang in ner:
                        ner[lang] = {}
                    for cls in ne[lang]:
                        if not cls in ner[lang]:
                            ner[lang][cls] = {}
                        for entity in ne[lang][cls]:
                            ner[lang][cls][entity] = ne[lang][cls][entity]

        logging.info ('module %s training data extraction done. %d training samples, %d tests' % (module_name, len(train_ds), len(tests)))

        # put training data into our DB

        td_set  = set()
        td_list = []

        for utt_lang, contexts, i, resp, loc_fn, loc_line, loc_col, prio in train_ds:

            inp = copy(contexts)
            inp.extend(i)

            inp_json  = json.dumps(inp)
            resp_json = json.dumps(resp)

            # utterance = u' '.join(map(lambda c: text_type(c), contexts))
            # if utterance:
            #     utterance += u' '
            # utterance += u' '.join(i)
            utterance = u' '.join(i)

            k = utt_lang + '#0#' + '#' + inp_json + '#' + resp_json
            if not k in td_set:
                td_set.add(k)
                td_list.append(model.TrainingData(lang      = utt_lang,
                                                  module    = module_name,
                                                  utterance = utterance,
                                                  inp       = inp_json,
                                                  resp      = resp_json,

                                                  prio      = prio,

                                                  loc_fn    = loc_fn,
                                                  loc_line  = loc_line,
                                                  loc_col   = loc_col,
                                                  ))

        logging.info ('module %s training data conversion done. %d unique training samples.' %(module_name, len(td_list)))

        start_time = time.time()
        logging.info (u'bulk saving to db...')
        self.session.bulk_save_objects(td_list)
        self.session.commit()
        logging.info (u'bulk saving to db... done. Took %fs.' % (time.time()-start_time))

        # put test data into our DB

        td_list = []

        for name, lang, prep, rounds, loc_fn, loc_line, loc_col in tests:

            prep_json   = prolog_to_json(prep)
            rounds_json = json.dumps(rounds)

            td_list.append(model.TestCase(lang      = lang,
                                          module    = module_name,
                                          name      = name,
                                          prep      = prep_json,
                                          rounds    = rounds_json,
                                          loc_fn    = loc_fn,
                                          loc_line  = loc_line,
                                          loc_col   = loc_col))

        logging.info ('module %s test data conversion done. %d tests.' %(module_name, len(td_list)))

        start_time = time.time()
        logging.info (u'bulk saving to db...')
        self.session.bulk_save_objects(td_list)
        self.session.commit()
        logging.info (u'bulk saving to db... done. Took %fs.' % (time.time()-start_time))

        # put NER data into our DB

        # import pdb; pdb.set_trace()

        ner_list = []

        for lang in ner:
            for cls in ner[lang]:
                for entity in ner[lang][cls]:
                    ner_list.append(model.NERData(lang      = lang,
                                                  module    = module_name,
                                                  cls       = cls,
                                                  entity    = entity,
                                                  label     = ner[lang][cls][entity]))

        logging.info ('module %s NER data conversion done. %d rows.' %(module_name, len(ner_list)))

        start_time = time.time()
        logging.info (u'bulk saving to db...')
        self.session.bulk_save_objects(ner_list)
        self.session.commit()
        logging.info (u'bulk saving to db... done. Took %fs.' % (time.time()-start_time))

        self.session.commit()

    def compile_module_multi (self, module_names):

        for module_name in module_names:

            if module_name == 'all':

                for mn2 in self.all_modules:
                    self.load_module (mn2)
                    self.compile_module (mn2)

            else:
                self.load_module (module_name)
                self.compile_module (module_name)

        self.session.commit()

    # _IGNORE_CONTEXT_KEYS = set([ 'user', 'lang', 'tokens', 'time', 'prev', 'resp' ])

    def _compute_net_input (self, res, cur_context):

        solutions = self.rt.search_predicate ('tokens', [cur_context, '_1'], env=res)
        tokens = solutions[0]['_1'].l

        solutions = self.rt.search_predicate ('context', [cur_context, '_2', '_3'], env=res)
        d = {}
        for s in solutions:

            k = s['_2']
            if not isinstance(k, Predicate):
                continue
            k = k.name

            v = s['_3']
            if isinstance(v, Predicate):
                v = v.name
            elif isinstance(v, StringLiteral):
                v = v.s
            else:
                v = text_type(v)

            d[k] = v

        # import pdb; pdb.set_trace()
        inp = []
        for t in reversed(tokens):
            inp.insert(0, t.s)

        for k in sorted(list(d)):
            inp.insert(0, [k, d[k]])

        return inp

    def find_prev_context (self, user, env={}):

        pc    = None
        ctxid = 0

        # logging.debug ('find_prev_context: user=%s' % user)

        for s in self.rt.search_predicate('user', ['_1', Predicate(user)], env=env):

            cid = int (s['_1'].name[7:])
            if not pc or cid>ctxid:
                pc = s['_1']
            # logging.debug ('find_prev_context: s=%s, pc=%s' % (unicode(s), unicode(pc)))

        return pc

    def _setup_context (self, user, lang, inp, prev_context, prev_res):

        cur_context = Predicate(do_gensym (self.rt, 'context'))
        res = { }
        if ASSERT_OVERLAY_VAR_NAME in prev_res:
            res[ASSERT_OVERLAY_VAR_NAME] = prev_res[ASSERT_OVERLAY_VAR_NAME].clone()

        res = do_assertz ({}, Clause ( Predicate('user',   [cur_context, Predicate(user)])  , location=self.dummyloc), res=res)
        res = do_assertz ({}, Clause ( Predicate('lang',   [cur_context, Predicate(lang)])  , location=self.dummyloc), res=res)

        token_literal = ListLiteral (list(map(lambda x: StringLiteral(x), inp)))
        res = do_assertz ({}, Clause ( Predicate('tokens', [cur_context, token_literal])    , location=self.dummyloc), res=res)

        currentTime = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat()
        res = do_assertz ({}, Clause ( Predicate('time',   [cur_context, StringLiteral(currentTime)]) , location=self.dummyloc), res=res)

        if prev_context:

            res = do_assertz ({}, Clause ( Predicate('prev', [cur_context, prev_context]) , location=self.dummyloc), res=res)

            # copy over all previous context statements to the new one
            s1s = self.rt.search_predicate ('context', [prev_context, '_1', '_2'], env=res)
            for s1 in s1s:
                res = do_assertz ({}, Clause ( Predicate('context', [cur_context, s1['_1'], s1['_2']]) , location=self.dummyloc), res=res)
            # copy over all previous mem statements to the new one
            s1s = self.rt.search_predicate ('mem', [prev_context, '_1', '_2'], env=res)
            for s1 in s1s:
                res = do_assertz ({}, Clause ( Predicate('mem', [cur_context, s1['_1'], s1['_2']]) , location=self.dummyloc), res=res)
            # import pdb; pdb.set_trace()

        res['C'] = cur_context

        return res, cur_context

    def _extract_response (self, cur_context, env):

        #import pdb; pdb.set_trace()

        res       = []
        s2s = self.rt.search_predicate ('c_say', [cur_context, '_1'], env=env)
        for s2 in s2s:
            if not '_1' in s2:
                continue
            res.append(s2['_1'].s)

        actions   = []
        s2s = self.rt.search_predicate ('c_action', [cur_context, '_1'], env=env)
        for s2 in s2s:
            if not '_1' in s2:
                continue
            actions.append(list(map (lambda x: text_type(x), s2['_1'].l)))

        score     = 0.0
        s2s = self.rt.search_predicate ('c_score', [cur_context, '_1'], env=env)
        for s2 in s2s:
            if not '_1' in s2:
                continue
            score += s2['_1'].f

        return res, actions, score

    def _reconstruct_prolog_code (self, acode):

        todo = [('and', [])]

        idx = 0
        while idx < len(acode):

            a = acode[idx]
            if a == 'or(':
                todo.append (('or', []))
            elif a == 'and(':
                todo.append (('and', []))
            elif a == ')':
                c = todo.pop()
                todo[len(todo)-1][1].append(Predicate (c[0], c[1]))
            else:

                clause = self.aip_parser.parse_line_clause_body (a)

                todo[len(todo)-1][1].append(clause.body)

            idx += 1

        if len(todo) != 1:
            logging.warn ('unbalanced acode detected.')
            return None

        c = todo.pop()
        return Predicate (c[0], c[1])

    def test_module (self, module_name, run_trace=False, test_name=None):

        self.rt.set_trace(run_trace)

        m = self.modules[module_name]

        logging.info('running tests of module %s ...' % (module_name))

        num_tests = 0
        num_fails = 0
        for tc in self.session.query(model.TestCase).filter(model.TestCase.module==module_name):

            if test_name:
                if tc.name != test_name:
                    logging.info ('skipping test %s' % tc.name)
                    continue

            num_tests += 1

            rounds = json.loads(tc.rounds)
            prep   = json_to_prolog(tc.prep)

            round_num    = 0
            prev_context = None
            res          = {}

            for t_in, t_out, test_actions in rounds:
               
                test_in  = u' '.join(t_in)
                test_out = u' '.join(t_out)

                logging.info("nlp_test: %s round %d test_in     : %s" % (tc.name, round_num, repr(test_in)) )
                logging.info("nlp_test: %s round %d test_out    : %s" % (tc.name, round_num, repr(test_out)) )
                logging.info("nlp_test: %s round %d test_actions: %s" % (tc.name, round_num, repr(test_actions)) )

                #if round_num>0:
                #    import pdb; pdb.set_trace()
                res, cur_context = self._setup_context ( user          = TEST_USER, 
                                                         lang          = tc.lang, 
                                                         inp           = t_in,
                                                         prev_context  = prev_context,
                                                         prev_res      = res)
                # prep

                if prep:
                    # import pdb; pdb.set_trace()
                    # self.rt.set_trace(True)
                    for p in prep:
                        solutions = self.rt.search (Clause(None, p, location=self.dummyloc), env=res)
                        if len(solutions) != 1:
                            raise(PrologRuntimeError('Expected exactly one solution from preparation code for test "%s", got %d.' % (tc.name, len(solutions))))
                        res = solutions[0]

                # inp / resp

                inp = self._compute_net_input (res, cur_context)

                # look up code in DB

                acode         = None
                matching_resp = False
                for tdr in self.session.query(model.TrainingData).filter(model.TrainingData.lang  == tc.lang,
                                                                         model.TrainingData.inp   == json.dumps(inp)):
                    if acode:
                        logging.warn (u'%s: more than one acode for test_in "%s" found in DB!' % (tc.name, test_in))

                    acode     = json.loads (tdr.resp)
                    pcode     = self._reconstruct_prolog_code (acode)
                    clause    = Clause (None, pcode, location=self.dummyloc)
                    solutions = self.rt.search (clause, env=res)
                    # import pdb; pdb.set_trace()

                    for solution in solutions:

                        actual_out, actual_actions, score = self._extract_response (cur_context, solution)

                        # logging.info("nlp_test: %s round %d %s" % (clause.location, round_num, repr(abuf)) )

                        if len(test_out) > 0:
                            if len(actual_out)>0:
                                actual_out = u' '.join(tokenize(u' '.join(actual_out), tc.lang))
                            logging.info("nlp_test: %s round %d actual_out  : %s (score: %f)" % (tc.name, round_num, actual_out, score) )
                            if actual_out != test_out:
                                logging.info("nlp_test: %s round %d UTTERANCE MISMATCH." % (tc.name, round_num))
                                continue # no match

                        logging.info("nlp_test: %s round %d UTTERANCE MATCHED!" % (tc.name, round_num))

                        # check actions

                        if len(test_actions)>0:

                            logging.info("nlp_test: %s round %d actual acts : %s" % (tc.name, round_num, repr(actual_actions)) )
                            # print repr(test_actions)

                            actions_matched = True
                            act             = None
                            for action in test_actions:
                                for act in actual_actions:
                                    # print "    check action match: %s vs %s" % (repr(action), repr(act))
                                    if action == act:
                                        break
                                if action != act:
                                    actions_matched = False
                                    break

                            if not actions_matched:
                                logging.info("nlp_test: %s round %d ACTIONS MISMATCH." % (tc.name, round_num))
                                continue

                            logging.info("nlp_test: %s round %d ACTIONS MATCHED!" % (tc.name, round_num))

                        matching_resp = True
                        res           = solution
                        break

                    if matching_resp:
                        break

                if acode is None:
                    logging.error('failed to find db entry for %s' % json.dumps(inp))
                    logging.error (u'Error: %s: no training data for test_in "%s" found in DB!' % (tc.name, test_in))
                    num_fails += 1
                    break

                if not matching_resp:
                    logging.error (u'nlp_test: %s round %d no matching response found.' % (tc.name, round_num))
                    num_fails += 1
                    break

                prev_context = cur_context
                round_num   += 1

        self.rt.set_trace(False)

        return num_tests, num_fails

    def run_tests_multi (self, module_names, run_trace=False, test_name=None):

        num_tests = 0
        num_fails = 0

        for module_name in module_names:

            if module_name == 'all':

                for mn2 in self.all_modules:
                    self.load_module (mn2)
                    self.init_module (mn2, run_trace=run_trace)
                    n, f = self.test_module (mn2, run_trace=run_trace, test_name=test_name)
                    num_tests += n
                    num_fails += f

            else:
                self.load_module (module_name)
                self.init_module (module_name, run_trace=run_trace)
                n, f = self.test_module (module_name, run_trace=run_trace, test_name=test_name)
                num_tests += n
                num_fails += f

        return num_tests, num_fails

    def _process_input_nnet (self, inp, res):

        solutions = []

        logging.debug('_process_input_nnet: %s' % repr(inp))

        try:

            # ok, exact matching has not yielded any results -> use neural network to
            # generate response(s)

            x = self.nlp_model.compute_x(inp)

            # logging.debug("x: %s -> %s" % (utterance, x))

            source, source_len, dest, dest_len = self.nlp_model._prepare_batch ([[x, []]], offset=0)

            # predicted_ids: GreedyDecoder; [batch_size, max_time_step, 1]
            # BeamSearchDecoder; [batch_size, max_time_step, beam_width]
            predicted_ids = self.tf_model.predict(self.tf_session, encoder_inputs=source, 
                                                  encoder_inputs_length=source_len)

            # for seq_batch in predicted_ids:
            #     for k in range(5):
            #         logging.debug('--------- k: %d ----------' % k)
            #         seq = seq_batch[:,k]
            #         for p in seq:
            #             if p == -1:
            #                 break
            #             decoded = self.inv_output_dict[p]
            #             logging.debug (u'%s: %s' %(p, decoded))

            # extract best codes only

            acodes = [[]]
            for p in predicted_ids[0][:,0]:
                if p == -1:
                    break
                decoded = self.inv_output_dict[p]
                if decoded == u'_EOS':
                    break
                if decoded == u'__OR__':
                    acodes.append([])
                acodes[len(acodes)-1].append(decoded)

            # FIXME: for now, we try the first solution only
            acode = acodes[0]

            pcode     = self._reconstruct_prolog_code (acode)
            logging.debug('_process_input_nnet: %s' % pcode)
            clause    = Clause (None, pcode, location=self.dummyloc)
            solutions = self.rt.search (clause, env=res)

        except:
            # probably ok (prolog code generated by neural network might not always work)
            logging.error('EXCEPTION CAUGHT %s' % traceback.format_exc())

        return solutions

    def process_input (self, utterance, utt_lang, user_uri, run_trace=False, do_eliza=True, prev_ctx=None):

        """ process user input, return score, responses, actions, solutions, context """

        prev_context = prev_ctx
        res          = {}

        tokens  = tokenize(utterance, utt_lang)

        res, cur_context = self._setup_context ( user          = user_uri, 
                                                 lang          = utt_lang, 
                                                 inp           = tokens,
                                                 prev_context  = prev_context,
                                                 prev_res      = res)

        inp = self._compute_net_input (res, cur_context)

        logging.debug('process_input: %s' % repr(inp))

        #
        # do we have an exact match in our training data for this input?
        #

        solutions      = []

        self.rt.set_trace(run_trace)
        for tdr in self.session.query(model.TrainingData).filter(model.TrainingData.lang  == utt_lang,
                                                                 model.TrainingData.inp   == json.dumps(inp)):

            acode     = json.loads (tdr.resp)
            pcode     = self._reconstruct_prolog_code (acode)
            clause    = Clause (None, pcode, location=self.dummyloc)
            sols      = self.rt.search (clause, env=res)

            if sols:
                solutions.extend(sols)

        if not solutions:
            
            solutions = self._process_input_nnet(inp, res)          

            #
            # try dropping the context if we haven't managed to produce a result yet
            #

            if not solutions:
                res, cur_context = self._setup_context ( user          = user_uri, 
                                                         lang          = utt_lang, 
                                                         inp           = tokens,
                                                         prev_context  = None,
                                                         prev_res      = {})
                inp = self._compute_net_input (res, cur_context)
                solutions = self._process_input_nnet(inp, res)          

            if not solutions and do_eliza:
                logging.info ('producing ELIZA-style response for input %s' % utterance)
                clause = self.aip_parser.parse_line_clause_body('do_eliza(C, %s)' % utt_lang)
                solutions = self.rt.search (clause, env=res)

        self.rt.set_trace(False)

        #
        # extract highest-scoring responses only:
        #

        best_score     = 0
        best_resps     = []
        best_actions   = []
        best_solutions = []

        for solution in solutions:

            actual_resp, actual_actions, score = self._extract_response (cur_context, solution)

            if score > best_score:
                best_score     = score
                best_resps     = []
                best_actions   = []
                best_solutions = []

            if score < best_score:
                continue

            best_resps.append(actual_resp)
            best_actions.append(actual_actions)
            best_solutions.append(solution)

        return best_score, best_resps, best_actions, best_solutions, cur_context

    def run_cronjobs (self, module_name, force=False, run_trace=False):

        m = self.modules[module_name]
        if not hasattr(m, 'CRONJOBS'):
            return

        self.rt.set_trace(run_trace)

        for name, interval, f in getattr (m, 'CRONJOBS'):

            cronjob = self.session.query(model.Cronjob).filter(model.Cronjob.module==module_name, model.Cronjob.name==name).first()

            t = time.time()

            next_run = cronjob.last_run + interval

            if force or t > next_run:

                logging.debug ('running cronjob %s' % name)
                f (self)

                cronjob.last_run = t

    def run_cronjobs_multi (self, module_names, force, run_trace=False):

        for module_name in module_names:

            if module_name == 'all':

                for mn2 in self.all_modules:
                    self.load_module (mn2)
                    self.init_module (mn2)
                    self.run_cronjobs (mn2, force=force, run_trace=run_trace)

            else:
                self.load_module (module_name)
                self.init_module (module_name)
                self.run_cronjobs (module_name, force=force, run_trace=run_trace)

        self.session.commit()

    def train (self, ini_fn, num_steps, incremental):

        self.setup_tf_model ('train', False, ini_fn)
        self.nlp_model.train(num_steps, incremental)


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

        req = self.session.query(model.TrainingData).filter(model.TrainingData.lang==lang)

        if module and module != 'all':
            req = req.filter(model.TrainingData.module==module)

        for dr in req:

            if not dic:
                all_utterances.append(dr.utterance)
            else:

                # is at least one word not covered by our dictionary?

                unk = False
                for t in tokenize(dr.utterance):
                    if not t in dic:
                        # print u"unknown word: %s in %s" % (t, dr.utterance)
                        unk = True
                        dic.add(t)
                        break
                if not unk:
                    continue

                all_utterances.append(dr.utterance)

        utts = set()

        if num_utterances > 0:

            while (len(utts) < num_utterances):

                i = random.randrange(0, len(all_utterances))
                utts.add(all_utterances[i])

        else:
            for utt in all_utterances:
                utts.add(utt)
                
        for utt in utts:
            print (utt)

    def setup_align_utterances (self, lang):
        if self.w2v_model and self.w2v_lang == lang:
            return

        logging.debug('loading all utterances from db...')

        self.w2v_all_utterances = []
        req = self.session.query(model.TrainingData).filter(model.TrainingData.lang==lang)
        for dr in req:
            self.w2v_all_utterances.append((dr.utterance, dr.module, dr.loc_fn, dr.loc_line))

        if not self.w2v_model:
            from gensim.models import word2vec

        model_fn  = self.config.get('semantics', 'word2vec_model_%s' % lang)
        logging.debug ('loading word2vec model %s ...' % model_fn)
        logging.getLogger('gensim.models.word2vec').setLevel(logging.WARNING)
        self.w2v_model = word2vec.Word2Vec.load_word2vec_format(model_fn, binary=True)
        self.w2v_lang = lang
        #list containing names of words in the vocabulary
        self.w2v_index2word_set = set(self.w2v_model.index2word)
        logging.debug ('loading word2vec model %s ... done' % model_fn)

    def align_utterances (self, lang, utterances):

        self.setup_align_utterances(lang)

        res = {}

        for utt1 in utterances:
            try:
                utt1t = tokenize(utt1, lang=lang)
                av1 = avg_feature_vector(utt1t, model=self.w2v_model, num_features=300, index2word_set=self.w2v_index2word_set)

                sims = {} # location -> score
                utts = {} # location -> utterance

                for utt2, module, loc_fn, loc_line in self.w2v_all_utterances:
                    try:
                        utt2t = tokenize(utt2, lang=lang)

                        av2 = avg_feature_vector(utt2t, model=self.w2v_model, num_features=300, index2word_set=self.w2v_index2word_set)

                        sim = 1 - cosine(av1, av2)

                        location = '%s:%s:%d' % (module, loc_fn, loc_line)
                        sims[location] = sim
                        utts[location] = utt2
                        # logging.debug('%10.8f %s' % (sim, location))
                    except:
                        logging.error('EXCEPTION CAUGHT %s' % traceback.format_exc())
                logging.info('sims for %s' % repr(utt1))
                cnt = 0
                res[utt1] = []
                for sim, location in sorted( ((v,k) for k,v in sims.iteritems()), reverse=True):
                    logging.info('%10.8f %s' % (sim, location))
                    logging.info('    %s' % (utts[location]))

                    res[utt1].append((sim, location, utts[location]))

                    cnt += 1
                    if cnt>5:
                        break
            except:
                logging.error('EXCEPTION CAUGHT %s' % traceback.format_exc())

        return res

    #
    # ASR
    #

    def setup_asr (self, kaldi_model_dir, kaldi_model):

        logging.debug ('loading ASR model %s from %s...' % (kaldi_model, kaldi_model_dir))
        start_time = time.time()
        self.nnet3_model = KaldiNNet3OnlineModel ( kaldi_model_dir, kaldi_model )
        logging.debug ('ASR model loaded. took %fs' % (time.time() - start_time))
        self.asr_decoders = {} # location -> decoder

    def asr_decode (self, loc, sample_rate, audio, do_finalize):

        if not loc in self.asr_decoders:
            self.asr_decoders[loc] = KaldiNNet3OnlineDecoder (self.nnet3_model)
        decoder = self.asr_decoders[loc]
        decoder.decode(sample_rate, np.array(audio, dtype=np.float32), do_finalize)

        if not do_finalize:
            return None, 0.0

        hstr, confidence = decoder.get_decoded_string()

        return hstr, confidence

