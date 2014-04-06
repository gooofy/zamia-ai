#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2014 Guenter Bartsch
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

import re, sys, os
import psycopg2
from gutils import detect_latin1, isgalnum, split_words
import ConfigParser
from os.path import expanduser

#
# import new/corrected information from db2 into our db
#

#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

db_server  = config.get("speech", "dbserver")
db_name    = config.get("speech", "dbname")
db_user    = config.get("speech", "dbuser")
db_pass    = config.get("speech", "dbpass")

db2_server = config.get("speech2", "dbserver")
db2_name   = config.get("speech2", "dbname")
db2_user   = config.get("speech2", "dbuser")
db2_pass   = config.get("speech2", "dbpass")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

conn2_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db2_server, db2_name, db2_user, db2_pass)
conn2 = psycopg2.connect(conn2_string)
cur2 = conn2.cursor()

cur2.execute ("SELECT word, id FROM words ORDER BY word ASC")
rows2 = cur2.fetchall()

for row2 in rows2:

    word = row2[0]
    wid2 = row2[1]

    # fetch pronounciation info for this word from both sides:

    cur2.execute ("SELECT phonemes FROM pronounciations WHERE wid=%s", (wid2,))
    rows3 = cur2.fetchall()
    if len(rows3) == 0:
        continue

    pcn2 = set()
    for row3 in rows3:
        pcn2.add(row3[0].decode('UTF8'))

    cur.execute ("SELECT id FROM words WHERE word=%s", (word,))
    row = cur.fetchone()
    if not row:
        print "new word: %s %s" % (word, repr(pcn2))

        cur.execute ("INSERT INTO words (word, occurences) VALUES (%s, 1) RETURNING id", (word,))
        wid = cur.fetchone()[0]

        for p in pcn2:
            cur.execute ("INSERT INTO pronounciations (phonemes, probability, points, wid) VALUES (%s,%s,%s,%s)",
                         (p, 100, 0, wid))

#    else:
#        wid = row[0]
#
#        cur.execute ("SELECT phonemes FROM pronounciations WHERE wid=%s", (wid,))
#
#        pcn = set()
#        rows3 = cur.fetchall()
#        for row3 in rows3:
#            pcn.add(row3[0].decode('UTF8'))
#
#        # FIXME: compare, merge
#
#        if len(pcn) == 0:
#            print "FIXME: new pronounciation(s) for word %s: %s" % (word, repr(pcn2))
#        else:
#            print "FIXME: merge pronounciations for word %s: %s" % (word)

conn.commit()

