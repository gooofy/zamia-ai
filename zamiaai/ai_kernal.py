#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016, 2017, 2018 Guenter Bartsch
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
# natural language -> [ tokenizer ] -> tokens -> [ seq2seq model ] -> Python/SWI-Prolog -> response
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
from six                    import text_type
from scipy.spatial.distance import cosine
from sqlalchemy             import create_engine
from sqlalchemy.orm         import sessionmaker
from xsbprolog              import xsb_hl_init, xsb_hl_command, xsb_hl_query, xsb_close, xsb_command_string, xsb_query_string, xsb_make_vars, xsb_var_string, xsb_next, xsb_hl_query_string

from nltools                import misc
from nltools.tokenizer      import tokenize
from zamiaai.data_engine    import DataEngine
from zamiaai                import model

USER_PREFIX        = u'user'
DEFAULT_USER       = USER_PREFIX + u'Default'
TEST_USER          = USER_PREFIX + u'Test'
TEST_TIME          = datetime.datetime(2016,12,6,13,28,6,tzinfo=get_localzone()).isoformat()
TEST_REALM         = '__test__'
MAX_NER_RESULTS    = 5
MAX_MEM_ENTRIES    = 5

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

class AIContext(object):

    def __init__(self, user, session, lang, realm, kernal, test_mode = False):
        self.dlg_log      = []
        self.staged_resps = []
        self.high_score   = 0.0
        self.inp          = u''
        self.user         = user
        self.realm        = realm
        self.ner_dict     = {} # DB cache
        self.session      = session
        self.lang         = lang
        self.kernal       = kernal
        self.test_mode    = test_mode

        tz = get_localzone()
        self.current_dt   = tz.localize(datetime.datetime.now())

    def set_inp(self, inp):
        self.inp = inp

    def resp(self, resp, score=0.0, action=None, action_arg=None):
        if score < self.high_score:
            return
        if score > self.high_score:
            self.high_score   = score
            self.staged_resps = []
        self.staged_resps.append( (resp, score, action, action_arg) )

        #print ("resp: score=%f staged_resps=%s" % (score, repr(self.staged_resps)))


    def get_resps(self):
        return self.staged_resps

    def commit_resp(self, i):
        self.dlg_log.append( { 'inp': self.inp, 
                               'out': self.staged_resps[i][0] })

        action     = self.staged_resps[i][2]
        action_arg = self.staged_resps[i][3]
        if action:
            if action_arg:
                action(self, action_arg)
            else:
                action(self)

        self.staged_resps = []
        self.high_score = 0.0
       
    def _ner_learn(self, lang, cls):

        entities = []
        labels   = []

        for nerdata in self.session.query(model.NERData).filter(model.NERData.lang==lang).filter(model.NERData.cls==cls):
            entities.append(nerdata.entity)
            labels.append(nerdata.label)

        if not lang in self.ner_dict:
            self.ner_dict[lang] = {}

        if not cls in self.ner_dict[lang]:
            self.ner_dict[lang][cls] = {}

        nd = self.ner_dict[lang][cls]

        for i, entity in enumerate(entities):

            label = labels[i]

            for j, token in enumerate(tokenize(label, lang=lang)):

                if not token in nd:
                    nd[token] = {}

                if not entity in nd[token]:
                    nd[token][entity] = set([])

                nd[token][entity].add(j)

                # logging.debug ('ner_learn: %4d %s %s: %s -> %s %s' % (i, entity, label, token, cls, lang))

        cnt = 0
        for token in nd:
            # import pdb; pdb.set_trace()
            # s1 = repr(nd[token])
            # s2 = limit_str(s1, 10)
            logging.debug ('ner_learn: nd[%-20s]=%s' % (token, misc.limit_str(repr(nd[token]), 80)))
            cnt += 1
            if cnt > 10:
                break
 
    def ner(self, lang, cls, tstart, tend):

        if not lang in self.ner_dict:
            self.ner_dict[lang] = {}
        if not cls in self.ner_dict[lang]:
            self._ner_learn(lang, cls)

        nd     = self.ner_dict[lang][cls]
        tokens = tokenize(self.inp, lang=lang)

        #
        # start scoring
        #

        max_scores = {}

        for tstart in range (tstart-1, tstart+2):
            if tstart <0:
                continue

            for tend in range (tend-1, tend+2):
                if tend > len(tokens):
                    continue

                scores = {}

                for tidx in range(tstart, tend):

                    toff = tidx-tstart

                    # logging.debug('tidx: %d, toff: %d [%d - %d]' % (tidx, toff, tstart, tend))

                    token = tokens[tidx]
                    if not token in nd:
                        # logging.debug('token %s not in nd %s %s' % (repr(token), repr(lang), repr(cls)))
                        continue

                    for entity in nd[token]:

                        if not entity in scores:
                            scores[entity] = 0.0

                        for eidx in nd[token][entity]:
                            points = 2.0-abs(eidx-toff)
                            if points>0:
                                scores[entity] += points

                logging.debug('scores: %s' % repr(scores))

                for entity in scores:
                    if not entity in max_scores:
                        max_scores[entity] = scores[entity]
                        continue
                    if scores[entity]>max_scores[entity]:
                        max_scores[entity] = scores[entity]

        res = []
        cnt = 0

        # for entity in max_scores:

        for entity, max_score in sorted(max_scores.iteritems(), key=lambda x: x[1], reverse=True):

            res.append((entity, max_score))

            cnt += 1
            if cnt > MAX_NER_RESULTS:
                break

        return res


class AIKernal(object):

    def __init__(self, db_url, xsb_root, all_modules=[], load_all_modules=False):

        #
        # database connection
        #

        self.engine  = create_engine(db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        model.Base.metadata.create_all(self.engine)

        #
        # TensorFlow (deferred, as tf can take quite a bit of time to set up)
        #

        self.tf_session = None
        self.nlp_model  = None

        #
        # module management, setup
        #

        self.modules             = {}
        self.consulted_modules   = set()
        self.initialized_modules = set()
        self.all_modules         = all_modules
        sys.path.append('modules')

        #
        # Prolog engine, data engine
        #

        xsb_hl_init([xsb_root])
        self.dte = DataEngine(self.session)

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


    # def clean (self, module_names, clean_all, clean_logic, clean_discourses, 
    #                                clean_cronjobs):

    #     for module_name in module_names:

    #         if clean_logic or clean_all:
    #             logging.info('cleaning logic for %s...' % module_name)
    #             if module_name == 'all':
    #                 self.db.clear_all_modules()
    #             else:
    #                 self.db.clear_module(module_name)

    #         if clean_discourses or clean_all:
    #             logging.info('cleaning discourses for %s...' % module_name)
    #             if module_name == 'all':
    #                 self.session.query(model.DiscourseRound).delete()
    #             else:
    #                 self.session.query(model.DiscourseRound).filter(model.DiscourseRound.module==module_name).delete()

    #         if clean_cronjobs or clean_all:
    #             logging.info('cleaning cronjobs for %s...' % module_name)
    #             if module_name == 'all':
    #                 self.session.query(model.Cronjob).delete()
    #             else:
    #                 self.session.query(model.Cronjob).filter(model.Cronjob.module==module_name).delete()

    #     self.session.commit()

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

            # for m2 in getattr (m, 'DEPENDS'):
            #     self.load_module(m2)

            # self.dte.load(module_name)

            # if hasattr(m, 'CRONJOBS'):

            #     # update cronjobs in db

            #     old_cronjobs = set()
            #     for cronjob in self.session.query(model.Cronjob).filter(model.Cronjob.module==module_name):
            #         old_cronjobs.add(cronjob.name)

            #     new_cronjobs = set()
            #     for name, interval, f in getattr (m, 'CRONJOBS'):

            #         logging.debug ('registering cronjob %s' %name)

            #         cj = self.session.query(model.Cronjob).filter(model.Cronjob.module==module_name, model.Cronjob.name==name).first()
            #         if not cj:
            #             cj = model.Cronjob(module=module_name, name=name, last_run=0)
            #             self.session.add(cj)

            #         cj.interval = interval
            #         new_cronjobs.add(cj.name)

            #     for cjn in old_cronjobs:
            #         if cjn in new_cronjobs:
            #             continue
            #         self.session.query(model.Cronjob).filter(model.Cronjob.module==module_name, model.Cronjob.name==cjn).delete()

            #     self.session.commit()

        except:
            logging.error('failed to load module "%s"' % module_name)
            logging.error(traceback.format_exc())
            sys.exit(1)

        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()

        return m

    def consult_module (self, module_name):

        if module_name in self.consulted_modules:
            return

        logging.debug("consulting module '%s'" % module_name)

        m = self.load_module(module_name)
        self.consulted_modules.add(module_name)

        try:

            # print m
            # print getattr(m, '__all__', None)

            # for name in dir(m):
            #     print name

            for m2 in getattr (m, 'DEPENDS'):
                self.consult_module(m2)

            if hasattr(m, 'PL_SOURCES'):

                for inputfn in m.PL_SOURCES:

                    pl_path = "modules/%s/%s" % (module_name, inputfn)

                    xsb_hl_command('consult', [pl_path])

        except:
            logging.error('failed to load module "%s"' % module_name)
            logging.error(traceback.format_exc())
            sys.exit(1)

        return m

    # def init_module (self, module_name, run_trace=False):

    #     if module_name in self.initialized_modules:
    #         return

    #     logging.debug("initializing module '%s'" % module_name)

    #     self.initialized_modules.add(module_name)

    #     m = self.load_module(module_name)

    #     if not m:
    #         raise Exception ('init_module: module "%s" not found.' % module_name)

    #     for m2 in getattr (m, 'DEPENDS'):
    #         self.init_module(m2)

    #     prolog_s = u'init(\'%s\')' % (module_name)
    #     c = self.aip_parser.parse_line_clause_body(prolog_s)

    #     self.rt.set_trace(run_trace)

    #     solutions = self.rt.search(c)

    #     if hasattr(m, 'init_module'):
    #         initializer = getattr(m, 'init_module')
    #         initializer(self)

    def compile_module (self, module_name):

        m = self.load_module(module_name)

        # tell prolog engine to consult all prolog files plus their dependencies

        self.consult_module(module_name)

        # prepare data engine for module compilation

        self.dte.prepare_compilation(module_name)

        if hasattr(m, 'get_data'):

            logging.info ('module %s data extraction...' % module_name)

            get_data = getattr(m, 'get_data')
            get_data(self)

        self.dte.commit()

        cnt_dt, cnt_ts = self.dte.get_stats()
        logging.info ('module %s data extraction done. %d training samples, %d tests' % (module_name, cnt_dt, cnt_ts))

    def compile_module_multi (self, module_names):

        for module_name in module_names:
            if module_name == 'all':
                for mn2 in self.all_modules:
                    self.compile_module (mn2)

            else:
                self.compile_module (module_name)

    def test_module (self, module_name, run_trace=False, test_name=None):

        if run_trace:
            xsb_command_string("trace.")
        else:
            xsb_command_string("notrace.")

        m = self.modules[module_name]

        logging.info('running tests of module %s ...' % (module_name))

        num_tests = 0
        num_fails = 0
        for tc in self.dte.lookup_tests(module_name):
            t_name, lang, prep_code, prep_fn, rounds, src_fn, self.src_line = tc

            if test_name:
                if t_name != test_name:
                    logging.info ('skipping test %s' % t_name)
                    continue

            ctx        = AIContext(TEST_USER, self.session, lang, TEST_REALM, self, test_mode=True)
            round_num  = 0
            num_tests += 1

            # prep

            if prep_code:
                pcode = '%s\n%s(ctx)\n' % (prep_code, prep_fn)
                try:
                    exec (pcode, globals(), locals())
                except:
                    logging.error('EXCEPTION CAUGHT %s' % traceback.format_exc())

            for test_inp, test_out, test_action, test_action_arg in rounds:
               
                logging.info("test_module: %s round %d test_inp    : %s" % (t_name, round_num, repr(test_inp)) )
                logging.info("test_module: %s round %d test_out    : %s" % (t_name, round_num, repr(test_out)) )

                # look up code in data engine

                matching_resp = False
                acode         = None

                ctx.set_inp(test_inp)
                self.mem_set (ctx.realm, 'action', None)

                for lang, d, md5s, args, src_fn, src_line in self.dte.lookup_data_train (test_inp, lang):

                    afn, acode = self.dte.lookup_code(md5s)
                    ecode = '%s\n%s(ctx' % (acode, afn)
                    if args:
                        for arg in args:
                            ecode += ',%s' % repr(arg)
                    ecode += ')\n'
                    # import pdb; pdb.set_trace()
                    try:
                        exec (ecode, globals(), locals())
                    except:
                        logging.error('test_module: %s round %d EXCEPTION CAUGHT %s' % (t_name, round_num, traceback.format_exc()))
                        logging.error(ecode)

                if acode is None:
                    logging.error (u'Error: %s: no training data for test_in "%s" found in DB!' % (t_name, test_inp))
                    num_fails += 1
                    break

                resps = ctx.get_resps()

                for i, resp in enumerate(resps):
                    actual_out, score, actual_action, actual_action_arg = resp
                    # logging.info("test_module: %s round %d %s" % (clause.location, round_num, repr(abuf)) )

                    if len(test_out) > 0:
                        if len(actual_out)>0:
                            actual_out = u' '.join(tokenize(actual_out, lang))
                        logging.info("test_module: %s round %d actual_out  : %s (score: %f)" % (t_name, round_num, actual_out, score) )
                        if actual_out != test_out:
                            logging.info("test_module: %s round %d UTTERANCE MISMATCH." % (t_name, round_num))
                            continue # no match

                    logging.info("test_module: %s round %d UTTERANCE MATCHED!" % (t_name, round_num))
                    matching_resp = True
                    ctx.commit_resp(i)

                    # check action

                    if test_action:
                        afn, acode = self.dte.lookup_code(test_action)
                        ecode = '%s\n%s(ctx' % (acode, afn)
                        if test_action_arg:
                            ecode += ',%s' % repr(test_action_arg)
                        ecode += ')\n'
                        exec (ecode, globals(), locals())

                    break

                if not matching_resp:
                    logging.error (u'test_module: %s round %d no matching response found.' % (t_name, round_num))
                    num_fails += 1
                    break

                round_num   += 1

        return num_tests, num_fails

    def run_tests_multi (self, module_names, run_trace=False, test_name=None):

        num_tests = 0
        num_fails = 0

        for module_name in module_names:

            if module_name == 'all':

                for mn2 in self.all_modules:
                    self.consult_module (mn2)
                    n, f = self.test_module (mn2, run_trace=run_trace, test_name=test_name)
                    num_tests += n
                    num_fails += f

            else:
                self.consult_module (module_name)
                n, f = self.test_module (module_name, run_trace=run_trace, test_name=test_name)
                num_tests += n
                num_fails += f

        return num_tests, num_fails


    def process_input (self, ctx, inp_raw, inp_lang, user_uri, run_trace=False, do_eliza=True):

        """ process user input, return score, responses, actions, solutions, context """

        if run_trace:
            xsb_command_string("trace.")
        else:
            xsb_command_string("notrace.")

        tokens_raw  = tokenize(inp_raw, inp_lang)
        tokens = []
        for t in tokens_raw:
            if t == u'nspc':
                continue
            tokens.append(t)
        inp = u" ".join(tokens)

        ctx.set_inp(inp)
        self.mem_set (ctx.realm, 'action', None)

        logging.debug('process_input: %s' % repr(inp))

        #
        # do we have an exact match in our training data for this input?
        #

        found_resp = False
        for lang, d, md5s, args, src_fn, src_line in self.dte.lookup_data_train (inp, inp_lang):

            afn, acode = self.dte.lookup_code(md5s)
            ecode = '%s\n%s(ctx' % (acode, afn)
            if args:
                for arg in args:
                    ecode += ',%s' % repr(arg)
            ecode += ')\n'

            logging.debug ('exact training data match found: %s:%s' % (src_fn, src_line))
            logging.debug (ecode)

            # import pdb; pdb.set_trace()
            try:
                exec (ecode, globals(), locals())
                found_resp = True
            except:
                logging.error('EXCEPTION CAUGHT %s' % traceback.format_exc())
                logging.error(ecode)

        if not found_resp:
            logging.debug('no exact training data match for this input found.')

        #
        # ask neural net if we did not find an answer
        #

        if not found_resp and self.nlp_model:
            
            from nlp_model      import OR_SYMBOL
            from seq2seq_model  import _EOS

            logging.debug('trying neural net on: %s' % repr(inp))

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

                # extract best codes, run them all to see which ones yield the highest scoring responses

                cmd = []
                for p in predicted_ids[0][:,0]:
                    if p in self.inv_output_dict:
                        decoded = self.inv_output_dict[p]
                    else:
                        decoded = p

                    if decoded == _EOS or decoded == -1 or decoded == OR_SYMBOL:

                        try:
                            logging.debug('trying cmd: %s' % repr(cmd))
                            afn, acode = self.dte.lookup_code(cmd[0])
                            ecode = '%s\n%s(ctx' % (acode, afn)
                            if len(cmd)>1:
                                for arg in cmd[1:]:
                                    ecode += ',%s' % repr(json.loads(arg))
                            ecode += ')\n'

                            logging.debug(ecode)

                            exec (ecode, globals(), locals())
                        except:
                            logging.debug('EXCEPTION CAUGHT %s' % traceback.format_exc())

                        cmd = []
                        if decoded == _EOS or decoded == -1:
                            break
                    else:
                        cmd.append(decoded)

            except:
                # probably ok (prolog code generated by neural network might not always work)
                logging.error('EXCEPTION CAUGHT %s' % traceback.format_exc())

            # if not solutions:
            #     res, cur_context = self._setup_context ( user          = user_uri, 
            #                                              lang          = inp_lang, 
            #                                              inp           = tokens,
            #                                              prev_context  = None,
            #                                              prev_res      = {})
            #     inp = self._compute_net_input (res, cur_context)
            #     solutions = self._process_input_nnet(inp, res)          


        xsb_command_string("notrace.")

        #
        # extract highest-scoring responses
        #

        resps = ctx.get_resps()

        if not resps and do_eliza:
            logging.debug ('producing ELIZA-style response for input %s' % inp)

            from psychology import psychology
            psychology.do_eliza(ctx)
            resps = ctx.get_resps()

        #
        # pick random response
        #

        if len(resps)>0:
            i = random.randrange(0, len(resps))
            out, score, action, action_arg = resps[i]
            ctx.commit_resp(i)

            logging.debug(u'picked resp #%d (score: %f): %s' % (i, score, out))

        else:
            out        = u''
            score      = 0.0
            action     = None
            action_arg = None
            logging.debug(u'No response found.')

        return out, score, action, action_arg 

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

        req = self.dte.session.query(model.TrainingData).filter(model.TrainingData.lang==lang)

        if module and module != 'all':
            req = req.filter(model.TrainingData.module==module)

        req_utts = []
        for dr in req:
            req_utts.append(dr.inp)

        if not dic:

            all_utterances = sorted(req_utts)

        else:

            all_utterances = []
            random.shuffle(req_utts)
            for utt in req_utts:

                # is at least one word not covered by our dictionary?

                unk = False
                for t in tokenize(utt):
                    if not t in dic:
                        # print u"unknown word: %s in %s" % (t, utt)
                        unk = True
                        break
                if not unk:
                    continue

                for t in tokenize(utt):
                    dic.add(t)
                all_utterances.append(utt)

        utts = set()

        if num_utterances > 0:

            while (len(utts) < num_utterances):

                i = random.randrange(0, len(all_utterances))
                utts.add(all_utterances[i])

        else:
            for utt in all_utterances:
                utts.add(utt)
                
        for utt in sorted(list(utts)):
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

    def mem_clear(self, realm):
        self.session.query(model.Mem).filter(model.Mem.realm==realm).delete()

    def mem_set(self, realm, k, v):
        self.session.query(model.Mem).filter(model.Mem.realm==realm).filter(model.Mem.k==k).delete()
        m = model.Mem(realm=realm, k=k, v=json.dumps(v))
        self.session.add(m)

    def mem_get(self, realm, k):
        m = self.session.query(model.Mem).filter(model.Mem.realm==realm).filter(model.Mem.k==k).first()
        if not m:
            return None
        return json.loads(m.v)

    def mem_get_multi (self, realm, k):

        m = self.mem_get(realm, k)
        if not m:
            return []
        if not isinstance (m, list):
            return [m, 1.0]

        s = 1.0
        res = []
        for m2 in m:
            res.append((m2, s))
            s = s / 2

        return res
    
    def mem_push (self, realm, k, v):
        oldv = self.mem_get(realm, k)
        if not oldv:
            newv = [v]
        elif isinstance (oldv, list):
            newv = [v] + oldv
        else:
            newv = [v, oldv]

        newv = newv[:MAX_MEM_ENTRIES]

        self.mem_set(realm, k, newv)

    def prolog_query(self, query):
        logging.debug ('prolog_query: %s' % query)
        return xsb_hl_query_string(query)

    def prolog_check(self, query):
        logging.debug ('prolog_check: %s' % query)
        res = xsb_hl_query_string(query)
        return len(res)>0

    def prolog_query_one(self, query, idx=0):
        logging.debug ('prolog_query_one: %s' % query)
        solutions = xsb_hl_query_string(query)
        if not solutions:
            return None
        return solutions[0][idx]

    def prolog_hl_query(self, fname, args):
        logging.debug ('prolog_hl_query: %s %s' % (fname, repr(args)))
        return xsb_hl_query(fname, args)

