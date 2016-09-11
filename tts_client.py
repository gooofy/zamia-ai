#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016 Guenter Bartsch
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

import traceback
import json
import zmq
import utils
from base64 import b64encode
import logging

MARY_VOICES = {

    'en_US': { 'male':   [ "cmu-rms-hsmm", "dfki-spike", "dfki-obadiah", "dfki-obadiah-hsmm", "cmu-bdl-hsmm"],
               'female': [ "cmu-slt-hsmm", "dfki-poppy", "dfki-poppy-hsmm", "dfki-prudence", "dfki-prudence-hsmm" ]
             },

    'de_DE': { 'male':   ["bits3", "bits3-hsmm", "dfki-pavoque-neutral", "dfki-pavoque-neutral-hsmm", "dfki-pavoque-styles"],
               'female': ["bits1-hsmm"]
             }
    }

ESPEAK_VOICES = ['en', 'de']

class TTSClient(object):

    def __init__(self, server, port, locale='en_US', engine='mary', voice='cmu-rms-hsmm'):

        #
        # zmq connection to tts server
        #

        self.context = zmq.Context()
        logging.debug ("Connecting to TTS server %s:%s ..." % (server, port))
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect ("tcp://%s:%s" % (server, port))

        logging.debug("conntected.")

        self.locale   = locale
        self.engine = engine
        self.voice  = voice

    def set_locale(self, locale):
        self.locale = locale

    def set_voice(self, voice):
        self.voice = voice

    def set_engine(self, engine):
        self.engine = engine

    def _comm (self, cmd, arg):

        # logging.debug("tts_comm: %s %s" % (cmd, arg))

        res = None

        try:

            rq = json.dumps ([cmd, arg])

            #print "Sending request %s" % rq
            self.socket.send (rq)

            #  Get the reply.
            message = self.socket.recv()
            res = json.loads(message)
        except:

            logging.error("tts_comm: EXCEPTION.")
            traceback.print_exc()

            pass

        return res

    def say (self, txt):

        self._comm('say', [self.locale, self.voice, self.engine, 'txt', txt])

    def say_ipa (self, ipa):

        self._comm('say', [self.locale, self.voice, self.engine, 'ipa', ipa])

    def gen_ipa (self, word):

        return self._comm('gen_ipa', [self.locale, self.voice, self.engine, word])

    def play_wav (self, wav):

        self._comm('play_wav', b64encode(wav))

if __name__ == "__main__":

    config = utils.load_config()

    host = config.get('tts', 'host')
    port = int(config.get('tts', 'port'))

    tts = TTSClient (host, port, locale='de', voice='bits3')

    # test mary

    tts.say ('hallo welt!')
    tts.say_ipa (u'ʔap-ʃpiːl-gə-ʁɛː-tə')

    print "IPA from mary:", tts.gen_ipa (u'klimaanlage')

    # test espeak

    tts.set_engine('espeak')
    tts.set_voice('de')
    tts.say ('hallo welt!')

    tts.say_ipa (u'ʔap-ʃpiːl-gə-ʁɛː-tə')

    print "IPA from espeak:", tts.gen_ipa (u'klimaanlage')

