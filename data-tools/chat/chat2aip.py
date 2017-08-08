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
# crude chat corpus to zamia ai prolog converter
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

DEFAULT_LOGLEVEL   = logging.DEBUG
DEFAULT_OUTPUT     = 'foo.aip'
DEFAULT_LANG       = 'en'
DEFAULT_LIMIT      = 12 # tokens
DEFAULT_PRIO       = -99

#
# init, cmdline
#

misc.init_app('chat2aip')

parser = OptionParser("usage: %prog [options] foo.chat [ bar.chat ... ]")

parser.add_option ("-L", "--limit", dest="limit", type = "int", default=DEFAULT_LIMIT,
                   help="length limit, default: %d" % DEFAULT_LIMIT)
parser.add_option ("-l", "--lang", dest="lang", type = "string", default=DEFAULT_LANG,
                   help="language, default: %s" % DEFAULT_LANG)
parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")
parser.add_option ("-o", "--output", dest="outputfn", type = "string", default=DEFAULT_OUTPUT,
                   help="output file, default: %s" % DEFAULT_OUTPUT)
parser.add_option ("-p", "--prio", dest="prio", type = "int", default=DEFAULT_PRIO,
                   help="priority, default: %d" % DEFAULT_PRIO)

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

outputfn = options.outputfn
lang     = options.lang

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

cnt        = 0
skipped    = 0

# read input

corpus    = {}

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

            # filter out specials
            if '[' in question or ']' in question or '[' in answer or ']' in answer:
                skipped += 1
                continue

            tq = tokenizer.tokenize(question, lang=lang)
            ta = tokenizer.tokenize(answer,   lang=lang)

            utt = u' '.join(tq)
            if utt in corpus or len(tq)==0:
                skipped += 1
                continue

            # tokenizer debugging
            # if u"'" in question:
            #     logging.info(question)
            #     logging.info(utt)

            lq = len(tq)
            la = len(ta)

            if lq>options.limit or la>options.limit:
                skipped += 1
                continue

            corpus[utt] = (question, answer)

            cnt += 1
            if cnt % 1000 == 0:
                print "%6d rounds, %6d skipped" % (cnt, skipped)


with codecs.open(outputfn, 'w', 'utf8') as outputf:

    outputf.write ('%prolog\n\n')
    outputf.write ('train_priority(%d).\n\n' % options.prio)

    for prefix in [u'', u'Computer, ']:

        for utt in sorted(corpus):
            question, answer = corpus[utt]

            if len(prefix)>0 and prefix in question:
                continue

            outputf.write (u"train(%s) :- \"%s%s\", \"%s\".\n" % (lang, prefix, question, answer))

logging.info ('%s written. %d rounds, %d skipped.' % (outputfn, cnt, skipped))

