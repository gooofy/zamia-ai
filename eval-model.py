#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import re
import os
from os.path import expanduser
import StringIO
import psycopg2
import ConfigParser
from gutils import compress_ws, run_command


#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

db_server = config.get("speech", "dbserver")
db_name   = config.get("speech", "dbname")
db_user   = config.get("speech", "dbuser")
db_pass   = config.get("speech", "dbpass")

workdir   = config.get("speech", "workdir")
mfccdir   = config.get("speech", "mfccdir")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# write list of all good mfc files 
#

print "Writing list of all good mfc files..."

cur.execute ("SELECT prompt,cfn FROM submissions WHERE reviewed=true AND noiselevel<2 AND truncated=false AND audiolevel<2 AND pcn<2")

outfn = '%s/mfcfiles.txt' % workdir
outf = open (outfn, 'w')

prompts = {}

rows = cur.fetchall()
for row in rows:

    prompt = row[0].decode('UTF8')
    cfn    = row[1]

    mfcfn = "%s/%s.mfc" % (mfccdir, cfn)

    #print "Running julius on %s, expect '%s' output" % (mfcfn, prompt)
    prompts[mfcfn] = prompt

    outf.write ('%s\n' % mfcfn)

outf.close()

print "%s written." % outfn
print

#
# run julius on all good submissions, check recognition quality
#

print "Running julius..."

logfn = "output/eval.log"
logf = open (logfn, 'w')

mfcrex = re.compile (r"^input MFCC file: (.+)$")
rex = re.compile (r"^wseq1: <s> ([^<]+)</s>$")

cnt    = 0
words  = 0
werr   = 0
mfcfn  = ""
pe     = ""

for line in run_command ( ['julius', '-input', 'mfcfile', '-filelist', outfn,
                           '-h', 'output/acoustic_model_files/hmmdefs', '-hlist', 'output/acoustic_model_files/tiedlist',
                           '-d', 'output/german.bingram', '-v', 'output/dict-julius.txt', '-fbank', '26', '-rawe'] ):

    logf.write(line)

    m = mfcrex.match(line)
    if m:
        mfcfn = m.group(1)
        pe    = prompts[mfcfn]

    m = rex.match(line)
    if m:

        print mfcfn
        pr = m.group(1)

        print pe
        print pr

        w1s = pe.split(' ')
        w2s = pr.split(' ')
        pos = 0
        words += len(w1s)
        for w1 in w1s:
            if pos < len(w2s):
                if w1 != w2s[pos]:
                    werr += 1

            pos += 1

        print "%3d%% word errors" % (werr * 100 / words)
        print

        cnt += 1



logf.close()
print "%s written." % logfn
print

