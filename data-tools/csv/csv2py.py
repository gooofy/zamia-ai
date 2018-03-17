#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017, 2018 Guenter Bartsch
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
#

#
# convert CSV training data to python
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
from nltools                import misc
from nltools.tokenizer      import tokenize
from sqlalchemy.orm         import sessionmaker

DEFAULT_OUTPUT       = 'bar.py'
DEFAULT_LENGTH_LIMIT = 12

#
# init, cmdline
#

misc.init_app('csv2py')

parser = OptionParser("usage: %prog [options] foo.csv")

parser.add_option ("-l", "--length-limit", dest="length_limit", type = "int", default=DEFAULT_LENGTH_LIMIT,
                   help="length limit in words, default: %d" % DEFAULT_LENGTH_LIMIT)
parser.add_option ("-o", "--output", dest="outputfn", type = "string", default=DEFAULT_OUTPUT,
                   help="output file, default: %s" % DEFAULT_OUTPUT)
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

logging.info ('computing training data set...')

td_covered = set()

for td in session.query(model.TrainingData).filter(model.TrainingData.lang=='en'):

    td_covered.add(td.inp)

logging.info ('computing training data set... %d rows done in %fs.' % (len(td_covered), time.time()-time_start))

#
# parse CSV input file, map uncovered inputs
#

logging.info('parsing %s ...' % csvfn)

map_dict = {} # inp_en -> (inp_en, resp_en, inp_de, resp_de)

with codecs.open(csvfn, 'r', 'utf8') as csvf:

    cnt = 0

    for line in csvf:

        cnt += 1

        parts = line.strip().split(';')
        if len(parts) != 4:
            logging.error('failed to parse line: %s' % line.strip())
            continue

        inp_en  = parts[0]
        resp_en = parts[1]
        inp_de  = parts[2]
        resp_de = parts[3]

        if '*' in inp_de:
            continue

        if len(tokenize(inp_en, lang='en'))>options.length_limit:
            logging.debug(u'skipping (too long): %s' % inp_en)
            continue
        if len(tokenize(inp_de, lang='de'))>options.length_limit:
            logging.debug(u'skipping (too long): %s' % inp_de)
            continue
        if len(tokenize(resp_en, lang='en'))>options.length_limit:
            logging.debug(u'skipping (too long): %s' % resp_en)
            continue
        if len(tokenize(resp_de, lang='de'))>options.length_limit:
            logging.debug(u'skipping (too long): %s' % resp_de)
            continue

        inp_en_t = tokenize(inp_en, lang='en')

        inp_en_t = u' '.join(inp_en_t)

        if inp_en_t in td_covered:
            logging.debug (u'%6d %s already covered. next.' % (cnt, inp_en))
            continue

        logging.debug (u'%6d %s' % (cnt, inp_en))
        map_dict[inp_en.lower()] = (inp_en, resp_en, inp_de, resp_de)

#
# generate output AI-Prolog source code
#

cnt = 0

with codecs.open(options.outputfn, 'w', 'utf8') as outf:

    outf.write('#!/usr/bin/env python\n')
    outf.write('# -*- coding: utf-8 -*-\n')
    outf.write('\n')
    outf.write('def get_data(k):\n')
    outf.write('\n')
    # outf.write('    k.dte.set_prefixes([u\'{self_address:W} \'])\n')
    outf.write('    k.dte.set_prefixes([u\'\'])\n')
    outf.write('\n')

    for ques_en_l in sorted(map_dict):

        ques_en, resp_en, ques_de, resp_de = map_dict[ques_en_l]
        ques_en = ques_en.replace('"',' ').replace('(',' ').replace(')',' ').replace('{',' ').replace('}',' ')
        resp_en = resp_en.replace('"',' ').replace('(',' ').replace(')',' ').replace('{',' ').replace('}',' ')
        ques_de = ques_de.replace('"',' ').replace('(',' ').replace(')',' ').replace('{',' ').replace('}',' ')
        resp_de = resp_de.replace('"',' ').replace('(',' ').replace(')',' ').replace('{',' ').replace('}',' ')

        outf.write('    k.dte.dt("en", u"%s", u"%s")\n' % (ques_en, resp_en))
        outf.write('    k.dte.dt("de", u"%s", u"%s")\n' % (ques_de, resp_de))
        outf.write('\n')
        cnt += 1

logging.info ('%s written. cnt: %d' % (options.outputfn, cnt))

