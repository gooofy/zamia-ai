#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2013, 2014 Guenter Bartsch
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
# train NLTK's punkt sentence segmenter
#

import sys
import re
import os
import traceback
import nltk
import pickle
from os.path import expanduser
import StringIO
import ConfigParser
from gutils import split_words, compress_ws
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint


#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

sentences = config.get("speech", "sentences")

trainer = nltk.tokenize.punkt.PunktTrainer()

count = 0

files = os.listdir (sentences)
for file in files:

    if not file.endswith ('.sent'):
        continue

    print "Training on sentences from '%s'" % file

    for line in open ('%s/%s' % (sentences, file)):

        sent = line.decode('UTF8').rstrip()

        trainer.train(sent, finalize=False, verbose=False)

        count += 1
        if count % 1000 == 0:
            print "%6d sentences." % count

print
print "Finalizing training..."
trainer.finalize_training(verbose=True)
print "Training done. %d sentences." % count
print

params = trainer.get_params()
print "Params: %s" % repr(params)

tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer(params)
with open("de_punkt.pickle", mode='wb') as f:
        pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)

print "All done."
print

