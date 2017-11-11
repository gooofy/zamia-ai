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
# ncurses based debugging application for Zamia AI
#
# allows for interactive testing of AI-Prolog (modules) as well as Speech
# recognition
#

import os
import sys
import traceback
import codecs
import logging
import random
import time
import curses
import curses.textpad
import locale
import wave
import struct
import json
import datetime
import dateutil
import paho.mqtt.client as mqtt

from optparse               import OptionParser
from StringIO               import StringIO
from threading              import Lock, Condition
from zamiaprolog.builtins   import ASSERT_OVERLAY_VAR_NAME
from zamiaprolog.logic      import Predicate, Clause
from zamiaprolog.logicdb    import LogicDB
from zamiaprolog.runtime    import PROLOG_LOGGER_NAME
from zamiaprolog.errors     import PrologError, PrologRuntimeError
from aiprolog.runtime       import USER_PREFIX
from zamiaai.ai_kernal      import AIKernal
from zamiaai                import model
from nltools                import misc
from nltools.vad            import VAD, BUFFER_DURATION
from nltools.pulserecorder  import PulseRecorder
from nltools.pulseplayer    import PulsePlayer
from nltools.tokenizer      import tokenize
from nltools.asr            import ASR, ASR_ENGINE_NNET3


PROC_TITLE        = 'ai_dbg'
AI_USER           = 'dbg'
AI_MODULE         = '__dbg__'
USER_URI          = USER_PREFIX + AI_USER
SAMPLE_RATE       = 16000
FRAMES_PER_BUFFER = SAMPLE_RATE * BUFFER_DURATION / 1000
TOPIC_INPUT_AUDIO = 'ai/input/audio'
MQTT_LOCATION     = 'livingroom'
MAX_AUDIO_AGE     = 2        # seconds, ignore any audio input older than this

hstr       = u''
prompt     = u''
inp        = None
responses  = []
recording  = []

match_module   = 'personality'
match_loc_fn   = None
match_loc_line = None

cur_context    = None

def on_connect(client, userdata, flag, rc):
    if rc==0:
        logging.info("connected OK Returned code=%s" % repr(rc))
        client.subscribe(TOPIC_INPUT_AUDIO)
    else:
        logging.error("Bad connection Returned code=%s" % repr(rc))

def on_message(client, userdata, message):

    global mqtt_listen, mqtt_finalize, mqtt_audio, mqtt_cond

    # logging.debug( "message received %s" % str(message.payload.decode("utf-8")))
    logging.debug( "message topic=%s" % message.topic)
    # logging.debug( "message qos=%s" % message.qos)
    # logging.debug( "message retain flag=%s" % message.retain)

    mqtt_cond.acquire()

    try:

        if message.topic == TOPIC_INPUT_AUDIO:

            if not mqtt_listen:
                logging.debug ('ignoring audio: not listening.')
                return

            data = json.loads(message.payload)

            mqtt_audio    = data['pcm']
            mqtt_finalize = data['final']
            loc           = data['loc']
            ts            = dateutil.parser.parse(data['ts'])
            
            # ignore old audio recordings that may have lingered in the message queue

            age = (datetime.datetime.now() - ts).total_seconds()
            if age > MAX_AUDIO_AGE:
                # logging.debug ("   ignoring audio that is too old: %fs > %fs" % (age, MAX_AUDIO_AGE))
                logging.debug ('ignoring audio: too old.')
                return

            # ignore audio from wrong location
            if loc != MQTT_LOCATION:
                logging.debug ('ignoring audio: wrong location %s vs %s.' % (repr(loc), repr(MQTT_LOCATION)))
                return

            logging.debug ('mqtt_cond.notify_all()')
            mqtt_cond.notify_all()

    except:
        logging.error('EXCEPTION CAUGHT %s' % traceback.format_exc())
    finally:
        mqtt_cond.release()

def do_rec():

    global rec, stdscr, loc, hstr, prompt, recording, asr, options, mqtt_finalize, mqtt_cond, mqtt_audio, mqtt_listen

    logging.debug ('do_rec...')

    time.sleep(0.1)

    recording = []
    swin = misc.message_popup(stdscr, 'Recording...', 'Please speak now.')

    if options.mqtt:

        mqtt_cond.acquire()
        try:
            mqtt_finalize = False
            mqtt_listen   = True
            while not mqtt_finalize:
                mqtt_cond.wait()

                logging.debug ('do_rec... got audio from mqtt')
                recording.extend(mqtt_audio)

                hstr, confidence = asr.decode(SAMPLE_RATE, mqtt_audio, mqtt_finalize, stream_id=MQTT_LOCATION)

            logging.debug ('do_rec... mqtt listen loop done')
            mqtt_listen   = False
        finally:
            mqtt_cond.release()

    else:

        rec.start_recording(FRAMES_PER_BUFFER)

        finalize  = False

        while not finalize:

            samples = rec.get_samples()

            audio, finalize = vad.process_audio(samples)
            if not audio:
                continue

            recording.extend(audio)

            hstr, confidence = asr.decode(SAMPLE_RATE, audio, finalize, stream_id=loc)

        rec.stop_recording()

    prompt = hstr

    stdscr.refresh()
    swin = misc.message_popup(stdscr, 'Processing input...', prompt)

    do_process_input()

def do_process_input():

    global stdscr, prompt, cur_context, next_context, lang, inp, responses, kernal
    global match_module, match_loc_fn, match_loc_line

    next_res, next_context = kernal._setup_context ( user          = USER_URI, 
                                                     lang          = lang, 
                                                     inp           = tokenize(prompt, lang=lang),
                                                     prev_context  = cur_context,
                                                     prev_res      = {})

    inp = kernal._compute_net_input (next_res, next_context)

    #
    # see if this input sequence is already covered by our training data
    #

    responses      = []
    match_loc_fn   = None
    match_loc_line = None
    highscore      = 0.0

    for tdr in kernal.session.query(model.TrainingData).filter(model.TrainingData.lang  == lang,
                                                               model.TrainingData.inp   == json.dumps(inp)):

        acode     = json.loads (tdr.resp)
        pcode     = kernal._reconstruct_prolog_code (acode)
        clause    = Clause (None, pcode, location=kernal.dummyloc)
        solutions = kernal.rt.search (clause, env=next_res)

        for solution in solutions:

            actual_out, actual_actions, score = kernal._extract_response (next_context, solution)

            if score > highscore:
                responses = []
                highscore = score

            if score < highscore:
                continue

            responses.append ((pcode, actual_out, actual_actions, score, solution))

            match_module   = tdr.module
            match_loc_fn   = tdr.loc_fn
            match_loc_line = tdr.loc_line

def do_apply_solution (sidx):

    global stdscr, responses, kernal, cur_context, next_context

    if sidx >= len(responses):
        misc.message_popup(stdscr, 'Error', 'Solution #%d does not exist.' % sidx)
        stdscr.getch()
        return

    # apply DB overlay, if any
    ovl = responses[sidx][4].get(ASSERT_OVERLAY_VAR_NAME)
    if ovl:
        ovl.do_apply(AI_MODULE, kernal.db, commit=True)

    responses = []
    cur_context = next_context

def do_clear_context ():

    global cur_context, prompt

    cur_context = None

    if prompt:
        do_process_input()


def do_playback():

    global recording, buf

    buf = StringIO()

    wf = wave.open(buf, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)

    packed_audio = struct.pack('%sh' % len(recording), *recording)
    wf.writeframes(packed_audio)

    player.play(buf.getvalue())

    buf.close()

def do_edit_prompt():

    global stdcr, prompt

    prompt = misc.edit_popup(stdscr, ' Prompt ', prompt)

    do_process_input()

def do_change_module():

    global stdcr, match_module

    match_module = misc.edit_popup(stdscr, ' Module ', match_module)

def do_align_module():

    global stdscr, match_module, kernal, prompt, lang

    misc.message_popup(stdscr, 'Align...', 'Matching prompt against existing utterances...')
    matches = kernal.align_utterances(lang=lang, utterances=[prompt])

    msg = u''

    for i, res in enumerate(matches[prompt]):
        sim, loc, utt = res
        msg += u'%d %s\n   %s\n\n' % (i, loc, utt)
        if i==4:
            break

    msg += 'Please select 0-%d >' % i

    stdscr.refresh()
    misc.message_popup(stdscr, 'Alignment Results', msg)

    while True:
        c = stdscr.getch()
        if c == ord('0'):
            match_location = matches[prompt][0][1]
            break    
        if c == ord('1'):
            match_location = matches[prompt][1][1]
            break    
        if c == ord('2'):
            match_location = matches[prompt][2][1]
            break    
        if c == ord('3'):
            match_location = matches[prompt][3][1]
            break    
        if c == ord('4'):
            match_location = matches[prompt][4][1]
            break    

    match_module = match_location.split(':')[0]

def do_help():

    global stdscr

    misc.message_popup(stdscr, 'Help', """
    simple question - response:

    "what are you called?",
    "I am called HAL 9000".

    context, patterns, variables::

    context(topic, wdeProgrammingLanguage),
    "what are you called (by the way|again|)?",
    or ( "I am called {self:rdfsLabel|en, s}",
         "My name is {self:rdfsLabel|en, s}").
    """)

    c = stdscr.getch()

def do_save_audio ():

    global prompt, vf_login, rec_dir, recording, stdscr

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

    packed_audio = struct.pack('%sh' % len(recording), *recording)
    wf.writeframes(packed_audio)
    wf.close()  

    # append etc/prompts-original file

    etcdirfn = '%s/%s-%s-rec/etc' % (rec_dir, vf_login, ds)
    logging.debug('etcdirfn: %s' % etcdirfn)
    misc.mkdirs(etcdirfn)

    promptsfn = '%s/prompts-original' % etcdirfn
    with codecs.open(promptsfn, 'a') as promptsf:
        promptsf.write('de5-%03d %s\n' % (cnt, prompt))

    misc.message_popup(stdscr, 'WAVE file written', audiofn)

    stdscr.getch()

#
# main curses interface
#

FILTER_HEADS=set([ 'c_say', 'c_score', 'lang', 'prev', 'time', 'tokens', 'user' ])

def paint_main():

    global stdscr, hstr, responses, prompt, inp, cur_context, kernal
    global match_module, match_loc_fn, match_loc_line

    stdscr.clear()

    my, mx = stdscr.getmaxyx()

    for x in range(mx):
        stdscr.insstr(   0, x, ' ', curses.A_REVERSE)
        stdscr.insstr(my-2, x, ' ', curses.A_REVERSE)
        stdscr.insstr(my-1, x, ' ', curses.A_REVERSE)

    # header

    # s = u"%2d/%2d %-30s QTY: %d" % (cur_ts+1, len(edit_ts), ts['cfn'], ts['quality'])

    # stdscr.insstr(0, 0, s.encode('utf8'), curses.A_BOLD | curses.A_REVERSE )
    stdscr.insstr(0, mx-17, 'Zamia AI Debugger', curses.A_REVERSE)

    # body

    stdscr.insstr(2, 2, 'ASR Result: (R:Record, P:Playback)', curses.A_DIM)
    stdscr.insstr(3, 4, hstr.encode('utf8'), curses.A_BOLD)

    stdscr.insstr(5, 2, 'Prompt: (E:Edit)', curses.A_DIM)
    stdscr.insstr(6, 4, prompt.encode('utf8'), curses.A_BOLD)

    stdscr.insstr(8, 2, 'Net Input:', curses.A_DIM)
    stdscr.insstr(9, 4, repr(inp), curses.A_BOLD)

    y = 11
    if match_loc_fn:
        stdscr.insstr(y, 2, 'Covered in: %s %s:%d' % (match_module, match_loc_fn, match_loc_line), curses.A_DIM)
        y += 1
        i = 0
        for pcode, actual_out, actual_actions, score, solution in responses:
            # stdscr.insstr(y, 2, '%s' % (repr(pcode)), curses.A_DIM)
            stdscr.insstr(y, 4, '%2d %5.1f %s %s' % (i, score, u' '.join(actual_out), repr(actual_actions)), curses.A_BOLD)
            y += 1

            ovl = solution.get(ASSERT_OVERLAY_VAR_NAME)
            if ovl:
                for k in sorted(ovl.d_retracted):
                    for p in ovl.d_retracted[k]:
                        stdscr.insstr(y, 7, '-%s' % unicode(p))
                        y+=1
                for k in sorted(ovl.d_assertz):
                    for clause in ovl.d_assertz[k]:
                        if clause.head.name in FILTER_HEADS:
                            continue
                        stdscr.insstr(y, 7, '+%s' % unicode(clause))
                        y+=1

            i += 1
    else:
        stdscr.insstr(y, 2, 'Not covered by DB. Current module (M:Change Module):', curses.A_DIM)
        y += 1
        stdscr.insstr(y, 4, '%s' % match_module, curses.A_BOLD)
        y += 1


    # context

    if cur_context:

        y = 2
        stdscr.insstr(y, 80, '%s: (C:Clear Context)' % cur_context.name, curses.A_DIM)
        y += 1

        s1s = kernal.rt.search_predicate ('context', [cur_context, '_1', '_2'], env={})
        for s1 in s1s:
            stdscr.insstr(y, 80, '%s is %s' % (s1['_1'], s1['_2']), curses.A_BOLD)
            y += 1
        y += 1

        stdscr.insstr(y, 80, 'Mem:', curses.A_DIM)
        y += 1

        s1s = kernal.rt.search_predicate ('mem', [cur_context, '_1', '_2'], env={})
        for s1 in s1s:
            stdscr.insstr(y, 80, '%s is %s' % (s1['_1'], s1['_2']), curses.A_BOLD)
            y += 1


    # footer

    stdscr.insstr(my-2, 0,     " R:Record   E:Prompt   P:Playback   S:Save Audio        ", curses.A_REVERSE )
    stdscr.insstr(my-1, 0,     " Module: M:Change   A:Align                             ", curses.A_REVERSE )
    stdscr.insstr(my-2, mx-40, " 0-9:Apply Solution   C:Clear Context   ", curses.A_REVERSE )
    stdscr.insstr(my-1, mx-40, "                         H:Help  Q:Quit ", curses.A_REVERSE )
    stdscr.refresh()

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

parser.add_option("-m", "--mqtt", action="store_true", dest="mqtt", 
                  help="listen for audio from mqtt bus instead of local pulseaudio")

parser.add_option("-v", "--verbose", action="store_true", dest="verbose", 
                  help="enable debug output")

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)
else:
    logging.basicConfig(level=logging.INFO)

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

broker_host                    = config.get      ('mqtt', 'broker_host')
broker_port                    = config.getint   ('mqtt', 'broker_port')
broker_user                    = config.get      ('mqtt', 'broker_user')
broker_pw                      = config.get      ('mqtt', 'broker_pw')

#
# curses
#

locale.setlocale(locale.LC_ALL,"")

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

try:

    paint_main()

    if options.mqtt:
        #
        # mqtt connect
        #

        logging.debug ('connection to MQTT broker %s:%d ...' % (broker_host, broker_port))

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

        logging.debug ('connection to MQTT broker %s:%d ... connected.' % (broker_host, broker_port))

        mqtt_listen = False
        mqtt_cond   = Condition()

        client.loop_start()

    else:

        #
        # pulseaudio recorder
        #

        misc.message_popup(stdscr, 'Initializing...', 'Init Pulseaudio Recorder...')
        rec = PulseRecorder (source, SAMPLE_RATE, volume)
        paint_main()
        logging.debug ('PulseRecorder initialized.')

    #
    # pulseaudio player
    #

    misc.message_popup(stdscr, 'Initializing...', 'Init Pulseaudio Player...')
    player = PulsePlayer('Zamia AI Debugger')
    paint_main()
    logging.debug ('PulsePlayer initialized.')

    #
    # VAD
    #

    misc.message_popup(stdscr, 'Initializing...', 'Init VAD...')
    vad = VAD(aggressiveness=aggressiveness, sample_rate=SAMPLE_RATE)
    paint_main()
    logging.debug ('VAD initialized.')

    #
    # setup AI Kernal
    #

    misc.message_popup(stdscr, 'Initializing...', 'Init AI Kernal...')
    db     = LogicDB(db_url)
    kernal = AIKernal(db=db, all_modules=all_modules, load_all_modules=True)
    # kernal.setup_tf_model (mode='decode', load_model=True, ini_fn=ai_model)
    # kernal.setup_align_utterances(lang=lang)
    paint_main()
    logging.debug ('AI kernal initialized.')

    #
    # context
    #

    cur_context = kernal.find_prev_context(USER_URI)

    #
    # ASR
    #

    misc.message_popup(stdscr, 'Initializing...', 'Init ASR...')
    asr = ASR(engine = ASR_ENGINE_NNET3, model_dir = kaldi_model_dir, model_name = kaldi_model,
              kaldi_beam = kaldi_beam, kaldi_acoustic_scale = kaldi_acoustic_scale,
              kaldi_frame_subsampling_factor = kaldi_frame_subsampling_factor)
    paint_main()
    logging.debug ('ASR initialized.')

    #
    # main loop
    #

    while True:
    
        paint_main()

        c = stdscr.getch()
        if c == ord('q'):
            break  
        elif c == ord('r'):
            do_rec()
        elif c == ord('p'):
            do_playback()
        elif c == ord('e'):
            do_edit_prompt()
        elif c == ord('m'):
            do_change_module()
        elif c == ord('a'):
            do_align_module()
        elif c == ord('h'):
            do_help()
        elif c >= ord('0') and c <= ord('9'):
            do_apply_solution(c - ord('0'))
        elif c == ord('c'):
            do_clear_context()
        elif c == ord('s'):
            do_save_audio()

except:
    logging.error('EXCEPTION CAUGHT %s' % traceback.format_exc())

finally:

    logging.info('resetting curses...')

    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()

