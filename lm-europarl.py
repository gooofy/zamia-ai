#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2013, 2014 Guenter Bartsch
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

import sys
import re
import os
from os.path import expanduser
import StringIO
import ConfigParser
from gutils import split_words

#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

workdir   = config.get("speech", "lmworkdir")
europarl  = config.get("speech", "europarl")

print
print "Reading sentences from %s..." % europarl

outfn = '%s/europarl.sent' % workdir
outf = open (outfn, 'w')

inf = open (europarl)
count = 0
for line in inf:

    l = line.decode('UTF8').upper()

    # split sentence into words and put it back together 
    # again using single spaces so we get rid of all non-word
    # characters in a uniform way 

    l = ' '.join(split_words(l))

    outf.write (('%s\n' % l).encode('UTF8') )

    count += 1
    if count % 100000 == 0:
        print "%7d sentences..." % count

inf.close()
outf.close()

print
print "%s written." % outfn
print 

