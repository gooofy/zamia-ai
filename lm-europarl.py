#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import re
import os
from os.path import expanduser
import StringIO
import ConfigParser
from gutils import compress_ws

#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

workdir   = config.get("speech", "lmworkdir")
europarl  = config.get("speech", "europarl")

outf = open ('%s/europarl.sent' % workdir, 'w')

inf = open (europarl)

for line in inf:

    l = compress_ws(line.decode('UTF8').rstrip().upper().replace(',',' ').rstrip('.').replace('!', ' ').replace('"', ' ').replace('?',' ')).lstrip(' ')

    #outf.write (('<s> %s </s>\n' % l).encode('UTF8') )
    outf.write (('%s\n' % l).encode('UTF8') )

 

