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
# given a prompt file, produce list of words missing in our dict
#


if len(sys.argv) != 2:
    print "usage: %s foo.txt" % sys.argv[0]
    sys.exit(1)

inf = open (sys.argv[1])

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

#
# read words from prompt file
#

words = set()

for line in inf:

    for word in split_words(line.decode('UTF8')):
        words.add(word)

#
# load dict from db
#

dict = set()

cur.execute ("SELECT words.word FROM words,pronounciations WHERE words.id = pronounciations.wid AND pronounciations.points > 0")
for row in cur.fetchall():
    dict.add (row[0].decode('UTF8'))

#
# print missing words
#
for word in words:

    if not word in dict:

        print "%s" % (word),


