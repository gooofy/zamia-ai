#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Guenter Bartsch
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
# align CSV discourse rounds to existing training data, output in alphabetical sorted order
#

import os
import sys
import traceback
import codecs
import logging
import time
import xml.etree.ElementTree as ET
import numpy as np

from optparse               import OptionParser
from gensim.models          import word2vec
from zamiaai                import model
from nltools                import misc, tokenizer
from sqlalchemy.orm         import sessionmaker

DEFAULT_LOGLEVEL   = logging.DEBUG
DEFAULT_OUTPUT     = 'bar.aip'

#
# init, cmdline
#

misc.init_app('csv2aip')

parser = OptionParser("usage: %prog [options] foo.csv")

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if len(args) != 1:
    parser.print_usage()
    sys.exit(1)

csvfn   = args[0]

#
# db
#

Session = sessionmaker(bind=model.engine)
session = Session()

#
# training data set
#

time_start = time.time()
cnt = 0

logging.info ('computing training data set...')

td_covered = set()

for td in session.query(model.TrainingData).filter(model.TrainingData.lang=='en', model.TrainingData.prio>=0):

    td_covered.add(td.utterance)

logging.info ('computing training data set...done. %d vectors computed in %fs.' % (cnt, time.time()-time_start))

#
# parse CSV input file, map uncovered questions to module:sourcefile keys
#

logging.info('parsing %s ...' % csvfn)

map_dict = {} # ques_en -> (ques_en, resp_en, ques_de, resp_de)

with codecs.open(csvfn, 'r', 'utf8') as csvf:

    cnt = 0

    for line in csvf:

        cnt += 1

        parts = line.strip().split(';')
        if len(parts) != 4:
            logging.error('failed to parse line: %s' % line.strip())
            continue

        ques_en = parts[0]
        resp_en = parts[1]
        ques_de = parts[2]
        resp_de = parts[3]

        if '*' in ques_de:
            continue

        ques_en_t = tokenizer.tokenize(ques_en, lang='en')

        ques_en_t = u' '.join(ques_en_t)

        if ques_en_t in td_covered:
            logging.debug (u'%6d %s already covered. next.' % (cnt, ques_en))
            continue

        logging.debug (u'%6d %s' % (cnt, ques_en))
        map_dict[ques_en.lower()] = (ques_en, resp_en, ques_de, resp_de)

#
# generate output AI-Prolog source code
#

cnt = 0

with codecs.open(DEFAULT_OUTPUT, 'w', 'utf8') as outf:

    for ques_en_l in sorted(map_dict):

        ques_en, resp_en, ques_de, resp_de = map_dict[ques_en_l]
        ques_de_t = u' '.join(tokenizer.tokenize(ques_de, lang='de'))

        outf.write('train(en) :- "%s", "".\t%% %s\n' % (ques_en.replace('"',' '), ques_de_t.replace('"',' ')))
        # outf.write('%% %s\n' % ques_en)
        # outf.write('\t\t\t\ttrain(en) :- "%s", "%s".\n' % (ques_en.replace('"',' '), resp_en.replace('"',' ')))
        # outf.write('\t\t\t\ttrain(de) :- "%s", "%s".\n' % (ques_de.replace('"',' '), resp_de.replace('"',' ')))
        cnt += 1

logging.info ('%s written. cnt: %d' % (DEFAULT_OUTPUT, cnt))

