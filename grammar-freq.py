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
import ConfigParser
import operator
from os.path import expanduser

from gutils import detect_latin1, isgalnum, compress_ws, kill_umlauts
from phonetic_alphabets import ipa2xsampa, xsampa2ipa, xsampa2xarpabet

#
# select top n most frequent prompts
#

NUM_PROMPTS = 100

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

# prompt -> num of submissions
prompt_cnt = {}

cur.execute ("SELECT prompt FROM submissions WHERE NOT cfn LIKE 'open%'")
rows = cur.fetchall()
for row in rows:
    prompt = row[0].decode('UTF8')

    if not prompt in prompt_cnt:
        prompt_cnt[prompt] = 1
    else:
        prompt_cnt[prompt] += 1

sorted_prompt_cnt = sorted(prompt_cnt.iteritems(), key=operator.itemgetter(1))

cnt = 0
for t in reversed(sorted_prompt_cnt):
    print t[0]
    cnt += 1

    if cnt > NUM_PROMPTS:
        break

