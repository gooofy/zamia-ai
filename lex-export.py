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
# export contents of our phonetic database to a dict file
#
# 2013 by G. Bartsch. License: LGPLv3
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
# check for illegal entries
#

print "Checking entries ",
sys.stdout.flush()

cur = conn.cursor()
cur.execute ("SELECT phonemes, grapheme_id, id FROM pronounciations")

num_illegal = 0
num_total = 0

rows = cur.fetchall()
for row in rows:

    ipa = row[0].decode('UTF8')
    gid = row[1]
    pid = row[2]

    cur.execute ("SELECT grapheme FROM graphemes WHERE id=%s", (gid,))

    row2 = cur.fetchone()
    if not row2:
        continue

    word = row2[0].decode('UTF8')
    num_total += 1

    if num_total % 250 == 0:
        print '.',
        sys.stdout.flush()

    try:
        xs = ipa2xsampa(word, ipa)
    except:

        print (u"while working on: %d %s %s" % (pid, word, ipa)).encode('UTF8')

        print "catched error: %s" % sys.exc_info()[0]
        
        #cur.execute ("DELETE FROM pronounciations WHERE id=%s", (pid,))

        #print "ENTRY DELETED."
        print

        num_illegal += 1

conn.commit()

print "done. %d entries total, %d illegal ones." % (num_total, num_illegal)

if num_illegal > 0:
    sys.exit(1)

#
# output translation table
#

#outf_julius = open ('output/dict-julius.txt', 'w')
outf_ipa    = open ('output/dict-ipa.txt', 'w')
outf_xsampa = open ('output/dict-xsampa.txt', 'w')

count = 0

cur = conn.cursor()
cur.execute ("SELECT phonemes, grapheme_id, id FROM pronounciations")

rows = cur.fetchall()
for row in rows:

    ipa = row[0].decode('UTF8')
    gid = row[1]
    pid = row[2]

    cur.execute ("SELECT grapheme FROM graphemes WHERE id=%s", (gid,))

    row2 = cur.fetchone()
    if not row2:
        continue

    word = row2[0].decode('UTF8')

    count += 1

    print (u"%7d/%7d : %7d %s %s" % (count, num_total, pid, word, ipa)).encode('UTF8')

    xs = ipa2xsampa(word, ipa)
    xa = xsampa2xarpabet(word, xs)

#    outf_julius.write ( (u"%s\t[%s]\t%s\n" % (word, word, xa)).encode('UTF8') )
    outf_ipa.write ( (u"%s\t%s\n" % (word, ipa)).encode('UTF8') )
    outf_xsampa.write ( (u"%s\t%s\n" % (word, xa)).encode('UTF8') )

#outf_julius.close()
outf_ipa.close()
outf_xsampa.close()

