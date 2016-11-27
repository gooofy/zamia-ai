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
#
# server accepting WAV files via ZMQ
# - stores them to be added to ASR training corpus
# - runs pocketsphinx on them
#

import os
import sys
import logging
import readline
import atexit
import traceback
import datetime

from optparse import OptionParser
from StringIO import StringIO

import utils

import zmq
import json
import logging
from setproctitle import setproctitle
import wave
import struct

from kaldisimple.nnet3 import KaldiNNet3OnlineDecoder
import numpy as np

PROC_TITLE        = 'hal_asr'

SAMPLE_RATE       = 16000

def hal_comm (cmd, arg):

    global getty_socket

    rq = json.dumps ([cmd, arg])

    #print "Sending request %s" % rq
    getty_socket.send (rq)

    #  Get the reply.
    message = getty_socket.recv()
    res = json.loads(message)

    return res


logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)

#
# init
#

setproctitle (PROC_TITLE)

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


#
# config
#

config = utils.load_config()

port_asr           = config.get('speech', 'port_asr')
extrasdir          = config.get('speech', 'extrasdir_de')
vf_login           = config.get('speech', 'vf_login')

kaldi_model_dir_de = config.get('speech', 'kaldi_model_dir_de')
kaldi_model_de     = config.get('speech', 'kaldi_model_de')

#
# zmq init
#

context = zmq.Context()
asr_socket = context.socket(zmq.REP)
asr_socket.bind ("tcp://*:%s" % port_asr)

#
# kaldi asr
#

print '%s loading model...' % kaldi_model_de
decoder = KaldiNNet3OnlineDecoder (kaldi_model_dir_de, kaldi_model_de)
print '%s loading model... done.' % kaldi_model_de


#
# main command loop
#

wf = None

while True:

    reply = (0.0, '')

    try:

        logging.debug("ready, waiting for messages...")

        message = asr_socket.recv()
        # logging.debug("received: '%s'" % message)

        msg = json.loads(message)

        logging.debug("msg[0]: %s" % repr(msg[0]))

        if msg[0] == 'DECODE':

            audios, do_record, do_asr, finalize = msg[1]

            audio = map(lambda x: int(x), audios.split(','))

            if do_record:

                # store recording in WAV format

                if not wf:

                    ds = datetime.date.strftime(datetime.date.today(), '%Y%m%d')
                    audiodirfn = '%s/%s-%s-rec/wav' % (extrasdir, vf_login, ds)
                    logging.debug('audiodirfn: %s' % audiodirfn)
                    utils.mkdirs(audiodirfn)

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
                    # FIXME ? wf.setnframes(len(audio)/2)

                packed_audio = struct.pack('%sh' % len(audio), *audio)
                wf.writeframes(packed_audio)

                if finalize:

                    wf.close()  
                    wf = None

                    reply = (0.0, os.path.basename(audiofn))

            if do_asr:
                decoder.decode(SAMPLE_RATE, np.array(audio, dtype=np.float32), finalize)

                if finalize:

                    hstr       = decoder.get_decoded_string()
                    confidence = decoder.get_likelihood()

                    print
                    print "*****************************************************************************"
                    print "**"
                    print "** %9.5f %s" % (confidence, hstr)
                    print "**"
                    print "*****************************************************************************"
                    print

                    reply = (confidence, hstr)

    except:
        logging.error("****************** ERROR: unexpected exception")
        logging.error(traceback.format_exc())

    logging.debug("reply: %s" % repr(reply))
    asr_socket.send (json.dumps(reply))

