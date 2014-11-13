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
# use pocketsphinx running to recognize new audio, then align text to promptsfile
#
# use current audio model
# but use a custom language model generated solely from promptsfile
# also add all missing words best-effort to dict
#

MIN_SENT_LEN   = 1
MAX_SENT_LEN   = 64
OFFSET_JITTER  = 2
REALIGN_JITTER = 20

# switch off for faster debugging
CREATE_DICT   = True

#WORST_SCORE =   -850000
WORST_SCORE  =  -8500000
#WORST_SCORE = -32274658

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

wdir      = config.get("speech", "workdir") 
workdir   = config.get("speech", "workdir") + "/align"
abook_dir = config.get("speech", "abookdir")
audiodir  = config.get("speech", "audiodir")
hmdir     = config.get("pocketsphinx", "hmm")
#dictf     = config.get("pocketsphinx", "dict")

# custom dict
dictf     = "/tmp/voxforge.dic"

featdir   = "/tmp"
featfn    = "foo.mfc"

#
# init
#

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

#
# command line
#

if len(sys.argv) != 3:
    print "usage: %s title partnum" % sys.argv[0]
    sys.exit(1)

abook_title  = sys.argv[1]
abook_part   = int(sys.argv[2])

promptfn = '%s/%s/prompts/part%02d.txt' % (abook_dir, abook_title, abook_part)

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# fetch cfn for this abook part from db
#

cur.execute ('SELECT cfn FROM abooks WHERE title=%s AND partnum=%s', (abook_title, abook_part))
row = cur.fetchone()

dir_name = row[0].decode('utf8')
dir_path = '%s/%s' % (audiodir, dir_name)

promptsfn  = "%s/etc/PROMPTS" % (dir_path)
opromptsfn = "%s/etc/prompts-original" % (dir_path)

#
# dump current dict
#

if CREATE_DICT:

    # read model phoneme list (we do not want to put words into our dict the model does not have phonemes for)
    
    phones_covered = set()
    
    phfn = '%s/etc/voxforge.phone' % wdir
    for line in open (phfn, 'r'):
        phones_covered.add(line.rstrip())
    
    #print repr(phones_covered)
    
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
    
        phones = xa.split(' ')
    
        #print "%s %s" % (word, repr(phones))
    
        covered = True
        for phone in phones:
            if not phone in phones_covered:
                print (u"Skipping word %s (at least one phoneme not covered)" % word).encode('utf8')
                covered = False
                break
        
        if not covered:
            continue
    
        if not word in word_counter:
            pdf.write ( (u'%s %s\n' % (word, xa)).encode('UTF8') )
            word_counter[word] = 1
    
        else:
            word_counter[word] += 1
            w2 = u'%s(%d)' % (word, word_counter[word])
            pdf.write ( (u'%s %s\n' % (w2, xa)).encode('UTF8') )
    
    #
    # generate phonemes for missing words
    #
    
    print
    print "Looking for missing words ..."
    
    missing_words = {}
    
    promptf = open (promptfn)
    
    for line in promptf:
        prompt = line.decode('UTF8').rstrip()
    
        ws = split_words(prompt)
    
        for word in ws:
    
            if not word in word_counter:
                missing_words[word] = ""
    
    
    promptf.close()
    
    print "done. %d missing words found. " % len(missing_words)
    print
    
    cnt = 0
    
    for word in missing_words:
    
        cnt += 1
    
        ipas = phonetisaurus_gen_ipa (word)
    
        xs = ipa2xsampa(word, ipas)
        xa = xsampa2xarpabet(word, xs)
    
        phones = xa.split(' ')
    
        print u"%5d/%5d %-18s %s" % (cnt, len(missing_words), word, ipas)
    
        covered = True
        for phone in phones:
            if not phone in phones_covered:
                print (u"Skipping word %s (at least one phoneme not covered)" % word).encode('utf8')
                covered = False
                break
        
        if not covered:
            continue
    
        missing_words[word] = ipas
    
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
# read all lines from prompts file, create long list of words
#

print 
print "reading %s ..." % promptfn

used_words = set()
allprompts = []

print "reading prompts..."

promptf = open (promptfn)
for line in promptf:
    prompt = line.decode('UTF8').rstrip()

    ws = split_words(prompt)

    for word in ws:
        used_words.add(word)

        allprompts.append(word)

promptf.close()

print "# unique words in prompts: %d" % len(used_words)

#
# sphinx_align files setup
#

def compute_alignment (featfn, prompt):

    os.system ("rm -rf %s" % workdir)
    os.system ("mkdir %s" % workdir)

    transfn = "%s/align.transcription" % workdir
    ctlfn   = "%s/align.fileids" % workdir

    transf = open (transfn, 'w')
    ctlf   = open (ctlfn, 'w')

    ctlf.write ('%s\n' % featfn)
    transf.write ((u'%s (%s)\n' % (prompt, featfn)).encode('utf8'))

    transf.close()  
    ctlf.close()

    #
    # run sphinx_align
    #
    
    segdir = "%s/segmentations" % workdir
    
    cmdline = "sphinx3_align \
        -hmm %s \
    	-dict %s \
    	-ctl %s \
    	-cepdir %s \
    	-cepext .mfc \
    	-insent %s \
    	-outsent %s/alignment_output.txt \
    	-wdsegdir %s,CTL &>/tmp/sphinx_align.log " % (hmdir, dictf, ctlfn, featdir, transfn, workdir, segdir)
    
    #print 
    #print cmdline
    
    os.system (cmdline)
    
    #
    # parse result, auto-transcribe good submissions
    #
    
    resfn = "%s/%s.wdseg" % (segdir, featfn)
    
    if not os.path.isfile(resfn):
        return -sys.maxint - 1
    
    wscore = 0
    
    resf = open(resfn)
    
    for line in resf:
    
        l = line.decode('utf8').rstrip()
    
        #print u"%s %s" % (resfn, l)
   
        m = re.match(r"^\s*Total\s+score:\s+([+\-]\d+)", l)

        #print repr(m)
 
        #m = re.match(r"^\s+\d+\s+\d+\s+([+\- ]\d+)", l)
        if not m:
            continue
   
        wscore = int (m.group(1))
        break
 
    resf.close()
   
    #sys.exit(0)
 
    return wscore

wav_files = sorted(os.listdir('%s/wav/' % dir_path))

base_offset = 0

for wav_idx in range (0, len(wav_files)-1):

    wavfn = wav_files[wav_idx]

    # check to see if this file has already been reviewed (if so, adjust base_offset and continue on)

    cfn = "%s_%s" % (dir_name, os.path.splitext(wavfn)[0])
    print cfn
    cur.execute ('SELECT prompt FROM submissions WHERE cfn=%s AND reviewed=true', (cfn,))
    row = cur.fetchone()
    if row:
        prompt = row[0].decode('utf8')
        print "already reviewed: %s" % prompt

        # adjust base_offset, allow for minor deviations

        p1 = split_words(prompt)
        min_dist = 10000
        min_offset = base_offset
        for offset in range (base_offset - REALIGN_JITTER, base_offset + REALIGN_JITTER):
            if offset<0:
                continue

            p2 = allprompts[offset:offset+len(p1)]
            dist = edit_distance(p1, p2)
            if dist<min_dist:
                min_dist = dist
                min_offset = offset

            print "offset adjustment: %5d %s vs %s" % (dist, ' '.join(p1), ' '.join(p2))

        base_offset = min_offset + len(p1)
        continue


    os.system ("sphinx_fe -i '%s/wav/%s' -part 1 -npart 1 -ei wav -o '%s/%s' -eo mfc -nist no -raw no -mswav yes -samprate 16000 -lowerf 130 -upperf 6800 -nfilt 25 -transform dct -lifter 22 &>/tmp/sphinx_fe.log" % (dir_path, wavfn, featdir, featfn) )

    best_prompt = ''
    best_score  = -sys.maxint - 1
    best_offset = base_offset
    best_len    = MIN_SENT_LEN

    failcnt = 0

    for offset in range (base_offset-OFFSET_JITTER, base_offset+OFFSET_JITTER):

        if offset < 0:
            continue

        for l in range (MIN_SENT_LEN, MAX_SENT_LEN):

            p_start = offset 
            p_end   = offset + l - 1

            if p_end >= len(allprompts):
                continue

            p = ' '.join(allprompts[p_start:p_end+1])

            score = compute_alignment (featfn, p)

            if score == -sys.maxint - 1:
                failcnt += 1
                if failcnt > 3:
                    break
                continue

            failcnt = 0

            if score > best_score:
                best_prompt = p
                best_offset = offset
                best_len    = l
                best_score  = score
                print "%s +++ %7d %4d %4d %4d %s" % (wavfn, score, base_offset, p_start, p_end, p)
            else:
                print "%s     %7d %4d %4d %4d %s" % (wavfn, score, base_offset, p_start, p_end, p)

    print "%s Done. Best prompt: %s" % (wavfn, best_prompt)

    if best_score < WORST_SCORE:
        print
        print "*** ERROR: Score too bad, lost sync. Exiting."
        print
        sys.exit(1)

    base_offset = best_offset + best_len

    cur.execute ('UPDATE submissions SET prompt=%s WHERE cfn=%s', (best_prompt, cfn))
    conn.commit()
    cur = conn.cursor()


