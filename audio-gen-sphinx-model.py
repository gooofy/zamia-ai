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
from os.path import expanduser
import StringIO
import ConfigParser
from optparse import OptionParser
import psycopg2

from gutils import detect_latin1, split_words
from phonetic_alphabets import ipa2xsampa, xsampa2ipa, xsampa2xarpabet

MIN_PHONE_COVERAGE = 10

# simple wrapper around os.system, will 
# - cd to workdir first
# - print out command to stdout
# - redirect output to logfile
def systemlog (cmd, logfile):

    lcmd = 'cd %s ; %s > logs/%s' % (workdir, cmd, logfile)
    print lcmd

    res = os.system (lcmd)

    if res != 0:
        sys.exit(res)

print
print "Step 1 - Preparation"
print

#
# commandline
#

parser = OptionParser("usage: %prog [options] [prefix]")

parser.add_option ("-p", "--pronounciation", dest="pronounciation", type = "int", default=1,
           help="worst acceptable pronounciation: 0=clean, 1=accent, 2=dialect, 3=error (default: 1)")

parser.add_option ("-a", "--audiolevel", dest="audiolevel", type = "int", default=1,
           help="worst acceptable audio level: 0=good, 1=low, 2=very low, 3=distorted (default: 1)")

parser.add_option ("-n", "--noiselevel", dest="noiselevel", type = "int", default=1,
           help="worst acceptable noise level: 0=low, 1=noticable, 2=high (default: 1)")

parser.add_option ("-c", "--continous", dest="continous", action="store_true",
           help="accept non-continous submissions (default: accept only continous submissions)")

(options, args) = parser.parse_args()

#print "Options: %s, args: %s" % (repr(options), repr(args))

prefix = ''
if len(args) ==1:
    prefix = args[0]

continous = True
if options.continous:
    continous = False

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

w16dir    = config.get("speech", "16khzdir")
workdir   = config.get("speech", "workdir")
lmworkdir = config.get("speech", "lmworkdir")
featdir   = config.get("speech", "featdir")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# prepare work dir
#

os.system ("rm -rf %s" % workdir)
os.system ("mkdir %s" % workdir)
os.system ("mkdir %s/logs" % workdir)

systemlog ('sphinxtrain -t voxforge setup', 'sphinxtrain_setup.log')

# generate sphinx_train.cfg, featdir in there

inf = open ('input_files/sphinx_train.cfg')
outf = open ('%s/etc/sphinx_train.cfg' % workdir, 'w')
for line in inf:
    s = line.decode('utf8').replace('%FEATDIR%', featdir)
    outf.write (s.encode('utf8'))
inf.close()
outf.close()

os.system ('cp input_files/voxforge.filler %s/etc' % workdir)
os.system ('cp %s/voxforge.lm.DMP %s/etc' % (lmworkdir, workdir))

print
print "Step 2 - Pronunciation Dictionnary"
print

# compute phoneme converage for all good submissions
# phoneme -> counter
phone_coverage = {}

sql = "SELECT phonemes,word FROM transcripts,submissions,pronounciations,words WHERE words.id=transcripts.wid AND transcripts.sid=submissions.id AND pronounciations.id=transcripts.pid AND reviewed=true AND noiselevel<=%s AND truncated=false AND audiolevel<=%s AND pcn<=%s AND cfn LIKE %s AND alignment_error=false "
if continous:
    sql += " AND continous=true"

#sql += " LIMIT 100000"

print "Computing phoneme coverage..."

print sql

cur.execute (sql, (options.noiselevel, options.audiolevel, options.pronounciation, prefix+"%") )
rows = cur.fetchall()

print "%d rows..." % len(rows)

for row in rows:

    ipa  = row[0].decode('UTF8')
    word = row[1].decode('UTF8')

    xs = ipa2xsampa(word, ipa)
    xa = xsampa2xarpabet(word, xs)
    
    phones = xa.split(' ')
    for phone in phones:

        if not phone in phone_coverage:
            phone_coverage[phone] = 1
        else:
            phone_coverage[phone] += 1

for phone in phone_coverage:
    print "%6s %d" % (phone, phone_coverage[phone])

print
print "Computing well-covered pids..."
print

# compute list of pids covered by good submissions (we will use only those in training)

pids_covered = set()

sql = "SELECT DISTINCT pid,phonemes,word FROM transcripts,submissions,pronounciations,words WHERE words.id=transcripts.wid AND pronounciations.id=transcripts.pid AND transcripts.sid=submissions.id AND reviewed=true AND noiselevel<=%s AND truncated=false AND audiolevel<=%s AND pcn<=%s AND cfn LIKE %s AND alignment_error=false"
if continous:
    sql += " AND continous=true"

cur.execute (sql, (options.noiselevel, options.audiolevel, options.pronounciation, prefix+"%") )
rows = cur.fetchall()
for row in rows:

    pid  = row[0]
    ipa  = row[1].decode('UTF8')
    word = row[2].decode('UTF8')

    xs = ipa2xsampa(word, ipa)
    xa = xsampa2xarpabet(word, xs)
    
    phones = xa.split(' ')
    covered = True
    lacking_phone = ""
    for phone in phones:

        if not phone in phone_coverage:
            lacking_phone = phone
            covered = False
            break
    
        coverage = phone_coverage[phone]
        if coverage < MIN_PHONE_COVERAGE:
            lacking_phone = phone
            covered = False
            break

    if covered:
        pids_covered.add(pid)
    else:
        print (u"skipping word for lack of coverage for phone %s in submissions: %s" % (lacking_phone, word)).encode('utf8')

# now: generate dict

print
print "Generating dictionary..."

pdfn = '%s/etc/voxforge.dic' % workdir
pdf  = open (pdfn, 'w')

phoneset = set()

# word -> int, used to generate (2) (3) ... markers for words with multiple pronounciations
word_counter = {}
# pid -> ( word | word(1) | word(2) | ... )
pmap = {}

cur.execute ("SELECT phonemes,word,pronounciations.id FROM pronounciations,words WHERE pronounciations.wid=words.id ORDER BY word ASC")
rows = cur.fetchall()
for row in rows:

    ipa  = row[0].decode('UTF8')
    word = row[1].decode('UTF8')
    pid  = row[2]

    if not pid in pids_covered:
        continue

    xs = ipa2xsampa(word, ipa)
    xa = xsampa2xarpabet(word, xs)
    
    if not word in word_counter:
        pdf.write ( (u'%s %s\n' % (word, xa)).encode('UTF8') )
        word_counter[word] = 1
        pmap[pid] = word

    else:
        word_counter[word] += 1
        w2 = u'%s(%d)' % (word, word_counter[word])
        pdf.write ( (u'%s %s\n' % (w2, xa)).encode('UTF8') )
        pmap[pid] = w2

    phones = xa.split(' ')
    for phone in phones:
        phoneset.add(phone)

pdf.close()

print "%s written." % pdfn

print "Got %d phones." % len(phoneset)

phfn = '%s/etc/voxforge.phone' % workdir
phf = open (phfn, 'w')

for phone in phoneset:
    phf.write ('%s\n' % phone)

phf.write ('SIL\n')
phf.close()

print "%s written." % phfn


print
print "Step 3 - Collect Prompts, generate voxforge.transcription"
print

#
# prompts
#

#widset = set()

train_fifn = '%s/etc/voxforge_train.fileids' % workdir
train_fif  = open (train_fifn, 'w')

train_tsfn = '%s/etc/voxforge_train.transcription' % workdir
train_tsf  = open (train_tsfn, 'w')

test_fifn = '%s/etc/voxforge_test.fileids' % workdir
test_fif  = open (test_fifn, 'w')

test_tsfn = '%s/etc/voxforge_test.transcription' % workdir
test_tsf  = open (test_tsfn, 'w')

sql = "SELECT id,cfn,prompt FROM submissions WHERE reviewed=true AND noiselevel<=%s AND truncated=false AND audiolevel<=%s AND pcn<=%s AND cfn LIKE %s AND alignment_error=false"

if continous:
    sql += " AND continous=true"

cur.execute (sql, (options.noiselevel, options.audiolevel, options.pronounciation, prefix+"%") )

count = 0

# keep track of words we have covered
dict_covered = set()

rows = cur.fetchall()
for row in rows:

    sid = row[0]
    cfn = row[1]
    prompt = row[2].decode('utf8')

    count += 1

    # check to see which words are covered by this submission
    uncovered_word = False
    for word in split_words(prompt):
        if word in dict_covered:
            continue
        dict_covered.add(word)
        uncovered_word = True

    # compute list of pids
    cur.execute ("SELECT pid FROM transcripts WHERE sid=%s ORDER BY id ASC" % (sid,))
    rows2 = cur.fetchall()

    # check to see if all pids are covered:
    pids_covered = True
    for row2 in rows2:
        pid  = row2[0]
        if not pid in pmap:
            pids_covered = False
            break

    if not pids_covered:
        print "Skipping submission %s (pid used not covered)" % cfn
        continue

    # up to 10% go to test data set
    if count % 10 == 0 and not uncovered_word:
        fif = test_fif
        tsf = test_tsf
    else:
        fif = train_fif
        tsf = train_tsf

    fif.write ('%s\n' % cfn)

    tsf.write ('<s> ')

    for row2 in rows2:
        pid  = row2[0]
        tsf.write ( (u"%s " % pmap[pid]).encode('UTF8') )

    tsf.write ('</s> (%s)\n' % cfn)

train_tsf.close()
train_fif.close()
test_tsf.close()
test_fif.close()

print "%s written." % train_tsfn
print "%s written." % train_fifn
print "%s written." % test_tsfn
print "%s written." % test_fifn

print
print "Step 4 - sphinxtrain"
print

systemlog ('sphinxtrain -s verify,g2p_train,lda_train,mllt_train,vector_quantize,falign_ci_hmm,force_align,vtln_align,ci_hmm,cd_hmm_untied,buildtrees,prunetree,cd_hmm_tied,lattice_generation,lattice_pruning,lattice_conversion,mmie_train,deleted_interpolation,decode run', 'sphinxtrain_run.log')


