#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016 Guenter Bartsch
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
# interactive nlp shell
#

import os
import sys
import logging
import readline
import atexit
import traceback
import random

from optparse import OptionParser
from StringIO import StringIO
from sqlalchemy.orm import sessionmaker

import numpy as np

import model

from logic import *
from logicdb import *
from prolog_parser import PrologParser, SYM_EOF, PrologError
from prolog_ai_engine import PrologAIEngine

from speech_tokenizer import tokenize

from nlp_model import NLPModel, BUCKETS, CKPT_FN
import tensorflow as tf

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

#
# init terminal
#

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

# session, connect to db

Session = sessionmaker(bind=model.engine)

session = Session()

#
# prolog environment setup
#

db = LogicDB(session)

prolog_engine = PrologAIEngine(db)

parser = PrologParser()

db.enable_module('weather')
db.enable_module('greetings-nlp')
db.enable_module('radio')

#
# readline, history
#

histfile = os.path.join(os.path.expanduser("~"), ".hal_nlp_history")
try:
    readline.read_history_file(histfile)
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(1000)
except IOError:
    pass
atexit.register(readline.write_history_file, histfile)

#
# load nlp model
#

nlp_model = NLPModel(session)

nlp_model.load_dicts()

# we need the inverse dict to reconstruct the output from tensor

inv_output_dict = {v: k for k, v in nlp_model.output_dict.iteritems()}

# setup config to use BFC allocator
config = tf.ConfigProto()  
config.gpu_options.allocator_type = 'BFC'

with tf.Session(config=config) as tf_session:

    tf_model = nlp_model.create_tf_model(tf_session, forward_only = True) 
    tf_model.batch_size = 1

    nlp_model.load_model(tf_session)

    while True:

        line = raw_input ('nlp> ')

        if line == 'quit' or line == 'exit':
            break

        # line = "huhu hal"
        # line = "hal, wie wird das wetter morgen in stuttgart?"

        # print line

        x = nlp_model.compute_x(line)

        # print x

        # which bucket does it belong to?
        bucket_id = min([b for b in xrange(len(BUCKETS)) if BUCKETS[b][0] > len(x)])

        # get a 1-element batch to feed the sentence to the model
        encoder_inputs, decoder_inputs, target_weights = tf_model.get_batch( {bucket_id: [(x, [])]}, bucket_id )

        # print "encoder_inputs, decoder_inputs, target_weights", encoder_inputs, decoder_inputs, target_weights

        # get output logits for the sentence
        _, _, output_logits = tf_model.step(tf_session, encoder_inputs, decoder_inputs, target_weights, bucket_id, True)

        # print "output_logits", output_logits

        # for logit in output_logits:
        #     print "logit", logit
        #     print "argmax", np.argmax(logit, axis=1)

        # this is a greedy decoder - outputs are just argmaxes of output_logits.
        outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]

        # print "outputs", outputs

        preds = map (lambda o: inv_output_dict[o], outputs)
        # print preds

        prolog_s = ''

        for p in preds:

            if p[0] == '_':
                continue # skip _EOS

            if len(prolog_s)>0:
                prolog_s += ', '
            prolog_s += p

        print '?-', prolog_s

        try:
            c = parser.parse_line_clause_body(prolog_s)
            # logging.debug( "Parse result: %s" % c)

            # logging.debug( "Searching for c:", c )

            prolog_engine.reset_utterances()
            prolog_engine.reset_actions()

            prolog_engine.search(c)

            utts = prolog_engine.get_utterances()
            if len(utts)>0:
                print "SAY", random.choice(utts)['utterance']

            actions = prolog_engine.get_actions()
            for action in actions:
                print "ACTION", action

        except PrologError as e:

            print "*** ERROR: %s" % e

