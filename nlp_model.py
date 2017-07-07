#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017 Guenter Bartsch
#
# some parts based on ideas from easy_seq2seq by Suriyadeepan Ramamoorthy
# https://github.com/suriyadeepan/easy_seq2seq
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
# nlp dictionaries, predicate terms, numpy model transformation
#

import os
import sys
import logging
import codecs
import math
import ConfigParser
import numpy as np
from time import time

from nltools.tokenizer import tokenize

from sqlalchemy.orm import sessionmaker
import model

import tensorflow as tf

from tensorflow.models.rnn.translate import seq2seq_model
from tensorflow.models.rnn.translate.data_utils import _PAD, PAD_ID, _GO, GO_ID, _EOS, EOS_ID, _UNK, UNK_ID

from nltools.misc import mkdirs
from zamiaprolog.logic import json_to_prolog, prolog_to_json

OR_SYMBOL = '__OR__'
MAX_NUM_RESP = 3

# We use a number of buckets and pad to the closest one for efficiency.
# See seq2seq_model.Seq2SeqModel for details of how they work.
# BUCKETS = [(5, 10), (10, 15), (20, 25), (40, 50)]
# BUCKETS = [(7, 4), 
#            (8, 25),
#            (14, 8), 
#            (28, 16)]

# BUCKETS = [
#            ( 8, 4), 
#            ( 8, 8), 
#            # ( 8, 28),
# 
#            (16, 8), 
#            (16, 18),
#            (16, 35),
# 
#           ]

#     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
#  0
#  1        ;  .  .
#  2        o  ;  ;  .
#  3        o  *  o  ;  .     ;           .           .
#  4        *  X  *  ;  .     ;           .           .
#  5        *  *  *  o  .  .  ;           .           .
#  6        *  o  *  ;     .  .
#  7        *  o  *  ;
#  8        *  o  *  ;
#  9        *  ;  *  ;
# 10        *  ;  *  ;
# 11        *  ;  *  ;
# 12        *  ;  *  .
# 13        o  ;  o
# 14        o  ;  o
# 15        ;  ;  o
# 16        ;  ;  o
# 17        .  ;  o
# 18        ;  ;  ;
# 19              .


# BUCKETS = [
#            ( 5,  4), 
#            ( 7,  5), 
#            #( 7, 17), 
#            (12,  6), 
#            #(20,  6), 
#            (20, 17), 
#           ]
# BUCKETS = [
#            ( 8, 4), 
#            ( 8, 13), 
#            ( 6, 17), 
#            (20, 9), 
#           ]



STEPS_PER_STAT             = 200

USE_LSTM                   = False
NUM_SAMPLES                = 32 
FORWARD_ONLY               = False

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

        self.config = ConfigParser.RawConfigParser()
        self.config.read(ini_fn)

        self.lang    = self.config.get("training", "lang")
        self.network = self.config.get("model", "network")

        # load discourses from db, resolve non-unique inputs (implicit or of responses)

        drs = {} 

        for dr in self.session.query(model.TrainingData).filter(model.TrainingData.lang==self.lang, model.TrainingData.layer==self.network):

            if not dr.inp in drs:
                drs[dr.inp] = set()

            drs[dr.inp].add(dr.resp)

        # parse json, implicit or responses:

        self.training_data = []

        for inp in drs:

            td_inp = map (lambda a: unicode(a), json_to_prolog(inp))

            td_resp  = []
            num_resp = 0
            for r in drs[inp]:
                td_r = map (lambda a: unicode(a), json_to_prolog(r))
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

        self.input_dict  = {_PAD : PAD_ID, _GO : GO_ID, _EOS : EOS_ID, _UNK : UNK_ID}
        self.output_dict = {_PAD : PAD_ID, _GO : GO_ID, _EOS : EOS_ID, _UNK : UNK_ID}

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

    def create_tf_model(self, tf_session, use_lstm                   = USE_LSTM,
                                          num_samples                = NUM_SAMPLES, 
                                          forward_only               = FORWARD_ONLY):


        layer_size                 = int(self.config.get  ('model', 'layer_size'))
        num_layers                 = int(self.config.get  ('model', 'num_layers'))
        max_gradient_norm          = float(self.config.get('model', 'max_gradient_norm'))
        batch_size                 = int(self.config.get  ('model', 'batch_size'))
        learning_rate              = float(self.config.get('model', 'learning_rate'))
        learning_rate_decay_factor = float(self.config.get('model', 'learning_rate_decay_factor'))

        logging.info("creating seq2seq model: %d layers of %d units." % (num_layers, layer_size))

        print len(self.input_dict), len(self.output_dict), self.buckets, layer_size, num_layers, max_gradient_norm, batch_size, learning_rate, learning_rate_decay_factor, num_samples, forward_only

        # 20000 20000 [(5, 10), (10, 15), (20, 25), (40, 50)] 128 1 5.0 64 0.5 0.99 True
        #   103    59 [(7, 4), (14, 8)]                       128 1 5.0 64 0.5 0.99 32 True

        self.model = seq2seq_model.Seq2SeqModel( len(self.input_dict), 
                                                 len(self.output_dict),
                                                 self.buckets, 
                                                 layer_size, 
                                                 num_layers, 
                                                 max_gradient_norm, 
                                                 batch_size, 
                                                 learning_rate, 
                                                 learning_rate_decay_factor, 
                                                 num_samples=num_samples,
                                                 forward_only=forward_only)
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

    # def __len__(self):
    #     return len(self.segments)

    # def __getitem__(self, key):
    #     return self.segments[key]

    # def __iter__(self):
    #     return iter(sorted(self.segments))


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

        # #
        # # input and output histograms
        # #

        # hist = self.compute_input_hist()

        # for l in hist:
        #     logging.debug(" input histogram len=%6d : %8d samples." % (l, hist[l]))

        # hist = self.compute_output_hist()

        # for l in hist:
        #     logging.debug(" output histogram len=%6d : %8d samples." % (l, hist[l]))

        #
        # compute datasets
        #

        logging.info("computing datasets...")

        ds_train = [[] for _ in self.buckets]
        ds_dev   = [[] for _ in self.buckets]

        cnt = 0
        for inp, resp in self.training_data:

            x = self.compute_x(inp)
            # print dr.inp, x

            y = self.compute_y(resp)
            # print dr.resp, y

            if cnt % 10 == 9:
                data_set = ds_dev
            else:
                data_set = ds_train

            bucket_found = False

            for bucket_id, (x_size, y_size) in enumerate(self.buckets):
                if len(x) < x_size and len(y) < y_size:
                    data_set[bucket_id].append([x, y])
                    bucket_found = True
                    break

            if not bucket_found:
                raise Exception ('ERROR: no bucket found for %d -> %d (%s -> %s)' % (len(x), len(y), inp, resp))

            cnt += 1

        train_bucket_sizes = [len(ds_train[b]) for b in xrange(len(self.buckets))]
        train_total_size = float(sum(train_bucket_sizes))

        dev_bucket_sizes = [len(ds_dev[b]) for b in xrange(len(self.buckets))]
        dev_total_size = float(sum(dev_bucket_sizes))

        for i, tbs in enumerate(train_bucket_sizes):
            logging.info('bucket %-10s train: %6d samples, dev: %6d samples' % (repr(self.buckets[i]), tbs, dev_bucket_sizes[i]))

        logging.info("total num samples: %d, train: %s, dev: %s" % (cnt, repr(train_bucket_sizes), repr(dev_bucket_sizes)))
        # logging.debug("ds_train: %s" % repr(ds_train))

        # A bucket scale is a list of increasing numbers from 0 to 1 that we'll use
        # to select a bucket. Length of [scale[i], scale[i+1]] is proportional to
        # the size if i-th training bucket, as used later.
        train_buckets_scale = [sum(train_bucket_sizes[:i + 1]) / train_total_size
                               for i in xrange(len(train_bucket_sizes))]

        #
        # seq2seq model setup and training starts here
        #

        # setup config to use BFC allocator
        config = tf.ConfigProto()  
        config.gpu_options.allocator_type = 'BFC'

        with tf.Session(config=config) as tf_session:
            with open('%s/train.log' % self.model_dir, 'w') as logf:

                tf_model = self.create_tf_model(tf_session)

                # this is the training loop

                step_time, loss, best_loss = 0.0, 0.0, 100000.0
                current_step    = 0
                best_step       = 0
                previous_losses = []
                while tf_model.global_step.eval() <= num_steps:
                    # Choose a bucket according to data distribution. We pick a random number
                    # in [0, 1] and use the corresponding interval in trainBUCKETS_scale.
                    random_number_01 = np.random.random_sample()
                    bucket_id = min([i for i in xrange(len(train_buckets_scale))
                                     if train_buckets_scale[i] > random_number_01])
             
                    # logging.debug("chose bucket id %d" % bucket_id)

                    # get a batch and make a step

                    start_time = time()
                    encoder_inputs, decoder_inputs, target_weights = tf_model.get_batch(ds_train, bucket_id)
              
                    # print ("encoder_inputs: %s, decoder_inputs: %s, target_weigths: %s" % (encoder_inputs, decoder_inputs, target_weights))
              
                    _, step_loss, _ = tf_model.step(tf_session, encoder_inputs, decoder_inputs, target_weights, bucket_id, False)

                    step_time += (time() - start_time) / STEPS_PER_STAT
                    loss += step_loss / STEPS_PER_STAT
                    current_step += 1
              
                    if current_step % STEPS_PER_STAT == 0:

                        # print statistics for the previous epoch.
                        perplexity = math.exp(loss) if loss < 300 else float('inf')

                        log_str = "global step %6d/%6d learning rate %.6f step-time %.6fs perplexity %.6f" % \
                                  (tf_model.global_step.eval(), num_steps, tf_model.learning_rate.eval(), step_time, perplexity)

                        logging.info (log_str)
                        logf.write(log_str + '\n')

                        # decrease learning rate if no improvement was seen over last 3 times.
                        if len(previous_losses) > 2 and loss > max(previous_losses[-3:]):
                            tf_session.run(tf_model.learning_rate_decay_op)

                        previous_losses.append(loss)
                        step_time, loss = 0.0, 0.0
               
                        sum_loss = 0.0
                
                        # run evals on development set and print their perplexity.
                        for bucket_id in xrange(len(self.buckets)):
                            if len(ds_dev[bucket_id]) == 0:
                                logging.info("  eval: empty bucket %d" % (bucket_id))
                                continue

                            encoder_inputs, decoder_inputs, target_weights = tf_model.get_batch( ds_dev, bucket_id)
                            _, eval_loss, _ = tf_model.step(tf_session, encoder_inputs, decoder_inputs, target_weights, bucket_id, True)
                            eval_ppx = math.exp(eval_loss) if eval_loss < 300 else float('inf')

                            log_str = "  eval: bucket %d perplexity %.6f" % (bucket_id, eval_ppx)
                            logging.info(log_str)
                            logf.write(log_str + '\n')
                            
                            sum_loss += eval_loss

                        if sum_loss < best_loss:
                            best_loss = sum_loss
                            best_step = tf_model.global_step.eval()

                            log_str = "*** best eval result so far (loss: %f)" % (sum_loss)
                            logging.info(log_str)
                            logf.write(log_str + '\n')

                            if best_step >= num_steps/5:
                                logging.info("saving model to %s ..." % self.model_fn)
                                self.save_model(tf_session, self.model_fn)
                        else:
                            log_str = "         eval result        (loss: %f, best loss: %f from step %d)" % (sum_loss, best_loss, best_step)
                            logging.info(log_str)
                            logf.write(log_str + '\n')

                        sys.stdout.flush()
                    logf.flush()

                logging.info("training finished.")

                # self.save_model(tf_session, CKPT_FN)

