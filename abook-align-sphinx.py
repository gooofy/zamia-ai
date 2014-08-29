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

hmdir     = config.get("pocketsphinx", "hmm")
#dictf     = config.get("pocketsphinx", "dict")

# custom dict
dictf     = "/tmp/voxforge.dic"

# custom lm
sentfn    = "/tmp/voxforge.txt"
vocabfn   = "/tmp/voxforge.vocab"
idngramfn = "/tmp/voxforge.idngram"
arpafn    = "/tmp/voxforge.arpa"
dmpfn     = "/tmp/voxforge.lm.DMP"

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
    print "usage: %s dir prompt.txt" % sys.argv[0]
    sys.exit(1)

dir_path = sys.argv[1]
dir_name = os.path.basename(dir_path)

promptfn = sys.argv[2]

promptsfn  = "%s/etc/PROMPTS" % (dir_path)
opromptsfn = "%s/etc/prompts-original" % (dir_path)

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# create CMUCLMTK Language Model
#

print 
print "creating CMUCLMTK language model..."

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

print "creating %s..." % vocabfn
vocabf = open(vocabfn, 'w')

for word in used_words:
    vocabf.write(('%s\n' % word).encode('utf8'))

vocabf.write('</s>\n')
vocabf.write('<s>\n')

vocabf.close()
print "%s written." % vocabfn

print "creating %s..." % sentfn

sentf = open (sentfn, 'w')

# create all sub-sentences 3 to 18 words

for offset in range(len(allprompts)):

    for l in range (3,18):

        if (offset+l) > len(allprompts):
            continue

        prompt_words = allprompts[offset:offset+l]

        prompt = ' '.join(prompt_words)
        sentf.write ( ('<s> %s </s>\n' % prompt).encode('utf8') )

sentf.close()

print "%s written." % sentfn

cmd = 'text2idngram -vocab %s -idngram %s < %s' % (vocabfn, idngramfn, sentfn)
print cmd
os.system (cmd)
cmd = 'idngram2lm -vocab_type 0 -idngram %s -vocab %s -arpa %s' % (idngramfn, vocabfn, arpafn)
print cmd
os.system (cmd)
cmd = 'sphinx_lm_convert -i %s -o %s' % (arpafn, dmpfn)
print cmd
os.system (cmd)
print

#
# dump current dict
#

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
# setup pocketsphinx decoder
#

config = pocketsphinx.Decoder.default_config()
config.set_string('-hmm', hmdir)
config.set_string('-lm', dmpfn)
config.set_string('-dict', dictf)
config.set_string('-logfn', "/dev/null")
decoder = pocketsphinx.Decoder(config)

#
# recognize wavs
#

promptsf  = open(promptsfn, 'w')
opromptsf  = open(opromptsfn, 'w')

for wfn in sorted(os.listdir('%s/wav/' % dir_path)):

    wavfn = '%s/wav/%s' % (dir_path, wfn)

    print 
    print "recognizing %s ... " % wavfn

    wavFile = file(wavfn,'rb')
    decoder.decode_raw(wavFile)

    # Retrieve hypothesis.
    hypothesis = decoder.hyp()

    hstr = hypothesis.hypstr.decode('UTF8').lstrip().rstrip()

    print u'HYPOTH: %s' % hstr

    # len in words
    hyp_words = split_words(hstr)
    hyp_len = len(hyp_words)

    best_dist   = 100000
    best_prompt = []

    for offset in range(len(allprompts)):

        for l in range (hyp_len-3,hyp_len+3):

            if l<1:
                continue

            if (offset+l) > len(allprompts):
                continue

            prompt_words = allprompts[offset:offset+l]

            #print
            #print "offset: %5d o: %5d l: %5d" % (offset, o, l)
            #print u"HYP   : %s" % hyp_words
            #print u"PROMPT: %s" % prompt_words

            dist = edit_distance (hyp_words, prompt_words)
            if dist < best_dist:
                best_dist   = dist
                best_prompt = prompt_words
            #print "Distance: %d, best distance: %d" % (dist, best_dist) 

    print 
    print u"HYP        : %s" % hyp_words
    print u"Best prompt: %s (%d)" % (best_prompt, best_dist)

    p = ' '.join(best_prompt)

    promptsf.write ( (u'%s/mfc/%s %s\n' % (dir_name, wfn[0:len(wfn)-4], p) ).encode('utf8') )
    promptsf.flush()

    opromptsf.write ( (u'%s %s\n' % (wfn[0:len(wfn)-4], p) ).encode('utf8') )
    opromptsf.flush()

print

promptsf.close()
opromptsf.close()
print "%s written, %s written." % (promptsfn, opromptsfn)
print

