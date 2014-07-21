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
from gutils import detect_latin1, isgalnum, compress_ws, split_words
import random
import datetime
import wave, struct

def gen_dirname ():

    global lvlogin

    today = datetime.date.today()
   
    rstr = '%c%c%c' % (random.randint(97,122),random.randint(97,122),random.randint(97,122))
 
    ds = today.strftime ('%Y%m%d')

    dir_name = '%s-%s-%s' % (lvlogin, ds, rstr)

    #print 'dir_name: %s' % dir_name

    return dir_name

random.seed (42)

SILENCE_THRESH     = 256
SILENCE_MIN_LENGTH = 4000

MIN_SEGMENT_LENGTH = 2 * 16000

W16FN = "/tmp/foo.wav"

#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

audiodir  = config.get("speech", "audiodir")

#
# command line
#

if len(sys.argv) != 3:
    print "usage: %s reader_name foo.wav" % sys.argv[0]
    sys.exit(1)

lvlogin  = sys.argv[1]
wavfn    = sys.argv[2]

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
# convert audio to 16kHz mono
#

cmd = "sox %s -r 16000 -c 1 %s" % (wavfn, W16FN)
print cmd

os.system (cmd)


#
# segment audio
#

wavf = wave.open(W16FN, 'r')

wavoutcnt = 0
wavoutfn  = "%s/wav/de10-%03d.wav" % (dir_path, wavoutcnt)

wavoutf   = wave.open(wavoutfn, 'w')
wavoutf.setparams((1, 2, 16000, 0, "NONE", "not compressed"))

cur_segment_length = 0
cur_silence_length = 0

length = wavf.getnframes()
for i in range(0,length):
    wd = wavf.readframes(1)
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


    else:
        cur_silence_length = 0


wavoutf.close()

