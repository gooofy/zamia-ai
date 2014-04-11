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
# use current audio model to detect good submissions and rate/transcribe them automatically
#

#
# commandline
#

parser = OptionParser("usage: %prog [options] login")

parser.add_option ("-p", "--pronounciation", dest="pronounciation", type = "int", default=0,
           help="pronounciation: 0=clean, 1=accent, 2=dialect, 3=error (default: 0)")

parser.add_option ("-t", "--truncated", dest="truncated", action="store_true",
           help="technical: truncated (default: false)")

parser.add_option ("-a", "--audiolevel", dest="audiolevel", type = "int", default=0,
           help="audio level: 0=good, 1=low, 2=very low, 3=distorted (default: 0)")

parser.add_option ("-n", "--noiselevel", dest="noiselevel", type = "int", default=0,
           help="noise level: 0=low, 1=noticable, 2=high (default: 0)")

parser.add_option ("-f", "--force", dest="force", action="store_true",
           help="set review parameters even if transcript exists (default: false)")

parser.add_option ("-c", "--continous", dest="continous", action="store_true",
           help="set continous flag to false (default: true)")

(options, args) = parser.parse_args()

#print "Options: %s, args: %s" % (repr(options), repr(args))

if len(args) != 1:
    print "usage: %s login" % sys.argv[0]
    sys.exit(1)

login = args[0]

truncated = False
if options.truncated:
    truncated = True

force = False
if options.force:
    force = True

continous = True
if options.continous:
    continous = False

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
cur.execute ('SELECT id,prompt,cfn FROM submissions WHERE cfn LIKE \'%s%%\' AND reviewed=false' % login)
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

    if prompt != hstr:
        print 'HYPOTH: %s' % repr(hstr)
        print "PROMPT: %s" % repr(prompt)
        continue

    print 'HYPOTH: ', hypothesis.best_score, hypothesis.hypstr
    print "MATCH!!!!!!"

    cur.execute ('DELETE FROM transcripts WHERE sid=%s', (sid,))

    # collect dictionary entries for all the words
   
    entries = []

    fail = False
 
    words = re.split ('\s+', prompt)
    for word in words:

        w = re.sub(r"[,.?\-! ;:]", '', word.rstrip()).upper()
        if len(w) > 0:

            # dict lookup

            cur.execute ('SELECT id FROM words WHERE word=%s', (word,))
            row = cur.fetchone()
            if row:
                wid = row[0]

                cur.execute ('SELECT id FROM pronounciations WHERE wid=%s', (wid,))
                rows2 = cur.fetchall()

                if len(rows2) != 1:
                    print "*** ERROR: no auto-transcribe possible for word this prompt."
                    fail = True
                    break

                entries.append ( (wid, rows2[0][0]) )
            else:
                print "ERROR: word %s not found in DB!" % w
                fail = True
                break

    if fail:
        continue

    for entry in entries:
        wid = entry[0]
        pid = entry[1]
        #print "%d : %d" % (wid, pid)
        cur.execute ('INSERT INTO transcripts (sid,wid,pid) VALUES (%s, %s, %s)', 
                     (sid, wid, pid))

    print "UPDATE DB..."

    cur.execute ('UPDATE submissions SET reviewed=true, noiselevel=%s, truncated=%s, audiolevel=%s, pcn=%s, continous=%s WHERE id=%s', 
                 (options.noiselevel, truncated, options.audiolevel, options.pronounciation, continous, sid))
    conn.commit()
    cur = conn.cursor()

    print "UPDATE DB...DONE."

