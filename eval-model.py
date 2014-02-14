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
from optparse import OptionParser
from gutils import compress_ws, run_command, split_words, edit_distance

AUDIO_LIMIT = 0 # debug purposes, 0 to disable

#
# commandline
#

parser = OptionParser("usage: %prog [options] [prefix]")

parser.add_option ("-p", "--pronounciation", dest="pronounciation", type = "int", default=1,
           help="worst acceptable pronounciation: 0=clean, 1=accent, 2=dialect, 3=error (default: 1)")

parser.add_option ("-a", "--audiolevel", dest="audiolevel", type = "int", default=1,
           help="worst acceptable audio level: 0=good, 1=low, 2=very low, 3=distorted (default: 1)")

parser.add_option ("-n", "--noiselevel", dest="noiselevel", type = "int", default=1,
           help="worst acceptable noise level: 0=low, 1=noticable, 2=high (default: 1)")

parser.add_option ("-c", "--continous", dest="continous", action="store_true",
           help="accept non-continous submissions (default: accept only continous submissions)")

(options, args) = parser.parse_args()

#print "Options: %s, args: %s" % (repr(options), repr(args))

prefix = ''
if len(args) ==1:
    prefix = args[0]

continous = True
if options.continous:
    continous = False

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
sql = "SELECT prompt,cfn,id FROM submissions WHERE reviewed=true AND noiselevel<=%s AND truncated=false AND audiolevel<=%s AND pcn<=%s AND cfn LIKE %s"

if continous:
    sql += " AND continous=true"

cur.execute (sql, (options.noiselevel, options.audiolevel, options.pronounciation, prefix+"%") )

#cur.execute ("SELECT prompt,cfn,id FROM submissions WHERE reviewed=true AND noiselevel<2 AND truncated=false AND audiolevel<2 AND pcn<2")

outfn = '%s/ps.ctl' % workdir
outf = open (outfn, 'w')

prompts = {}
sids    = {}

filecount = 0
rows = cur.fetchall()
for row in rows:

    prompt = row[0].decode('UTF8')
    cfn    = row[1]
    sid    = row[2]

    #print "Running pocketsphinx on %s, expect '%s' output" % (mfcfn, prompt)
    prompts[cfn] = prompt
    sids[cfn]    = sid

    outf.write ('%s\n' % cfn)
    filecount += 1

    if AUDIO_LIMIT > 0 and filecount >= AUDIO_LIMIT:
        break

    cur.execute ('SELECT id FROM eval WHERE sid=%s', (sid,))
    row = cur.fetchone()
    if not row:
        cur.execute ('INSERT INTO eval (sid) VALUES (%s)', (sid,))

outf.close()

print "%s written (%d files to evaluate)." % (outfn, filecount)
print

#
# run pocketsphinx on all good submissions, check recognition quality
#

print "Running pocketsphinx..."

hypfn = 'result/eval.hyp'
segfn = 'result/eval.seg'

os.system ('cd %s; pocketsphinx_batch -cepdir feat -cepext .mfc -ctl ps.ctl -hmm model_parameters/voxforge.cd_cont_4000 -lw 10 -feat 1s_c_d_dd -beam 1e-80 -wbeam 1e-40 -dict /home/ai/voxforge/de/work/etc/voxforge.dic -lm /home/ai/voxforge/de/work/etc/voxforge.lm.DMP -wip 0.2 -hyp %s -hypseg %s &>logs/eval.log' % (workdir, hypfn, segfn))

hyprex = re.compile (r"^([^(]*)\((\S+)\s([+-][0-9]+)\)$")

cnt    = 0
words  = 0
werr   = 0
mfcfn  = ""
pe     = ""

cur.execute ("UPDATE eval SET psresp=NULL, pswerr=NULL, psscore=NULL")

hypf = open ('%s/%s' % (workdir, hypfn))
for line in hypf:

    l = line.decode ('UTF8')

    m = hyprex.match (l)
    if m:

        pr    = m.group(1)
        cfn   = m.group(2)
        score = int(m.group(3))

        pe    = prompts[cfn]
        sid   = sids[cfn]

        print "%-25s Score: %d" % (cfn, score)

        print "    expected: %s" % pe
        print "    got     : %s" % pr

        w1s = split_words(pe)
        w2s = split_words(pr)

        words += len(w1s)
        n_errs = edit_distance(w1s, w2s)

        werr += n_errs

        print "    +%2d word errors, total: %4d errors in %4d words => rate = %3d%%" % (n_errs, werr, words, werr * 100 / words)
        print

        cur.execute ('UPDATE eval SET psresp=%s, pswerr=%s, psscore=%s WHERE sid=%s', (pr, n_errs, score, sid))

        conn.commit()
        cur = conn.cursor()

        cnt += 1

    else:
        print "not matched: %s" % l

