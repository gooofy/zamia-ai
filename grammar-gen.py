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
from os.path import expanduser

from gutils import detect_latin1, isgalnum, compress_ws, kill_umlauts
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

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# generate dict (all words from prompts we have pronounciations for)
#

outf_voca = open ('output/eval.voca', 'w')

outf_voca.write ("% NS_B\n<s>        sil\n\n% NS_E\n</s>        sil\n\n") 

print 
print "Fetching dict entries for transcript words from db..."

cur.execute ("SELECT DISTINCT word,phonemes FROM submissions,transcripts,words,pronounciations WHERE transcripts.sid=submissions.id AND transcripts.wid=words.id AND transcripts.pid = pronounciations.id AND reviewed=true AND noiselevel<2 AND truncated=false AND audiolevel<2 AND pcn<2 ORDER BY word ASC", )

rows = cur.fetchall()
cnt = 1
words = set()
for row in rows:

    word = kill_umlauts(row[0].decode ('UTF8'))

    if word in words:
        continue
    words.add(word)

    ipa  = row[1].decode ('UTF8')

    xs = ipa2xsampa(word, ipa)
    xa = xsampa2xarpabet(word, xs)

    #print word.encode('UTF8')

    outf_voca.write ("%% %s\n%-25s %s\n\n" % (word, word,xa))

    cnt += 1

print
print "Found %d entries." % cnt
print 

outf_voca.close()

print "output/eval.voca written." 
print

#
# prompts => grammar
#

outf_grammar = open ('output/eval.grammar', 'w')

outf_grammar.write ("S : NS_B SENT NS_E\n") 

cur.execute ("SELECT id FROM submissions WHERE reviewed=true AND noiselevel<2 AND truncated=false AND audiolevel<2 AND pcn<2")

rows = cur.fetchall()
for row in rows:

    id = row[0]

    outf_grammar.write ('SENT: ')

    cur.execute ("SELECT word FROM words, transcripts WHERE words.id=transcripts.wid AND transcripts.sid=%s ORDER BY transcripts.id ASC", (id,))
    rows2 = cur.fetchall()
    for row2 in rows2:
        word = kill_umlauts(row2[0].decode ('UTF8'))

        outf_grammar.write (('%s ' % word).encode('ISO-8859-1'))

    outf_grammar.write ('\n')

outf_grammar.close()

print "output/eval.grammar written." 
print


