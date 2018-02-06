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
# crude aiml to flat csv format converter, uses google translate for english/german translation
#

import os
import sys
import traceback
import codecs
import logging
import time

# import xml.etree.ElementTree as ET
from optparse          import OptionParser
from lxml              import etree as ET

from nltools           import misc
from nltools.tokenizer import tokenize

from googletrans       import Translator

DEFAULT_LOGLEVEL   = logging.DEBUG
DEFAULT_OUTPUT     = 'foo.csv'
DEFAULT_LANG       = 'de'

#
# init, cmdline
#

misc.init_app('aim2csv')

parser = OptionParser("usage: %prog [options] foo.aiml [bar.aiml ...]")

parser.add_option ("-l", "--lang", dest="lang", type = "string", default=DEFAULT_LANG,
                   help="language, default: %s" % DEFAULT_LANG)
parser.add_option ("-n", "--aiml-namespace", action="store_true", dest="aiml_namespace",
                   help="use aiml: tags")
parser.add_option ("-o", "--output", dest="outputfn", type = "string", default=DEFAULT_OUTPUT,
                   help="output file, default: %s" % DEFAULT_OUTPUT)
parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

outputfn = options.outputfn

if options.aiml_namespace:

    AIML_CATEGORY = 'aiml:category'
    AIML_PATTERN  = 'aiml:pattern'
    AIML_TEMPLATE = 'aiml:template'
    AIML_SRAI     = 'aiml:srai'
    AIML_THAT     = 'aiml:that'
    AIML_BOT      = 'aiml:bot'
    AIML_SET      = 'aiml:set'
    AIML_GET      = 'aiml:get'

else:

    AIML_CATEGORY = 'category'
    AIML_PATTERN  = 'pattern'
    AIML_TEMPLATE = 'template'
    AIML_SRAI     = 'srai'
    AIML_THAT     = 'that'
    AIML_BOT      = 'bot'
    AIML_SET      = 'set'
    AIML_GET      = 'get'


#
# logging
#

logging.basicConfig(level=DEFAULT_LOGLEVEL)
logging.getLogger("requests").setLevel(logging.WARNING)

#
# main
#

cnt = 0

res = {}

for aimlfn in args:

    #
    # parse xml
    #

    logging.info('parsing %s ...' % aimlfn)

    try:

        # tree = ET.parse(aimlfn)
        parser = ET.XMLParser(recover=True)
        tree = ET.parse(aimlfn, parser)

        # logging.info('parsing done. converting...')

        root = tree.getroot()

        logging.debug('root tag: %s' % root.tag)

        ns = {'aiml': 'http://alicebot.org/2001/AIML-1.0.1'}

        for category in root.findall(AIML_CATEGORY, ns):

            pattern = category.find(AIML_PATTERN, ns)
            pt      = pattern.text

            if not pt:
                continue

            logging.debug('pattern: %s' % pt)

            for tmpl in category.findall(AIML_TEMPLATE, ns):

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

                # t = t.replace('"', ' ').replace('\n', ' ').replace('\'', ' ')
                t = t.replace('\n', ' ')

                # skip pattern if it contains any aiml mechanics
                # we only want pure text here

                skip_pattern = '*' in pt or '_' in pt or '*' in t or len(t) == 0
                keep_xml    = False
                if tmpl.find(AIML_SRAI, ns) is not None:
                    keep_xml = True
                    skip_pattern = True
                if tmpl.find(AIML_THAT, ns) is not None:
                    keep_xml = True
                    skip_pattern = True
                if tmpl.find(AIML_BOT, ns) is not None:
                    keep_xml = True
                    skip_pattern = True
                if tmpl.find(AIML_SET, ns) is not None:
                    keep_xml = True
                    skip_pattern = True
                if tmpl.find(AIML_GET, ns) is not None:
                    keep_xml = True
                    skip_pattern = True

                # print '   ', t

                # skip_pattern=False

                if not skip_pattern:
                    pt = pt.lower()

                    # check for empty utterances, ignore those
                    if len(tokenize(t, lang=options.lang))==0:
                        continue
                    if len(tokenize(pt, lang=options.lang))==0:
                        continue

                    res[pt] = t

                    cnt += 1
                    if cnt % 1000 == 0:
                        logging.info('   %6d samples extracted.' % cnt)

        logging.info('   %6d samples extracted from this AIML. Unique: %6d' % (cnt, len(res)))

    except:
        logging.error(traceback.format_exc())

#
# translator
#

translator = Translator()

print 'translating...',

with codecs.open(outputfn, 'w', 'utf8') as outputf:

    cnt = 0

    delay = 0.1

    for pt in sorted(res):

        try:

            t = res[pt]

            if options.lang == 'en':
                ques_en = pt
                resp_en = t

                t2 = translator.translate(pt, src=u'en', dest=u'de')
                ques_de = t2.text
                t2 = translator.translate(t, src=u'en', dest=u'de')
                resp_de = t2.text

            elif options.lang == 'de':
     
                ques_de = pt
                resp_de = t

                t2 = translator.translate(pt, src=u'de', dest=u'en')
                ques_en = t2.text
                t2 = translator.translate(t, src=u'de', dest=u'en')
                resp_en = t2.text

            ques_en = ques_en.replace(';',' ').replace('\n',' ')
            resp_en = resp_en.replace(';',' ').replace('\n',' ')
            ques_de = ques_de.replace(';',' ').replace('\n',' ')
            resp_de = resp_de.replace(';',' ').replace('\n',' ')

            line = u"%s;%s;%s;%s" % (ques_en, resp_en, ques_de, resp_de)

            outputf.write(u"%s\n" % line)
            logging.debug(line)

            time.sleep(delay)
        
            cnt += 1
            print '\rtranslating: %d of %d (%5.1f%%)' % (cnt, len(res), cnt*100.0/len(res)),

            if cnt % 100 == 0:
                translator = Translator()

        except:
            logging.error(traceback.format_exc())
            print u"error translating %s" % t
            translator = Translator()

logging.info ('%s written, %d samples total.' % (outputfn, cnt))

