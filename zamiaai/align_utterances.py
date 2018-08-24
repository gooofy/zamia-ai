#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016, 2017, 2018 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# right now this is just a dumping ground for the align_utterance code
# will be turned into a proper zaicli command soon along with the other
# data tools
#

from __future__ import print_function


def avg_feature_vector(words, model, num_features, index2word_set):
    #function to average all words vectors in a given paragraph
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0

    for word in words:
        if word in index2word_set:
            nwords = nwords+1
            featureVec = np.add(featureVec, model[word])

    if nwords > 0:
        featureVec = np.divide(featureVec, nwords)
    return featureVec


#     #
#     # alignment / word2vec (on-demand model loading)
#     #
#     self.w2v_model          = None
#     self.w2v_all_utterances = []
# 
# 
#     def setup_align_utterances (self):
#         if self.w2v_model:
#             return
# 
#         logging.debug('loading all utterances from db...')
# 
#         self.w2v_all_utterances = []
#         req = self.session.query(model.TrainingData).filter(model.TrainingData.lang==self.lang)
#         for dr in req:
#             self.w2v_all_utterances.append((dr.utterance, dr.module, dr.loc_fn, dr.loc_line))
# 
#         if not self.w2v_model:
#             from gensim.models import word2vec
# 
#         model_fn  = self.config.get('semantics', 'word2vec_model_%s' % self.lang)
#         logging.debug ('loading word2vec model %s ...' % model_fn)
#         logging.getLogger('gensim.models.word2vec').setLevel(logging.WARNING)
#         self.w2v_model = word2vec.Word2Vec.load_word2vec_format(model_fn, binary=True)
#         #list containing names of words in the vocabulary
#         self.w2v_index2word_set = set(self.w2v_model.index2word)
#         logging.debug ('loading word2vec model %s ... done' % model_fn)
# 
#     def align_utterances (self, utterances):
# 
#         self.setup_align_utterances()
# 
#         res = {}
# 
#         for utt1 in utterances:
#             try:
#                 utt1t = tokenize(utt1, lang=self.lang)
#                 av1 = avg_feature_vector(utt1t, model=self.w2v_model, num_features=300, index2word_set=self.w2v_index2word_set)
# 
#                 sims = {} # location -> score
#                 utts = {} # location -> utterance
# 
#                 for utt2, module, loc_fn, loc_line in self.w2v_all_utterances:
#                     try:
#                         utt2t = tokenize(utt2, lang=self.lang)
# 
#                         av2 = avg_feature_vector(utt2t, model=self.w2v_model, num_features=300, index2word_set=self.w2v_index2word_set)
# 
#                         sim = 1 - cosine(av1, av2)
# 
#                         location = '%s:%s:%d' % (module, loc_fn, loc_line)
#                         sims[location] = sim
#                         utts[location] = utt2
#                         # logging.debug('%10.8f %s' % (sim, location))
#                     except:
#                         logging.error('EXCEPTION CAUGHT %s' % traceback.format_exc())
#                 logging.info('sims for %s' % repr(utt1))
#                 cnt = 0
#                 res[utt1] = []
#                 for sim, location in sorted( ((v,k) for k,v in sims.iteritems()), reverse=True):
#                     logging.info('%10.8f %s' % (sim, location))
#                     logging.info('    %s' % (utts[location]))
# 
#                     res[utt1].append((sim, location, utts[location]))
# 
#                     cnt += 1
#                     if cnt>5:
#                         break
#             except:
#                 logging.error('EXCEPTION CAUGHT %s' % traceback.format_exc())
# 
#         return res

