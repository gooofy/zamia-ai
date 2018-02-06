#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017, 2018 Guenter Bartsch
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

