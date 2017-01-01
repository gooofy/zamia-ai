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

import model

from nlp_engine import NLPEngine

import tensorflow as tf

#
# init terminal
#

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

#
# commandline
#

parser = OptionParser("usage: %prog [options] [foo.pl ...] ")

parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                  help="verbose output")

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

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
# setup nlp engine, tensorflow session
#

# setup config to use BFC allocator
config = tf.ConfigProto()  
config.gpu_options.allocator_type = 'BFC'

with tf.Session(config=config) as tf_session:
    nlp_engine = NLPEngine(tf_session)

    while True:

        line = raw_input ('nlp> ')

        if line == 'quit' or line == 'exit':
            break

        utts, actions = nlp_engine.process_line(line)

        if len(utts)>0:
            print "SAY", random.choice(utts)['utterance']

        for action in actions:
            print "ACTION", action

