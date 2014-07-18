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
import psycopg2
import pocketsphinx
from phonetic_alphabets import ipa2xsampa, xsampa2ipa, xsampa2xarpabet

#
# use current audio model to detect good submissions via forced alignment scores and rate/transcribe them automatically
#

WORST_SCORE = -850000
DEBUG_LIMIT = 5000

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

workdir   = config.get("speech", "workdir") + "/align"
featdir   = config.get("speech", "featdir")

hmdir     = config.get("pocketsphinx", "hmm")
lmdir     = config.get("pocketsphinx", "lm")
#dictf     = config.get("pocketsphinx", "dict")
dictf     = "/tmp/voxforge.dic"

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# dump current dict
#

print "dumping current dict..."

pdf  = open (dictf, 'w')

# word -> int, used to generate (2) (3) ... markers for words with multiple pronounciations
word_counter = {}

cur.execute ("SELECT phonemes,word FROM pronounciations,words WHERE pronounciations.wid=words.id ORDER BY word ASC")
rows = cur.fetchall()
for row in rows:

    ipa  = row[0].decode('UTF8')
    word = row[1].decode('UTF8')

    xs = ipa2xsampa(word, ipa)
    xa = xsampa2xarpabet(word, xs)
    
    if not word in word_counter:
        pdf.write ( (u'%s %s\n' % (word, xa)).encode('UTF8') )
        word_counter[word] = 1

    else:
        word_counter[word] += 1
        w2 = u'%s(%d)' % (word, word_counter[word])
        pdf.write ( (u'%s %s\n' % (w2, xa)).encode('UTF8') )

pdf.close()

print "%s written. %d words." % (dictf, len(word_counter))

#
# sphinx_align files setup
#


os.system ("rm -rf %s" % workdir)
os.system ("mkdir %s" % workdir)

transfn = "%s/align.transcription" % workdir
ctlfn   = "%s/align.fileids" % workdir

transf = open (transfn, 'w')
ctlf   = open (ctlfn, 'w')

cnt = 0

cur.execute ('SELECT id,prompt,cfn FROM submissions WHERE cfn LIKE \'%s%%\' AND reviewed=false' % login)
rows = cur.fetchall()
for row in rows:

    sid         = row[0]
    prompt      = row[1].decode('UTF8').lstrip().rstrip()
    cfn         = row[2].decode('UTF8')

    ctlf.write ('%s\n' % cfn)
    transf.write ((u'%s (%s)\n' % (prompt, cfn)).encode('utf8'))

    # FIXME: debug
    cnt += 1
    if cnt > DEBUG_LIMIT:
        break

transf.close()
print "%s written." % transfn
    
ctlf.close()
print "%s written." % ctlfn
   
#
# run sphinx_align
#

segdir = "%s/segmentations" % workdir

cmdline = "sphinx3_align \
    -hmm %s \
	-dict %s \
	-ctl %s \
	-cepdir %s \
	-cepext .mfc \
	-insent %s \
	-outsent %s/alignment_output.txt \
	-wdsegdir %s,CTL " % (hmdir, dictf, ctlfn, featdir, transfn, workdir, segdir)

print 
print cmdline

os.system (cmdline)

#
# parse results, auto-transcribe good submissions
#

for row in rows:

    sid         = row[0]
    prompt      = row[1].decode('UTF8').lstrip().rstrip()
    cfn         = row[2].decode('UTF8')

    resfn = "%s/%s.wdseg" % (segdir, cfn)

    if not os.path.isfile(resfn):
        continue

    wscore = 0

    resf = open(resfn)

    for line in resf:

        l = line.decode('utf8').rstrip()

        #print u"%s %s" % (resfn, l)

        m = re.match(r"^\s+\d+\s+\d+\s+([+\- ]\d+)", l)
        if not m:
            continue

        score = int(m.group(1))
        #print "    score: %d" % score

        # worst score
        if score < wscore:
            wscore = score


    resf.close()

    if wscore < WORST_SCORE:
        print "%-30s %d" % (cfn, wscore)
        continue

    print "%-30s %d ACCEPT!" % (cfn, wscore)
    
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

