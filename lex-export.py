#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import StringIO
import re
import sys
import locale
import ConfigParser
import psycopg2
from os.path import expanduser

from phonetic_alphabets import ipa2xsampa, xsampa2ipa, xsampa2xarpabet

#
# export contents of our phonetic database to files
#
# 2013, 2014 by G. Bartsch. License: LGPLv3
#

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
# conntect to database
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)
conn = psycopg2.connect(conn_string)

#
# output translation table
#

print
print "Exporting dict..."
print

outf_ipa    = open ('output/dict-ipa.txt', 'w')
outf_xsampa = open ('output/dict-xsampa.txt', 'w')

count = 0

cur = conn.cursor()
cur.execute ("SELECT word,phonemes FROM words,pronounciations WHERE words.id=pronounciations.wid ORDER BY word ASC")

rows = cur.fetchall()
for row in rows:

    word = row[0].decode('UTF8')
    ipa  = row[1].decode('UTF8')

    xs = ipa2xsampa(word, ipa)
    xa = xsampa2xarpabet(word, xs)

    outf_ipa.write ( (u"%s\t%s\n" % (word, ipa)).encode('UTF8') )
    outf_xsampa.write ( (u"%s\t%s\n" % (word, xa)).encode('UTF8') )

    count += 1

outf_ipa.close()
outf_xsampa.close()

print 'output/dict-ipa.txt written.'
print 'output/dict-xsampa.txt written.'
print
print "total: %d entries." % count
print

