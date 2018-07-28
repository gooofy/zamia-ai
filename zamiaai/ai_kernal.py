#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016, 2017, 2018 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# ai kernal, central hub for all the other components to hook into
#
# natural language -> [ tokenizer ] -> tokens -> [ seq2seq model ] -> Python/Prolog -> response
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
from pyxsb                  import pyxsb_start_session, pyxsb_command, pyxsb_query, xsb_to_json, json_to_xsb, XSBString, XSBFunctor, XSBAtom

from nltools                import misc
from nltools.tokenizer      import tokenize
from zamiaai.data_engine    import DataEngine
from zamiaai.ai_context     import AIContext
from zamiaai                import model

USER_PREFIX          = u'user'
DEFAULT_USER         = USER_PREFIX + u'Default'
TEST_USER            = USER_PREFIX + u'Test'
TEST_TIME            = datetime.datetime(2016,12,6,13,28,6,tzinfo=get_localzone()).isoformat()
TEST_REALM           = '__test__'
MAX_MEM_ENTRIES      = 5
LANGUAGES            = ['en', 'de']

DEFAULT_LANG         = 'en'
DEFAULT_DB_URL       = 'sqlite:///zamiaai.db'
DEFAULT_XSB_ARCH_DIR = None
DEFAULT_TOPLEVEL     = 'toplevel'
DEFAULT_MPATHS       = None
DEFAULT_MODEL_INI    = 'model.ini'
DEFAULT_REALM        = '__realm__'

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

    def __init__(self, db_url=DEFAULT_DB_URL, xsb_arch_dir=DEFAULT_XSB_ARCH_DIR, toplevel=DEFAULT_TOPLEVEL, mpaths=DEFAULT_MPATHS, lang=DEFAULT_LANG):

        self.lang = lang

        #
        # database connection
        #

        self.engine  = model.data_engine_setup(db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        #
        # TensorFlow (deferred, as tf can take quite a bit of time to set up)
        #

        self.tf_session = None
        self.nlp_model  = None

        #
        # module management, setup
        #

        self.modules             = {}   # module_name -> module obj
        self.module_paths        = {}   # module_name -> pathname
        self.consulted_modules   = set()
        self.toplevel            = toplevel
        self.all_modules         = []
        
        # import pdb; pdb.set_trace()

        if mpaths:
            for mp in mpaths[::-1]:
                sys.path.insert(0,mp)
        else:
            # auto-config

            # __file__ -> ../skills
            mp = os.path.dirname(os.path.abspath(__file__)) + '/skills'
            sys.path.insert(0, mp)

            # ./skills
            cwd = os.getcwd()
            sys.path.insert(0, cwd + '/skills')

            # .
            sys.path.insert(0, cwd)

        for mp in sys.path:
            logging.debug ("Module search path: %s" % mp)

        self.load_module(toplevel)

        #
        # Prolog engine, data engine
        #

        pyxsb_start_session(xsb_arch_dir)
        self.dte = DataEngine(self.session)

        pyxsb_command('import default_sys_error_handler/1 from error_handler.')
        pyxsb_command('assertz((default_user_error_handler(Ball):-default_sys_error_handler(Ball))).')

        #
        # restore memory
        #

        q = u''
        for m in self.session.query(model.Mem):

            v = json_to_xsb(m.v)

            if q:
                q += ', '
            q += u"assertz(memory('%s', '%s', %s, %f))" % (m.realm, m.k, unicode(v), m.score)

        if not q:
            q = u'assertz(memory(self, self, self, 1.0))'
        q += u'.'
        pyxsb_command(q)

        #
        # alignment / word2vec (on-demand model loading)
        #
        self.w2v_model          = None
        self.w2v_all_utterances = []

    # FIXME: this will work only on the first call
    def setup_tf_model (self, mode='decode', load_model=True, ini_fn=DEFAULT_MODEL_INI, global_step=0):

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

            self.modules[module_name]      = m
            self.module_paths[module_name] = pathname

            for m2 in getattr (m, 'DEPENDS'):
                self.load_module(m2)

        except:
            logging.error('failed to load module "%s" (%s)' % (module_name, pathname))
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
        module_dir = self.module_paths[module_name]

        try:

            # print m
            # print getattr(m, '__all__', None)

            # for name in dir(m):
            #     print name

            for m2 in getattr (m, 'DEPENDS'):
                self.consult_module(m2)

            if hasattr(m, 'PL_SOURCES'):

                for inputfn in m.PL_SOURCES:

                    pl_path = "%s/%s" % (module_dir, inputfn)

                    pyxsb_command("consult('%s')."% pl_path)

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

    def create_context (self, user=DEFAULT_USER, realm=DEFAULT_REALM, test_mode=False):
        return AIContext(user, self.session, self.lang, realm, self, test_mode=test_mode)

    def test_module (self, module_name, run_trace=False, test_name=None):

        if run_trace:
            pyxsb_command("trace.")
        else:
            pyxsb_command("notrace.")

        m = self.modules[module_name]

        logging.info('running tests of module %s ...' % (module_name))

        num_tests = 0
        num_fails = 0
        for tc in self.dte.lookup_tests(module_name):
            t_name, self.lang, prep_code, prep_fn, rounds, src_fn, self.src_line = tc

            if test_name:
                if t_name != test_name:
                    logging.info ('skipping test %s' % t_name)
                    continue

            ctx        = AIContext(user=TEST_USER, realm=TEST_REALM, test_mode=True)
            round_num  = 0
            num_tests += 1

            self.mem_clear(TEST_REALM)
            self.mem_clear(TEST_USER)

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

                for lang, d, md5s, args, src_fn, src_line in self.dte.lookup_data_train (test_inp, self.lang):

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
                            actual_out = u' '.join(tokenize(actual_out, self.lang))
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


    def process_input (self, ctx, inp_raw, run_trace=False, do_eliza=True):

        """ process user input, return score, responses, actions, solutions, context """

        if run_trace:
            pyxsb_command("trace.")
        else:
            pyxsb_command("notrace.")

        tokens_raw  = tokenize(inp_raw, ctx.lang)
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
        for lang, d, md5s, args, src_fn, src_line in self.dte.lookup_data_train (inp, ctx.lang):

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

        pyxsb_command("notrace.")

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
            for k, v, score in memd:
                logging.debug(u'MEM:    %-20s: %s (%f)' % (k, v, score))
            logging.debug(u'MEM: %s' % ctx.user)
            memd = self.mem_dump(ctx.user)
            for k, v, score in memd:
                logging.debug(u'MEM:    %-20s: %s (%f)' % (k, v, score))

        else:
            out        = u''
            score      = 0.0
            logging.debug(u'No response found.')

        action = self.mem_get (ctx.realm, 'action')
        return out, score, action

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

    def setup_align_utterances (self):
        if self.w2v_model:
            return

        logging.debug('loading all utterances from db...')

        self.w2v_all_utterances = []
        req = self.session.query(model.TrainingData).filter(model.TrainingData.lang==self.lang)
        for dr in req:
            self.w2v_all_utterances.append((dr.utterance, dr.module, dr.loc_fn, dr.loc_line))

        if not self.w2v_model:
            from gensim.models import word2vec

        model_fn  = self.config.get('semantics', 'word2vec_model_%s' % self.lang)
        logging.debug ('loading word2vec model %s ...' % model_fn)
        logging.getLogger('gensim.models.word2vec').setLevel(logging.WARNING)
        self.w2v_model = word2vec.Word2Vec.load_word2vec_format(model_fn, binary=True)
        #list containing names of words in the vocabulary
        self.w2v_index2word_set = set(self.w2v_model.index2word)
        logging.debug ('loading word2vec model %s ... done' % model_fn)

    def align_utterances (self, utterances):

        self.setup_align_utterances()

        res = {}

        for utt1 in utterances:
            try:
                utt1t = tokenize(utt1, lang=self.lang)
                av1 = avg_feature_vector(utt1t, model=self.w2v_model, num_features=300, index2word_set=self.w2v_index2word_set)

                sims = {} # location -> score
                utts = {} # location -> utterance

                for utt2, module, loc_fn, loc_line in self.w2v_all_utterances:
                    try:
                        utt2t = tokenize(utt2, lang=self.lang)

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
        if not isinstance(realm, basestring):
            raise Exception ("mem_set: realm must be string-typed.")
        q = u"retractall(memory('%s', _, _, _))." % realm
        # logging.debug (q)
        self.prolog_query(q)

    def mem_dump(self, realm):
        if not isinstance(realm, basestring):
            raise Exception ("mem_set: realm must be string-typed.")

        entries = []

        q = u"memory('%s', K, V, S)." % realm
        # logging.debug (q)
        res = self.prolog_query(q)
        if res:
            for r in res:
                k     = r[0]
                v     = r[1]
                score = r[2]
                entries.append((k, v, score))

        # import pdb; pdb.set_trace()

        return entries

    def mem_set(self, realm, k, v):

        if not isinstance(realm, basestring) or not isinstance(k, basestring):
            raise Exception ("mem_set: realm and key must be string-typed.")

        q = u"retractall(memory('%s', '%s', _, _))" % (realm, k)
        if v:
            q += u", assertz(memory('%s', '%s', %s, 1.0))." % (realm, k, unicode(v))
        else:
            q += '.' 
        # logging.debug (q)

        self.prolog_query(q)

    def mem_get(self, realm, k):
        if not isinstance(realm, basestring) or not isinstance(k, basestring):
            raise Exception ("mem_set: realm and key must be string-typed.")

        q = u"memory('%s', '%s', V, S)." % (realm, k)
        # logging.debug (q)
        res = self.prolog_query(q)
        if not res:
            return None

        score = 0.0
        v = None
        for r in res:
            if not v or r[1] > score:
                score = r[1]
                v     = r[0]

        return v

    def mem_get_multi (self, realm, k):
        if not isinstance(realm, basestring) or not isinstance(k, basestring):
            raise Exception ("mem_set: realm and key must be string-typed.")

        entries = []

        q = u"memory('%s', '%s', V, S)." % (realm, k)
        # logging.debug (q)
        res = self.prolog_query(q)
        if res:
            for r in res:
                score = r[1]
                v     = r[0]
                entries.append((v, score))

        return entries
    
    def mem_push (self, realm, k, v):
        if not isinstance(realm, basestring) or not isinstance(k, basestring):
            raise Exception ("mem_set: realm and key must be string-typed.")

        entries = [(1.0, v)]

        # re-score existing entries

        q = u"memory('%s', '%s', V, S)." % (realm, k)
        # logging.debug (q)
        res = self.prolog_query(q)
        if res:
            for r in res:
                score = r[1]
                v     = r[0]
                if score < 0.125:
                    continue
                entries.append((score/2, v))

        # put all entries into the KB
        q = u"retractall(memory('%s', '%s', _, _))" % (realm, k)
        for score, v in entries:
            if v:
                q += u", assertz(memory('%s', '%s', %s, %f))" % (realm, k, unicode(v), score)
        q += u'.'
        # logging.debug (q)

        self.prolog_query(q)

    def prolog_query(self, query):
        logging.debug ('prolog_query: %s' % query)
        return pyxsb_query(query)

    def prolog_check(self, query):
        logging.debug ('prolog_check: %s' % query)
        res = pyxsb_query(query)
        return len(res)>0

    def prolog_query_one(self, query, idx=0):
        logging.debug ('prolog_query_one: %s' % query)
        solutions = pyxsb_query(query)
        if not solutions:
            return None
        return solutions[0][idx]

    def prolog_persist(self):
        """ persist all currently asserted dynamic memory predicates from the prolog KB """

        # q = 'predicate_property(Head, (dynamic)), clause(Head,Bod).'
        # for r in self.prolog_query(q):
        #     logging.info(repr(r))
        #     # print "%s" % repr(r)

        self.session.query(model.Mem).delete()

        q = u'memory(REALM, K, V, S).'
        for r in self.prolog_query(q):
            # logging.info(repr(r))

            realm = r[0].name
            k     = r[1].name
            v     = xsb_to_json(r[2])
            score = r[3]

            m = model.Mem(realm=realm, k=k, v=v, score=score)
            self.session.add(m)

        # import pdb; pdb.set_trace()
        self.session.commit()

