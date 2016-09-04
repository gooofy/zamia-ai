#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import os
import re
import math
import logging

import ConfigParser
from time import time
from datetime import date
from optparse import OptionParser, OptionGroup
from os.path import expanduser

import numpy as np

#from predict.kerasutils import KerasHelper

from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding, LSTM

from speech_tokenizer import tokenize
from nlp_model import NLPModel, KERAS_WEIGHTS_FN

NUM_EPOCHS = 99
BATCH_SIZE = 128

KERAS_MODEL_FN   = 'data/dst/lstm_model.json'

#
# init
#

logging.basicConfig(level=logging.DEBUG)

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

#
# load model
#

nlp_model = NLPModel()

#
# output term index
#

out_idx = nlp_model.compute_output_term_index()
nlp_model.save_output_term_index()

#
# compute input dict
#

dictionary, max_len, num_segments = nlp_model.compute_input_dict()
nlp_model.save_input_dict()

#
# compute dataset
#

batch_x = np.zeros([0, max_len], np.int32)
batch_y = np.zeros([0, len(out_idx)], np.float32)

cnt = 0
for segment in nlp_model:

    x = nlp_model.compute_x(segment[0])

    y = np.zeros(len(out_idx), np.float32)

    for term in segment[1]:
        y[out_idx[term]] = 1.0

    cnt += 1
    logging.debug("%4d/%4d: Generating training data %s -> %s" % (cnt, num_segments, x, y))

    batch_x = np.append(batch_x, [x], axis=0)
    batch_y = np.append(batch_y, [y], axis=0)
    
# print batch_x
# print batch_y

#
# keras model
#

model = nlp_model.create_keras_model()

# with open(KERAS_MODEL_FN, 'w') as f:
#     f.write(model.to_json())
# 
# logging.info("%s written." % KERAS_MODEL_FN)

# print model.metrics_names
#while True:
#    print model.train_on_batch(batch_x, batch_y)

h = model.fit (batch_x, batch_y, batch_size=BATCH_SIZE, nb_epoch=99)

model.save_weights(KERAS_WEIGHTS_FN, overwrite=True)

sys.exit(0)


num_epochs = 0
best_acc  = 0.0
best_loss = 1000.0
while num_epochs < NUM_EPOCHS:
    h = model.fit (batch_x, batch_y, batch_size=BATCH_SIZE, nb_epoch=1)
    num_epochs += 1

    acc = h.history['acc'][0]
    acc = h.history['acc'][0]

    if acc > best_acc:
        logging.info( "*** EPOCH %3d/%3d: acc=%f" % (num_epochs, NUM_EPOCHS, acc))
        best_acc = acc

        model.save_weights(nlp_model.KERAS_WEIGHTS_FN, overwrite=True)

        logging.info("%s written." % nlp_model.KERAS_WEIGHTS_FN)

    else:
        logging.info("    EPOCH %3d/%3d: acc=%f" % (num_epochs, NUM_EPOCHS, acc))

