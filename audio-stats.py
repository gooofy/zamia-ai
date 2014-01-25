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
from gutils import run_command, split_words
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

mfccdir   = config.get("speech", "mfccdir")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

cur.execute ("SELECT cfn,reviewed,noiselevel,truncated,audiolevel,pcn,id,numsamples,prompt FROM submissions")

reviewed_num_samples = 0
reviewed_num_files   = 0
good_num_samples     = 0
good_num_files       = 0
total_num_samples    = 0
total_num_files      = 0

samples_per_user     = {}
words_per_user       = {}

rows = cur.fetchall()
for row in rows:

    cfn         = row[0]
    reviewed    = row[1]
    noiselevel  = row[2]
    truncated   = row[3]
    audiolevel  = row[4]
    pcn         = row[5]
    sid         = row[6]
    num_samples = row[7]
    prompt      = row[8]
    num_words   = len(split_words(prompt))

    login       = cfn.split('-')[0]

    total_num_samples += num_samples
    total_num_files   += 1

    if reviewed:
        reviewed_num_samples += num_samples
        reviewed_num_files   += 1

        if noiselevel < 2 and not truncated and audiolevel<2 and pcn<2:
            good_num_samples += num_samples
            good_num_files   += 1

            if login in samples_per_user:
                samples_per_user[login] += num_samples
            else:
                samples_per_user[login] = num_samples

            if login in words_per_user:
                words_per_user[login] += num_words
            else:
                words_per_user[login] = num_words
           

print
print "STATS: total    %6d files, total    length: %8.2fmin" % (total_num_files, total_num_samples / (60 * 100.0))
print "STATS: reviewed %6d files, reviewed length: %8.2fmin" % (reviewed_num_files, reviewed_num_samples / (60 * 100.0))
print "STATS: good     %6d files, good     length: %8.2fmin" % (good_num_files, good_num_samples / (60 * 100.0))
print
print "good contributions per user: "
print

for login in samples_per_user:
    samples = samples_per_user[login]
    words = words_per_user[login]
    print "%-25s : %8.2fmin %5d words" % (login, samples / (60*100.0), words)

print

