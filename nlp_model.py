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
import numpy as np
from time import time

from speech_tokenizer import tokenize

from sqlalchemy.orm import sessionmaker
import model

import tensorflow as tf

from tensorflow.models.rnn.translate import seq2seq_model
from tensorflow.models.rnn.translate.data_utils import _PAD, PAD_ID, _GO, GO_ID, _EOS, EOS_ID, _UNK, UNK_ID

OUT_DICT_FN  = 'data/dst/nlp_out_dict.csv'
IN_DICT_FN   = 'data/dst/nlp_in_dict.csv'

CKPT_FN      = 'data/dst/nlp_model.ckpt'

# We use a number of buckets and pad to the closest one for efficiency.
# See seq2seq_model.Seq2SeqModel for details of how they work.
# BUCKETS = [(5, 10), (10, 15), (20, 25), (40, 50)]
BUCKETS = [(7, 4), (14, 8)]

# number of network layers : 1/2/3
NUM_LAYERS                 = 1
# typical options : 128, 256, 512, 1024
LAYER_SIZE                 = 128
BATCH_SIZE                 = 64
STEPS_PER_STAT             = 200

LEARNING_RATE              = 0.5
LEARNING_RATE_DECAY_FACTOR = 0.99
MAX_GRADIENT_NORM          = 5.0
USE_LSTM                   = False
NUM_SAMPLES                = 32 
FORWARD_ONLY               = False

class NLPModel(object):

    def __init__(self, session, input_dim = 16 ):
        self.session   = session
        self.input_dim = input_dim

    def compute_input_hist(self):

        hist = {}

        for dr in self.session.query(model.DiscourseRound).all():

            tokens = tokenize (dr.inp)

            if not (len(tokens) in hist):
                hist[len(tokens)] = 0

            hist[len(tokens)] += 1
            
        return hist

    def compute_output_hist(self):

        hist = {}

        for dr in self.session.query(model.DiscourseRound).all():

            preds = dr.resp.split(';')

            if not (len(preds) in hist):
                hist[len(preds)] = 0

            hist[len(preds)] += 1
            
        return hist


    def compute_dicts(self):

        # build input and output dicts

        self.input_dict  = {_PAD : PAD_ID, _GO : GO_ID, _EOS : EOS_ID, _UNK : UNK_ID}
        self.output_dict = {_PAD : PAD_ID, _GO : GO_ID, _EOS : EOS_ID, _UNK : UNK_ID}

        self.input_max_len  = 0
        self.output_max_len = 0

        self.num_segments = 0

        for dr in self.session.query(model.DiscourseRound).all():

            # input

            tokens = tokenize (dr.inp)

            l = len(tokens)

            if l > self.input_max_len:
                self.input_max_len = l

            i = 0
            for token in tokens:

                if not token in self.input_dict:
                    self.input_dict[token] = len(self.input_dict)

            # output

            preds = dr.resp.split(';')
            l = len(preds) + 1 # +1 to account for _EOS token

            if l > self.output_max_len:
                self.output_max_len = l

            i = 0
            for pred in preds:
                if not pred in self.output_dict:
                    self.output_dict[pred] = len(self.output_dict)

            self.num_segments += 1

        logging.info ('dicts done. input: %d enties, input_max_len=%d. output: %d enties, input_max_len=%d.  num_segments: %d' %
                      (len(self.input_dict), self.input_max_len, len(self.output_dict), self.output_max_len, self.num_segments))


    def save_dicts(self):

        with open(IN_DICT_FN, 'w') as f:

            f.write("%d\n" % self.input_max_len)

            for k in sorted(self.input_dict):

                f.write((u"%d;%s\n" % (self.input_dict[k], k)).encode('utf8'))

        logging.info ('%s written.', IN_DICT_FN)

        with open(OUT_DICT_FN, 'w') as f:

            f.write("%d\n" % self.output_max_len)

            for k in sorted(self.output_dict):

                f.write((u"%d;%s\n" % (self.output_dict[k], k)).encode('utf8'))

        logging.info ('%s written.', OUT_DICT_FN)

    def load_dicts(self):

        with open(IN_DICT_FN, 'r') as f:

            self.input_max_len = int(f.readline().rstrip())

            self.input_dict = {}

            while True:
                line = f.readline()
                if not line:
                    break

                line = line.lstrip().rstrip()

                parts = line.split(';')

                self.input_dict[parts[1]] = int(parts[0])

        logging.info ('%s read, %d entries, output_max_len=%d.' % (IN_DICT_FN, len(self.input_dict), self.input_max_len))

        with open(OUT_DICT_FN, 'r') as f:

            self.output_max_len = int(f.readline().rstrip())

            self.output_dict = {}

            while True:
                line = f.readline()
                if not line:
                    break

                line = line.lstrip().rstrip()

                parts = line.split(';')

                self.output_dict[parts[1]] = int(parts[0])

        logging.info ('%s read, %d entries, output_max_len=%d.' % (OUT_DICT_FN, len(self.output_dict), self.output_max_len))

    def compute_x(self, txt):

        tokens = tokenize(txt)

        return map(lambda token: self.input_dict[token] if token in self.input_dict else UNK_ID, tokens)

        # x = np.zeros(self.input_max_len, np.int32)
        #l = len(tokens)
        #i = 0
        #for token in tokens:
        #    x[self.input_max_len - l + i] = self.input_dict[token] if token in self.input_dict else 0
        #    i += 1

        #return x

    def compute_y(self, response):

        preds = map(lambda pred: self.output_dict[pred] if pred in self.output_dict else UNK_ID, response.split(';'))

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

    def create_tf_model(self, tf_session, layer_size                 = LAYER_SIZE, 
                                          num_layers                 = NUM_LAYERS, 
                                          max_gradient_norm          = MAX_GRADIENT_NORM, 
                                          batch_size                 = BATCH_SIZE,
                                          learning_rate              = LEARNING_RATE, 
                                          learning_rate_decay_factor = LEARNING_RATE_DECAY_FACTOR, 
                                          use_lstm                   = USE_LSTM,
                                          num_samples                = NUM_SAMPLES, 
                                          forward_only               = FORWARD_ONLY):

        logging.info("creating seq2seq model: %d layers of %d units." % (num_layers, layer_size))

        print len(self.input_dict), len(self.output_dict), BUCKETS, layer_size, num_layers, max_gradient_norm, batch_size, learning_rate, learning_rate_decay_factor, num_samples, forward_only

        # 20000 20000 [(5, 10), (10, 15), (20, 25), (40, 50)] 128 1 5.0 64 0.5 0.99 True
        #   103    59 [(7, 4), (14, 8)]                       128 1 5.0 64 0.5 0.99 32 True

        self.model = seq2seq_model.Seq2SeqModel( len(self.input_dict), 
                                                 len(self.output_dict),
                                                 BUCKETS, 
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

    def save_model (self, tf_session, fn=CKPT_FN):
        # self.model.saver.save(tf_session, fn, global_step=self.model.global_step)
        self.model.saver.save(tf_session, fn)
        logging.info("model saved to %s ." % fn)

    def load_model(self, tf_session, fn=CKPT_FN):
        self.model.saver.restore(tf_session, fn)
        logging.info("model restored from %s ." % fn)

    # def __len__(self):
    #     return len(self.segments)

    # def __getitem__(self, key):
    #     return self.segments[key]

    # def __iter__(self):
    #     return iter(sorted(self.segments))


    def train(self, num_steps):

        #
        # create input/output dicts
        #

        logging.info("computing input and output dicts...")

        self.compute_dicts()
        self.save_dicts()

        #
        # input and output histograms
        #

        hist = self.compute_input_hist()

        for l in hist:
            logging.debug(" input histogram len=%6d : %8d samples." % (l, hist[l]))

        hist = self.compute_output_hist()

        for l in hist:
            logging.debug(" output histogram len=%6d : %8d samples." % (l, hist[l]))

        #
        # compute datasets
        #

        logging.info("computing datasets...")

        ds_train = [[] for _ in BUCKETS]
        ds_dev   = [[] for _ in BUCKETS]

        cnt = 0
        for dr in self.session.query(model.DiscourseRound).all():

            x = self.compute_x(dr.inp)
            # print dr.inp, x

            y = self.compute_y(dr.resp)
            # print dr.resp, y

            if cnt % 10 == 9:
                data_set = ds_dev
            else:
                data_set = ds_train

            for bucket_id, (x_size, y_size) in enumerate(BUCKETS):
                if len(x) < x_size and len(y) < y_size:
                    data_set[bucket_id].append([x, y])
                    break
            cnt += 1

        train_bucket_sizes = [len(ds_train[b]) for b in xrange(len(BUCKETS))]
        train_total_size = float(sum(train_bucket_sizes))

        dev_bucket_sizes = [len(ds_dev[b]) for b in xrange(len(BUCKETS))]
        dev_total_size = float(sum(dev_bucket_sizes))

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

            tf_model = self.create_tf_model(tf_session)

            # this is the training loop

            step_time, loss = 0.0, 0.0
            current_step = 0
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
                    logging.info ("global step %6d learning rate %.4f step-time %.4fs perplexity %.4f" % \
                                  (tf_model.global_step.eval(), tf_model.learning_rate.eval(), step_time, perplexity))

                    # decrease learning rate if no improvement was seen over last 3 times.
                    if len(previous_losses) > 2 and loss > max(previous_losses[-3:]):
                        tf_session.run(tf_model.learning_rate_decay_op)

                    previous_losses.append(loss)
            
                    step_time, loss = 0.0, 0.0
            
                    # run evals on development set and print their perplexity.
                    for bucket_id in xrange(len(BUCKETS)):
                        if len(ds_dev[bucket_id]) == 0:
                            logging.info("  eval: empty bucket %d" % (bucket_id))
                            continue

                        encoder_inputs, decoder_inputs, target_weights = tf_model.get_batch( ds_dev, bucket_id)
                        _, eval_loss, _ = tf_model.step(tf_session, encoder_inputs, decoder_inputs, target_weights, bucket_id, True)
                        eval_ppx = math.exp(eval_loss) if eval_loss < 300 else float('inf')
                        logging.info("  eval: bucket %d perplexity %.4f" % (bucket_id, eval_ppx))

                    sys.stdout.flush()

            logging.info("training finished. saving model...")

            self.save_model(tf_session, CKPT_FN)


