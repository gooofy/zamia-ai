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
# ncurses based training application for Zamia AI
#
# allowes for interactive generation of training data for
# AI-Prolog (modules) as well as Speech recognition
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

from optparse               import OptionParser
from StringIO               import StringIO
from zamiaprolog.builtins   import ASSERT_OVERLAY_VAR_NAME
from zamiaprolog.logic      import Predicate, Clause
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


PROC_TITLE        = 'ai_trainer'
AI_USER           = 'trainer'
AI_MODULE         = '__trainer__'
USER_URI          = USER_PREFIX + AI_USER
SAMPLE_RATE       = 16000
FRAMES_PER_BUFFER = SAMPLE_RATE * BUFFER_DURATION / 1000

hstr       = u''
prompt     = u''
inp        = None
responses  = []
recording  = []

match_module   = 'personality'
match_loc_fn   = None
match_loc_line = None

prev_context   = None
res            = {}

def do_rec():

    global rec, stdscr, loc, hstr, prompt, recording

    logging.debug ('do_rec...')

    time.sleep(0.1)

    rec.start_recording(FRAMES_PER_BUFFER)

    finalize  = False
    recording = []

    swin = misc.message_popup(stdscr, 'Recording...', 'Please speak now.')

    while not finalize:

        samples = rec.get_samples()

        audio, finalize = vad.process_audio(samples)
        if not audio:
            continue

        recording.extend(audio)

        hstr, confidence = kernal.asr_decode(loc, SAMPLE_RATE, audio, finalize)

    rec.stop_recording()

    prompt = hstr

    do_process_input()

def do_process_input():

    global stdscr, prompt, res, prev_context, lang, inp, responses, kernal
    global match_module, match_loc_fn, match_loc_line

    res, cur_context = kernal._setup_context ( user          = AI_USER, 
                                               lang          = lang, 
                                               inp           = tokenize(prompt, lang=lang),
                                               prev_context  = prev_context,
                                               prev_res      = res)

    inp = kernal._compute_net_input (res, cur_context)

    #
    # see if this input sequence is already covered by our training data
    #

    responses      = []
    match_loc_fn   = None
    match_loc_line = None

    for tdr in kernal.session.query(model.TrainingData).filter(model.TrainingData.lang  == lang,
                                                               model.TrainingData.inp   == json.dumps(inp)):

        acode     = json.loads (tdr.resp)
        pcode     = kernal._reconstruct_prolog_code (acode)
        clause    = Clause (None, pcode, location=kernal.dummyloc)
        solutions = kernal.rt.search (clause, env=res)

        match_module   = tdr.module
        match_loc_fn   = tdr.loc_fn
        match_loc_line = tdr.loc_line

        # import pdb; pdb.set_trace()

        for solution in solutions:

            actual_out, actual_actions, score = kernal._extract_response (cur_context, solution)

            responses.append ((pcode, actual_out, actual_actions, score))

    prev_context = cur_context

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

#
# main curses interface
#

def paint_main():

    global stdscr, hstr, responses, prompt, inp, prev_context, kernal
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
    stdscr.insstr(0, mx-17, 'Zamia AI Trainer', curses.A_REVERSE)

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
        for pcode, actual_out, actual_actions, score in responses:
            # stdscr.insstr(y, 2, '%s' % (repr(pcode)), curses.A_DIM)
            stdscr.insstr(y, 4, '%5.1f %s %s' % (score, u' '.join(actual_out), repr(actual_actions)), curses.A_BOLD)
            y += 1
    else:
        stdscr.insstr(y, 2, 'Not covered by DB. Current module (M:Change Module):', curses.A_DIM)
        y += 1
        stdscr.insstr(y, 4, '%s' % match_module, curses.A_BOLD)
        y += 1


    # context

    if prev_context:

        y = 2
        stdscr.insstr(y, 80, 'Context: (%s)' % prev_context.name, curses.A_DIM)
        y += 1

        s1s = kernal.rt.search_predicate ('context', [prev_context, '_1', '_2'], env={})
        for s1 in s1s:
            stdscr.insstr(y, 80, '%s is %s' % (s1['_1'], s1['_2']), curses.A_BOLD)
            y += 1
        y += 1

        stdscr.insstr(y, 80, 'Mem:', curses.A_DIM)
        y += 1

        s1s = kernal.rt.search_predicate ('mem', [prev_context, '_1', '_2'], env={})
        for s1 in s1s:
            stdscr.insstr(y, 80, '%s is %s' % (s1['_1'], s1['_2']), curses.A_BOLD)
            y += 1


    # footer

    stdscr.insstr(my-2, 0,     " R:Record   E:Prompt   P:Playback                       ", curses.A_REVERSE )
    stdscr.insstr(my-1, 0,     " Module: M:Change  A:Align                              ", curses.A_REVERSE )
    stdscr.insstr(my-2, mx-40, "                                        ", curses.A_REVERSE )
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
tts_speed           = config.getint('tts',    'tts_speed')
tts_pitch           = config.getint('tts',    'tts_pitch')

loc                 = config.get   ('vad',    'loc')
source              = config.get   ('vad',    'source')
volume              = config.getint('vad',    'volume')
aggressiveness      = config.getint('vad',    'aggressiveness')

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

    #
    # pulseaudio recorder / player
    #

    misc.message_popup(stdscr, 'Initializing...', 'Init Pulseaudio...')
    rec = PulseRecorder (source, SAMPLE_RATE, volume)
    player = PulsePlayer('Zamia AI Trainer')
    paint_main()
    logging.debug ('PulseRecorder initialized.')

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
    kernal = AIKernal(load_all_modules=True)
    # kernal.setup_tf_model (mode='decode', load_model=True, ini_fn=ai_model)
    # kernal.setup_align_utterances(lang=lang)
    paint_main()
    logging.debug ('AI kernal initialized.')

    #
    # prev context
    #

    prev_context = kernal.find_prev_context(USER_URI)

    #
    # TTS
    #

    misc.message_popup(stdscr, 'Initializing...', 'Init TTS...')
    kernal.setup_tts (tts_host, tts_port, locale=tts_locale, voice=tts_voice, engine=tts_engine, speed=tts_speed, pitch=tts_pitch)
    paint_main()
    logging.debug ('TTS initialized.')

    #
    # ASR
    #

    misc.message_popup(stdscr, 'Initializing...', 'Init ASR...')
    kernal.setup_asr (kaldi_model_dir, kaldi_model)
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

except:
    logging.error('EXCEPTION CAUGHT %s' % traceback.format_exc())

finally:

    logging.info('resetting curses...')

    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()

