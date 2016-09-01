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
# for now, just stores them to be added to ASR training corpus
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

PROC_TITLE        = 'hal_asr'
SAMPLE_RATE       = 16000

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

zmqport     = config.get('speech', 'asr_port')
extrasdir   = config.get('speech', 'extrasdir_de')
vf_login    = config.get('speech', 'vf_login')

#
# zmq init
#

context = zmq.Context()
zmq_socket = context.socket(zmq.REP)
zmq_socket.bind ("tcp://*:%s" % zmqport)

#
# main command loop
#

logging.debug("ready, waiting for messages...")

while True:

    try:
        message = zmq_socket.recv()
        # logging.debug("received: '%s'" % message)
        reply = 0

        msg = json.loads(message)

        # logging.debug("decoded: %s" % repr(msg))

        if msg[0] == 'REC':

            audio = map(lambda x: int(x), msg[1].split(','))

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

            wf = wave.open(audiofn, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.setnframes(len(audio)/2)

            packed_audio = struct.pack('%sh' % len(audio), *audio)
            wf.writeframes(packed_audio)

            wf.close()
            logging.info("%s written." % audiofn)

    except:
        logging.error("****************** ERROR: unexpected exception")
        logging.error(traceback.format_exc())

    logging.debug("reply: %s" % repr(reply))
    zmq_socket.send (json.dumps(reply))

