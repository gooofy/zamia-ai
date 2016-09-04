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

import nlp_model

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

out_idx = nlp_model.load_output_term_index()

print (repr(out_idx))

dictionary, max_len = nlp_model.load_input_dict()

print repr(dictionary)

model = nlp_model.create_keras_model(dictionary, max_len, out_idx)

model.load_weights(nlp_model.KERAS_WEIGHTS_FN)

#
# main
#

db = LogicDB(session)

engine = PrologEngine(db)
prolog_builtins.register_builtins(engine)

parser = PrologParser()

while True:

    line = raw_input ('nlp> ')

    if line == 'quit' or line == 'exit':
        break

    try:

        x = nlp_model.compute_x(line, max_len, dictionary)

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



