#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Guenter Bartsch
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
# align AIML patterns to our existing discourse rounds, print likely matches
#
# the idea here is to give the user hints where (module/line) to add new nlp_gen patterns
#

import os
import sys
import traceback
import codecs
import logging

from optparse import OptionParser
import xml.etree.ElementTree as ET

from gensim.models import word2vec
import model

from nltools import misc, tokenizer

from sqlalchemy.orm import sessionmaker

import numpy as np
from scipy.spatial.distance import cosine

DEFAULT_LOGLEVEL   = logging.DEBUG
DEFAULT_OUTPUT     = 'foo.pl'

def avg_feature_vector(words, model, num_features, index2word_set):
        #function to average all words vectors in a given paragraph
        featureVec = np.zeros((num_features,), dtype="float32")
        nwords = 0

        for word in words:
            if word in index2word_set:
                nwords = nwords+1
                featureVec = np.add(featureVec, model[word])

        if(nwords>0):
            featureVec = np.divide(featureVec, nwords)
        return featureVec

#
# init, cmdline
#

misc.init_app('aim2topics')

parser = OptionParser("usage: %prog [options] foo.aiml")

parser.add_option ("-l", "--lang", dest="lang", type = "string", default='en',
                   help="language, default: en")
parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if len(args) != 1:
    parser.print_usage()
    sys.exit(1)

aimlfn   = args[0]

#
# db
#

Session = sessionmaker(bind=model.engine)
session = Session()

#
# vectors
#

WORD2VEC_MODEL = '/home/bofh/projects/ai/data/word2vec/GoogleNews-vectors-negative300.bin'

logging.info('loading %s...' % WORD2VEC_MODEL)

word2vec_model = word2vec.Word2Vec.load_word2vec_format(WORD2VEC_MODEL, binary=True)

#list containing names of words in the vocabulary
index2word_set = set(word2vec_model.index2word)

#
# parse AIML input file
#

logging.info('parsing %s ...' % aimlfn)

tree = ET.parse(aimlfn)

logging.info('parsing done. converting...')

root = tree.getroot()

logging.debug('root tag: %s' % root.tag)

ns = {'aiml': 'http://alicebot.org/2001/AIML-1.0.1'}

for category in root.findall('aiml:category', ns):

    pattern = category.find('aiml:pattern', ns)
    pt      = pattern.text

    if not pt:
        continue

    pt = tokenizer.tokenize(pt, lang=options.lang)

    if len(pt)<3:
        continue

    pt = u' '.join(pt)

    print 'pattern: %s' % pt
    if session.query(model.DiscourseRound).filter(model.DiscourseRound.lang==options.lang, model.DiscourseRound.inp==pt).count()>0:
        print "   already covered, next."
        continue

    sentence_1_avg_vector = avg_feature_vector(pt.split(), model=word2vec_model, num_features=300, index2word_set=index2word_set)

    # print "sentence_1_avg_vector", repr(sentence_1_avg_vector)

    best_sim = 0.0

    for dr in session.query(model.DiscourseRound).filter(model.DiscourseRound.lang==options.lang):

        try:

            # print dr.inp

            sentence_2 = dr.inp
            sentence_2_avg_vector = avg_feature_vector(sentence_2.split(), model=word2vec_model, num_features=300, index2word_set=index2word_set)
            # print "sentence_2_avg_vector", repr(sentence_2_avg_vector)

            sen1_sen2_similarity =  1 - cosine(sentence_1_avg_vector,sentence_2_avg_vector)

            if sen1_sen2_similarity > best_sim:
                best_sim = sen1_sen2_similarity

                if best_sim > 0.85:
                    print '%10.8f %-35s %4d %s' % (sen1_sen2_similarity, dr.loc_fn, dr.loc_line, dr.inp)

        except:
            print '   (runtime exception supressed)'

    for tmpl in category.findall('aiml:template', ns):

        t = tmpl.text.strip() if tmpl.text else ''
        for child in tmpl:
            if child.text:
                if len(t) > 0:
                    t += ' '
                t += child.text.strip()

            if child.tail:
                if len(t) > 0:
                    t += ' '
                t += ' ' + child.tail.strip()

        t = t.replace('"', ' ').replace('\n', ' ').replace('\'', ' ')

        # comment out pattern if it contains any aiml mechanics
        # we do not support yet

        # comment_out = '*' in pt or '_' in pt or '*' in t or len(t) == 0
        # keep_xml    = False
        # if tmpl.find('aiml:srai', ns) is not None:
        #     keep_xml = True
        #     comment_out = True
        # if tmpl.find('aiml:that', ns) is not None:
        #     keep_xml = True
        #     comment_out = True
        # if tmpl.find('aiml:bot', ns) is not None:
        #     keep_xml = True
        #     comment_out = True
        # if tmpl.find('aiml:set', ns) is not None:
        #     keep_xml = True
        #     comment_out = True
        # if tmpl.find('aiml:get', ns) is not None:
        #     keep_xml = True
        #     comment_out = True

        # print '   ', t

        for l in ET.tostringlist(tmpl, 'utf8'):
            print "# %s" % l.replace('\n','')

        print "##              '%s').\n\n" % t

    print 

sys.exit(0)

#get average vector for sentence 1
sentence_1 = "computer wie geht es dir"
sentence_1_avg_vector = avg_feature_vector(sentence_1.split(), model=word2vec_model, num_features=300, index2word_set=index2word_set)

# print "sentence_1_avg_vector", repr(sentence_1_avg_vector)

best_sim = 0.0

for dr in session.query(model.DiscourseRound).filter(model.DiscourseRound.lang==options.lang):

    try:

        # print dr.inp

        sentence_2 = dr.inp
        sentence_2_avg_vector = avg_feature_vector(sentence_2.split(), model=word2vec_model, num_features=300, index2word_set=index2word_set)
        # print "sentence_2_avg_vector", repr(sentence_2_avg_vector)

        sen1_sen2_similarity =  1 - cosine(sentence_1_avg_vector,sentence_2_avg_vector)

        if sen1_sen2_similarity > best_sim:
            best_sim = sen1_sen2_similarity

            print '%10.8f %s' % (sen1_sen2_similarity, dr.inp)

    except:
        print '   (runtime exception supressed)'


sys.exit()



