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

cur.execute ("SELECT DISTINCT id, prompt, cfn FROM submissions WHERE NOT reviewed ORDER BY id ASC") 

failed_words = {}

rows = cur.fetchall()
for row in rows:

    prompt = row[1].decode('UTF8').rstrip().lstrip()
    cfn    = row[2].decode('UTF8')

    #print prompt

    words  = split_words(prompt)

    for word in words:

        if word in failed_words:   
            failed_words[word].add(cfn)
            continue

        if not d.check(word):
            failed_words[word] = set([cfn])

for word in failed_words:

    print "%s\t%s" % (word, repr(failed_words[word]))
    #print "%s" % (word)




