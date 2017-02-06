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
# crude aiml to HAL Prolog converter
#

import os
import sys
import traceback
import codecs
import logging

from optparse import OptionParser
import xml.etree.ElementTree as ET

from nltools import misc, tokenizer

DEFAULT_LOGLEVEL   = logging.DEBUG
DEFAULT_OUTPUT     = 'foo.pl'

#
# init, cmdline
#

misc.init_app('aim2halp')

parser = OptionParser("usage: %prog [options] foo.aiml")

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")
parser.add_option ("-o", "--output", dest="outputfn", type = "string", default=DEFAULT_OUTPUT,
                   help="output file, default: %s" % DEFAULT_OUTPUT)

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

aimlfn   = args[0]
outputfn = options.outputfn

#
# logging
#

logging.basicConfig(level=DEFAULT_LOGLEVEL)
logging.getLogger("requests").setLevel(logging.WARNING)

#
# parse xml
#

logging.info('parsing %s ...' % aimlfn)

tree = ET.parse(aimlfn)

with codecs.open(outputfn, 'w', 'utf8') as outputf:

    outputf.write ('% prolog\n\n')

    logging.info('parsing done. converting...')

    root = tree.getroot()

    logging.debug('root tag: %s' % root.tag)

    ns = {'aiml': 'http://alicebot.org/2001/AIML-1.0.1'}

    for category in root.findall('aiml:category', ns):

        pattern = category.find('aiml:pattern', ns)
        pt      = pattern.text

        if not pt:
            continue

        logging.debug('pattern: %s' % pt)

        for tmpl in category.findall('aiml:template', ns):

            t = tmpl.text.strip() if tmpl.text else ''
            for child in tmpl:
                if child.text:
                    if len(t) > 0:
                        t += ' '
                    t += child.text.strip()

                if child.tail:
                    if len(t) > 0:
                        t += ' '
                    t += ' ' + child.tail.strip()

            t = t.replace('"', ' ').replace('\n', ' ').replace('\'', ' ')

            # comment out pattern if it contains any aiml mechanics
            # we do not support yet

            comment_out = '*' in pt or '_' in pt or '*' in t or len(t) == 0
            keep_xml    = False
            if tmpl.find('aiml:srai', ns) is not None:
                keep_xml = True
                comment_out = True
            if tmpl.find('aiml:that', ns) is not None:
                keep_xml = True
                comment_out = True
            if tmpl.find('aiml:bot', ns) is not None:
                keep_xml = True
                comment_out = True
            if tmpl.find('aiml:set', ns) is not None:
                keep_xml = True
                comment_out = True
            if tmpl.find('aiml:get', ns) is not None:
                keep_xml = True
                comment_out = True


            # print '   ', t

            if comment_out:
                if keep_xml:
                    for l in ET.tostringlist(tmpl, 'utf8'):
                        outputf.write("%% %s',\n" % l.replace('\n',''))

                outputf.write("%% nlp_gen (de, '(HAL,|Computer,|) %s',\n" % pt)
                outputf.write("%%              '%s').\n\n" % t)
            else:
                pt = pt.lower()

                outputf.write("nlp_gen (de, '(HAL,|Computer,|) %s',\n" % pt)
                outputf.write("             '%s').\n\n" % t)

logging.info ('%s written.' % outputfn)

