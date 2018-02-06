#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2018 Guenter Bartsch
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
# train keras module alignment model
#

import os
import sys
import traceback
import codecs
import logging
import time
import numpy as np

from tensorflow import keras

from optparse               import OptionParser
from zamiaai                import model
from nltools                import misc
from nltools.tokenizer      import tokenize
from sqlalchemy.orm         import sessionmaker

# DEBUG_LIMIT        = 5000
DEBUG_LIMIT        = 0
LANG               = 'en'
MODEL_DIR          = 'model'
_PAD               = '__pad'
_PAD_ID            = 0
INPUT_MAX_LEN      = 30

# model / keras
EMB_DIM            = 32
DENSE1_DIM         = 64
DENSE2_DIM         = 64
EPOCHS             = 100
BATCH_SIZE         = 512
VALIDATION_SPLIT   = 0.1

class AlignModel(object):

    def __init__(self, session ):
        self.session     = session
       
        self.keras_weights_fn = '%s/keras_weights.hdf5'  % (MODEL_DIR)
        self.in_dict_fn       = '%s/in_dict.csv'  % (MODEL_DIR)
        self.out_dict_fn      = '%s/out_dict.csv' % (MODEL_DIR)

    def train(self, num_steps, incremental):

        # load discourses from db
        
        logging.info('load discourses from db...')

        self.training_data = []
        tds      = set()
        for td in self.session.query(model.TrainingData).filter(model.TrainingData.lang==LANG).filter(model.TrainingData.module!='bots'):

            if td.inp in tds:
                continue
            tds.add(td.inp)

            inp = tokenize(td.inp, lang=LANG)
            if len(inp) > INPUT_MAX_LEN:
                inp = inp[:INPUT_MAX_LEN]

            self.training_data.append((inp, td.module))

            if DEBUG_LIMIT and len(tds)>DEBUG_LIMIT:
                break

        #
        # set up model dir
        #

        if not incremental:
            try:
                shutil.rmtree(MODEL_DIR)
            except:
                pass

            misc.mkdirs(MODEL_DIR)

        #
        # load or create input/output dicts
        #

        if incremental:
            logging.info("loading input and output dicts...")
            self.load_dicts()

        else:
            logging.info("computing input and output dicts...")

            self.compute_dicts()
            self.save_dicts()

        #
        # compute datasets
        #

        logging.info("computing datasets...")

        train_x = []
        train_y = []

        cnt = 0
        for inp, mn in self.training_data:

            x = self.compute_x(inp)
            y = self.compute_y(mn)

            train_x.append(x)
            train_y.append(y)

            cnt += 1

        self.train_x = np.array(train_x, np.int32)
        self.train_y = keras.utils.to_categorical(train_y, len(self.output_dict))

        logging.info("computing datasets done. train:x=%s,y=%s" % (self.train_x.shape, self.train_y.shape))

        #
        # define the keras model
        #

        keras_model = keras.Sequential()
        keras_model.add(keras.layers.Embedding(len(self.input_dict), EMB_DIM, input_length=INPUT_MAX_LEN))
        keras_model.add(keras.layers.Flatten())
        keras_model.add(keras.layers.Dense(DENSE1_DIM, activation='relu'))
        keras_model.add(keras.layers.Dense(DENSE2_DIM, activation='relu'))
        keras_model.add(keras.layers.Dense(len(self.output_dict), activation='softmax'))

        keras_model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

        logging.info(keras_model.summary())

        #
        # fit training data
        #

        best_loss  = 100.0
        best_epoch = 0

        for epoch in range(EPOCHS):

            h = keras_model.fit(self.train_x, self.train_y, epochs=1, validation_split=VALIDATION_SPLIT, batch_size=BATCH_SIZE)

            cur_loss = h.history['val_loss'][0]

            if cur_loss < best_loss:
                logging.info("*** BEST LOSS SO FAR IN THIS RUN")

                best_loss  = cur_loss
                best_epoch = epoch

                # save the result

                keras_model.save_weights(self.keras_weights_fn, overwrite=True)
                logging.info ('%s written.' % self.keras_weights_fn)




    def compute_dicts(self):

        # build input and output dicts

        self.input_dict  = {_PAD: _PAD_ID}
        self.output_dict = {_PAD: _PAD_ID}

        for inp, mn in self.training_data:

            # input

            i = 0
            for token in inp:
                if not token in self.input_dict:
                    self.input_dict[token] = len(self.input_dict)

            # output

            if not mn in self.output_dict:
                self.output_dict[mn] = len(self.output_dict)

        logging.info ('dicts done. input: %d entries, output: %d entries' %
                      (len(self.input_dict), len(self.output_dict)))

    def save_dicts(self):

        with codecs.open(self.in_dict_fn, 'w', 'utf8') as f:

            for k in sorted(self.input_dict):

                f.write(u"%d;%s\n" % (self.input_dict[k], k))

        logging.info ('%s written.', self.in_dict_fn)

        with codecs.open(self.out_dict_fn, 'w', 'utf8') as f:

            for k in sorted(self.output_dict):

                f.write(u"%d;%s\n" % (self.output_dict[k], k))

        logging.info ('%s written.', self.out_dict_fn)

    def load_dicts(self):

        with codecs.open(self.in_dict_fn, 'r', 'utf8') as f:

            self.input_dict = {}

            while True:
                line = f.readline()
                if not line:
                    break

                line = line.lstrip().rstrip()

                parts = line.split(';')

                self.input_dict[parts[1]] = int(parts[0])

        logging.info ('%s read, %d entries.' % (self.in_dict_fn, len(self.input_dict)))

        with codecs.open(self.out_dict_fn, 'r', 'utf8') as f:

            self.output_dict = {}

            while True:
                line = f.readline()
                if not line:
                    break

                line = line.lstrip().rstrip()

                parts = line.split(';')

                self.output_dict[parts[1]] = int(parts[0])

        logging.info ('%s read, %d entries.' % (self.out_dict_fn, len(self.output_dict)))
 
    def compute_x(self, inp):

        x = list(map(lambda token: self.input_dict[unicode(token)] if unicode(token) in self.input_dict else _PAD_ID, inp))

        while len(x) < INPUT_MAX_LEN:
            x.append(_PAD_ID)

        return x

    def compute_y(self, mn):
        y = self.output_dict[mn] if mn in self.output_dict else PAD_ID

        return y

#
# init, cmdline
#

misc.init_app('train_model')

parser = OptionParser("usage: %prog [options]")

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

#
# db
#

Session = sessionmaker(bind=model.engine)
session = Session()

#
# train
#

align_model = AlignModel(session)
align_model.train(100000, False)

