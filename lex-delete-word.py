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

# delete unwanted (typically misspelled) word from dict:
# - remove pronounciations
# - remove transcripts
# - invalidate submissions
# - delete word

import re, sys, os
import psycopg2
import ConfigParser
from os.path import expanduser

from gutils import detect_latin1, isgalnum, split_words

#
# commandline
#

if len(sys.argv) != 2:
    print "usage: %s WORD" % sys.argv[0]
    sys.exit(1)

delword = sys.argv[1]

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

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

print "looking up wid..."

cur.execute ("SELECT id FROM words WHERE word=%s", (delword,))
row = cur.fetchone()
if not row:
    print "Word not found."
    print
    sys.exit(1)

delwid = row[0]

print "wid: %d" % delwid
print

print "Looking for submissions using the word..."

cur.execute ("SELECT DISTINCT sid FROM transcripts WHERE wid=%s", (delwid,))

rows = cur.fetchall()
for row in rows:
    sid = row[0]
    print "Invalidating sid %d" % sid

    cur.execute ("DELETE FROM transcripts WHERE sid=%s", (sid,))
    cur.execute ("UPDATE submissions SET reviewed=False WHERE id=%s", (sid,))

print
print "Deleting pronounciations, word"
cur.execute ("DELETE FROM pronounciations WHERE wid=%s", (delwid,))
cur.execute ("DELETE FROM words WHERE id=%s", (delwid,))

conn.commit()

print
print "all done."
print

