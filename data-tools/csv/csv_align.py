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
# align CSV input to existing training data sort and export in python format
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
from nltools                import misc, tokenizer
from align_model            import AlignModel

OUTPUT_DIR  = 'out'

#
# init, cmdline
#

misc.init_app('csv_align')

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
# load model
#

align_model = AlignModel(None)
align_model.load()

#
# parse CSV input file, map uncovered questions to module:sourcefile keys
#

logging.info('parsing %s ...' % csvfn)

map_dict = {} # module -> {inp_en -> (resp_en, inp_de, resp_de)}

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

        mn = align_model.predict(inp_en)

        if not mn in map_dict:
            map_dict[mn] = {}

        # logging.debug (u'%6d inp_en: %s -> %s' % (cnt, inp_en, mn))
        map_dict[mn][inp_en] = (resp_en, inp_de, resp_de)


# print repr(map_dict)

#
# generate output files
#


for mn in map_dict:

    outfn = '%s/%s.csv' % (OUTPUT_DIR, mn)
    with codecs.open(outfn, 'w', 'utf8') as outf:

        for ques_en in sorted(map_dict[mn]):

            resp_en, ques_de, resp_de = map_dict[mn][ques_en]

            line = u"%s;%s;%s;%s" % (ques_en, resp_en, ques_de, resp_de)
            outf.write(u"%s\n" % line)

    logging.info ('%s written.' % outfn)

