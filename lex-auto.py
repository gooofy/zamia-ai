#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import re
import os
import StringIO
import ConfigParser
from os.path import expanduser
import subprocess
import psycopg2
import pocketsphinx

from phonetic_alphabets import ipa2xsampa, xsampa2ipa, xsampa2xarpabet, mary2ipa
from gutils import split_words

from maryclient import mary_say_phonemes, mary_gather_ph, mary_gen_phonemes, mary_init, mary_set_voice
from espeakclient import espeak_gen_ipa
from phonetisaurusclient import phonetisaurus_gen_ipa

#
# auto-generate phonemes for missing words, rate them by using sphinx_align and the current model
# only keep those we're sure meet our quality requirements
#

WORST_SCORE = -850000
DEBUG_LIMIT = 5000

#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

webroot   = config.get("speech", "webroot")

db_server = config.get("speech", "dbserver")
db_name   = config.get("speech", "dbname")
db_user   = config.get("speech", "dbuser")
db_pass   = config.get("speech", "dbpass")

wdir      = config.get("speech", "workdir") 
workdir   = config.get("speech", "workdir") + "/align"
featdir   = config.get("speech", "featdir")

hmdir     = config.get("pocketsphinx", "hmm")
lmdir     = config.get("pocketsphinx", "lm")
#dictf     = config.get("pocketsphinx", "dict")
dictf     = "/tmp/voxforge.dic"

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# mary
#

mary_init()

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

cur.execute ("SELECT DISTINCT prompt FROM submissions WHERE reviewed=FALSE") 
rows = cur.fetchall()
for row in rows:

    prompt = row[0].decode('UTF8')

    ws = split_words(prompt)

    for word in ws:

        if not word in word_counter:
            missing_words[word] = ""

print "done. %d missing words found." % len(missing_words)
print

cnt = 0

for word in missing_words:

    cnt += 1

    # try phonetisaurus first, see if result meets quality stds
    # fall back to mary otherwise

    ipas = phonetisaurus_gen_ipa (word)

    if (ipas.count(u'-') > 0) and (ipas.count(u"'") > 0):

        print (u"%4d/%4d PHONETISAURUS %-18s %s" % (cnt, len(missing_words), word, ipas)).encode('utf8')

    else:
        mp = mary_gen_phonemes (word)
        ipas = mary2ipa(word, mp)

        print (u"%4d/%4d MARY          %-18s %s" % (cnt, len(missing_words), word, ipas)).encode('utf8')

    xs = ipa2xsampa(word, ipas)
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
# sphinx_align files setup
#


os.system ("rm -rf %s" % workdir)
os.system ("mkdir %s" % workdir)

transfn = "%s/align.transcription" % workdir
ctlfn   = "%s/align.fileids" % workdir

transf = open (transfn, 'w')
ctlf   = open (ctlfn, 'w')

cur.execute ('SELECT id,prompt,cfn FROM submissions WHERE reviewed=false')
rows = cur.fetchall()
for row in rows:

    sid         = row[0]
    prompt      = row[1].decode('UTF8').lstrip().rstrip()
    cfn         = row[2].decode('UTF8')

    ctlf.write ('%s\n' % cfn)
    transf.write ((u'%s (%s)\n' % (prompt, cfn)).encode('utf8'))

transf.close()
print "%s written." % transfn
    
ctlf.close()
print "%s written." % ctlfn
   
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
	-wdsegdir %s,CTL " % (hmdir, dictf, ctlfn, featdir, transfn, workdir, segdir)

print 
print cmdline

os.system (cmdline)

#
# parse results, auto-transcribe good submissions
#

validated_words = set()

for row in rows:

    sid         = row[0]
    prompt      = row[1].decode('UTF8').lstrip().rstrip()
    cfn         = row[2].decode('UTF8')

    resfn = "%s/%s.wdseg" % (segdir, cfn)

    if not os.path.isfile(resfn):
        continue

    wscore = 0

    resf = open(resfn)

    for line in resf:

        l = line.decode('utf8').rstrip()

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

    if wscore < WORST_SCORE:
        print "%-30s %d" % (cfn, wscore)
        continue

    print "%-30s %d ACCEPT!" % (cfn, wscore)
    
    words = re.split ('\s+', prompt)
    for word in words:

        if word in missing_words:
            print (u"   MISSING WORD COVERED: %s" % word).encode('utf8')
            validated_words.add(word)

print
print "done. %d pronounciations validated." % len(validated_words)

#
# put ipas into db
#

for word in validated_words:

    print (u"Putting pronounciation for word %s into db..." % word).encode('utf8')

    wid = 0

    cur.execute ('SELECT id FROM words WHERE word=%s', (word,))

    row = cur.fetchone()
    if not row:
        cur.execute ('INSERT INTO words (word, occurences) VALUES (%s, 1) RETURNING id', (word, ))
        row = cur.fetchone()
        wid = row[0]
    else:
        wid = row[0]
        cur.execute ('UPDATE words SET oov=false WHERE id=%s', (wid,))

    # just to be sure...
    cur.execute ('DELETE FROM pronounciations WHERE wid=%s', (wid,))

    ipas = missing_words[word]

    cur.execute ('INSERT INTO pronounciations (phonemes, probability, points, wid) VALUES (%s,%s,%s,%s)', (ipas, 100, 5, wid))

    conn.commit()
    
    cur = conn.cursor()

print
print "All done."
print

