#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Heiko Schaefer, Guenter Bartsch
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
# crude chat corpus to zamia ai python converter
#
# suitable chat corpora can be found here: https://github.com/Marsan-Ma/chat_corpus/
#

import os
import sys
import re
import traceback
import codecs
import logging

from optparse import OptionParser

from nltools import misc, tokenizer
from sqlalchemy.orm import sessionmaker
import model

DEFAULT_LOGLEVEL   = logging.DEBUG
DEFAULT_OUTPUT     = 'foo.py'
DEFAULT_LANG       = 'en'
DEFAULT_LIMIT      = 12 # tokens

#
# db
#

Session = sessionmaker(bind=model.engine)
session = Session()

#
# init, cmdline
#

misc.init_app('convert_chat')

parser = OptionParser("usage: %prog [options] foo.chat [ bar.chat ... ]")

parser.add_option ("-L", "--limit", dest="limit", type = "int", default=DEFAULT_LIMIT,
                   help="length limit, default: %d" % DEFAULT_LIMIT)
parser.add_option ("-l", "--lang", dest="lang", type = "string", default=DEFAULT_LANG,
                   help="language, default: %s" % DEFAULT_LANG)
parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")
parser.add_option ("-o", "--output", dest="outputfn", type = "string", default=DEFAULT_OUTPUT,
                   help="output file, default: %s" % DEFAULT_OUTPUT)

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

outputfn = options.outputfn
lang     = options.lang

#
# existing utterances
#

logging.info('reading existing utterances...')

utterances = set()
for td in session.query(model.TrainingData).filter(model.TrainingData.lang==options.lang, model.TrainingData.module!='ms'):
    utterances.add(td.utterance)

logging.info('reading existing utterances done, %d utterances found.' % len(utterances))

#
# regexp compile
#

MINUS_LINE_PATTERN = re.compile(r"([-]+)")

def replace_minus_line (m):

    s = m.group(0)

    return s.replace(m.group(1), u"-")

#
# main
#

cnt     = 0
skipped = 0

with codecs.open(outputfn, 'w', 'utf8') as outputf:

    outputf.write ('#!/usr/bin/env python\n')
    outputf.write ('# -*- coding: utf-8 -*- \n')

    outputf.write ('from base.utils import nlp_add_round\n')

    outputf.write ('\ndef nlp_train(res):\n')

    for inputfn in args:

        logging.info('processing %s ...' % inputfn)

        with codecs.open(inputfn, 'r', 'utf8', errors='ignore') as inputf:
            while True:

                question = inputf.readline()
                if not question:
                    break
                question = question.strip().replace('"', ' ').replace('+++$+++','').replace('...','.')
                answer   = inputf.readline().strip().replace('"', ' ').replace('%', ' percent ').replace('+++$+++','').replace('...','.')

                question = MINUS_LINE_PATTERN.sub(replace_minus_line, question)
                answer   = MINUS_LINE_PATTERN.sub(replace_minus_line, answer)

                tq = tokenizer.tokenize(question, lang=lang)
                ta = tokenizer.tokenize(answer,   lang=lang)

                utt = u' '.join(tq)
                if utt in utterances or len(tq)==0:
                    skipped += 1
                    continue

                utterances.add(utt)

                # tokenizer debugging
                # if u"'" in question:
                #     logging.info(question)
                #     logging.info(utt)

                lq = len(tq)
                la = len(ta)

                if lq>options.limit or la>options.limit:
                    skipped += 1
                    continue

                for prefix in [u'', u'Computer, ']:

                    outputf.write (u"    res = nlp_add_round(res, \"%s\", u\"%s%s\", u\"%s\")\n" % (lang, prefix, question, answer))

                    cnt += 1
                    if cnt % 1000 == 0:
                        print "%6d rounds, %6d skipped" % (cnt, skipped)

    outputf.write ('\n    return res\n')

logging.info ('%s written. %d rounds, %d skipped.' % (outputfn, cnt, skipped))

