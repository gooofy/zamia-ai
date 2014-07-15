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
import wave, struct

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

#cur.execute ("SELECT dir,audiofn,cfn,audiolevel FROM submissions WHERE reviewed=TRUE AND audiolevel=3")
#cur.execute ("SELECT dir,audiofn,cfn,audiolevel,id FROM submissions WHERE reviewed=FALSE OR audiolevel<3")
cur.execute ("SELECT dir,audiofn,cfn,audiolevel,id FROM submissions WHERE reviewed=FALSE")

rows = cur.fetchall()

cnt = 0

for row in rows:

    cnt += 1

    dir        = row[0]
    audiofn    = row[1]
    cfn        = row[2]
    audiolevel = row[3]
    sid        = row[4]

    wavfn = audiodir + '/' + dir + '/wav/' + audiofn + '.wav'

    wavf = wave.open(wavfn, 'r')

    #
    # detect volume min/max
    #

    min_sample =  100000
    max_sample = -100000

    length = wavf.getnframes()
    for i in range(0,length):
        wd = wavf.readframes(1)
        data = struct.unpack("<h", wd)
    
        sample = int(data[0])
    
        if sample > max_sample:
            max_sample = sample
        if sample < min_sample:
            min_sample = sample
    
    #    print sample
    
    #    sys.exit(0)
   
    volume = max_sample - min_sample
 
    print "%6d/%6d: %3d%% %-27s min: %7d, max: %7d, vol: %7d, %s" % (cnt, len(rows), cnt * 100 / len(rows), cfn, min_sample, max_sample, volume, wavfn)
    
    wavf.rewind()
    
    bound = 0.70 * volume
 
    last_sample = 0
    
    for i in range(0,length):
        wd = wavf.readframes(1)
        data = struct.unpack("<h", wd)
    
        sample = int(data[0])

        diff = abs(sample - last_sample)
    
        if diff > bound:
            print "         DIFF %7d CLIP DETECTED at sample #%d" % (diff, i)

            cur.execute ("UPDATE submissions SET reviewed=TRUE, audiolevel=3 WHERE id=%s", (sid,))
            conn.commit()
            cur = conn.cursor()

            break
    
        last_sample = sample
    
