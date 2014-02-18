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

#
# count word occurences in corpora, compute top-n list
#

import sys
import re
import os
import traceback
import nltk
import pickle
from os.path import expanduser
import StringIO
import ConfigParser
from gutils import compress_ws, split_words
import psycopg2

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

workdir   = config.get("speech", "lmworkdir")

TOTAL_WORD_LIMIT = 15000 # total number of words in active dict when done
TOPWORD_LIMIT    = 7000  # number of top-words we intend to cover by our prompts
MIN_SENTENCE_LEN = 3
MAX_SENTENCE_LEN = 10
PROMPT_LIMIT     = 100   # number of prompts per file generated

SENTENCE_LIMIT   = 0 # debug purposes, 0 to disable

def count_words(fn):

    print "Reading %s..." % fn

    count = 0

    with open(fn) as inf:

        for line in inf:

            l = line.decode('UTF8').rstrip()

            words = split_words(l)

            for word in words:

                if len(word) < 2:
                    continue
        
                if word in dict:
                    dict[word] += 1
                else:
                    dict[word] = 1

            count += 1
            if count % 10000 == 0:
                print "%7d sentences. %6d unique words." % (count, len(dict))

            #sentences.append(words)

            if SENTENCE_LIMIT > 0 and count > SENTENCE_LIMIT:
                break


def collect_sentences(fn):

    global sentences, words_all, words_missing

    print "Reading %s..." % fn

    count = 0

    with open(fn) as inf:

        for line in inf:

            l = line.decode('UTF8').rstrip()
            count += 1

            words = split_words(l)

            if len(words) < MIN_SENTENCE_LEN or len(words) > MAX_SENTENCE_LEN:
                continue

            score = 0
            for word in words:
                if word in words_missing:
                    score += 1
   
            if score == 0:
                continue
 
            sentences.append(words)

            if len(sentences) % 1000 == 0:
                print "%7d of %7d sentences collected." % (len(sentences), count)

            if SENTENCE_LIMIT > 0 and count > SENTENCE_LIMIT:
                break

#
# main
#

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# count word occurences in all corpora sentences
#

# word -> occurences
dict = {}

count_words('%s/prompts.sent' % workdir)
#count_words('%s/europarl.sent' % workdir)
count_words('%s/parole.sent' % workdir)

print 
print "Got %d unique words from corpora." % len(dict)

#print repr(sentences)

# compute top-n

topwords = set()
outfn = "output/topwords.txt" 
outf = open (outfn, 'w')

count = 0
for word in reversed(sorted(dict.iteritems(), key=lambda (k,v): (v,k))):
    #print word

    if len(word) < 2:
        continue

    topwords.add(word)

    outf.write ( ('%s\n' % word[0]).encode('UTF8') )

    count += 1
    if count >= TOPWORD_LIMIT:
        break

print
print "Computed top %d words." % count
outf.close()
print "%s written." % outfn

#
# compute set of words already covered by submissions
#

words_covered = set()

cur.execute ("SELECT DISTINCT word FROM submissions,words,transcripts WHERE submissions.id=transcripts.sid AND transcripts.wid=words.id AND reviewed=true AND noiselevel<2 AND truncated=false AND audiolevel<2 AND pcn<2")
rows = cur.fetchall()
for row in rows:
    words_covered.add(row[0].decode('UTF8'))

print 
print "Already covered by submissions: %d words." % len(words_covered)

words_missing = set()
for entry in topwords:
    word = entry[0]
    if word not in words_covered:
        #print "topword not covered yet: %s" % word
        words_missing.add(word)

print
print "Words not covered: %d" % len(words_missing)

words_all = words_covered | words_missing

#
# compute list of sentences we can pick from to cover words later
#

sentences = []

collect_sentences('%s/prompts.sent' % workdir)
#collect_sentences('%s/europarl.sent' % workdir)
collect_sentences('%s/parole.sent' % workdir)

print
print "%d sentences collected to cover words with." % len(sentences)

#
# now, look for prompts that cover the missing words 
# but use nothing but the words in words_all:
#

count = 0
pcnt  = 0
outfn = 'prompts/topwords-%03d' % pcnt
outf = open (outfn, 'w')

while len(words_all) < TOTAL_WORD_LIMIT:

    # look for sentence that may also cover other words:
    best_score = 0
    best_sentence = None

    for words in sentences:

        score = 0
        for word in words:
            if len(word) < 2:
                score = 0
                break
            if word in words_missing:
                score += 1

        #print "score %d: %s" % (score, repr(words))

        if score > best_score:
            best_score    = score
            best_sentence = words

    if best_score == 0:
        print "Failed to cover: %s" % repr (words_missing)
        break

    outf.write ( ('%s\n' % ' '.join(best_sentence)).encode('UTF8') )

    count += 1
    if count % PROMPT_LIMIT == 0:

        outf.close()
        print
        print "%s written." % outfn
        print
        pcnt += 1
        outfn = 'prompts/topwords-%03d' % pcnt
        outf = open (outfn, 'w')

    for word in best_sentence:
        if word in words_missing:
            words_missing.remove(word)
        if not word in words_all:
            print "   new word: %s" % word
        words_covered.add(word)
        words_all.add(word)

    print "Covered %d words, %4d words still missing, %4d prompts generated, dict size: %d" % (best_score, len(words_missing), count, len(words_all))

print
print "%d prompts to read." % count
print

outf.close()
print "%s written." % outfn
print


