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
from zamiaai.ai_context     import AIContext
from zamiaai                import model

USER_PREFIX        = u'user'
DEFAULT_USER       = USER_PREFIX + u'Default'
TEST_USER          = USER_PREFIX + u'Test'
TEST_TIME          = datetime.datetime(2016,12,6,13,28,6,tzinfo=get_localzone()).isoformat()
TEST_REALM         = '__test__'
MAX_MEM_ENTRIES    = 5
LANGUAGES          = ['en', 'de']

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

    def __init__(self, db_url, xsb_root, toplevel):

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
        self.toplevel            = toplevel
        self.all_modules         = []
        sys.path.append('modules')
        self.load_module(toplevel)

        #
        # Prolog engine, data engine
        #

        xsb_hl_init([xsb_root])
        self.dte = DataEngine(self.session)

        xsb_command_string('import default_sys_error_handler/1 from error_handler.')
        xsb_command_string('assertz((default_user_error_handler(Ball):-default_sys_error_handler(Ball))).')

        #
        # alignment / word2vec (on-demand model loading)
        #
        self.w2v_model          = None
        self.w2v_lang           = None
        self.w2v_all_utterances = []

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


    def clean (self, module_names):

        for module_name in module_names:
            self.dte.clean(module_name)

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

            for m2 in getattr (m, 'DEPENDS'):
                self.load_module(m2)

        except:
            logging.error('failed to load module "%s"' % module_name)
            logging.error(traceback.format_exc())
            sys.exit(1)

        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()

        if not module_name in self.all_modules:
            self.all_modules.append(module_name)

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

        logging.debug('===============================================================================')
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

        resps = ctx.get_resps()
        if not resps and self.nlp_model:
            
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

            logging.debug(u'MEM: %s' % ctx.realm)
            memd = self.mem_dump(ctx.realm)
            for k in memd:
                logging.debug(u'MEM:    %-20s: %s' % (k, memd[k]))
            logging.debug(u'MEM: %s' % user_uri)
            memd = self.mem_dump(user_uri)
            for k in memd:
                logging.debug(u'MEM:    %-20s: %s' % (k, memd[k]))

        else:
            out        = u''
            score      = 0.0
            action     = None
            action_arg = None
            logging.debug(u'No response found.')

        return out, score, action, action_arg 

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

    def stats (self):

        stats = {}

        for module_name in self.all_modules:    
            stats[module_name] = {}
            for lang in LANGUAGES:
                cnt = self.session.query(model.TrainingData).filter(model.TrainingData.module==module_name,
                                                                    model.TrainingData.lang==lang).count()
                stats[module_name][lang] = cnt

        return stats

    def mem_clear(self, realm):
        self.session.query(model.Mem).filter(model.Mem.realm==realm).delete()

    def mem_dump(self, realm):
        res = {}
        for m in self.session.query(model.Mem).filter(model.Mem.realm==realm):
            res[m.k] = m.v
        return res

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

