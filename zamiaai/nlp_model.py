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
# nlp dictionaries, fasttext embedding, numpy model transformation, 
# keras seq2seq model setup
#

from __future__ import print_function

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
from random            import randint
from copy              import deepcopy

import model

from nltools.tokenizer import tokenize
from nltools.misc      import mkdirs

# extra decoder symbols

_START   = '_START'
_STOP    = '_STOP' 
_OR      = '__OR__'

START_ID = 0
STOP_ID  = 1
OR_ID    = 2

DEBUG_LIMIT                = 0
# DEBUG_LIMIT                = 1000

class NLPModel(object):

    def __init__(self, lang, session, model_args ):

        self.model_dir       = model_args['model_dir']
        self.lang            = lang
        self.session         = session
        self.max_inp_len     = model_args['max_input_len']
        self.lstm_latent_dim = model_args['lstm_latent_dim']
        self.batch_size      = model_args['batch_size']


        # if global_step>0:
        #     self.model_fn    = '%s/latest.ckpt-%d' % (self.model_dir, global_step)
        # else:
        #     self.model_fn    = '%s/latest.ckpt' % (self.model_dir)
        self.weights_fn      = '%s/weights.h5' % (self.model_dir)
        # self.in_dict_fn  = '%s/in_dict.csv' % (self.model_dir)
        self.decoder_dict_fn = '%s/decoder_dict.csv' % (self.model_dir)


    def _compute_2d_diagram(self):

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

            if not longest_inp or (inp_len > len(longest_inp[0])):
                longest_inp = (deepcopy(inp), deepcopy(resp))
            if not longest_resp or (resp_len > len(longest_resp[1])):
                longest_resp = (deepcopy(inp), deepcopy(resp))

        logging.info('longest input: %s' % repr(longest_inp[0]))
        logging.info('               %s' % repr(longest_inp[1]))
        logging.info('longest resp : %s' % repr(longest_resp[0]))
        logging.info('               %s' % repr(longest_resp[1]))

        return dia

    def _compute_decoder_dict(self):

        self.decoder_dict = {_START : START_ID, _STOP : STOP_ID, _OR : OR_ID}

        self.num_segments = 0
        for inp, resp in self.training_data:
            for pred in resp:
                if not pred in self.decoder_dict:
                    self.decoder_dict[pred] = len(self.decoder_dict)

            self.num_segments += 1

        logging.info ('decoder dict done: %d entries. num_segments: %d.' %
                      (len(self.decoder_dict), self.num_segments))

        self.reverse_decoder_dict = dict( (i, token) for token, i in self.decoder_dict.items() )

    def _save_decoder_dict(self):

        with codecs.open(self.decoder_dict_fn, 'w', 'utf8') as f:

            f.write("%d\n" % self.max_resp_len)

            for k in sorted(self.decoder_dict):

                f.write(u"%d;%s\n" % (self.decoder_dict[k], k))

        logging.info ('%s written.', self.decoder_dict_fn)

    def _load_decoder_dict(self):
        with codecs.open(self.decoder_dict_fn, 'r', 'utf8') as f:

            self.max_resp_len = int(f.readline().rstrip())

            self.decoder_dict = {}

            while True:
                line = f.readline()
                if not line:
                    break

                line = line.lstrip().rstrip()

                parts = line.split(';')

                self.decoder_dict[parts[1]] = int(parts[0])

        logging.info ('%s read, %d entries, max_resp_len=%d.' % (self.decoder_dict_fn, len(self.decoder_dict), self.max_resp_len))

        self.reverse_decoder_dict = dict( (i, token) for token, i in self.decoder_dict.items() )

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

    def restore(self):
        self._load_word_embeddings()
        self._load_decoder_dict()
        self._create_keras_model()
        self.keras_model_train.load_weights(self.weights_fn)


    def predict (self, inp):

        td_inp  = tokenize(inp, lang=self.lang)
        num_decoder_tokens = len (self.decoder_dict)

        encoder_input_data  = np.zeros( (1, self.max_inp_len, self.embed_dim), dtype='float32')

        for j, token in enumerate(td_inp):
            if unicode(token) in self.embedding_dict:
                encoder_input_data[0, j] = self.embedding_dict[unicode(token)]

        logging.debug('encoder_input_data[0]: %s' % str(encoder_input_data[0])) 

        # import pdb; pdb.set_trace()

        # Encode the input as state vectors.
        states_value = self.keras_model_encoder.predict(encoder_input_data)

        # Generate empty target sequence of length 1.
        target_seq = np.zeros((1, 1, num_decoder_tokens))
        # Populate the first token of target sequence with the start token.
        target_seq[0, 0, self.decoder_dict[_START]] = 1.

        # Sampling loop for a batch of sequences
        # (to simplify, here we assume a batch of size 1).
        stop_condition = False
        decoded_sequence = []
        while not stop_condition:
            output_tokens, h, c = self.keras_model_decoder.predict([target_seq] + states_value)

            # Sample a token
            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            sampled_token = self.reverse_decoder_dict[sampled_token_index]
            decoded_sequence.append(sampled_token)

            logging.debug('sampled_token_index=%d, sampled_token=%s' % (sampled_token_index, sampled_token)) 

            # Exit condition: either hit max length
            # or find stop token.
            if (sampled_token == _STOP or len(decoded_sequence) > self.max_resp_len):
                stop_condition = True

            # Update the target sequence (of length 1).
            target_seq = np.zeros((1, 1, num_decoder_tokens))
            target_seq[0, 0, sampled_token_index] = 1.

            # Update states
            states_value = [h, c]

        return decoded_sequence

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

    def _create_keras_model(self):

        # for an explanation on how this works, see:
        # https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html

        num_encoder_tokens = self.embed_dim
        num_decoder_tokens = len (self.decoder_dict)

        # Define an input sequence and process it.
        encoder_inputs = keras.layers.Input(shape=(None, num_encoder_tokens))
        encoder        = keras.layers.LSTM(self.lstm_latent_dim, return_state=True)
        encoder_outputs, state_h, state_c = encoder(encoder_inputs)
        # We discard `encoder_outputs` and only keep the states.
        encoder_states = [state_h, state_c]

        # Set up the decoder, using `encoder_states` as initial state.
        decoder_inputs = keras.layers.Input(shape=(None, num_decoder_tokens))
        # We set up our decoder to return full output sequences,
        # and to return internal states as well. We don't use the 
        # return states in the training model, but we will use them in inference.
        decoder_lstm = keras.layers.LSTM(self.lstm_latent_dim, return_sequences=True, return_state=True)
        decoder_outputs, _, _ = decoder_lstm(decoder_inputs,
                                             initial_state=encoder_states)
        decoder_dense = keras.layers.Dense(num_decoder_tokens, activation='softmax')
        decoder_outputs = decoder_dense(decoder_outputs)

        # training

        # `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
        self.keras_model_train = keras.Model([encoder_inputs, decoder_inputs], decoder_outputs)

        self.keras_model_train.compile(optimizer='rmsprop', loss='categorical_crossentropy')
        self.keras_model_train.summary()

        # inference

        self.keras_model_encoder = keras.Model(encoder_inputs, encoder_states)

        decoder_state_input_h = keras.layers.Input(shape=(self.lstm_latent_dim,))
        decoder_state_input_c = keras.layers.Input(shape=(self.lstm_latent_dim,))
        decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
        decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
        decoder_states  = [state_h, state_c]
        decoder_outputs = decoder_dense(decoder_outputs)
        self.keras_model_decoder = keras.Model( [decoder_inputs] + decoder_states_inputs,
                                                [decoder_outputs] + decoder_states)



    def train(self, num_epochs, incremental):

        # load discourses from db, resolve non-unique inputs (implicit or of responses)
        
        logging.info('load discourses from db...')

        drs      = {} 
        for dr in self.session.query(model.TrainingData).filter(model.TrainingData.lang==self.lang):

            if not dr.inp in drs:
                drs[dr.inp] = set()

            resp = [dr.md5s]

            args = json.loads(dr.args)
            if args:
                for arg in args:
                    resp.append(json.dumps(arg))

            drs[dr.inp].add(tuple(resp))

            if DEBUG_LIMIT>0 and len(drs)>=DEBUG_LIMIT:
                logging.warn('  stopped loading discourses because DEBUG_LIMIT of %d was reached.' % DEBUG_LIMIT)
                break
 
        # parse json, add start/stop tokens, implicit or responses:

        self.training_data = []
        self.max_resp_len  = 0

        for inp in drs:

            td_inp  = tokenize(inp, lang=self.lang)
            l = len(td_inp)
            if l > self.max_inp_len:
                raise Exception ('input too long: %s' % repr(td_inp))
                # self.max_inp_len = l

            td_resp = [_START]
            for resp in drs[inp]:
                if len(td_resp)>1:
                    td_resp.append(_OR)
                td_resp.extend(resp)
            td_resp.append(_STOP)
            l = len(td_resp)
            if l > self.max_resp_len:
                self.max_resp_len = l

            # print ("training data: %s -> %s" % (repr(td_inp), repr(td_resp)))

            self.training_data.append((td_inp, td_resp))

        #
        # set up model dir
        #

        if not incremental:
            mkdirs(self.model_dir)

        #
        # 2D diagram of available data
        #

        dia = self._compute_2d_diagram()

        print ("     n  i  o 01020304050607080910111213141516171819202122232425262728293031323334353637383940414243444546474849505152535455")

        for inp_len in range(len(dia)):
            s          = 0
            l          = ''
            cnt        = 0
            for n in dia[inp_len]:
                if cnt<56:
                    l   += ' ' + self._ascii_art(n)
                s   += n
                cnt += 1

            print ('%6d %2d %2d %s' % (s, inp_len+1, self.max_resp_len, l))

        #
        # load word embeddings
        #

        self._load_word_embeddings()

        #
        # load or create decoder dict
        #

        if incremental:
            logging.info("loading decoder dict...")
            self._load_decoder_dict()

        else:
            logging.info("computing decoder dict...")
            self._compute_decoder_dict()
            self._save_decoder_dict()

        #
        # compute datasets
        #

        logging.info("computing datasets...")

        num_decoder_tokens = len (self.decoder_dict)

        encoder_input_data  = np.zeros( (len(self.training_data), self.max_inp_len,  self.embed_dim),
                                        dtype='float32')
        decoder_input_data  = np.zeros( (len(self.training_data), self.max_resp_len, num_decoder_tokens),
                                        dtype='float32')
        decoder_target_data = np.zeros( (len(self.training_data), self.max_resp_len, num_decoder_tokens),
                                        dtype='float32')


        for i, (inp, resp) in enumerate(self.training_data):

            for j, token in enumerate(inp):
                if unicode(token) in self.embedding_dict:
                    encoder_input_data[i, j] = self.embedding_dict[unicode(token)]

            for j, token in enumerate(resp):
                # decoder_target_data is ahead of decoder_input_data by one timestep
                decoder_input_data[i, j, self.decoder_dict[token]] = 1.
                if j > 0:
                    # decoder_target_data will be ahead by one timestep
                    # and will not include the start character.
                    decoder_target_data[i, j - 1, self.decoder_dict[token]] = 1.

        logging.info("computing datasets done. encoder_input_data.shape=%s" % repr(encoder_input_data.shape))
        # print(encoder_input_data[42,2])
        # print (decoder_input_data[42,0])
        # print (decoder_input_data[42,1])
        # print (decoder_input_data[42,2])

        #
        # seq2seq model setup and training starts here
        #

        self._create_keras_model()

        self.keras_model_train.fit([encoder_input_data, decoder_input_data], decoder_target_data,
                             batch_size=self.batch_size,
                             epochs=num_epochs,
                             validation_split=0.2)

        self.keras_model_train.save_weights(self.weights_fn)

        logging.info("weights written to %s ." % self.weights_fn)
