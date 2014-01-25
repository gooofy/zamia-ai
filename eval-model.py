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
import psycopg2
import ConfigParser
from gutils import compress_ws, run_command, split_words, edit_distance


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

filecount = 0
rows = cur.fetchall()
for row in rows:

    prompt = row[0].decode('UTF8')
    cfn    = row[1]

    mfcfn = "%s/%s.mfc" % (mfccdir, cfn)

    #print "Running julius on %s, expect '%s' output" % (mfcfn, prompt)
    prompts[mfcfn] = prompt

    outf.write ('%s\n' % mfcfn)
    filecount += 1

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

    l = line.decode ('UTF8')

    m = mfcrex.match(l)
    if m:
        mfcfn = m.group(1)
        pe    = prompts[mfcfn]

    m = rex.match(l)
    if m:

        print "%5d/%5d: %s" % (cnt, filecount, mfcfn)
        pr = m.group(1)

        print "    expected: %s" % pe
        print "    got     : %s" % pr

        w1s = split_words(pe)
        w2s = split_words(pr)

        words += len(w1s)
        n_errs = edit_distance(w1s, w2s)

        werr += n_errs

        print "    +%2d word errors, total: %4d errors in %4d words => rate = %3d%%" % (n_errs, werr, words, werr * 100 / words)
        print

        cnt += 1

logf.close()
print "%s written." % logfn
print

