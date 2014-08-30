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

import sys
import re
import os
import StringIO
import ConfigParser
from os.path import expanduser
from gutils import detect_latin1, isgalnum, compress_ws, split_words, edit_distance
import random
import datetime
import psycopg2
from phonetic_alphabets import ipa2xsampa, xsampa2ipa, xsampa2xarpabet
import pocketsphinx
from phonetisaurusclient import phonetisaurus_gen_ipa

#
# for specified audio submission:
# - export fixed prompts from DB to prompts files, 
# - create tarball ready for upload to voxforge
#
#

#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

db_server  = config.get("speech", "dbserver")
db_name    = config.get("speech", "dbname")
db_user    = config.get("speech", "dbuser")
db_pass    = config.get("speech", "dbpass")

audiodir   = config.get("speech", "audiodir") 
contribdir = config.get("speech", "contribdir") 

#
# init
#

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

#
# command line
#

if len(sys.argv) != 2:
    print "usage: %s cfn-prefix" % sys.argv[0]
    sys.exit(1)

dir_name = sys.argv[1]

dir_path = "%s/%s" % (audiodir, dir_name)
promptsfn  = "%s/%s/etc/PROMPTS" % (audiodir, dir_name)
opromptsfn = "%s/%s/etc/prompts-original" % (audiodir, dir_name)

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# re-write prompt files
#

promptsf  = open(promptsfn, 'w')
opromptsf  = open(opromptsfn, 'w')

cur.execute ('SELECT prompt,audiofn FROM submissions WHERE cfn LIKE %s ORDER BY cfn ASC', ('%s%%' % dir_name,))

rows = cur.fetchall()
for row in rows:

    prompt  = row[0].decode('utf8')
    audiofn = row[1].decode('utf8')

    print u"%s %s" % (audiofn, prompt)

    promptsf.write ( (u'%s/mfc/%s %s\n' % (dir_name, audiofn, prompt) ).encode('utf8') )
    promptsf.flush()

    opromptsf.write ( (u'%s %s\n' % (audiofn, prompt) ).encode('utf8') )
    opromptsf.flush()

print

promptsf.close()
opromptsf.close()
print "%s written, %s written." % (promptsfn, opromptsfn)
print

#
# create tarball
#

cmd = "cd %s ; tar cfvz %s/%s.tgz %s" % (audiodir, contribdir, dir_name, dir_name)

print cmd

os.system(cmd)

print

