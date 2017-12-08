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
# take a list of generated aip lines and transform them into two or-blocks, one per language
#
# example input:
#
# train(en) :- "i am a programmer", "".   % ich bin programmiererin
# train(en) :- "i am a soldier", "".  % ich bin soldat
# train(en) :- "i am a student", "".  % ich bin studentin
# train(en) :- "i am a teacher", "".  % ich bin lehrerin
# train(en) :- "i am a woman", "".    % ich bin eine frau
#
# output:
#
# train(en) :- or("i am a programmer",
#                 "i am a soldier",
#                 "i am a student",
#                 "i am a teacher",
#                 "i am a woman"),
#              or("", "").
#
# train(de) :- or("ich bin programmiererin",
#                 "ich bin soldat",
#                 "ich bin studentin",
#                 "ich bin lehrerin",
#                 "ich bin eine frau"),
#              or("", "").
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

def dump():

    global utts_en, utts_de

    if len(utts_en)==1:
        print 'train(en) :- "%s", "".' % utts_en[0]
        print 'train(de) :- "%s", "".' % utts_de[0]

    else:

        print 'train(en) :- or('
        for i, utt in enumerate(utts_en):
            if i < len(utts_en)-1:
                print '                "%s",' % utt
            else:
                print '                "%s"' % utt
        print '               ),'
        print '             or ("", "").'
        print 'train(de) :- or('
        for i, utt in enumerate(utts_de):
            if i < len(utts_de)-1:
                print '                "%s",' % utt
            else:
                print '                "%s"' % utt
        print '               ),'
        print '             or ("", "").'

    print

#
# init, cmdline
#

misc.init_app('transform-block')

parser = OptionParser("usage: %prog [options]")

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

print "Enter/paste source code to be transformed:"

finished = False

utts_de = []
utts_en = []

while not finished:

    try:
        line = raw_input()

        if not line:
            dump()
            utts_de = []
            utts_en = []
            continue

        parts1 = line.split('%')
        if len(parts1) != 2:
            print "*** parsing failed"
            continue

        parts2 = parts1[0].split('"')
        utts_en.append(parts2[1])

        utts_de.append(parts1[1][1:])
    except EOFError:
        finished = True

