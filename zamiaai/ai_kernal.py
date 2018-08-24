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
import ConfigParser

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

USER_PREFIX                 = u'user'
DEFAULT_USER                = USER_PREFIX + u'Default'
TEST_USER                   = USER_PREFIX + u'Test'
TEST_TIME                   = datetime.datetime(2016,12,6,13,28,6,tzinfo=get_localzone()).isoformat()
TEST_REALM                  = '__test__'
MAX_MEM_ENTRIES             = 5
LANGUAGES                   = ['en', 'de']

DEFAULT_LANG                = 'en'
DEFAULT_DB_URL              = 'sqlite:///zamiaai.db'
DEFAULT_XSB_ARCH_DIR        = None
DEFAULT_TOPLEVEL            = 'toplevel'
DEFAULT_SKILL_PATHS         = None
DEFAULT_REALM               = '__realm__'
DEFAULT_NUM_EPOCHS          = 100
DEFAULT_NUM_EPOCHS_UTTCLASS = 10

DEFAULTS             = {'db_url'      : DEFAULT_DB_URL,
                        'xsb_arch_dir': DEFAULT_XSB_ARCH_DIR,
                        'toplevel'    : DEFAULT_TOPLEVEL,
                        'skill_paths' : DEFAULT_SKILL_PATHS,
                        'lang'        : DEFAULT_LANG }
DEFAULT_NLP_MODEL_ARGS = {
                          'model_dir'       : 'model',
                          'lstm_latent_dim' : 256,
                          'batch_size'      : 64,
                          'max_input_len'   : 20, # tokens
                         }
DEFAULT_UTTCLASS_MODEL_ARGS = {
                            'model_dir'       : 'model',
                            'conv_filters'    : 128,
                            'dense_dim'       : 256,
                            'batch_size'      : 64,
                            'max_input_len'   : 20, # tokens
                            'optimizer'       : 'adam',
                            'dropout'         : 0.5,
                           }

DEFAULT_SKILL_ARGS   = {}
DEFAULT_INI_FILENAME = 'zamiaai.ini'

class AIKernal(object):

    @classmethod
    def from_ini_file(cls, 
                      inifn                    = DEFAULT_INI_FILENAME, 
                      defaults                 = DEFAULTS, 
                      default_nlp_model_args   = DEFAULT_NLP_MODEL_ARGS,
                      default_skill_args       = DEFAULT_SKILL_ARGS,
                      default_uttclass_model_args = DEFAULT_UTTCLASS_MODEL_ARGS):

        config = ConfigParser.ConfigParser()
        config.add_section('main')
        for k,v in defaults.items():
            config.set('main', k, v)
        config.add_section('nlpmodel')
        for k,v in default_nlp_model_args.items():
            config.set('nlpmodel', k, str(v))
        config.add_section('skills')
        for k,v in default_skill_args.items():
            config.set('skills', k, str(v))
        config.add_section('uttclassmodel')
        for k,v in default_uttclass_model_args.items():
            config.set('uttclassmodel', k, str(v))

        if os.path.exists(inifn):
            config.read(inifn)

        toplevel     = config.get('main', 'toplevel')
        xsb_arch_dir = config.get('main', 'xsb_arch_dir')
        db_url       = config.get('main', 'db_url')
        skill_paths  = config.get('main', 'skill_paths')
        lang         = config.get('main', 'lang')

        nlp_model_args = {
                          'model_dir'       : config.get('nlpmodel', 'model_dir'),
                          'lstm_latent_dim' : config.getint('nlpmodel', 'lstm_latent_dim'),
                          'batch_size'      : config.getint('nlpmodel', 'batch_size'),
                          'max_input_len'   : config.getint('nlpmodel', 'max_input_len'),
                         }

        skill_args = {}
        for k,v in config.items('skills'):
            skill_args[k] = v

        uttclass_model_args = {
                            'model_dir'       : config.get('uttclassmodel', 'model_dir'),
                            'conv_filters'    : config.getint('uttclassmodel', 'conv_filters'),
                            'dense_dim'       : config.getint('uttclassmodel', 'dense_dim'),
                            'batch_size'      : config.getint('uttclassmodel', 'batch_size'),
                            'max_input_len'   : config.getint('uttclassmodel', 'max_input_len'),
                            'optimizer'       : config.get('uttclassmodel', 'optimizer'),
                            'dropout'         : config.getfloat('uttclassmodel', 'dropout'),
                           }

        return AIKernal(db_url=db_url, xsb_arch_dir=xsb_arch_dir, toplevel=toplevel, skill_paths=skill_paths, lang=lang,
                        nlp_model_args=nlp_model_args, skill_args=skill_args, uttclass_model_args=uttclass_model_args)

    def __init__(self, 
                 db_url              = DEFAULT_DB_URL, 
                 xsb_arch_dir        = DEFAULT_XSB_ARCH_DIR, 
                 toplevel            = DEFAULT_TOPLEVEL, 
                 skill_paths         = DEFAULT_SKILL_PATHS, 
                 lang                = DEFAULT_LANG, 
                 nlp_model_args      = DEFAULT_NLP_MODEL_ARGS,
                 skill_args          = DEFAULT_SKILL_ARGS,
                 uttclass_model_args = DEFAULT_UTTCLASS_MODEL_ARGS):

        self.lang                = lang
        self.nlp_model_args      = nlp_model_args
        self.skill_args          = skill_args
        self.uttclass_model_args = uttclass_model_args

        #
        # database connection
        #

        self.engine  = model.data_engine_setup(db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        #
        # TensorFlow (deferred, as tf can take quite a bit of time to set up)
        #

        self.tf_session     = None
        self.nlp_model      = None
        self.uttclass_model = None

        #
        # skill management, setup
        #

        self.skills             = {}   # skill_name -> module obj
        self.skill_paths        = {}   # skill_name -> pathname
        self.consulted_skills   = set()
        self.toplevel           = toplevel
        self.all_skills         = []
        
        # import pdb; pdb.set_trace()

        if skill_paths:
            for sp in skill_paths[::-1]:
                sys.path.insert(0,sp)
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

        self.load_skill(toplevel)

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

    # FIXME: this will work only on the first call
    def setup_nlp_model (self, restore=True):

        if self.nlp_model:
            raise Exception ('Tensorflow model can be set up only once.')

        from nlp_model import NLPModel

        self.nlp_model = NLPModel(lang=self.lang, session=self.session, model_args=self.nlp_model_args)

        if restore:
            self.nlp_model.restore()


    def clean (self, skill_names):

        for skill_name in skill_names:
            self.dte.clean(skill_name)

        self.session.commit()

    def load_skill (self, skill_name):

        if skill_name in self.skills:
            return self.skills[skill_name]

        logging.debug("loading skill '%s'" % skill_name)

        # fp, pathname, description = imp.find_module(skill_name, ['skills'])
        fp, pathname, description = imp.find_module(skill_name)

        # print fp, pathname, description

        m = None

        try:
            m = imp.load_module(skill_name, fp, pathname, description)

            self.skills[skill_name]      = m
            self.skill_paths[skill_name] = pathname

            for m2 in getattr (m, 'DEPENDS'):
                self.load_skill(m2)

        except:
            logging.error('failed to load skill "%s" (%s)' % (skill_name, pathname))
            logging.error(traceback.format_exc())
            sys.exit(1)

        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()

        if not skill_name in self.all_skills:
            self.all_skills.append(skill_name)

        return m

    def consult_skill (self, skill_name):

        if skill_name in self.consulted_skills:
            return

        logging.debug("consulting skill '%s'" % skill_name)

        m = self.load_skill(skill_name)
        self.consulted_skills.add(skill_name)
        skill_dir = self.skill_paths[skill_name]

        try:

            # print m
            # print getattr(m, '__all__', None)

            # for name in dir(m):
            #     print name

            for m2 in getattr (m, 'DEPENDS'):
                self.consult_skill(m2)

            if hasattr(m, 'PL_SOURCES'):

                for inputfn in m.PL_SOURCES:

                    pl_path = "%s/%s" % (skill_dir, inputfn)

                    pyxsb_command("consult('%s')."% pl_path)

        except:
            logging.error('failed to load skill "%s"' % skill_name)
            logging.error(traceback.format_exc())
            sys.exit(1)

        return m

    def compile_skill (self, skill_name):

        m = self.load_skill(skill_name)

        # tell prolog engine to consult all prolog files plus their dependencies

        self.consult_skill(skill_name)

        # prepare data engine for skill compilation

        self.dte.prepare_compilation(skill_name)

        if hasattr(m, 'get_data'):

            logging.info ('skill %s data extraction...' % skill_name)

            get_data = getattr(m, 'get_data')
            get_data(self)

        self.dte.commit()

        cnt_dt, cnt_ts = self.dte.get_stats()
        logging.info ('skill %s data extraction done. %d training samples, %d tests' % (skill_name, cnt_dt, cnt_ts))

    def compile_skill_multi (self, skill_names):

        for skill_name in skill_names:
            if skill_name == 'all':
                for mn2 in self.all_skills:
                    self.compile_skill (mn2)

            else:
                self.compile_skill (skill_name)

    def create_context (self, user=DEFAULT_USER, realm=DEFAULT_REALM, test_mode=False):
        return AIContext(user, self.session, self.lang, realm, self, test_mode=test_mode)

    def test_skill (self, skill_name, run_trace=False, test_name=None):

        if run_trace:
            pyxsb_command("trace.")
        else:
            pyxsb_command("notrace.")

        m = self.skills[skill_name]

        logging.info('running tests of skill %s ...' % (skill_name))

        num_tests = 0
        num_fails = 0
        for tc in self.dte.lookup_tests(skill_name):
            t_name, self.lang, prep_code, prep_fn, rounds, src_fn, self.src_line = tc

            if test_name:
                if t_name != test_name:
                    logging.info ('skipping test %s' % t_name)
                    continue

            ctx        = self.create_context(user=TEST_USER, realm=TEST_REALM, test_mode=True)
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
               
                logging.info("test_skill: %s round %d test_inp    : %s" % (t_name, round_num, repr(test_inp)) )
                logging.info("test_skill: %s round %d test_out    : %s" % (t_name, round_num, repr(test_out)) )

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
                        logging.error('test_skill: %s round %d EXCEPTION CAUGHT %s' % (t_name, round_num, traceback.format_exc()))
                        logging.error(ecode)

                if acode is None:
                    logging.error (u'Error: %s: no training data for test_in "%s" found in DB!' % (t_name, test_inp))
                    num_fails += 1
                    break

                resps = ctx.get_resps()

                for i, resp in enumerate(resps):
                    actual_out, score, actual_action, actual_action_arg = resp
                    # logging.info("test_skill: %s round %d %s" % (clause.location, round_num, repr(abuf)) )

                    if len(test_out) > 0:
                        if len(actual_out)>0:
                            actual_out = u' '.join(tokenize(actual_out, self.lang))
                        logging.info("test_skill: %s round %d actual_out  : %s (score: %f)" % (t_name, round_num, actual_out, score) )
                        if actual_out != test_out:
                            logging.info("test_skill: %s round %d UTTERANCE MISMATCH." % (t_name, round_num))
                            continue # no match

                    logging.info("test_skill: %s round %d UTTERANCE MATCHED!" % (t_name, round_num))
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
                    logging.error (u'test_skill: %s round %d no matching response found.' % (t_name, round_num))
                    num_fails += 1
                    break

                round_num   += 1

        return num_tests, num_fails

    def run_tests_multi (self, skill_names, run_trace=False, test_name=None):

        num_tests = 0
        num_fails = 0

        for skill_name in skill_names:

            if skill_name == 'all':

                for mn2 in self.all_skills:
                    self.consult_skill (mn2)
                    n, f = self.test_skill (mn2, run_trace=run_trace, test_name=test_name)
                    num_tests += n
                    num_fails += f

            else:
                self.consult_skill (skill_name)
                n, f = self.test_skill (skill_name, run_trace=run_trace, test_name=test_name)
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
            
            from nlp_model import _START, _STOP, _OR

            logging.debug('trying neural net on: %s' % repr(inp))

            try:
                # ok, exact matching has not yielded any results -> use neural network to
                # generate response(s)

                # import pdb; pdb.set_trace()

                predicted_ids = self.nlp_model.predict(inp)

                # x = self.nlp_model.compute_x(inp)

                # # logging.debug("x: %s -> %s" % (utterance, x))

                # source, source_len, dest, dest_len = self.nlp_model._prepare_batch ([[x, []]], offset=0)

                # # predicted_ids: GreedyDecoder; [batch_size, max_time_step, 1]
                # # BeamSearchDecoder; [batch_size, max_time_step, beam_width]
                # predicted_ids = self.tf_model.predict(self.tf_session, encoder_inputs=source, 
                #                                       encoder_inputs_length=source_len)

                # # for seq_batch in predicted_ids:
                # #     for k in range(5):
                # #         logging.debug('--------- k: %d ----------' % k)
                # #         seq = seq_batch[:,k]
                # #         for p in seq:
                # #             if p == -1:
                # #                 break
                # #             decoded = self.inv_output_dict[p]
                # #             logging.debug (u'%s: %s' %(p, decoded))

                # extract best codes, run them all to see which ones yield the highest scoring responses

                cmd = []
                # for p in predicted_ids[0][:,0]:
                for decoded in predicted_ids:
                    # if p in self.inv_output_dict:
                    #     decoded = self.inv_output_dict[p]
                    # else:
                    #     decoded = p

                    if decoded == _STOP or decoded == _OR:

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
                        if decoded == _STOP:
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

    def train (self, num_epochs=DEFAULT_NUM_EPOCHS, incremental=False):

        self.setup_nlp_model (restore=incremental)
        self.nlp_model.train(num_epochs, incremental)

    def dump_utterances (self, num_utterances, dictfn, skill):

        dic = None
        if dictfn:
            dic = set()
            with codecs.open(dictfn, 'r', 'utf8') as dictf:
                for line in dictf:
                    parts = line.strip().split(';')
                    if len(parts) != 2:
                        continue
                    dic.add(parts[0])

        req = self.dte.session.query(model.TrainingData).filter(model.TrainingData.lang==self.lang)

        if skill and skill != 'all':
            req = req.filter(model.TrainingData.skill==skill)

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

    def stats (self):

        stats = {}

        for skill_name in self.all_skills:    
            stats[skill_name] = {}
            for lang in LANGUAGES:
                cnt = self.session.query(model.TrainingData).filter(model.TrainingData.skill==skill_name,
                                                                    model.TrainingData.lang==lang).count()
                stats[skill_name][lang] = cnt

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

    # FIXME: this will work only on the first call
    def setup_uttclass_model (self, restore=True):

        if self.nlp_model:
            raise Exception ('Tensorflow model can be set up only once.')

        from utt_class_model import UttClassModel

        self.uttclass_model = UttClassModel(lang=self.lang, session=self.session, model_args=self.uttclass_model_args)

        if restore:
            self.uttclass_model.restore()

    def uttclass_train (self, num_epochs=DEFAULT_NUM_EPOCHS, incremental=False):

        self.setup_uttclass_model (restore=incremental)
        self.uttclass_model.train (num_epochs, incremental)

    def uttclass_predict (self, utterances):

        self.setup_uttclass_model (restore=True)
        self.uttclass_model.predict (utterances)

