#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017 Guenter Bartsch
#
# some parts based on code and ideas from Suriyadeepan Ramamoorthy, Jaehong Park
# https://github.com/suriyadeepan/easy_seq2seq
# https://github.com/suriyadeepan/practical_seq2seq
# https://github.com/JayParks/tf-seq2seq
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
# nlp dictionaries, numpy model transformation, seq2seq wrapper/helper
#

import os
import sys
import logging
import codecs
import math
import ConfigParser
import json

import numpy      as np
import tensorflow as tf

from time              import time
from random            import randint
from sqlalchemy.orm    import sessionmaker

import model

from nltools.tokenizer import tokenize
from nltools.misc      import mkdirs
from seq2seq_model     import Seq2SeqModel, GO_ID, EOS_ID, UNK_ID, _GO, _EOS, _UNK

OR_SYMBOL = '__OR__'
MAX_NUM_RESP = 3

STEPS_PER_STAT             = 25

DEBUG_LIMIT                = 0

NUM_EVAL_STEPS             = 23

class NLPModel(object):

    def __init__(self, session, ini_fn ):
        self.session     = session
        
        if not ini_fn.endswith('.ini'):
            raise Exception ("no .ini filename extension detected.")

        #
        # set up model dir
        #

        self.model_dir   = ini_fn[:len(ini_fn)-4]
        mkdirs(self.model_dir)

        self.model_fn    = '%s/latest.ckpt' % (self.model_dir)
        self.in_dict_fn  = '%s/in_dict.csv' % (self.model_dir)
        self.out_dict_fn = '%s/out_dict.csv' % (self.model_dir)

        # parse config

        self.config = ConfigParser.ConfigParser()
        self.config.read(ini_fn)

        self.lang       = self.config.get("training", "lang")
        self.network    = 1 if self.config.get("training", "network") == 'output' else 0
        self.batch_size = self.config.getint("training", "batch_size")

        # load discourses from db, resolve non-unique inputs (implicit or of responses)
        
        logging.info('load discourses from db...')

        drs = {} 

        for dr in self.session.query(model.TrainingData).filter(model.TrainingData.lang==self.lang, model.TrainingData.layer==self.network):

            if not dr.inp in drs:
                drs[dr.inp] = set()

            drs[dr.inp].add(dr.resp)
            if DEBUG_LIMIT>0 and len(drs)>=DEBUG_LIMIT:
                logging.warn('  stopped loading discourses because DEBUG_LIMIT of %d was reached.' % DEBUG_LIMIT)
                break

        # parse json, implicit or responses:

        self.training_data = []

        for inp in drs:

            td_inp = map (lambda a: unicode(a), json.loads(inp))

            td_resp  = []
            num_resp = 0
            for r in drs[inp]:
                td_r = map (lambda a: unicode(a), json.loads(r))
                if len(td_resp)>0:
                    td_resp.append(OR_SYMBOL)
                td_resp.extend(td_r)
                if len(td_r)>0:
                    num_resp += 1
                if num_resp > MAX_NUM_RESP:
                    break

            self.training_data.append((td_inp, td_resp))

        self.buckets = []

        bucket_idx = 1
        while True:
            bucket_id = 'bucket%02d' % bucket_idx
            if not self.config.has_option('model', bucket_id):
                break

            bucket_str = self.config.get('model', bucket_id)
            parts      = bucket_str.split(',')
            if len(parts) != 2:
                raise Exception ('Error parsing bucket specification for %s: 2 numbers separated by comma expected, got: "%s"' % (bucket_id, bucket_str))

            self.buckets.append((int(parts[0]), int(parts[1])))

            bucket_idx += 1


    def compute_2d_diagram(self):

        dia = []

        longest_inp  = []
        longest_resp = []

        for inp, resp in self.training_data:

            inp_len   = len(inp)
            resp_len  = len(resp) + 1 # +1 because EOS_ID gets appended later

            while len(dia)<=inp_len:
                dia.append([])

            while len(dia[inp_len])<=resp_len:
                dia[inp_len].append(0)

            dia[inp_len][resp_len] += 1

            # if inp_len == 8 and 'tallinn' in inp:
            #     print "2d diagram: %d -> %d %s %s" % (inp_len, resp_len, inp, resp)

            if inp_len > len(longest_inp):
                longest_inp = inp
            if resp_len > len(longest_resp):
                longest_resp = resp

        logging.info('longest input: %s' % repr(longest_inp))
        logging.info('longest resp : %s' % repr(longest_resp))

        return dia

    def compute_output_hist(self):

        hist = {}

        for inp, resp in self.training_data:

            if not (len(resp) in hist):
                hist[len(resp)] = 0

            hist[len(resp)] += 1
            
        return hist


    def compute_dicts(self):

        # build input and output dicts

        self.input_dict  = {_GO : GO_ID, _EOS : EOS_ID, _UNK : UNK_ID}
        self.output_dict = {_GO : GO_ID, _EOS : EOS_ID, _UNK : UNK_ID}

        self.input_max_len  = 0
        self.output_max_len = 0

        self.num_segments = 0

        for inp, resp in self.training_data:

            # input

            l = len(inp)

            if l > self.input_max_len:
                self.input_max_len = l

            i = 0
            for token in inp:

                if not token in self.input_dict:
                    self.input_dict[token] = len(self.input_dict)

            # output

            l = len(resp) + 1 # +1 to account for _EOS token

            if l > self.output_max_len:
                self.output_max_len = l

            i = 0
            for pred in resp:
                if not pred in self.output_dict:
                    self.output_dict[pred] = len(self.output_dict)

            self.num_segments += 1

        logging.info ('dicts done. input: %d entries, input_max_len=%d. output: %d entries, output_max_len=%d.  num_segments: %d' %
                      (len(self.input_dict), self.input_max_len, len(self.output_dict), self.output_max_len, self.num_segments))

    def save_dicts(self):

        with codecs.open(self.in_dict_fn, 'w', 'utf8') as f:

            f.write("%d\n" % self.input_max_len)

            for k in sorted(self.input_dict):

                f.write(u"%d;%s\n" % (self.input_dict[k], k))

        logging.info ('%s written.', self.in_dict_fn)

        with codecs.open(self.out_dict_fn, 'w', 'utf8') as f:

            f.write("%d\n" % self.output_max_len)

            for k in sorted(self.output_dict):

                f.write(u"%d;%s\n" % (self.output_dict[k], k))

        logging.info ('%s written.', self.out_dict_fn)

    def load_dicts(self):

        with codecs.open(self.in_dict_fn, 'r', 'utf8') as f:

            self.input_max_len = int(f.readline().rstrip())

            self.input_dict = {}

            while True:
                line = f.readline()
                if not line:
                    break

                line = line.lstrip().rstrip()

                parts = line.split(';')

                self.input_dict[parts[1]] = int(parts[0])

        logging.info ('%s read, %d entries, output_max_len=%d.' % (self.in_dict_fn, len(self.input_dict), self.input_max_len))

        with codecs.open(self.out_dict_fn, 'r', 'utf8') as f:

            self.output_max_len = int(f.readline().rstrip())

            self.output_dict = {}

            while True:
                line = f.readline()
                if not line:
                    break

                line = line.lstrip().rstrip()

                parts = line.split(';')

                self.output_dict[parts[1]] = int(parts[0])

        logging.info ('%s read, %d entries, output_max_len=%d.' % (self.out_dict_fn, len(self.output_dict), self.output_max_len))

    def compute_x(self, inp):

        return map(lambda token: self.input_dict[token] if token in self.input_dict else UNK_ID, inp)

        # x = np.zeros(self.input_max_len, np.int32)
        #l = len(tokens)
        #i = 0
        #for token in tokens:
        #    x[self.input_max_len - l + i] = self.input_dict[token] if token in self.input_dict else 0
        #    i += 1

        #return x

    def compute_y(self, response):

        preds = map(lambda pred: self.output_dict[pred] if pred in self.output_dict else UNK_ID, response)

        preds.append(EOS_ID)

        return preds

        # y = np.zeros((self.output_max_len, len(self.output_dict)), np.float32)

        # preds = response.split(';')

        # l = len(preds)
        # i = 0
        # for pred in preds:
        #     out_idx = self.output_dict[pred] if pred in self.output_dict else 0
        #     y[self.output_max_len - l + i, out_idx] = 1.0
        #     i += 1

        # return y

    def create_tf_model(self, tf_session, mode): 

        config = {
            'optimizer'            : self.config.get('training', 'optimizer'),

            'cell_type'            : self.config.get('model', 'cell_type'),
            'attention_type'       : self.config.get('model', 'attention_type'),

            'hidden_units'         : self.config.getint('model', 'hidden_units'),
            'depth'                : self.config.getint('model', 'depth'),
            'embedding_size'       : self.config.getint('model', 'embedding_size'),

            # 'num_encoder_symbols'  : self.config.getint('model', 'num_encoder_symbols'),
            # 'num_decoder_symbols'  : self.config.getint('model', 'num_decoder_symbols'),
            'num_encoder_symbols'  : len(self.input_dict),
            'num_decoder_symbols'  : len(self.output_dict),

            'use_residual'         : self.config.getboolean('model', 'use_residual'),
            'attn_input_feeding'   : self.config.getboolean('model', 'attn_input_feeding'),
            'use_dropout'          : self.config.getboolean('model', 'use_dropout'),

            'dropout_rate'         : self.config.getfloat('model', 'dropout_rate'),

            'learning_rate'        : self.config.getfloat('training', 'learning_rate'),
            'max_gradient_norm'    : self.config.getfloat('training', 'max_gradient_norm'),

            'use_fp16'             : self.config.getboolean('model', 'use_fp16'),

            }


        logging.info("creating %s seq2seq model: %d layer(s) of %d units." % (mode, config['depth'], config['hidden_units']))

        self.model = Seq2SeqModel( config, mode)

        init = tf.global_variables_initializer()
        tf_session.run(init)

        return self.model

    def save_model (self, tf_session, fn=None):
        if not fn:
            fn = self.model_fn
        # self.model.saver.save(tf_session, fn, global_step=self.model.global_step)
        self.model.saver.save(tf_session, fn)
        logging.info("model saved to %s ." % fn)

    def load_model(self, tf_session, fn=None):
        if not fn:
            fn = self.model_fn
        self.model.saver.restore(tf_session, fn)
        logging.info("model restored from %s ." % fn)

    def _ascii_art(self, n):

        if n == 0:
            return ' '
        if n < 10:
            return '.'
        if n < 100:
            return ';'
        if n < 1000:
            return 'o'
        if n < 10000:
            return '*'

        return 'X'

    def _prepare_batch(self, ds):

        seqs_x    = []
        seqs_y    = []

        for i in range(self.batch_size):
            data = ds[randint(0, len(ds)-1)]
            seqs_x.append(data[0])
            seqs_y.append(data[1])

        # seqs_x, seqs_y: a list of sentences
        lengths_x = [len(s) for s in seqs_x]
        lengths_y = [len(s) for s in seqs_y]
        
        x_lengths = np.array(lengths_x)
        y_lengths = np.array(lengths_y)

        maxlen_x = np.max(x_lengths)
        maxlen_y = np.max(y_lengths)

        x = np.ones((self.batch_size, maxlen_x)).astype('int32') * EOS_ID 
        y = np.ones((self.batch_size, maxlen_y)).astype('int32') * EOS_ID 
        
        for idx, [s_x, s_y] in enumerate(zip(seqs_x, seqs_y)):
            x[idx, :lengths_x[idx]] = s_x
            y[idx, :lengths_y[idx]] = s_y
        return x, x_lengths, y, y_lengths


    def train(self):

        #
        # get config
        #

        num_steps = int(self.config.get("training", "num_steps"))

        #
        # 2D diagram of available data
        #

        dia = self.compute_2d_diagram()

        print "     n  i  o 01020304050607080910111213141516171819202122232425262728293031323334353637383940414243444546474849505152535455"

        mol = 0

        for inp_len in range(len(dia)):
            s          = 0
            l          = ''
            output_len = 0
            cnt        = 0
            for n in dia[inp_len]:
                if cnt<56:
                    l   += ' ' + self._ascii_art(n)
                s   += n
                cnt += 1
                if n>0:
                    output_len = cnt

            if output_len > mol:
                mol = output_len

            print '%6d %2d %2d %s' % (s, inp_len+1, mol, l)


        #
        # create input/output dicts
        #

        logging.info("computing input and output dicts...")

        self.compute_dicts()
        self.save_dicts()

        #
        # compute datasets
        #

        logging.info("computing datasets...")

        self.ds_train = []
        self.ds_dev   = []

        cnt = 0
        for inp, resp in self.training_data:

            x = self.compute_x(inp)
            # print dr.inp, x

            y = self.compute_y(resp)
            # print dr.resp, y

            if cnt % 10 == 9:
                data_set = self.ds_dev
            else:
                data_set = self.ds_train

            data_set.append([x, y])
            cnt += 1

        logging.info("computing datasets done. len(ds_train)=%d, len(ds_dev)=%d" % (len(self.ds_train), len(self.ds_dev)))

        #
        # seq2seq model setup and training starts here
        #

        # # setup config to use BFC allocator
        config = tf.ConfigProto()  
        # config.gpu_options.allocator_type = 'BFC'

        with tf.Session(config=config) as tf_session:
            with open('%s/train.log' % self.model_dir, 'w') as logf:

                tf_model = self.create_tf_model(tf_session, 'train')

                # this is the training loop

                step_time, loss, best_perplexity = 0.0, 0.0, 100000.0
                current_step    = 0
                best_step       = 0
                # previous_losses = []
                while tf_model.global_step.eval() <= num_steps:

                    # get a random training batch and perform a training step on it

                    start_time = time()
                    source, source_len, target, target_len = self._prepare_batch(self.ds_train)

                    step_loss, summary = tf_model.train(tf_session, 
                                                        encoder_inputs=source, encoder_inputs_length=source_len, 
                                                        decoder_inputs=target, decoder_inputs_length=target_len)

                    step_time += (time() - start_time) / STEPS_PER_STAT
                    loss += step_loss / STEPS_PER_STAT
                    current_step += 1
              
                    if current_step % STEPS_PER_STAT == 0:

                        # print statistics for the previous epoch.
                        perplexity = math.exp(loss) if loss < 300 else float('inf')

                        steps_done = tf_model.global_step.eval()
                        eta        = (num_steps - steps_done) * step_time

                        # # decrease learning rate if no improvement was seen over last 3 times.
                        # if len(previous_losses) > 2 and loss > max(previous_losses[-3:]):
                        #     tf_session.run(tf_model.learning_rate_decay_op)
                        # previous_losses.append(loss)

                        # get a random dev batch and perform an eval step on it

                        source, source_len, target, target_len = self._prepare_batch(self.ds_dev)

                        sum_dev_loss = 0.0

                        for i in range (NUM_EVAL_STEPS):

                            dev_loss, summary = tf_model.eval (tf_session, 
                                                                encoder_inputs=source, encoder_inputs_length=source_len, 
                                                                decoder_inputs=target, decoder_inputs_length=target_len)
                            sum_dev_loss += dev_loss

                        dev_perplexity = math.exp(sum_dev_loss/NUM_EVAL_STEPS) if sum_dev_loss < 300 else float('inf')

                        log_str = "global step %6d/%6d step-time %.6fs ETA %.2fs train_perpl %.6f dev_perpl %.6f" % \
                                  (steps_done, num_steps, step_time, eta, perplexity, dev_perplexity)

                        logging.info (log_str)
                        logf.write(log_str + '\n')

                        if dev_perplexity < best_perplexity:
                            best_perplexity = dev_perplexity
                            best_step = tf_model.global_step.eval()

                            log_str = "   *** best eval result so far"
                            logging.info(log_str)
                            logf.write(log_str + '\n')

                            # if best_step >= num_steps/5:
                            # logging.info("   saving model to %s ..." % self.model_fn)
                            # self.save_model(tf_session, self.model_fn)
                            tf_model.save(tf_session, self.model_fn, global_step=tf_model.global_step)
                            # logging.info("   saving model to %s ... done." % self.model_fn)
                        # else:
                        #     log_str = "            eval result        (loss: %f, best loss: %f from step %d)" % (dev_loss, best_perplexity, best_step)
                        #     logging.info(log_str)
                        #     logf.write(log_str + '\n')

                        step_time, loss = 0.0, 0.0
               
                        sys.stdout.flush()
                    logf.flush()

                logging.info("training finished.")

                # self.save_model(tf_session, CKPT_FN)

