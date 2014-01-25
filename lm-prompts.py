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
from gutils import compress_ws

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

workdir   = config.get("speech", "lmworkdir")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# collect prompts from DB
#

fn = '%s/prompts.sent' % workdir
outf = open (fn, 'w')

cur.execute ("SELECT prompt FROM submissions WHERE reviewed=true AND noiselevel<2 AND truncated=false AND audiolevel<2 AND pcn<2")

rows = cur.fetchall()
for row in rows:

    transcript = row[0].decode('UTF8')

    l = compress_ws(transcript.rstrip().upper().replace(',',' ').rstrip('.').replace('!', ' ').replace('"', ' ').replace('?',' ')).lstrip(' ')

    outf.write (('%s\n' % l).encode('UTF8') )

outf.close()

print "%s written." % fn
print



