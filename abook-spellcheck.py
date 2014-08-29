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

import sys
import os
import codecs
from gutils import split_words
import enchant
import ConfigParser
from os.path import expanduser
import psycopg2
import traceback

#
# interactive, DB wrt based spellchecker
# useful for semi-automated audiobook transcript preprocessing
#

if len(sys.argv) != 3:
    print "usage: %s foo.txt prompts.txt" % sys.argv[0]
    sys.exit(1)

#
# init
#

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

#sys.stdin = codecs.getreader(sys.stdin.encoding)(sys.stdin)

d = enchant.Dict("de_DE")

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
# main loop
#

inf = open (sys.argv[1])
outf = open (sys.argv[2], 'w')

linecnt = 0

for line in inf:

    l = line.decode('utf8').lstrip().rstrip()
    linecnt += 1

    edit_loop = True
    while edit_loop:

        edit_loop = False

        words = split_words(l)
        res = []

        word_loop = True

        for word in words:

            if len(word)<1:
                continue

            if d.check(word):

                res.append(word)

            else:

                # look up word in DB

                cur.execute ('SELECT repl FROM wrt WHERE word=%s', (word,))
                row = cur.fetchone()
                if row:
                    repl = row[0].decode('utf8')
                    res.append(repl)

                else:

                    print
                    print u'%6d: %s' % (linecnt, l)
                    print
                    print ' '.join(words)
                    print ' '.join(res)
                    print
                    print u"spellcheck failed for %s (%s)" % (word.lower(), repr(word))
                    print "   suggestions:"
                    for s in d.suggest(word):
                        print "      %s" % s
                    print

                    while True:           
                        print "(a)ccept, (r)eplace, (e)dit line, (q)uit > ",
                        reply = sys.stdin.readline().rstrip()

                        if reply == 'a':
                            cur.execute ('INSERT INTO wrt(word,repl) VALUES (%s, %s)', (word, word))
                            conn.commit()
                            cur = conn.cursor()
                            res.append(word)
                            break
                        elif reply == 'q':
                            sys.exit(0)
                        elif reply == 'r':
                            print "replace with: ",
                            repl = sys.stdin.readline().decode('utf8').rstrip()
                            print u"reply: %s" % repl
                            cur.execute ('INSERT INTO wrt(word,repl) VALUES (%s, %s)', (word, repl))
                            conn.commit()
                            cur = conn.cursor()
                            res.append(repl)
                            break
 
            if not word_loop:
                break

    outf.write (("%s\n" % (' '.join(res))).encode('utf8'))

outf.close()

