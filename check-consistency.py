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

#
# run various consistency checks on the db
#

import sys
import re
import os
import StringIO
import ConfigParser
from os.path import expanduser
from gutils import run_command
import psycopg2

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

mfccdir   = config.get("speech", "mfccdir")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# look for pronounciations used in transcripts that do not exist
#

print
print "Looking for missing pronounciations still referenced from transcript..."

pids = set()

cur.execute ("SELECT id FROM pronounciations")

rows = cur.fetchall()
for row in rows:
    pid = row[0]
    pids.add(pid)


cur.execute ("SELECT pid,sid FROM transcripts")
rows = cur.fetchall()
for row in rows:
    pid = row[0]
    sid = row[1]
    if pid in pids:
        continue
    print "ERROR: pid %7d not in dict." % pid

    cur.execute ("SELECT prompt, cfn FROM submissions WHERE id=%s", (sid,))
    row2 = cur.fetchone()
    if not row2:
        print "*** ERROR ERROR: sid %d does not exist!!" % sid
    else:
        print (u"   %s prompt: %s" % (row2[1].decode('UTF8'), row2[0].decode('UTF8'))).encode('UTF8')

#
# check transcripts, make sure they match prompts
#

print
print "Checking transcripts against prompts..."

cur.execute ("SELECT id, prompt, cfn FROM submissions WHERE reviewed=true AND noiselevel<=1 AND truncated=false AND audiolevel<=1 AND pcn<=1 AND alignment_error=false")

rows = cur.fetchall()
for row in rows:
    sid    = row[0]
    prompt = row[1].decode('utf8').lstrip().rstrip()
    cfn    = row[2].decode('utf8')

    transcript = ""

    cur.execute ("SELECT word FROM words,transcripts WHERE words.id=transcripts.wid AND transcripts.sid=%s ORDER BY transcripts.id ASC", (sid,))
    rows2 = cur.fetchall()
    for row2 in rows2:
        word = row2[0].decode('utf8')

        transcript += " " + word

    transcript = transcript.lstrip().rstrip()

    if transcript == prompt:
        continue

    print 
    print "PROMPT MISMATCH: %s" % cfn
    print "PROMPT:     %s" % prompt
    print "TRANSCRIPT: %s" % transcript



