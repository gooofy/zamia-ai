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
# ai context - keep track of context semantics in current natural language processing
#

from __future__ import print_function

import os
import sys
import logging
import traceback
import time
import datetime

import numpy as np

from tzlocal                import get_localzone # $ pip install tzlocal

from nltools                import misc
from nltools.tokenizer      import tokenize
from zamiaai                import model

MAX_NER_RESULTS    = 5

class AIContext(object):

    def __init__(self, user, session, lang, realm, kernal, test_mode = False):
        self.dlg_log      = []
        self.staged_resps = []
        self.high_score   = 0.0
        self.inp          = u''
        self.user         = user
        self.realm        = realm
        self.ner_dict     = {} # DB cache
        self.session      = session
        self.lang         = lang
        self.kernal       = kernal
        self.test_mode    = test_mode

        tz = get_localzone()
        self.current_dt   = tz.localize(datetime.datetime.now())

    def set_inp(self, inp):
        self.inp = inp

    def resp(self, resp, score=0.0, action=None, action_arg=None):
        if score < self.high_score:
            return
        if score > self.high_score:
            self.high_score   = score
            self.staged_resps = []
        self.staged_resps.append( (resp, score, action, action_arg) )

        #print ("resp: score=%f staged_resps=%s" % (score, repr(self.staged_resps)))


    def get_resps(self):
        return self.staged_resps

    def commit_resp(self, i):
        self.dlg_log.append( { 'inp': self.inp, 
                               'out': self.staged_resps[i][0] })

        action     = self.staged_resps[i][2]
        action_arg = self.staged_resps[i][3]
        if action:
            if action_arg:
                action(self, action_arg)
            else:
                action(self)

        self.staged_resps = []
        self.high_score = 0.0

        self.kernal.prolog_persist()
       
    def _ner_learn(self, lang, cls):

        entities = []
        labels   = []

        for nerdata in self.session.query(model.NERData).filter(model.NERData.lang==lang).filter(model.NERData.cls==cls):
            entities.append(nerdata.entity)
            labels.append(nerdata.label)

        if not lang in self.ner_dict:
            self.ner_dict[lang] = {}

        if not cls in self.ner_dict[lang]:
            self.ner_dict[lang][cls] = {}

        nd = self.ner_dict[lang][cls]

        for i, entity in enumerate(entities):

            label = labels[i]

            for j, token in enumerate(tokenize(label, lang=lang)):

                if not token in nd:
                    nd[token] = {}

                if not entity in nd[token]:
                    nd[token][entity] = set([])

                nd[token][entity].add(j)

                # logging.debug ('ner_learn: %4d %s %s: %s -> %s %s' % (i, entity, label, token, cls, lang))

        cnt = 0
        for token in nd:
            # import pdb; pdb.set_trace()
            # s1 = repr(nd[token])
            # s2 = limit_str(s1, 10)
            logging.debug ('ner_learn: nd[%-20s]=%s' % (token, misc.limit_str(repr(nd[token]), 80)))
            cnt += 1
            if cnt > 10:
                break
 
    def ner(self, lang, cls, tstart, tend):

        if not lang in self.ner_dict:
            self.ner_dict[lang] = {}
        if not cls in self.ner_dict[lang]:
            self._ner_learn(lang, cls)

        nd     = self.ner_dict[lang][cls]
        tokens = tokenize(self.inp, lang=lang)

        #
        # start scoring
        #

        max_scores = {}

        for tstart in range (tstart-1, tstart+2):
            if tstart <0:
                continue

            for tend in range (tend-1, tend+2):
                if tend > len(tokens):
                    continue

                scores = {}

                for tidx in range(tstart, tend):

                    toff = tidx-tstart

                    # logging.debug('tidx: %d, toff: %d [%d - %d]' % (tidx, toff, tstart, tend))

                    token = tokens[tidx]
                    if not token in nd:
                        # logging.debug('token %s not in nd %s %s' % (repr(token), repr(lang), repr(cls)))
                        continue

                    for entity in nd[token]:

                        if not entity in scores:
                            scores[entity] = 0.0

                        for eidx in nd[token][entity]:
                            points = 2.0-abs(eidx-toff)
                            if points>0:
                                scores[entity] += points

                logging.debug('scores: %s' % repr(scores))

                for entity in scores:
                    if not entity in max_scores:
                        max_scores[entity] = scores[entity]
                        continue
                    if scores[entity]>max_scores[entity]:
                        max_scores[entity] = scores[entity]

        res = []
        cnt = 0

        # for entity in max_scores:

        for entity, max_score in sorted(max_scores.iteritems(), key=lambda x: x[1], reverse=True):

            res.append((entity, max_score))

            cnt += 1
            if cnt > MAX_NER_RESULTS:
                break

        return res


