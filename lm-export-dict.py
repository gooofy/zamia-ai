#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import re, sys, os
import psycopg2
import ConfigParser
from os.path import expanduser

from gutils import detect_latin1, isgalnum, compress_ws
from phonetic_alphabets import ipa2xsampa, xsampa2ipa, xsampa2xarpabet

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

minqual   = config.getint("speech", "minqual")

workdir   = config.get("speech", "lmworkdir")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# generate dict (all words from prompts we have pronounciations for)
#

dict = {}

print 
print "Fetching dict entries for transcript words from db..."

cur.execute ("SELECT transcript FROM audio WHERE quality >= %s ORDER BY QUALITY DESC", (minqual,))

rows = cur.fetchall()
for row in rows:

    transcript = row[0].decode('UTF8')

    l = compress_ws(transcript.rstrip().upper().replace(',',' ').rstrip('.').replace('!', ' ').replace('"', ' ').replace('?',' ')).lstrip(' ')

    words = l.split(' ')

    for word in words:

        if word in dict:
            continue

        cur.execute ("SELECT id FROM graphemes WHERE grapheme=%s", (word,))

        row = cur.fetchone()
        if not row:
            print "*** WARNING: word '%s' not found in lexicon." % word
            continue

        gid = row[0]

        cur.execute ("SELECT phonemes FROM pronounciations WHERE grapheme_id=%s", (gid,))

        row = cur.fetchone()
        if not row:
            print "*** ERROR: word '%s' has no pronounciation in lexicon." % word
            sys.exit(2)

        ipa = row[0].decode('UTF8')

        xs = ipa2xsampa(word, ipa)
        xa = xsampa2xarpabet(word, xs)

        dict[word] = xa

        if len(dict) % 1000 == 0:
            print "   %d entries..." % len(dict)

print
print "Found %d entries." % len(dict)
print 


#
# optionally restrict dictionary based on errors from julius logs
#

#if len(sys.argv) == 2:
#
#    print "Restricting by julius output..."
#
#    inf = open (sys.argv[1])
#
#    for line in inf:
#
#        m = re.match (r"^Error: voca_load_htkdict: the line content was: (\S+)", line.decode('UTF8'))
#
#        if not m:
#            continue
#
#        word = m.group(1)
#
#        print "Removing word: %s" % word
#
#        dict.pop(word, None)

#print
#print "Final dict has %d entries." % len(dict)
#print

outf_wlist = open ('%s/wlist.txt' % workdir, 'w')
outf_julius = open ('%s/dict-julius.txt' % workdir, 'w')

outf_julius.write ("<s> [<s>] sil\n</s> [</s>] sil\n") 

cnt = 1
for word in dict:

    xa = dict[word]

    outf_wlist.write (("%s\n" % word).encode('UTF8'))
    outf_julius.write (("%d\t[%s]\t%s\n" % (cnt, word, xa)).encode('UTF8'))

    cnt += 1

outf_wlist.close()
outf_julius.close()

print "%s/wlist.txt written." % workdir
print "%s/dict-julius.txt written." % workdir
print

