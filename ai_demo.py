#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017 Guenter Bartsch
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
# console demo for Zamia AI with speech recognition
#

import os
import sys
import traceback
import logging
import random
import datetime
import wave
import struct
import codecs
 
from optparse               import OptionParser
from zamiaprolog.builtins   import ASSERT_OVERLAY_VAR_NAME
from zamiaprolog.logicdb    import LogicDB
from aiprolog.runtime       import USER_PREFIX
from zamiaai.ai_kernal      import AIKernal
from nltools                import misc
from nltools.vad            import VAD, BUFFER_DURATION
from nltools.pulserecorder  import PulseRecorder
from nltools.pulseplayer    import PulsePlayer
from nltools.tokenizer      import tokenize
from nltools.asr            import ASR, ASR_ENGINE_NNET3

PROC_TITLE        = 'ai_demo'
AI_USER           = 'demo'
AI_MODULE         = '__demo__'
USER_URI          = USER_PREFIX + AI_USER
SAMPLE_RATE       = 16000
FRAMES_PER_BUFFER = SAMPLE_RATE * BUFFER_DURATION / 1000
LOG_FILE          = 'tmp/demo.log'

#
# init 
#

misc.init_app(PROC_TITLE)

#
# command line
#

parser = OptionParser("usage: %prog [options])")

parser.add_option("-l", "--lang", dest="lang", type = "str", default='de',
                  help="language (default: de)")

parser.add_option("-r", "--record", action="store_true", dest="record_audio", 
                  help="record audio")

parser.add_option("-v", "--verbose", action="store_true", dest="verbose", 
                  help="enable debug output")

(options, args) = parser.parse_args()

#
# logger
#

logging.basicConfig( filename = LOG_FILE,
                     filemode = 'a',
                     level = logging.INFO,
                     format = '%(asctime)s - %(levelname)s: %(message)s')
if options.verbose:
    # logging.basicConfig(level=logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)

#
# config
#

config = misc.load_config('.airc')

ai_model                       = config.get      ('server', 'model')
lang                           = config.get      ('server', 'lang')
vf_login                       = config.get      ('server', 'vf_login')
rec_dir                        = config.get      ('server', 'rec_dir')
kaldi_model_dir                = config.get      ('server', 'kaldi_model_dir')
kaldi_model                    = config.get      ('server', 'kaldi_model')
kaldi_acoustic_scale           = config.getfloat ('server', 'kaldi_acoustic_scale') 
kaldi_beam                     = config.getfloat ('server', 'kaldi_beam') 
kaldi_frame_subsampling_factor = config.getint   ('server', 'kaldi_frame_subsampling_factor') 
all_modules                    = list(map (lambda m: m.strip(), config.get('semantics', 'modules').split(',')))
db_url                         = config.get      ('db', 'url')

loc                            = config.get      ('vad',    'loc')
source                         = config.get      ('vad',    'source')
volume                         = config.getint   ('vad',    'volume')
aggressiveness                 = config.getint   ('vad',    'aggressiveness')

#
# pulseaudio recorder
#

rec = PulseRecorder (source, SAMPLE_RATE, volume)
logging.debug ('PulseRecorder initialized.')

#
# pulseaudio player
#

player = PulsePlayer('Zamia AI Debugger')
logging.debug ('PulsePlayer initialized.')

#
# VAD
#

vad = VAD(aggressiveness=aggressiveness, sample_rate=SAMPLE_RATE)
logging.debug ('VAD initialized.')

#
# setup AI DB, Kernal and Context
#

db     = LogicDB(db_url)
kernal = AIKernal(db=db, all_modules=all_modules, load_all_modules=True)
kernal.setup_tf_model (mode='decode', load_model=True, ini_fn=ai_model)
current_ctx = kernal.find_prev_context(USER_URI)
logging.debug ('AI kernal initialized.')

#
# ASR
#

asr = ASR(engine = ASR_ENGINE_NNET3, model_dir = kaldi_model_dir, model_name = kaldi_model,
          kaldi_beam = kaldi_beam, kaldi_acoustic_scale = kaldi_acoustic_scale,
          kaldi_frame_subsampling_factor = kaldi_frame_subsampling_factor)
logging.debug ('ASR initialized.')

#
# main loop
#


while True:

    #
    # record audio, run VAD
    #

    print "Please speak.",

    rec.start_recording(FRAMES_PER_BUFFER)

    finalize  = False
    recording  = []

    while not finalize:

        samples = rec.get_samples()

        audio, finalize = vad.process_audio(samples)
        if not audio:
            continue

        recording.extend(audio)

        hstr, confidence = asr.decode(SAMPLE_RATE, audio, finalize, stream_id=loc)

        print "\r             \rYou: %s      " % hstr,

        if finalize and not hstr:
            finalize = False
            recording  = []

    logging.info ("conv_hstr: %s" % hstr)

    rec.stop_recording()
    print

    score, resps, actions, solutions, current_ctx = kernal.process_input(hstr, kernal.nlp_model.lang, USER_URI, prev_ctx=current_ctx)

    for idx in range (len(resps)):
        logging.debug('[%05d] %s ' % (score, u' '.join(resps[idx])))

    # if we have multiple responses, pick one at random

    if len(resps)>0:

        idx = random.randint(0, len(resps)-1)

        # apply DB overlay, if any
        ovl = solutions[idx].get(ASSERT_OVERLAY_VAR_NAME)
        if ovl:
            ovl.do_apply(AI_MODULE, kernal.db, commit=True)

        resp = resps[idx]
        print('AI : %s' % u' '.join(resps[idx]))

        logging.info ("conv_resp: %s" % u' '.join(resps[idx]))

        for act in actions[idx]:
            print('     %s' % repr(act))
            logging.info ("conv_action: %s" % repr(act))

    print

    #
    # save audio recording, if requested
    #

    if options.record_audio:

        ds = datetime.date.strftime(datetime.date.today(), '%Y%m%d')
        audiodirfn = '%s/%s-%s-rec/wav' % (rec_dir, vf_login, ds)
        misc.mkdirs(audiodirfn)

        cnt = 0
        while True:
            cnt += 1
            audiofn = '%s/de5-%03d.wav' % (audiodirfn, cnt)
            if not os.path.isfile(audiofn):
                break

        # create wav file 

        wf = wave.open(audiofn, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)

        packed_audio = struct.pack('%sh' % len(recording), *recording)
        wf.writeframes(packed_audio)
        wf.close()  

        # append etc/prompts-original file

        etcdirfn = '%s/%s-%s-rec/etc' % (rec_dir, vf_login, ds)
        misc.mkdirs(etcdirfn)

        promptsfn = '%s/prompts-original' % etcdirfn
        with codecs.open(promptsfn, 'a') as promptsf:
            promptsf.write('de5-%03d %s\n' % (cnt, hstr))

        logging.info('conv_recording saved to %s' % audiofn)

