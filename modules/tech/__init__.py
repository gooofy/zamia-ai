#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import logging
from base.ner import ner_learn

DEPENDS    = [ 'base', 'config', 'humans' ]

AIP_SOURCES = [
               'tech.aip',
              ]

def init_module(kernal):

    # import pdb; pdb.set_trace()

    logging.info ('tech NER training ...')

    for lang in ['en', 'de']:

        # operating systems

        # ner_learn_operating_systems(LANG) :- 
        #     operating_system_category(CAT), 
        #     wdpdInstanceOf(OS, CAT),
        #     rdfsLabel(OS, LANG, LABEL),
        #     ner_learn(LANG, operating_system, OS, LABEL).

        for cat in ['wdeMultiTaskingOperatingSystem', 'wdeOperatingSystem']:
            s1s = kernal.rt.search_predicate('wdpdInstanceOf', ['OS', cat])
            for s1 in s1s:
                s2s = kernal.rt.search_predicate('rdfsLabel', [s1['OS'], lang, 'L'])
                for s2 in s2s:
                    ner_learn (lang, 'operating_system', [s1['OS'].name], [s2['L'].s])

        # home computers
        # ner_learn_home_computers(LANG) :- 
        #     wdpdInstanceOf(HOME_COMPUTER, wdeHomeComputer),
        #     rdfsLabel(HOME_COMPUTER, LANG, LABEL),
        #     ner_learn(LANG, home_computer, HOME_COMPUTER, LABEL).

        for cat in ['wdeHomeComputer']:
            s1s = kernal.rt.search_predicate('wdpdInstanceOf', ['H', cat])
            for s1 in s1s:
                s2s = kernal.rt.search_predicate('rdfsLabel', [s1['H'], lang, 'L'])
                for s2 in s2s:
                    ner_learn (lang, 'home_computer', [s1['H'].name], [s2['L'].s])

        # programming languages
        # ner_learn_programming_languages(LANG) :- 
        #     wdpdInstanceOf(L, wdeProgrammingLanguage),
        #     rdfsLabel(L, LANG, LABEL),
        #     ner_learn(LANG, programming_language, L, LABEL).

        for cat in ['wdeProgrammingLanguage1']:
            s1s = kernal.rt.search_predicate('wdpdInstanceOf', ['L', cat])
            for s1 in s1s:
                s2s = kernal.rt.search_predicate('rdfsLabel', [s1['L'], lang, 'L'])
                for s2 in s2s:
                    ner_learn (lang, 'programming_language', [s1['L'].name], [s2['L'].s])

    logging.info ('tech NER training ... done.')

