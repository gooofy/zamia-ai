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

from gutils import detect_latin1, isgalnum, compress_ws, kill_umlauts, split_words
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
# read sentences relevant for our eval grammar
#

print 
print "reading grammar/eval.sent ..."

inf = open ('grammar/eval.sent')

outf_grammar = open ('output/grammar/eval.grammar', 'w')
outf_grammar.write ("S : NS_B SENT NS_E\n") 

prompts = []
words = set()

for line in inf:

    p = compress_ws(line.decode('UTF8')).upper().rstrip()

    prompts.append (p)

    for word in split_words (p):
        words.add(word)

    outf_grammar.write ('SENT: %s\n' % kill_umlauts(p))

inf.close()

print "%d prompts, %d unique words" % (len(prompts), len(words))

outf_grammar.close()

print "output/grammar/eval.grammar written." 
print

#
# generate dict (all words from prompts we have pronounciations for)
#

outf_voca = open ('output/grammar/eval.voca', 'w')

outf_voca.write ("% NS_B\n<s>        sil\n\n% NS_E\n</s>        sil\n\n") 

print 
print "Fetching dict entries for transcript words from db..."

for word in words:

    cur.execute ("SELECT phonemes FROM words,pronounciations WHERE words.id=pronounciations.wid AND words.word=%s ORDER BY word ASC", (word,))

    rows = cur.fetchall()

    w = kill_umlauts(word)
    outf_voca.write ('%% %s\n' % (w))

    for row in rows:

        ipa  = row[0].decode ('UTF8')

        xs = ipa2xsampa(word, ipa)
        xa = xsampa2xarpabet(word, xs)

        #print word.encode('UTF8')

        outf_voca.write ('%-25s %s\n' % (w, xa))

    outf_voca.write ('\n')

outf_voca.close()

print "output/grammar/eval.voca written." 
print

