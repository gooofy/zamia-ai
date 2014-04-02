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

import re, sys, os
import psycopg2
import ConfigParser
from optparse import OptionParser
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

outf_wlist = open ('%s/wlist.txt' % workdir, 'w')
outf_julius = open ('%s/dict-julius.txt' % workdir, 'w')

outf_julius.write ("<s> [<s>] sil\n</s> [</s>] sil\n") 

print 
print "Fetching dict entries from db..."

sql = "SELECT DISTINCT word,phonemes FROM words,pronounciations WHERE words.id=pronounciations.wid ORDER BY word ASC"

cur.execute (sql)

rows = cur.fetchall()
cnt = 1
words = set()
for row in rows:

    word = row[0].decode ('UTF8')
    ipa  = row[1].decode ('UTF8')

    xs = ipa2xsampa(word, ipa)
    xa = xsampa2xarpabet(word, xs)

    if not word in words:
        outf_wlist.write (("%s\n" % word).encode('UTF8'))
        words.add(word)
    outf_julius.write (("%s\t[%s]\t%s\n" % (word, word, xa)).encode('UTF8'))

    cnt += 1

print
print "Found %d entries." % cnt
print 

outf_wlist.close()
outf_julius.close()

print "%s/wlist.txt written." % workdir
print "%s/dict-julius.txt written." % workdir
print

