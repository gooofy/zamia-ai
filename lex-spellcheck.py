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

import re, sys, os
import psycopg2
from gutils import detect_latin1, isgalnum, split_words
import ConfigParser
from os.path import expanduser
import enchant

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

d = enchant.Dict("de_DE")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

cur.execute ("SELECT DISTINCT word, id FROM words WHERE NOT words.spellchecked ORDER BY word ASC") 

rows = cur.fetchall()
for row in rows:

    word = row[0].decode('UTF8')
    wid = row[1]

    if not d.check(word):
        print
        print "spellcheck failed for '%s'" % word
        print "   suggestions:"
        for s in d.suggest(word):
            print "      %s" % s
        print

        while True:
            print "(a)ccept, (r)emove, (i)gnore > ",
            reply = sys.stdin.readline().rstrip()

            if reply == 'a':
                cur.execute ("UPDATE words SET spellchecked=true WHERE id=%s", (wid,))
                conn.commit()
                cur = conn.cursor()
                break
            elif reply == 'i':
                break
            elif reply == 'r':

                cur.execute ("SELECT DISTINCT sid FROM transcripts WHERE wid=%s", (wid,))

                rows2 = cur.fetchall()
                for row2 in rows2:
                    sid = row2[0]
                    print "Invalidating sid %d" % sid

                    cur.execute ("DELETE FROM transcripts WHERE sid=%s", (sid,))
                    cur.execute ("UPDATE submissions SET reviewed=False WHERE id=%s", (sid,))

                print
                print "Deleting pronounciations, word"
                cur.execute ("DELETE FROM pronounciations WHERE wid=%s", (wid,))
                cur.execute ("DELETE FROM words WHERE id=%s", (wid,))

                conn.commit()
                cur = conn.cursor()
                break
                
    else:

        cur.execute ("UPDATE words SET spellchecked=true WHERE id=%s", (wid,))
        conn.commit()
        cur = conn.cursor()


