#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import re, sys, os
import psycopg2
import ConfigParser
from os.path import expanduser

from gutils import detect_latin1, isgalnum

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

print "loading prompts...",
sys.stdout.flush() 

words = set()

cur.execute ("SELECT prompt FROM audio") 
rows = cur.fetchall()
for row in rows:

    prompt = row[0].decode('UTF8')

    ws = re.split ('\s+', prompt)

    for word in ws:

        w = re.sub(r"[,.?\-! ;:]", '', word.lstrip().rstrip()).upper()
        if len(w) > 0:
            if not isgalnum(w):
                #print "SKIPPING: %s" % w
                continue

            if not w in words:
                #print "New word from prompts: %s" % w
                words.add(w)

print "done. %d unique words found." % len(words)

print "Looking up words in dictionary...",
sys.stdout.flush() 

count = 0

for word in words:

    cur.execute ("SELECT pronounciations.id FROM words,pronounciations WHERE words.word=%s AND words.id = pronounciations.wid", (word,)) 
   
    if not cur.fetchone():
        count += 1

print "done"
print

print "STATS: %d of %d words have no entry yet => %d%% done." % (count, len(words), (len(words) - count) * 100 / len(words))

