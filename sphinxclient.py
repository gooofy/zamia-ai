#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import re
import os
import StringIO
import ConfigParser
from os.path import expanduser
import random
import datetime
import locale
import traceback
import wave
from time import sleep

import pocketsphinx

# DECODE_CHUNK_LEN = 2048 * 2
DECODE_CHUNK_LEN = 1024

class SphinxClient(object):

    def __init__ (self, hmdir, dictf, kws=None, lm=None):

        config = pocketsphinx.Decoder.default_config()
         
        config.set_string('-hmm', hmdir)
        config.set_string('-dict', dictf)
        if kws:
            config.set_string('-kws', kws) 
            config.set_float ('-kws_threshold', 1e-9)
        if lm:
            config.set_string('-lm', lm) 

        config.set_string('-logfn', "/dev/null")
        
        # config.set_float ('-lw', 10) 
        # config.set_string('-feat', '1s_c_d_dd')
        # config.set_float ('-beam', 1e-80)
        # config.set_float ('-wbeam', 1e-40)
        # config.set_float ('-wip', 0.2) 
        # config.set_string('-agc', 'none')
        # config.set_string('-varnorm', 'no') 
        # config.set_string('-cmn', 'current')

        self.decoder = pocketsphinx.Decoder(config)

    def decode (self, buf):

        self.decoder.start_utt()

        offset      = 0

        while offset < len(buf):

            n = DECODE_CHUNK_LEN
            if offset + n > len(buf):
                n = len(buf) - offset

            subbuf = buf[offset:offset+n]

            # print "decoding %d at offset %d" % (len(subbuf), offset)

            self.decoder.process_raw(subbuf, False, False)

            offset += n

        self.decoder.end_utt()

        hypothesis = self.decoder.hyp()
        hstr       = hypothesis.hypstr
        logmath    = self.decoder.get_logmath()

        confidence = logmath.exp(hypothesis.prob)

        # print 'Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", confidence
        # print 'Best hypothesis segments: ', [seg.word for seg in self.decoder.seg()]

        return confidence, hstr


    # def decode_old (self, buf):

    #     #self.decoder.start_utt('sphinx')
    #     self.decoder.start_utt()

    #     offset      = 0
    #     utt_started = False
    #     hypothesis  = None
    #     hstr        = None

    #     while offset < len(buf):

    #         #print "decoding at offset %d" % offset

    #         n = DECODE_CHUNK_LEN
    #         if offset + n > len(buf):
    #             n = len(buf) - offset

    #         self.decoder.process_raw(buf[offset:offset+n], False, False)
    #         in_speech = self.decoder.get_in_speech()
    #         #print "  in_speech: %s" % repr(in_speech)

    #         if in_speech and  not utt_started:
    #             utt_started = True;
    #         if not in_speech and utt_started:
    #             self.decoder.end_utt()
    #             hypothesis = self.decoder.hyp()
    #             #self.decoder.start_utt('sphinx')
    #             self.decoder.start_utt()
    #             utt_started = False

    #             if hypothesis:
    #                 #print type(hypothesis)
    #                 hstr = hypothesis.hypstr.decode('UTF8').lstrip().rstrip()
    #                 break

    #         offset += n

    #     self.decoder.end_utt()

    #     return hypothesis, hstr

