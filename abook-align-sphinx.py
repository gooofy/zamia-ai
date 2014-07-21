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
import psycopg2
from phonetic_alphabets import ipa2xsampa, xsampa2ipa, xsampa2xarpabet


MAX_PROMPT_WORDS = 30
MAX_FAILS        = 3


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

workdir   = config.get("speech", "workdir") + "/align"
hmdir     = config.get("pocketsphinx", "hmm")
dictf     = "/tmp/voxforge.dic"


#
# command line
#

if len(sys.argv) != 3:
    print "usage: %s dir prompt.txt" % sys.argv[0]
    sys.exit(1)

dir_path = sys.argv[1]
dir_name = os.path.basename(dir_path)

promptfn = sys.argv[2]

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# dump current dict
#

print "dumping current dict..."

pdf  = open (dictf, 'w')

# word -> int, used to generate (2) (3) ... markers for words with multiple pronounciations
word_counter = {}

cur.execute ("SELECT phonemes,word FROM pronounciations,words WHERE pronounciations.wid=words.id ORDER BY word ASC")
rows = cur.fetchall()
for row in rows:

    ipa  = row[0].decode('UTF8')
    word = row[1].decode('UTF8')

    xs = ipa2xsampa(word, ipa)
    xa = xsampa2xarpabet(word, xs)
    
    if not word in word_counter:
        pdf.write ( (u'%s %s\n' % (word, xa)).encode('UTF8') )
        word_counter[word] = 1

    else:
        word_counter[word] += 1
        w2 = u'%s(%d)' % (word, word_counter[word])
        pdf.write ( (u'%s %s\n' % (w2, xa)).encode('UTF8') )

pdf.close()

print "%s written. %d words." % (dictf, len(word_counter))

#
# ordered list of words from prompt file
#

words = []

for line in open (promptfn):
    for w in split_words(line.decode('utf8')):
        words.append(w)

#print repr(words)

#
# align wav files to text, in right order
#

os.system ("rm -rf %s" % workdir)
os.system ("mkdir %s" % workdir)

featfn  = "%s/align.mfc" % workdir
transfn = "%s/align.transcription" % workdir
ctlfn   = "%s/align.fileids" % workdir
resfn   = "%s/align.wdseg" % (workdir)
logfn   = "%s/align.log" % (workdir)

promptsfn  = "%s/etc/PROMPTS" % (dir_path)
opromptsfn = "%s/etc/prompts-original" % (dir_path)

promptsf  = open(promptsfn, 'w')
opromptsf = open(opromptsfn, 'w')

ctlf = open (ctlfn, 'w')
ctlf.write('align\n')
ctlf.close()

cut_pos = 0

for wfn in sorted(os.listdir('%s/wav/' % dir_path)):

    wavfn = '%s/wav/%s' % (dir_path, wfn)

    print 
    print "Aligning %s ... " % wavfn

    # convert to mfcc

    os.system ("sphinx_fe -i '%s' -part 1 -npart 1 -ei wav -o '%s' -eo mfc -nist no -raw no -mswav yes -samprate 16000 -lowerf 130 -upperf 6800 -nfilt 25 -transform dct -lifter 22" % (wavfn, featfn) )

    best_score  = -10000000
    best_cut    = cut_pos + 1
    best_prompt = ''

    num_fails = 0

    for i in range (1,MAX_PROMPT_WORDS):

        if i > 5 and num_fails > MAX_FAILS:
            break

        prompt = ' '.join(words[cut_pos:cut_pos + i])

        print prompt

        if os.path.isfile(resfn):
            os.remove (resfn)

        transf = open (transfn, 'w')
        transf.write ( (u'%s (align)\n' % prompt).encode('utf8') )
        transf.close()

        cmdline = "sphinx3_align \
            -hmm %s \
        	-dict %s \
        	-ctl %s \
        	-cepdir %s \
        	-cepext .mfc \
        	-insent %s \
        	-outsent %s/alignment_output.txt \
        	-wdsegdir %s,CTL >>%s 2>&1" % (hmdir, dictf, ctlfn, workdir, transfn, workdir, workdir, logfn)

        #print cmdline
        os.system (cmdline)

        # parse result
    
        if not os.path.isfile(resfn):
            num_fails += 1
            continue
    
        num_fails = 0

        wscore = 0
    
        resf = open(resfn)
    
        for line in resf:
    
            l = line.decode('utf8').rstrip()
   
            print l
 
            #print u"%s %s" % (resfn, l)
    
            m = re.match(r"^\s+\d+\s+\d+\s+([+\- ]\d+)", l)
            if not m:
                continue
    
            score = int(m.group(1))
            #print "    score: %d" % score
    
            # worst score
            if score < wscore:
                wscore = score
    
        resf.close()

        print "SCORE: %s" % wscore
    
        if wscore > best_score:
            best_score  = wscore
            best_prompt = prompt
            best_cut    = cut_pos + i

    print
    print "%s BEST SCORE : %d" % (wfn, best_score)
    print "%s BEST PROMPT: %s" % (wfn, best_prompt)

    cut_pos = best_cut

    promptsf.write ( (u'%s/mfc/%s %s\n' % (dir_name, wfn[0:len(wfn)-4], best_prompt) ).encode('utf8') )
    promptsf.flush()

    opromptsf.write ( (u'%s %s\n' % (wfn[0:len(wfn)-4], best_prompt) ).encode('utf8') )
    opromptsf.flush()

