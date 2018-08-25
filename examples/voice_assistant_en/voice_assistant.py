#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
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
# console voice assistant demo for Zamia AI
#

import sys
import logging
  
from optparse               import OptionParser
from zamiaai.ai_kernal      import AIKernal
from nltools                import misc
from nltools.vad            import VAD
from nltools.pulserecorder  import PulseRecorder
from nltools.pulseplayer    import PulsePlayer
from nltools.asr            import ASR
from nltools.tts            import TTS

PROC_TITLE          = 'voice_assistant'
LANG                = 'en'

DEFAULT_MIC_VOLUME  = 150
DEFAULT_ASR_MODEL   = '/opt/kaldi/model/kaldi-generic-en-tdnn_sp'

#
# init 
#

misc.init_app(PROC_TITLE)

#
# command line
#

parser = OptionParser("usage: %prog [options])")

parser.add_option("-a", "--asr-model", dest="asr_model", type = "str", default=DEFAULT_ASR_MODEL,
                  help="ASR model dir, default: %s" % DEFAULT_ASR_MODEL)

parser.add_option("-m", "--mic-volume", dest="mic_volume", type = "float", default=DEFAULT_MIC_VOLUME,
                  help="Microphone volume, default: %d%%" % DEFAULT_MIC_VOLUME)

parser.add_option("-v", "--verbose", action="store_true", dest="verbose", 
                  help="enable debug output")

(options, args) = parser.parse_args()

#
# logger
#

if options.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)
else:
    logging.basicConfig(level=logging.INFO)

#
# pulseaudio recorder
#

rec = PulseRecorder (volume=options.mic_volume)
logging.debug ('PulseRecorder initialized.')

#
# pulseaudio player
#

player = PulsePlayer('Zamia AI Voie Assistant')
logging.debug ('PulsePlayer initialized.')

#
# VAD
#

vad = VAD()
logging.debug ('VAD initialized.')

#
# setup AI DB, Kernal and Context
#

kernal = AIKernal.from_ini_file()
for skill in kernal.all_skills:
    kernal.consult_skill (skill)
kernal.setup_nlp_model()
ctx  = kernal.create_context()
logging.debug ('AI kernal initialized.')

#
# ASR
#

asr = ASR(model_dir = options.asr_model)
logging.debug ('ASR initialized.')

#
# TTS
#

tts = TTS(engine="espeak", voice="en")

#
# main loop
#

print(chr(27) + "[2J")
while True:

    #
    # record audio, run VAD
    #

    print "Please speak.",

    rec.start_recording()

    finalize  = False
    recording  = []

    while not finalize:

        samples = rec.get_samples()

        audio, finalize = vad.process_audio(samples)
        if not audio:
            continue

        recording.extend(audio)

        user_utt, confidence = asr.decode(audio, finalize)

        print "\r             \rYou: %s      " % user_utt,

        if finalize and not user_utt:
            finalize = False
            recording  = []

    logging.info ("conv_user: %s" % user_utt)

    rec.stop_recording()
    print

    # import pdb; pdb.set_trace()
    ai_utt, score, action = kernal.process_input(ctx, user_utt)

    print('AI : %s' % ai_utt)
    logging.info ("conv_ai   : %s" % ai_utt)

    if action:
        print('     %s' % repr(action))
        logging.info ("conv_action: %s" % repr(action))

    if ai_utt:
        tts.say(ai_utt)

    print
