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
import random
import datetime
import wave, struct

#
# audiobook preprocessing tool
# - interactive, DB wrt based spellchecker
#   (useful for semi-automated audiobook transcript preprocessing)
# - add audiobook to db
# - convert audio to wav
# - segment
#

random.seed (42)

# silence: anything < 20% of avg volume
SILENCE_THRESH     = 0.2

SAMPLE_RATE        = 16000

# segment length: minimum 4 seconds, max 15 seconds
MIN_SEGMENT_LENGTH =  4 * SAMPLE_RATE
MAX_SEGMENT_LENGTH = 15 * SAMPLE_RATE
# segment has to contain at least 1s of content
MIN_VOICE_LENGTH   =  1 * SAMPLE_RATE

# debug purposes only, set to 0 to disable debug limit
#DEBUG_LENGTH       = 5000000
DEBUG_LENGTH       = 0

def gen_dirname ():

    global abook_reader

    today = datetime.date.today()
   
    rstr = '%c%c%c' % (random.randint(97,122),random.randint(97,122),random.randint(97,122))
 
    ds = today.strftime ('%Y%m%d')

    dir_name = '%s-%s-%s' % (abook_reader, ds, rstr)

    #print 'dir_name: %s' % dir_name

    return dir_name

if len(sys.argv) != 4:
    print "usage: %s title partnum reader" % sys.argv[0]
    print
    sys.exit(1)

abook_title  = sys.argv[1]
abook_part   = int(sys.argv[2])
abook_reader = sys.argv[3]

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

abook_dir = config.get("speech", "abookdir")
audiodir  = config.get("speech", "audiodir")

tmpwavfn  = '%s/%s/tmp_%08x.wav' % (abook_dir, abook_title, os.getpid())
tmpwav16fn= '%s/%s/tmp16_%08x.wav' % (abook_dir, abook_title, os.getpid())
mp3fn     = '%s/%s/mp3/part%02d.mp3' % (abook_dir, abook_title, abook_part)

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# main loop
#

txtfn    = '%s/%s/txt/part%02d.txt' % (abook_dir, abook_title, abook_part)
promptfn = '%s/%s/prompts/part%02d.txt' % (abook_dir, abook_title, abook_part)

inf = open (txtfn)
outf = open (promptfn, 'w')

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

print 
print "%s written." % (promptfn)
print

#
# segment audio
#

os.system ('mpg123 -w %s %s' % (tmpwavfn, mp3fn))

#
# generate dir name
#

dir_name = ''
dir_path = ''

while True:

    dir_name = gen_dirname()

    dir_path = '%s/%s' % (audiodir, dir_name)

    print "path: %s" % dir_path

    if not os.path.isdir (dir_path):
        break

#
# generate skeleton
#

os.system ('rm -rf %s' % (dir_path))
os.system ('mkdir %s' % (dir_path))
os.system ('mkdir %s/etc' % (dir_path))
os.system ('mkdir %s/wav' % (dir_path))
os.system ('cp input_files/voxforge-librivox-LICENSE %s/LICENSE' % (dir_path))
os.system ('cp input_files/voxforge-librivox-README %s/etc/README' % (dir_path))

#
# abook db entry
#

cur.execute ('INSERT INTO abooks(title,partnum,reader,cfn) VALUES (%s,%s,%s,%s)', (abook_title,abook_part,abook_reader,dir_name))
conn.commit()
cur = conn.cursor()

#
# convert audio to 16kHz mono
#

cmd = "sox %s -r 16000 -c 1 %s" % (tmpwavfn, tmpwav16fn)
print cmd

os.system (cmd)

#
# read all samples into memory so we have random access to them
# when we're looking for cut-points
#

wavf = wave.open(tmpwav16fn, 'r')
length = wavf.getnframes()

if DEBUG_LENGTH>0 and length >DEBUG_LENGTH:
    length = DEBUG_LENGTH

samples = []
avg = 0.0

print "Reading %6d/%6d samples from %s..." % (len(samples), length, tmpwav16fn),

for i in range(0,length):

    wd = wavf.readframes(1)

    try:

        data = struct.unpack("<h", wd)
        sample = int(data[0])
        samples.append(sample)
        avg += abs(float(sample))

        if i % 1000 == 0:
            p = len(samples) * 100 / length
            print "\rReading %9d/%9d %3d%% samples from %s..." % (len(samples), length, p, tmpwav16fn),

    except:
        print "*** ERROR: unexpected error:", sys.exc_info()[0]
        traceback.print_exc()
        print "wd: %s" % repr(wd)

avg = int(avg/length)

print "\ndone. Read %d samples, avg: %d" % (len(samples), avg)

silence_thresh = int(SILENCE_THRESH * avg + 1)

cur_pos   = 0
wavoutcnt = 0

while cur_pos < length:

    cut_pos             = cur_pos + MIN_SEGMENT_LENGTH
    best_silence_pos    = cut_pos 
    best_silence_length = 0

    cur_silence_pos     = cut_pos
    cur_silence_length  = 0

    max_pos             = cur_pos + MAX_SEGMENT_LENGTH
    if max_pos > length:
        max_pos = length

    #print "cur_pos: %d, max_pos: %d, best_silence_pos: %d" % (cur_pos, max_pos, best_silence_pos)

    while cut_pos < max_pos:

        sample  = samples[cut_pos]
        cut_pos += 1

        if sample < silence_thresh:
            cur_silence_length += 1
    
        else:

            if cur_silence_length > best_silence_length:
                best_silence_length = cur_silence_length
                best_silence_pos    = cur_silence_pos

            cur_silence_length = 0
            cur_silence_pos    = cut_pos

    print "Segment detected: %5ds -> %5ds (len: %2ds, silence: %5d samples)" % (cur_pos / SAMPLE_RATE, best_silence_pos / SAMPLE_RATE, (best_silence_pos - cur_pos) / SAMPLE_RATE, best_silence_length)

    #print "best_silence_pos: %d" % (best_silence_pos)


    csp = best_silence_pos if best_silence_pos < length else length

    cur_voice_len = 0
    for i in range (cur_pos, csp):
        if samples[i] >= silence_thresh:
            cur_voice_len += 1

    if cur_voice_len >= MIN_VOICE_LENGTH:
        wavoutfn  = "%s/wav/de10-%03d.wav" % (dir_path, wavoutcnt)
        #wavoutfn  = "/tmp/de10-%03d.wav" % (wavoutcnt)

        wavoutf   = wave.open(wavoutfn, 'w')
        wavoutf.setparams((1, 2, 16000, 0, "NONE", "not compressed"))
        for i in range (cur_pos, csp):
            wd = struct.pack("<h", samples[i])
            wavoutf.writeframes(wd)
        wavoutf.close()
        wavoutcnt += 1

        print "%s written." % wavoutfn
    else:
        print "Voice content too short (%5d samples), wav file not written." % (cur_voice_len)

    cur_pos = best_silence_pos + 1


# cleanup
#
os.system ('rm %s' % tmpwavfn)
os.system ('rm %s' % tmpwav16fn)

