#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016, 2017 Guenter Bartsch
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
# Zamia AI MQTT server
#
# can be used for chatbot-like applications (text-only)
# as well as full-blown speech i/o based home assistant type
# setups
#

# Text NLP Processing
# -------------------
# 
# * topic `ai/input/text`
# * payload (JSON encoded dict): 
#   * "utt"  : utterance to be processed 
#   * "lang" : language of utterance
#   * "user" : user who uttered the utterance
# 
# publishes:
#
# * topic `ai/response`
# * payload:
#   * "utt"     : utterance
#   * "intents" : intents
# 
# Example:
#
# hbmqtt_pub --url mqtt://dagobert -t ai/input/text -m '{"utt":"hello computer","lang":"en","user":"tux"}'

import os
import sys
import logging
import traceback
import json
import random
import time
import datetime
import dateutil
import wave
import struct

import paho.mqtt.client as mqtt
import numpy            as np

from optparse             import OptionParser
from threading            import RLock, Lock

from zamiaai              import model
from zamiaprolog.builtins import ASSERT_OVERLAY_VAR_NAME
from zamiaai.ai_kernal    import AIKernal
from aiprolog.runtime     import USER_PREFIX
from nltools              import misc
from nltools.tts          import TTS
from kaldisimple.nnet3    import KaldiNNet3OnlineDecoder

PROC_TITLE        = 'ai_mqtt'
AI_SERVER_MODULE  = '__server__'

AI_USER           = 'server' # FIXME: some sort of presence information maybe?
SAMPLE_RATE       = 16000
MAX_AUDIO_AGE     = 2        # seconds, ignore any audio input older than this
ATTENTION_SPAN    = 30       # seconds
AUDIO_EXTRA_DELAY = 0.5      # seconds
AUDIO_LOC_CNT     = 5        # seconds

TOPIC_INPUT_TEXT  = 'ai/input/text'
TOPIC_INPUT_AUDIO = 'ai/input/audio'
TOPIC_CONFIG      = 'ai/config'
TOPIC_RESPONSE    = 'ai/response'
TOPIC_INTENT      = 'ai/intent'
TOPIC_STATE       = 'ai/state'

DEFAULTS = {
            'broker_host'   : 'localhost',
            'broker_port'   : '1883',
            'broker_user'   : '',
            'broker_pw'     : '',
            'tts_host'      : 'local',
            'tts_port'      : 8300,
            'tts_locale'    : 'de',
            'tts_voice'     : 'de',
            'tts_engine'    : 'espeak',
           }

CLIENT_NAME = 'Zamia AI MQTT Server'

# state

do_listen       = True
do_asr          = True
attention       = 0
do_rec          = False
astr            = ''
hstr            = ''
audio_cnt       = 0
audio_loc       = None
audio_loc_cnt   = 0       # countdown audio location in case terminal dies and therefore fails to send finalize msg

# audio recording state

audiofn = ''   # path to current wav file being written
wf      = None # current wav file being written

#
# MQTT
#

def on_connect(client, userdata, flag, rc):
    if rc==0:
        logging.info("connected OK Returned code=%s" % repr(rc))
        client.subscribe(TOPIC_INPUT_TEXT)
        client.subscribe(TOPIC_INPUT_AUDIO)
        client.subscribe(TOPIC_CONFIG)
        client.subscribe(TOPIC_RESPONSE)
    else:
        logging.error("Bad connection Returned code=%s" % repr(rc))

def publish_state(client):

    global attention, hstr, astr, state_lock

    state_lock.acquire()
    try:
        data = {}

        data['attention'] = attention
        data['hstr']      = hstr
        data['astr']      = astr

        logging.debug ('publish_state: %s' % repr(data))
     
        client.publish(TOPIC_STATE, json.dumps(data))
    finally:
        state_lock.release()

def on_message(client, userdata, message):

    global kernal, lang, state_lock    
    global do_listen, do_asr, attention, do_rec
    global wf, vf_login, rec_dir, audiofn, hstr, astr, audio_cnt, audio_loc, audio_loc_cnt
    global ignore_audio_before, tts, tts_lock

    # logging.debug( "message received %s" % str(message.payload.decode("utf-8")))
    logging.debug( "message topic=%s" % message.topic)
    # logging.debug( "message qos=%s" % message.qos)
    # logging.debug( "message retain flag=%s" % message.retain)

    try:

        if message.topic == TOPIC_INPUT_AUDIO:

            data = json.loads(message.payload)

            audio       = data['pcm']
            do_finalize = data['final']
            loc         = data['loc']
            ts          = dateutil.parser.parse(data['ts'])
            
            # ignore old audio recordings that may have lingered in the message queue

            age = (datetime.datetime.now() - ts).total_seconds()
            if age > MAX_AUDIO_AGE:
                logging.debug ("   ignoring audio that is too old: %fs > %fs" % (age, MAX_AUDIO_AGE))
                return

            if ts < ignore_audio_before:
                logging.debug ("   ignoring audio that is ourselves talking: %s < %s" % (unicode(ts), unicode(ignore_audio_before)))
                return

            # we listen to one location at a time only (FIXME: implement some sort of session handling)

            if audio_loc and audio_loc != loc:
                logging.debug ("   ignoring audio from wrong location: %s" % loc)
                return

            if do_finalize:
                audio_loc     = None
            else:
                audio_loc     = loc
                audio_loc_cnt = AUDIO_LOC_CNT

            confidence  = 0.0

            audio_cnt += 1
            hstr = '.' * (audio_cnt/4)
            astr = ''

            if do_rec:

                # store recording in WAV format

                if not wf:

                    ds = datetime.date.strftime(datetime.date.today(), '%Y%m%d')
                    audiodirfn = '%s/%s-%s-rec/wav' % (rec_dir, vf_login, ds)
                    logging.debug('audiodirfn: %s' % audiodirfn)
                    misc.mkdirs(audiodirfn)

                    cnt = 0
                    while True:
                        cnt += 1
                        audiofn = '%s/de5-%03d.wav' % (audiodirfn, cnt)
                        if not os.path.isfile(audiofn):
                            break

                    logging.debug('audiofn: %s' % audiofn)

                    # create wav file 

                    wf = wave.open(audiofn, 'wb')
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(SAMPLE_RATE)

                packed_audio = struct.pack('%sh' % len(audio), *audio)
                wf.writeframes(packed_audio)

                if do_finalize:

                    hstr = audiofn
                    logging.debug('audiofn %s written.' % audiofn)

                    wf.close()  
                    wf = None

            else:
                audiofn = ''
                if do_finalize:
                        hstr = '***'

            if do_finalize:
                audio_cnt = 0


            if do_asr:
                decoder.decode(SAMPLE_RATE, np.array(audio, dtype=np.float32), do_finalize)

                if do_finalize:

                    hstr       = decoder.get_decoded_string()
                    confidence = decoder.get_likelihood()

                    # FIXME: remove debug code
                    # hstr = u'hallo computer'
                    # confidence = 1.0

                    logging.debug ( "*****************************************************************************")
                    logging.debug ( "**")
                    logging.debug ( "** %9.5f %s" % (confidence, hstr))
                    logging.debug ( "**")
                    logging.debug ( "*****************************************************************************")

                    if hstr:
                        
                        data = {}

                        data['lang'] = lang
                        data['utt']  = hstr
                        data['user'] = AI_USER
                     
                        client.publish(TOPIC_INPUT_TEXT, json.dumps(data))


            publish_state(client)
                
        elif message.topic == TOPIC_INPUT_TEXT:

            data = json.loads(message.payload)

            # print data

            utt      = data['utt']
            lang     = data['lang']
            user_uri = USER_PREFIX + data['user']

            if kernal.nlp_model.lang != lang:
                logging.warn('incorrect language for model: %s' % lang)
                return

            score, resps, actions, solutions = kernal.process_input(utt, kernal.nlp_model.lang, user_uri)

            # for idx in range (len(resps)):
            #     logging.debug('[%05d] %s ' % (score, u' '.join(resps[idx])))

            # if we have multiple responses, pick one at random

            do_publish = attention>0

            if len(resps)>0:

                idx = random.randint(0, len(resps)-1)

                # apply DB overlay, if any
                ovl = solutions[idx].get(ASSERT_OVERLAY_VAR_NAME)
                if ovl:
                    ovl.do_apply(AI_SERVER_MODULE, kernal.db, commit=True)

                state_lock.acquire()
                try:

                    # refresh attention span on each new interaction step
                    if attention>0:
                        attention = ATTENTION_SPAN

                    acts = actions[idx]
                    for action in acts:
                        logging.debug("ACTION %s" % repr(action))
                        if len(action) == 2 and action[0] == u'attention':
                            if action[1] == u'on':
                                attention = ATTENTION_SPAN
                            else:
                                attention = 1
                            do_publish = True

                    # FIXME: bug in audio/language model prevents "ok, computer"
                    if utt.strip() == u'hallo computer':
                        attention  = ATTENTION_SPAN
                        do_publish = True
                        logging.debug ('hello workaround worked: %s vs %s' % (repr(utt), repr(u'hallo computer')))

                finally:
                    state_lock.release()

                resp = resps[idx]
                logging.debug('RESP: [%05d] %s' % (score, u' '.join(resps[idx])))

                msg = {'utt': u' '.join(resp), 'score': score, 'lang': lang}

            else:
                logging.error(u'no solution found for input %s' % utt)

                # FIXME
                # logging.debug("ELIZA")
                # # abufs = kernal.do_eliza(line, kernal.nlp_model.lang, trace=False)
                # # abuf = random.choice(abufs)
                # # logging.debug("abuf: %s" % repr(abuf)) 

                msg = {'utt': u'', 'score': 0.0, 'lang': lang}
                acts = []

            if do_publish:
                (rc, mid) = client.publish(TOPIC_RESPONSE, json.dumps(msg))
                logging.debug("%s : %s" % (TOPIC_RESPONSE, json.dumps(msg)))
                for act in acts:
                    (rc, mid) = client.publish(TOPIC_INTENT, json.dumps(act))
                    logging.debug("%s : %s" % (TOPIC_INTENT, json.dumps(act)))

            # generate astr

            astr = msg['utt']
            if acts:
                if astr:
                    astr += ' - '
            for action in acts:
                astr += repr(action)

            publish_state(client)


        elif message.topic == TOPIC_RESPONSE:

            msg = json.loads(message.payload)

            if msg['utt']:

                tts_lock.acquire()
                try:
                    logging.debug('tts.say...')
                    tts.say(msg['utt'])
                    logging.debug('tts.say finished.')

                except:
                    logging.error('TTS EXCEPTION CAUGHT %s' % traceback.format_exc())
                finally:
                    tts_lock.release()

                ignore_audio_before = datetime.datetime.now() + datetime.timedelta(seconds=AUDIO_EXTRA_DELAY)

        elif message.topic == TOPIC_CONFIG:

            data = json.loads(message.payload)

            do_listen = data['listen']
            do_rec    = data['record']
            do_asr    = data['asr']


    except:
        logging.error('EXCEPTION CAUGHT %s' % traceback.format_exc())

#
# init
#

misc.init_app(PROC_TITLE)

#
# config, cmdline
#

config = misc.load_config('.airc', defaults = DEFAULTS)

broker_host         = config.get   ('mqtt', 'broker_host')
broker_port         = config.getint('mqtt', 'broker_port')
broker_user         = config.get   ('mqtt', 'broker_user')
broker_pw           = config.get   ('mqtt', 'broker_pw')

ai_model            = config.get   ('server', 'model')
lang                = config.get   ('server', 'lang')
vf_login            = config.get   ('server', 'vf_login')
rec_dir             = config.get   ('server', 'rec_dir')
kaldi_model_dir     = config.get   ('server', 'kaldi_model_dir')
kaldi_model         = config.get   ('server', 'kaldi_model')

tts_host            = config.get   ('tts',    'tts_host')
tts_port            = config.getint('tts',    'tts_port')
tts_locale          = config.get   ('tts',    'tts_locale')
tts_voice           = config.get   ('tts',    'tts_voice')
tts_engine          = config.get   ('tts',    'tts_engine')

#
# commandline
#

parser = OptionParser("usage: %prog [options]")

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")

parser.add_option ("-H", "--host", dest="host", type = "string", default=broker_host,
                   help="MQTT broker host, default: %s" % broker_host)

parser.add_option ("-p", "--port", dest="port", type = "int", default=broker_port,
                   help="MQTT broker port, default: %d" % broker_port)

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

#
# TTS
#

tts_lock = Lock()
tts = TTS (tts_host, tts_port, locale=tts_locale, voice=tts_voice, engine=tts_engine)
# this is used to ignore any voice input that is just us hearing ourselves 
# when answer is synthesized
ignore_audio_before = datetime.datetime.now()

#
# setup nlp kernal
#

kernal = AIKernal()
for mn2 in kernal.all_modules:
    kernal.load_module (mn2)
    kernal.init_module (mn2)
kernal.setup_tf_model ('decode', True, ai_model)

#
# ASR
#

logging.debug ('loading ASR model %s from %s...' % (kaldi_model, kaldi_model_dir))

start_time = time.time()

decoder = KaldiNNet3OnlineDecoder ( kaldi_model_dir, kaldi_model )

logging.debug ('ASR model loaded. took %fs' % (time.time() - start_time))

#
# state lock
#

state_lock = Lock()

#
# mqtt connect
#

logging.debug ('connecting to MQTT broker %s:%d ...' % (broker_host, broker_port))

client = mqtt.Client()
client.username_pw_set(broker_user, broker_pw)
client.on_message=on_message
client.on_connect=on_connect

connected = False
while not connected:
    try:

        client.connect(broker_host, port=broker_port, keepalive=10)

        connected = True

    except:
        logging.error('connection to %s:%d failed. retry in %d seconds...' % (broker_host, broker_port, RETRY_DELAY))
        time.sleep(RETRY_DELAY)

logging.debug ('connecting to MQTT broker %s:%d ... connected.' % (broker_host, broker_port))

#
# main loop - count down attention, publish state while >0
#

client.loop_start()
while True:

    state_lock.acquire()
    if attention>0:
        attention -= 1
        state_lock.release()
        try:
            publish_state(client)
        except:
            logging.error('EXCEPTION CAUGHT %s' % traceback.format_exc())
    else:
        state_lock.release()

    if audio_loc_cnt>0:
        audio_loc_cnt -= 1
        if audio_loc_cnt == 0:
            audio_loc = None

    time.sleep(1)

