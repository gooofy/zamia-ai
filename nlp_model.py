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

from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding, LSTM

from speech_tokenizer import tokenize

OUT_TERM_IDX_FN  = 'data/dst/lstm_out_term_idx.csv'
IN_DICT_FN       = 'data/dst/lstm_in_dict.csv'

KERAS_WEIGHTS_FN = 'data/dst/lstm_weights.h5'

DATA_COMPUTED    = 'data/dst'

class NLPModel(object):

    def __init__(self):

        # read segments from .sem files

        self.segments = []

        for fn in os.listdir(DATA_COMPUTED):
            if not fn.endswith('.sem'):
                continue

            logging.info("reading %s..." % fn)

            with codecs.open('%s/%s' % (DATA_COMPUTED, fn), 'r', encoding='utf8') as f:
                for line in f:
                    parts = line.rstrip().split(';')

                    self.segments.append((parts[0], set(map(lambda x: x.lstrip(), parts[1:]))))

    def compute_output_term_index(self):

        # build output term index

        logging.info ('Computing output term index...')

        out_front  = set()
        out_middle = set()
        out_back   = set()

        for segment in self.segments:

            for term in segment[1]:

                # FIXME: hardcoded order, make user configurable

                if 'answer' in term:
                    out_back.add(term)
                elif 'context' in term:
                    out_front.add(term)
                else:
                    out_middle.add(term)


        self.out_idx    = {}
        for term in out_front:
            self.out_idx[term] = len(self.out_idx)
        for term in out_middle:
            self.out_idx[term] = len(self.out_idx)
        for term in out_back:
            self.out_idx[term] = len(self.out_idx)

        logging.info ('%d terms found.' % len(self.out_idx))

        return self.out_idx

    def save_output_term_index(self, fn=OUT_TERM_IDX_FN):

        with open (fn, 'w') as f:

            for k in sorted(self.out_idx):

                f.write((u"%d;%s\n" % (self.out_idx[k], k)).encode('utf8'))

        logging.info ('%s written.', fn)

    def load_output_term_index(self, fn = OUT_TERM_IDX_FN, reverse = True):

        self.out_idx = {}

        with open(fn) as f:

            while True:
                line = f.readline()
                if not line:
                    break

                line = line.lstrip().rstrip()

                parts = line.split(';')

                if reverse:
                    self.out_idx[int(parts[0])] = parts[1]
                else:
                    self.out_idx[parts[1]] = int(parts[0])

        return self.out_idx

    def compute_input_dict(self):

        logging.info ('Computing input dict...')

        self.dictionary = {'': 0}

        self.max_len = 0
        self.num_segments = 0

        for segment in self.segments:

            tokens = tokenize (segment[0])

            # print segment.txt, '->', repr(tokens)

            l = len(tokens)

            if l > self.max_len:
                self.max_len = l

            i = 0
            for token in tokens:
                if not token in self.dictionary:
                    self.dictionary[token] = len(self.dictionary)

            self.num_segments += 1

        logging.info ('input dict done. %d entries, max segment len is %d tokens.' % (len(self.dictionary), self.max_len))

        return self.dictionary, self.max_len, self.num_segments

    def save_input_dict(self, fn=IN_DICT_FN):

        with open(fn, 'w') as f:

            f.write("%d\n" % self.max_len)

            for k in sorted(self.dictionary):

                f.write((u"%d;%s\n" % (self.dictionary[k], k)).encode('utf8'))

        logging.info ('%s written.', IN_DICT_FN)

    def load_input_dict(self, fn=IN_DICT_FN):

        with open(fn) as f:

            self.max_len = int(f.readline().rstrip())

            self.dictionary = {}

            while True:
                line = f.readline()
                if not line:
                    break

                line = line.lstrip().rstrip()

                parts = line.split(';')

                self.dictionary[parts[1]] = int(parts[0])

        return self.dictionary, self.max_len

    def compute_x(self, txt):

        x = np.zeros(self.max_len, np.int32)

        tokens = tokenize(txt)

        l = len(tokens)
        i = 0
        for token in tokens:
            x[self.max_len - l + i] = self.dictionary[token] if token in self.dictionary else 0
            i += 1

        return x

    def create_keras_model(self):

        logging.info ("Creating Keras model...")

        model = Sequential()

        model.add(Embedding(len(self.dictionary), 16, input_length=self.max_len))

        model.add(LSTM(16, dropout_W=0.2, dropout_U=0.2))  # try using a GRU instead, for fun
        model.add(Dense(len(self.out_idx)))
        model.add(Activation('sigmoid'))

        # try using different optimizers and different optimizer configs
        # model.compile(loss='mse',
        #               optimizer='adam',
        #               metrics=['accuracy'])
        model.compile(loss='binary_crossentropy', optimizer='adam')


        return model

    def __len__(self):
        return len(self.segments)

    def __getitem__(self, key):
        return self.segments[key]

    def __iter__(self):
        return iter(sorted(self.segments))
