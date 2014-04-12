#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import re
import os
import StringIO
import ConfigParser
from optparse import OptionParser
from os.path import expanduser
import subprocess
import json
import psycopg2
from cgi import parse_qs, escape
import pdb
import pocketsphinx
from itertools import izip

#
# use current audio model to detect bad submissions and set them to reviewed=false automatically
#

#
# commandline
#

if len(sys.argv) != 2:
    print "usage: %s <prefix>" % sys.argv[0]
    print
    sys.exit(1)

login = sys.argv[1]

#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

webroot   = config.get("speech", "webroot")

db_server = config.get("speech", "dbserver")
db_name   = config.get("speech", "dbname")
db_user   = config.get("speech", "dbuser")
db_pass   = config.get("speech", "dbpass")

w16dir    = config.get("speech", "16khzdir")

hmdir     = config.get("pocketsphinx", "hmm")
lmdir     = config.get("pocketsphinx", "lm")
dictf     = config.get("pocketsphinx", "dict")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

config = pocketsphinx.Decoder.default_config()
config.set_string('-hmm', hmdir)
config.set_string('-lm', lmdir)
config.set_string('-dict', dictf)
config.set_string('-logfn', "/dev/null")
decoder = pocketsphinx.Decoder(config)

cnt = 0
cur.execute ('SELECT id,prompt,cfn FROM submissions WHERE cfn LIKE \'%s%%\' AND reviewed=true AND noiselevel<=1 AND truncated=false AND audiolevel<=1 AND pcn<=1' % login)
rows = cur.fetchall()
for row in rows:

    sid         = row[0]
    prompt      = row[1].decode('UTF8').lstrip().rstrip()
    cfn         = row[2].decode('UTF8')

    cnt += 1

    print 
    print "%6d/%6d Decoding %s..." % (cnt, len(rows), cfn)

    wavfile = "%s/%s.wav" % (w16dir, cfn)

    wavFile = file(wavfile,'rb')
    decoder.decode_raw(wavFile)

    # Retrieve hypothesis.
    hypothesis = decoder.hyp()

    hstr = hypothesis.hypstr.decode('UTF8').lstrip().rstrip()

    if prompt == hstr:
        print 'HYPOTH: ', hypothesis.best_score, hypothesis.hypstr
        print "MATCH!!!!!!"
        continue

    print 'HYPOTH: %s' % repr(hstr)
    print "PROMPT: %s" % repr(prompt)

    print "UPDATE DB..."

    cur.execute ('DELETE FROM transcripts WHERE sid=%s', (sid,))

    cur.execute ('UPDATE submissions SET reviewed=False WHERE id=%s', (sid,))
    conn.commit()
    cur = conn.cursor()

    print "UPDATE DB...DONE."

