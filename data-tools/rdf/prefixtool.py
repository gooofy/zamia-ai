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
# simple prefix merger
#
# source for prefixes: http://prefix.cc/popular/all.sparql
#

import os
import sys
import traceback
import codecs
import logging
import random
import time
import rdflib
import dateutil.parser

from copy        import deepcopy
from optparse    import OptionParser
from nltools     import misc
from config      import RDF_PREFIXES

#
# init, config,  cmdline
#

misc.init_app('prefixtool')

parser = OptionParser("usage: %prog [options]")

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

#
# main
#

prefixes = deepcopy(RDF_PREFIXES)
urls = set()
for p in prefixes:
    urls.add(prefixes[p])

with codecs.open('all.sparql', 'r', 'utf8') as allf:

    while True:

        line = allf.readline()
        if not line:
            break

        parts = line.split(':')

        prefix = parts[0].strip()
        url    = ':'.join(parts[1:]).strip()[1:]
        url = url[:len(url)-1]

        if url in urls:
            logging.debug('URL already covered   : %s -> %s' % (prefix, url))
            continue

        if prefix in prefixes:
            logging.debug('PREFIX already taken  : %s -> %s' % (prefix, url))
            continue

        logging.debug('ADDING                : %s -> %s' % (prefix, url))

        prefixes[prefix] = url
        urls.add(url)

for foo in sorted(prefixes.items(), key=lambda x: x[1]):
    print"                %-14s: '%s'," % ("'"+foo[0]+"'", foo[1])

