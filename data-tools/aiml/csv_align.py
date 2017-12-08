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
# align CSV discourse rounds to existing training data sort and export as AI-Prolog
#

import os
import sys
import traceback
import codecs
import logging
import time
import xml.etree.ElementTree as ET
import numpy as np

from optparse               import OptionParser
from gensim.models          import word2vec
from zamiaai                import model
from nltools                import misc, tokenizer
from sqlalchemy.orm         import sessionmaker
from scipy.spatial.distance import cosine

DEFAULT_LOGLEVEL   = logging.DEBUG
DEFAULT_OUTPUT     = 'foo.aip'

def avg_feature_vector(words, model, num_features, index2word_set):
        #function to average all words vectors in a given paragraph
        featureVec = np.zeros((num_features,), dtype="float32")
        nwords = 0

        for word in words:
            if word in index2word_set:
                nwords = nwords+1
                featureVec = np.add(featureVec, model[word])

        if nwords>0:
            featureVec = np.divide(featureVec, nwords)
        return featureVec

#
# init, cmdline
#

misc.init_app('csv_align')

parser = OptionParser("usage: %prog [options] foo.csv")

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

csvfn   = args[0]

#
# db
#

Session = sessionmaker(bind=model.engine)
session = Session()

#
# vectors
#

time_start = time.time()
WORD2VEC_MODEL = '/home/bofh/projects/ai/data/word2vec/GoogleNews-vectors-negative300.bin'

logging.info('loading %s...' % WORD2VEC_MODEL)

word2vec_model = word2vec.Word2Vec.load_word2vec_format(WORD2VEC_MODEL, binary=True)

#list containing names of words in the vocabulary
index2word_set = set(word2vec_model.index2word)

logging.info('loading %s... done. took %fs' % (WORD2VEC_MODEL, time.time()-time_start))

#
# pre-compute training data vectors
#

time_start = time.time()
cnt = 0

logging.info ('precomputing training data word vectors...')

td_vectors = []
td_covered = set()

for td in session.query(model.TrainingData).filter(model.TrainingData.lang=='en', model.TrainingData.prio>=0):

    td_covered.add(td.utterance)

    try:

        sentence_2 = tokenizer.tokenize(td.inp, lang='en')
        sentence_2_avg_vector = avg_feature_vector(sentence_2, model=word2vec_model, num_features=300, index2word_set=index2word_set)

        key = td.module + ':' + td.loc_fn
        td_vectors.append((key, sentence_2_avg_vector))

        # logging.debug ('%6d: vector for %s is %s' % (cnt, repr(sentence_2), repr(sentence_2_avg_vector)))

        cnt += 1

        # if cnt > 1000:
        #     break

        if cnt % 1000 == 0:
            logging.info ('   %6d vectors computed in %fs.' % (cnt, time.time()-time_start))

    except:
        logging.error(traceback.format_exc())

logging.info ('precomputing training data word vectors...done. %d vectors computed in %fs.' % (cnt, time.time()-time_start))

#
# parse CSV input file, map uncovered questions to module:sourcefile keys
#

logging.info('parsing %s ...' % csvfn)

map_dict = {} # key -> {ques_en -> (resp_en, ques_de, resp_de)}

with codecs.open(csvfn, 'r', 'utf8') as csvf:

    cnt = 0

    for line in csvf:

        cnt += 1

        parts = line.strip().split(';')
        if len(parts) != 4:
            logging.error('failed to parse line: %s' % line.strip())
            continue

        ques_en = parts[0]
        resp_en = parts[1]
        ques_de = parts[2]
        resp_de = parts[3]

        ques_en_t = tokenizer.tokenize(ques_en, lang='en')

        ques_en_t = u' '.join(ques_en_t)

        if ques_en_t in td_covered:
            logging.debug (u'%6d ques_en: %s already covered. next.' % (cnt, ques_en))
            continue

        ques_en_avg_vector = avg_feature_vector(ques_en_t, model=word2vec_model, num_features=300, index2word_set=index2word_set)

        # logging.debug("ques_en_avg_vector: %s" % repr(ques_en_avg_vector))

        best_sim = 0.0
        best_key = 'misc'

        for key, td_v in td_vectors:

            try:

                sen1_sen2_similarity =  1 - cosine(ques_en_avg_vector, td_v)

                if sen1_sen2_similarity > best_sim:
                    best_sim = sen1_sen2_similarity
                    best_key = key

            except:
                logging.error(traceback.format_exc())

        if not best_key in map_dict:
            map_dict[best_key] = {}

        logging.debug (u'%6d ques_en: %s -> %s %f' % (cnt, ques_en, best_key, best_sim))
        map_dict[best_key][ques_en] = (resp_en, ques_de, resp_de)

        # if cnt > 50:
        #     break

# print repr(map_dict)

#
# generate output AI-Prolog source code
#

with codecs.open(DEFAULT_OUTPUT, 'w', 'utf8') as outf:

    for key in map_dict:

        outf.write(u'\n%%\n%% %s\n%%\n\n' % key)

        for ques_en in sorted(map_dict[key]):

            resp_en, ques_de, resp_de = map_dict[key][ques_en]

            outf.write('train(en) :- "%s",\n             "%s".\n'   % (ques_en, resp_en))
            outf.write('train(de) :- "%s",\n             "%s".\n\n' % (ques_de, resp_de))

logging.info ('%s written.' % DEFAULT_OUTPUT)

