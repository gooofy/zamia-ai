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

from sphinxclient import SphinxClient

PROC_TITLE        = 'hal_asr'

SAMPLE_RATE       = 16000

hmdir     = 'data/dst/speech/de/cmusphinx/model_parameters/voxforge.cd_cont_3000'
dictf     = 'data/dst/speech/de/cmusphinx/etc/voxforge.dic'
lm        = 'data/dst/speech/de/cmusphinx/etc/voxforge.lm.DMP'
#dictf     = 'data/dst/lm/hal.dic'
#lm        = 'data/dst/lm/hal.lm.DMP'

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

port_asr    = config.get('speech', 'port_asr')
extrasdir   = config.get('speech', 'extrasdir_de')
vf_login    = config.get('speech', 'vf_login')

#
# zmq init
#

context = zmq.Context()
asr_socket = context.socket(zmq.REP)
asr_socket.bind ("tcp://*:%s" % port_asr)

#
# pocketsphinx
#

sphinx = SphinxClient (hmdir, dictf, lm=lm)

#
# main command loop
#

while True:

    reply = 0

    try:

        logging.debug("ready, waiting for messages...")

        message = asr_socket.recv()
        # logging.debug("received: '%s'" % message)

        msg = json.loads(message)

        logging.debug("msg[0]: %s" % repr(msg[0]))

        if msg[0] == 'DECODE':

            audios, save = msg[1]

            audio = map(lambda x: int(x), audios.split(','))
            packed_audio = struct.pack('%sh' % len(audio), *audio)

            # create wav file in memory

            wav_buffer = StringIO()
            wf = wave.open(wav_buffer, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.setnframes(len(audio)/2)

            wf.writeframes(packed_audio)

            wf.close()

            if save:
                # store recording in WAV format
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

                with open(audiofn, 'wb') as audiof:
                    wav_buffer.seek(0)
                    audiof.write(wav_buffer.read())

                logging.info("%s written." % audiofn)

            wav_buffer.seek(0)
            confidence, hstr = sphinx.decode(wav_buffer.read())

            if hstr:
                print
                print "*****************************************************************************"
                print "**"
                print "** %9.5f %s" % (confidence, hstr)
                print "**"
                print "*****************************************************************************"
                print

                reply = (confidence, hstr)
            else:
                reply = (0.0, '???')

        elif msg[0] == 'RECSTART':

            hal_comm('ASR_RECSTART', None)

    except:
        logging.error("****************** ERROR: unexpected exception")
        logging.error(traceback.format_exc())

    logging.debug("reply: %s" % repr(reply))
    asr_socket.send (json.dumps(reply))

