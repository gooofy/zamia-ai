#!/usr/bin/env python
# -*- coding: utf-8 -*- 

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

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

cur.execute ("SELECT id,dir,audiofn,cfn,noiselevel,truncated,audiolevel,pcn,comment,numsamples FROM submissions WHERE reviewed=TRUE")

print "id,dir,audiofn,cfn,noiselevel,truncated,audiolevel,pcn,comment,prompt,ipa,numsamples"

rows = cur.fetchall()
for row in rows:

    #print "Submission ID %s" % row[0]

    cur.execute ("SELECT phonemes, word FROM transcripts, pronounciations, words WHERE sid=%s AND transcripts.wid=words.id AND transcripts.pid=pronounciations.id ORDER BY transcripts.id ASC", (row[0],))

    prompt = ""
    ipa = ""

    rows2 = cur.fetchall()
    for row2 in rows2:
        #print "%s [%s] " % (row2[1], row2[0])

        if len(prompt)>0:
            prompt += ' '
        prompt += row2[1]

        if len(ipa)>0:
            ipa += ' '
        ipa += row2[0]

    print '%s,"%s","%s","%s",%s,%s,%s,%s,"%s","%s","%s",%s' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], prompt, ipa, row[9])





