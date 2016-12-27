#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016 Guenter Bartsch
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

import numpy as np

import codecs

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

# number of LSTM layers : 1/2/3
NUM_LAYERS = 1
# typical options : 128, 256, 512, 1024
LAYER_SIZE = 128

BATCH_SIZE = 64

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

            tokens = tokenize (dr.inp_tokenized)

            if not (len(tokens) in hist):
                hist[len(tokens)] = 0

            hist[len(tokens)] += 1
            
        return hist

    def compute_output_hist(self):

        hist = {}

        for dr in self.session.query(model.DiscourseRound).all():

            preds = dr.response.split(';')

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

            tokens = tokenize (dr.inp_tokenized)

            l = len(tokens)

            if l > self.input_max_len:
                self.input_max_len = l

            i = 0
            for token in tokens:

                if not token in self.input_dict:
                    self.input_dict[token] = len(self.input_dict)

            # output

            preds = dr.response.split(';')
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

        tf_session.run(tf.initialize_all_variables())

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
