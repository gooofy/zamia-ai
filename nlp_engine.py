#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016, 2017 Guenter Bartsch
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
# core nlp engine
#
# natural language -> [ tokenizer ] -> tokens -> [ seq2seq model ] -> prolog -> [ prolog engine ] -> say/action preds
#

import os
import sys
import logging
import traceback

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

class NLPEngine(object):

    def __init__(self, tf_session):

        self.tf_session = tf_session

        # session, connect to db

        Session = sessionmaker(bind=model.engine)

        session = Session()

        #
        # prolog environment setup
        #

        db = LogicDB(session)

        self.prolog_engine = PrologAIEngine(db)

        self.parser = PrologParser()

        for m in model.config.get("semantics", "modules").split(','):
            m = m.strip()
            logging.debug("enabling module %s" % repr(m))
            db.enable_module(m)

        #
        # load nlp model
        #

        self.nlp_model = NLPModel(session)

        self.nlp_model.load_dicts()

        # we need the inverse dict to reconstruct the output from tensor

        self.inv_output_dict = {v: k for k, v in self.nlp_model.output_dict.iteritems()}

        self.tf_model = self.nlp_model.create_tf_model(self.tf_session, forward_only = True) 
        self.tf_model.batch_size = 1

        self.nlp_model.load_model(self.tf_session)

    def process_line(self, line):

        x = self.nlp_model.compute_x(line)

        logging.debug("x: %s -> %s" % (line, x))

        # which bucket does it belong to?
        bucket_id = min([b for b in xrange(len(BUCKETS)) if BUCKETS[b][0] > len(x)])

        # get a 1-element batch to feed the sentence to the model
        encoder_inputs, decoder_inputs, target_weights = self.tf_model.get_batch( {bucket_id: [(x, [])]}, bucket_id )

        # print "encoder_inputs, decoder_inputs, target_weights", encoder_inputs, decoder_inputs, target_weights

        # get output logits for the sentence
        _, _, output_logits = self.tf_model.step(self.tf_session, encoder_inputs, decoder_inputs, target_weights, bucket_id, True)

        logging.debug("output_logits: %s" % repr(output_logits))

        # this is a greedy decoder - outputs are just argmaxes of output_logits.
        outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]

        # print "outputs", outputs

        preds = map (lambda o: self.inv_output_dict[o], outputs)
        logging.debug("preds: %s" % repr(preds))

        prolog_s = ''

        for p in preds:

            if p[0] == '_':
                continue # skip _EOS

            if len(prolog_s)>0:
                prolog_s += ', '
            prolog_s += p

        logging.debug('?- %s' % prolog_s)

        try:
            c = self.parser.parse_line_clause_body(prolog_s)
            logging.debug( "Parse result: %s" % c)

            self.prolog_engine.reset_utterances()
            self.prolog_engine.reset_actions()

            self.prolog_engine.search(c)

            utts    = self.prolog_engine.get_utterances()
            actions = self.prolog_engine.get_actions()

            return utts, actions

        except PrologError as e:

            logging.error("*** ERROR: %s" % e)

        return [], []

