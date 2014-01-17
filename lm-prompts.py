#!/usr/bin/env python
# -*- coding: utf-8 -*- 

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
minqual   = config.getint("speech", "minqual")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# collect prompts from DB
#

outf = open ('%s/prompts.sent' % workdir, 'w')

cur.execute ("SELECT transcript FROM audio WHERE quality >= %s ORDER BY QUALITY DESC", (minqual,))

rows = cur.fetchall()
for row in rows:

    transcript = row[0].decode('UTF8')

    l = compress_ws(transcript.rstrip().upper().replace(',',' ').rstrip('.').replace('!', ' ').replace('"', ' ').replace('?',' ')).lstrip(' ')

    outf.write (('%s\n' % l).encode('UTF8') )


