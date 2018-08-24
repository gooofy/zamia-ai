#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
#
# some parts based on code and ideas from Suriyadeepan Ramamoorthy, Jaehong Park
# https://github.com/suriyadeepan/easy_seq2seq
# https://github.com/suriyadeepan/practical_seq2seq
# https://github.com/JayParks/tf-seq2seq
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
# similar to nlp model but will not generate an answer sequence
# but instead do a skill classification (i.e. compute which skill
# seems to be the best place to handle each utterance in)
#

from __future__ import print_function
from six import iteritems

import os
import sys
import logging
import codecs
import math

import json
import shutil

import numpy      as np
import tensorflow as tf

from tensorflow        import keras
from time              import time
from random            import randint, shuffle
from copy              import deepcopy

import model

from nltools.tokenizer import tokenize
from nltools.misc      import mkdirs

DEBUG_LIMIT                = 0
# DEBUG_LIMIT                = 1000

class UttClassModel(object):

    def __init__(self, lang, session, model_args ):

        self.model_dir       = model_args['model_dir']
        self.lang            = lang
        self.session         = session
        self.max_inp_len     = model_args['max_input_len']
        self.conv_filters    = model_args['conv_filters']
        self.dense_dim       = model_args['dense_dim']
        self.batch_size      = model_args['batch_size']
        self.optimizer       = model_args['optimizer']
        self.dropout         = model_args['dropout']

        self.weights_fn      = '%s/utt_class_weights.h5' % (self.model_dir)
        self.skills_dict_fn  = '%s/skills.csv' % (self.model_dir)

    def _load_word_embeddings(self):

        embdfn = '%s/word_embeddings.vec' % self.model_dir
        logging.info('loading word embeddings from %s ...' % embdfn)

        self.embedding_dict = {}
        self.embed_dim      = 0

        with codecs.open(embdfn, encoding='utf-8') as embdf:
            first_line = True
            for line in embdf:
                if first_line:
                    first_line = False
                    continue
                values = line.rstrip().rsplit(' ')
                word = values[0]
                coefs = np.asarray(values[1:], dtype='float32')
                self.embedding_dict[word] = coefs
                if not self.embed_dim: 
                    self.embed_dim = coefs.shape[0]
        nb_words = len(self.embedding_dict)
        logging.info('found %s word vectors of dimension %d.' % (nb_words, self.embed_dim))

    def _compute_skills_dict(self):

        self.skills_dict = {} # skill -> int

        for inp, skill in iteritems(self.drs):
            if not skill in self.skills_dict:
                self.skills_dict[skill] = len(self.skills_dict)

        logging.info ('skills dict done: %d entries.' % len(self.skills_dict))

        self.reverse_skills_dict = dict( (i, token) for token, i in self.skills_dict.items() )

    def _save_skills_dict(self):

        with codecs.open(self.skills_dict_fn, 'w', 'utf8') as f:

            for k in sorted(self.skills_dict):

                f.write(u"%d;%s\n" % (self.skills_dict[k], k))

        logging.info ('%s written.', self.skills_dict_fn)

    def _load_skills_dict(self):
        with codecs.open(self.skills_dict_fn, 'r', 'utf8') as f:

            self.skills_dict = {}
            while True:
                line = f.readline()
                if not line:
                    break

                line = line.lstrip().rstrip()

                parts = line.split(';')

                self.skills_dict[parts[1]] = int(parts[0])

        logging.info ('%s read, %d entries.' % (self.skills_dict_fn, len(self.skills_dict)))

        self.reverse_skills_dict = dict( (i, token) for token, i in self.skills_dict.items() )

    def restore(self):
        self._load_word_embeddings()
        self._load_skills_dict()
        self._create_keras_model()
        self.keras_model_train.load_weights(self.weights_fn)

    def _create_keras_model(self):

        num_skills = len(self.skills_dict)
 
        input_layer  = keras.layers.Input(shape=(self.max_inp_len, self.embed_dim))

        # layer        = keras.layers.LSTM(self.lstm_latent_dim)(input_layer)
        # layer        = keras.layers.Dense(self.dense_dim, name='dense1', activation='relu')(layer)
        # layer        = keras.layers.Dropout(self.dropout, name='dropout1')(layer)

        layer = keras.layers.Conv1D(self.conv_filters, 5, activation='relu', name='conv1')(input_layer)
        layer = keras.layers.MaxPooling1D(5, name='pool1')(layer)
        # layer = keras.layers.Conv1D(128, 2, activation='relu', name='conv2')(layer)
        # layer = keras.layers.MaxPooling1D(2, name='pool2')(layer)
        # layer = keras.layers.Conv1D(128, 5, activation='relu', name='conv3')(layer)
        # layer = keras.layers.MaxPooling1D(35, name='pool3')(layer)  # global max pooling
        layer = keras.layers.Flatten(name='flatten1')(layer)
        layer = keras.layers.Dense(self.dense_dim, activation='relu', name='dense1')(layer)

        output_layer = keras.layers.Dense(num_skills, name='out_layer', activation='softmax')(layer)
        
        self.keras_model_train = keras.Model([input_layer], output_layer)
        self.keras_model_train.compile(optimizer=self.optimizer, loss='categorical_crossentropy')
        self.keras_model_train.summary()

    def predict (self, utterances):

        #
        # compute datasets
        #

        logging.info("computing datasets...")

        num_decoder_tokens = len (self.skills_dict)

        num_inputs = DEBUG_LIMIT if DEBUG_LIMIT else len(utterances)

        input_data = np.zeros( (num_inputs, self.max_inp_len,  self.embed_dim), dtype='float32')

        for i, utt in enumerate(utterances):
            for j, token in enumerate(tokenize(utt, lang=self.lang)):
                if unicode(token) in self.embedding_dict:
                    input_data[i, j] = self.embedding_dict[unicode(token)]

            if DEBUG_LIMIT and i>=(DEBUG_LIMIT-1):
                logging.warn("debug limit of %d utterances reached." % DEBUG_LIMIT)
                break


        # import pdb; pdb.set_trace()

        logging.info("computing dataset done. input_data.shape=%s" % repr(input_data.shape))

        predictions = self.keras_model_train.predict([input_data])

        logging.info("predictions done: %s" % repr(predictions.shape))

        result = []
        for i, utt in enumerate(utterances):
            skill_idx = np.argmax(predictions[i])
            skill = self.reverse_skills_dict.get(skill_idx, '?')

            logging.info("%2d %-10s %s" % (skill_idx, skill, utt))
            result.append(skill)

            if DEBUG_LIMIT and i>=(DEBUG_LIMIT-1):
                break

        return result
        

    def train(self, num_epochs, incremental):

        # load discourses from db, resolve non-unique inputs (implicit or of responses)
        
        logging.info('load discourses from db...')

        self.drs = {} 
        self.training_data = []
        for dr in self.session.query(model.TrainingData).filter(model.TrainingData.lang==self.lang):

            self.drs[dr.inp] = dr.skill
            self.training_data.append((tokenize(dr.inp, lang=self.lang), dr.skill))

            if DEBUG_LIMIT>0 and len(self.drs)>=DEBUG_LIMIT:
                logging.warn('  stopped loading discourses because DEBUG_LIMIT of %d was reached.' % DEBUG_LIMIT)
                break

        shuffle(self.training_data)
 
        #
        # set up model dir
        #

        if not incremental:
            mkdirs(self.model_dir)

        #
        # load word embeddings
        #

        self._load_word_embeddings()

        #
        # load or create decoder dict
        #

        if incremental:
            logging.info("loading skills dict...")
            self._load_skills_dict()

        else:
            logging.info("computing skills dict...")
            self._compute_skills_dict()
            self._save_skills_dict()

        #
        # compute datasets
        #

        logging.info("computing datasets...")

        num_decoder_tokens = len (self.skills_dict)

        encoder_input_data  = np.zeros( (len(self.training_data), self.max_inp_len,  self.embed_dim),
                                        dtype='float32')
        decoder_target_data = np.zeros( (len(self.training_data), len(self.skills_dict)),
                                        dtype='float32')

        for i, (inp, skill) in enumerate(self.training_data):

            for j, token in enumerate(inp):
                if unicode(token) in self.embedding_dict:
                    encoder_input_data[i, j] = self.embedding_dict[unicode(token)]

            skill_idx = self.skills_dict[skill]

            decoder_target_data[i, skill_idx] = 1.

            # logging.debug ("%-10s %2d %s" % (skill, skill_idx, repr(inp)))

            # import pdb; pdb.set_trace()

        logging.info("computing datasets done. encoder_input_data.shape=%s, decoder_target_data.shape=%s" % (repr(encoder_input_data.shape), repr(decoder_target_data.shape)))

        #
        # LSTM RNN classifier model setup and training starts here
        #

        self._create_keras_model()

        self.keras_model_train.fit([encoder_input_data], decoder_target_data,
                                   batch_size=self.batch_size,
                                   epochs=num_epochs,
                                   validation_split=0.2)

        self.keras_model_train.save_weights(self.weights_fn)

        logging.info("weights written to %s ." % self.weights_fn)
