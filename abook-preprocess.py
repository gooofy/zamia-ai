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

SILENCE_THRESH     = 256
SILENCE_MIN_LENGTH = 4000

MIN_SEGMENT_LENGTH = 2 * 16000

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
# segment audio
#

wavf = wave.open(tmpwav16fn, 'r')

wavoutcnt = 0
wavoutfn  = "%s/wav/de10-%03d.wav" % (dir_path, wavoutcnt)

wavoutf   = wave.open(wavoutfn, 'w')
wavoutf.setparams((1, 2, 16000, 0, "NONE", "not compressed"))

cur_segment_length = 0
cur_silence_length = 0
cur_voice_length   = 0

length = wavf.getnframes()
for i in range(0,length):
    wd = wavf.readframes(1)

    try:

        data = struct.unpack("<h", wd)
    
        sample = int(data[0])
    
        wavoutf.writeframes(wd)
        cur_segment_length += 1
    
        if sample < SILENCE_THRESH:
            cur_silence_length += 1
    
            if cur_silence_length == SILENCE_MIN_LENGTH:
    
                print "%07d / %07d Silence detected, segment length: %ds" % (i/16000, length/16000, cur_segment_length/16000)
    
                if cur_segment_length > MIN_SEGMENT_LENGTH:
    
                    wavoutcnt += 1
                    wavoutfn  = "%s/wav/de10-%03d.wav" % (dir_path, wavoutcnt)
    
                    print "    CUT TO %s" % wavoutfn
    
                    wavoutf.close()
    
                    wavoutf   = wave.open(wavoutfn, 'w')
                    wavoutf.setparams((1, 2, 16000, 0, "NONE", "not compressed"))
    
                    cur_segment_length = 0
                    cur_voice_length = 0
    
    
        else:
            cur_silence_length = 0
            cur_voice_length  += 1

    except:
        print "*** ERROR: unexpected error:", sys.exc_info()[0]
        traceback.print_exc()
        print "wd: %s" % repr(wd)

wavoutf.close()

if cur_voice_length <= SILENCE_MIN_LENGTH:
    print "deleting silent last segment %s" % wavoutfn
    os.system ('rm %s' % wavoutfn)

#
# cleanup
#
os.system ('rm %s' % tmpwavfn)
os.system ('rm %s' % tmpwav16fn)

