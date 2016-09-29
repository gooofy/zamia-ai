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
# run HAL nlp tests
#

import os
import sys
import logging
import readline
import codecs
import traceback

from optparse import OptionParser
from StringIO import StringIO
from sqlalchemy.orm import sessionmaker

import numpy as np

import model
from logic import *
from logicdb import *
from prolog_engine import PrologEngine
from prolog_parser import PrologParser, PrologError
import prolog_builtins

from speech_tokenizer import tokenize

from nlp_model import NLPModel, KERAS_WEIGHTS_FN

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
# load nlp model
#

nlp_model = NLPModel()

out_idx = nlp_model.load_output_term_index()

print
print 'out idx:'
for i in sorted(out_idx):
    print '    %3d %s' % (i, out_idx[i])

dictionary, max_len = nlp_model.load_input_dict()

print
print 'dictionary:'
for i in sorted(dictionary):
    print '    %3d %s' % (dictionary[i], i)

model = nlp_model.create_keras_model()

model.load_weights(KERAS_WEIGHTS_FN)

#
# init prolog engine
#

db = LogicDB(session)

engine = PrologEngine(db)
prolog_builtins.register_builtins(engine)

parser = PrologParser()

#
# iterate over all data/dst/*.test files, runs tests
#

# 0;computer schalte bitte new rock ein;;action(media, tune, newrock)
# 1;hal mach das radio aus;;action(media, off)
# 2;schalte bitte das radio ein;;action(media, tune, newrock)

for fn in os.listdir('data/dst'):

    if not fn.endswith('.test'):
        continue

    testfn = 'data/dst/%s' % fn
    print 'running tests from %s' % testfn

    for line in codecs.open(testfn, 'r', 'utf8'):
        parts = line.split(';')
        cnt     = int(parts[0])
        nlp_in  = parts[1]
        nlp_out = parts[2]
    
        print 'nlp_in: %s' % nlp_in

        x = nlp_model.compute_x(nlp_in)

        print 'x:', x

        batch_x = np.zeros([0, max_len], np.int32)
        batch_x = np.append(batch_x, [x], axis=0)

        y = model.predict(batch_x)

        y = y[0]

        print 'y:', y
      
        prolog_s = ''

        for i in range(len(y)):

            if y[i] > 0.5:
                if len(prolog_s)>0:
                    prolog_s += ', '
                prolog_s += out_idx[i]
        print '?-', prolog_s

        try:
            c = parser.parse_line_clause_body(prolog_s)
            logging.debug( "Parse result: %s" % c)

            logging.debug( "Searching for c:", c )

            print engine.search(c)

        except PrologError as e:

            print "*** ERROR: %s" % e

sys.exit(0)

while True:

    line = raw_input ('nlp> ')

    if line == 'quit' or line == 'exit':
        break

    try:

        x = nlp_model.compute_x(line)

        print 'x:', x

        batch_x = np.zeros([0, max_len], np.int32)
        batch_x = np.append(batch_x, [x], axis=0)

        y = model.predict(batch_x)

        y = y[0]

        print 'y:', y
      
        prolog_s = ''

        for i in range(len(y)):

            if y[i] > 0.5:
                if len(prolog_s)>0:
                    prolog_s += ', '
                prolog_s += out_idx[i]
        print '?-', prolog_s

        try:
            c = parser.parse_line_clause_body(prolog_s)
            logging.debug( "Parse result: %s" % c)

            logging.debug( "Searching for c:", c )

            print engine.search(c)

        except PrologError as e:

            print "*** ERROR: %s" % e


#         c = parser.parse_line_clause_body(line)
#         logging.debug( "Parse result: %s" % c)
# 
#         logging.debug( "Searching for c:", c )
# 
#         print engine.search(c)

    except PrologError as e:

        print "*** ERROR: %s" % e



