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

import sys
import re
import os
import StringIO
import ConfigParser
from optparse import OptionParser
from os.path import expanduser
import subprocess
import psycopg2
from gutils import split_words

#
# split prompts into words and put them back together again, so 
# gutil's cleaning + word replacement table applies to original
# prompts
#

#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

webroot   = config.get("speech", "webroot")

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

cur.execute ('SELECT id,prompt,cfn FROM submissions WHERE reviewed=false')
rows = cur.fetchall()
for row in rows:

    sid         = row[0]
    prompt      = row[1].decode('UTF8').rstrip().lstrip()
    cfn         = row[2].decode('UTF8').rstrip().lstrip()

    cprompt     = ' '.join(split_words(prompt))

    if prompt == cprompt:
        continue

    print
    print cfn
    print "PROMPT: %s" % prompt
    print "CLEAN : %s" % cprompt

    cur.execute ('UPDATE submissions SET prompt=%s WHERE id=%s', (cprompt, sid))

conn.commit()


