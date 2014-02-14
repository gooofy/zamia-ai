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

def eval_model (col):

    cur.execute ("SELECT cfn,numsamples,prompt,%s FROM submissions,eval WHERE submissions.id=eval.sid and %s IS NOT null" % (col, col))
    
    samples_per_user     = {}
    words_per_user       = {}
    werr_per_user        = {}
    
    rows = cur.fetchall()
    for row in rows:
    
        cfn         = row[0]
        numsamples  = row[1]
        prompt      = row[2].decode('UTF8')
        num_words   = len(split_words(prompt))
        num_werr    = row[3]
    
        login       = cfn.split('-')[0]
    
        if login in samples_per_user:
            samples_per_user[login] += numsamples
        else:
            samples_per_user[login] = numsamples
    
        if login in words_per_user:
            words_per_user[login] += num_words
        else:
            words_per_user[login] = num_words
    
        if login in werr_per_user:
            werr_per_user[login] += num_werr
        else:
            werr_per_user[login] = num_werr
               
    
    print "results per user: "
    print
    
    total_words = 0
    total_werr  = 0
    
    for login in sorted(samples_per_user):
        samples = samples_per_user[login]
        words   = words_per_user[login]
        werr    = werr_per_user[login]
        print "%-25s : %8.2fmin %5d words %5d werrs (%5.1f%%)" % (login, samples / (60*100.0), words, werr, werr * 100.0 / words)
    
        total_werr  += werr
        total_words += words
    
    print
    print "Total: %d words, %d errors (%5.1f%%)" % (total_words, total_werr, total_werr * 100.0 / total_words)
    print
    


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

audiodir  = config.get("speech", "audiodir")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# total model size, active dict size
#

print
print "Review Statistics"
print "================="
print

reviewed_numsamples = 0
reviewed_num_files   = 0
good_numsamples     = 0
good_num_files       = 0
total_numsamples    = 0
total_num_files      = 0

total_words          = set()
good_words           = set()

cur.execute ("SELECT reviewed,noiselevel,truncated,audiolevel,prompt,numsamples,pcn FROM submissions")
rows = cur.fetchall()
for row in rows:

    reviewed   = row[0]
    noiselevel = row[1]
    truncated  = row[2]
    audiolevel = row[3]
    prompt     = row[4].decode('UTF8')
    numsamples = row[5]
    pcn        = row[6]

    words = split_words(prompt)
    for word in words:
        total_words.add(word)

    total_numsamples += numsamples
    total_num_files   += 1

    if reviewed:
        reviewed_numsamples += numsamples
        reviewed_num_files   += 1

        if noiselevel < 2 and not truncated and audiolevel<2 and pcn<2:
            good_numsamples += numsamples
            good_num_files   += 1
            for word in words:
                good_words.add(word)

print
print "total    %6d files, total    length: %8.2fmin" % (total_num_files, total_numsamples / (60 * 100.0))
print "reviewed %6d files, reviewed length: %8.2fmin (%3d%% done)" % (reviewed_num_files, reviewed_numsamples / (60 * 100.0), reviewed_num_files * 100 / total_num_files)
print "good     %6d files, good     length: %8.2fmin (%3d%% good)" % (good_num_files, good_numsamples / (60 * 100.0), good_num_files * 100 /reviewed_num_files)
print
print "unique words in all submissions: %d, unique words in reviewed good submissions: %d" % (len(total_words), len(good_words))
print

#
# evaluate statistical model
#

print
print "Evaluation: audio model: sphinxtrain all good submissions, engine: pocketsphinx, language model: CMUCLMTK prompts+parole"
print "========================================================================================================================"
print

eval_model('pswerr')

sys.exit(0)

print
print "Evaluation: audio model: HTK matching good submissions, engine: Julius, language model: 101 grammar"
print "==================================================================================================="
print

eval_model('jgwerr')

