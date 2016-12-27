#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Copyright 2016 Guenter Bartsch. All Rights Reserved.
#
# some parts based on easy_seq2seq by Suriyadeepan Ramamoorthy
# https://github.com/suriyadeepan/easy_seq2seq
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
# ==============================================================================

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

from sqlalchemy.orm import sessionmaker
import model

from nlp_model import NLPModel, BUCKETS, CKPT_FN
import tensorflow as tf

# NUM_STEPS = 200
NUM_STEPS = 2000

STEPS_PER_STAT = 200

#
# init
#

logging.basicConfig(level=logging.DEBUG)

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

#
# session, connect to db
#

Session = sessionmaker(bind=model.engine)

session = Session()

#
# load model
#

nlp_model = NLPModel(session)

#
# create input/output dicts
#

logging.info("computing input and output dicts...")

nlp_model.compute_dicts()
nlp_model.save_dicts()

#
# input and output histograms
#

hist = nlp_model.compute_input_hist()

for l in hist:
    logging.debug(" input histogram len=%6d : %8d samples." % (l, hist[l]))

hist = nlp_model.compute_output_hist()

for l in hist:
    logging.debug(" output histogram len=%6d : %8d samples." % (l, hist[l]))

#
# compute datasets
#

logging.info("computing datasets...")

ds_train = [[] for _ in BUCKETS]
ds_dev   = [[] for _ in BUCKETS]

cnt = 0
for dr in session.query(model.DiscourseRound).all():

    x = nlp_model.compute_x(dr.inp_tokenized)
    # print dr.inp_tokenized, x

    y = nlp_model.compute_y(dr.response)
    # print dr.response, y

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

    tf_model = nlp_model.create_tf_model(tf_session)

    # this is the training loop

    step_time, loss = 0.0, 0.0
    current_step = 0
    previous_losses = []
    while tf_model.global_step.eval() <= NUM_STEPS:
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

    nlp_model.save_model(tf_session, CKPT_FN)

