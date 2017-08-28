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
# simple ai mqtt server
#
# Process NLP input line
# ----------------------
# 
# * topic `ai/utt_in`
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
# hbmqtt_pub --url mqtt://dagobert -t ai/utt_in -m '{"utt":"hello computer","lang":"en","user":"bimbo"}'

import os
import sys
import logging
import traceback
import json
import random
import time

from optparse             import OptionParser
from setproctitle         import setproctitle
import paho.mqtt.client as paho

from zamiaai              import model

from zamiaprolog.builtins import ASSERT_OVERLAY_VAR_NAME
from zamiaai.ai_kernal    import AIKernal
from aiprolog.runtime     import USER_PREFIX
from nltools              import misc

PROC_TITLE        = 'ai_mqtt'
AI_SERVER_MODULE  = '__server__'

TOPIC_IN  = 'ai/utt_in'
TOPIC_OUT = 'ai/response'

def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

    client.subscribe(TOPIC_IN)
    
def on_message(client, userdata, msg):

    global kernal

    print(msg.topic+" "+str(msg.payload))

    try:
        data = json.loads(msg.payload)

        # print data

        utt      = data['utt']
        lang     = data['lang']
        user_uri = USER_PREFIX + data['user']

        if kernal.nlp_model.lang != lang:
            logging.warn('incorrect language for model: %s' % lang)
            return

        score, resps, actions, solutions = kernal.process_input(utt, kernal.nlp_model.lang, user_uri)

        for idx in range (len(resps)):
            logging.debug('[%05d] %s ' % (score, u' '.join(resps[idx])))

        # if we have multiple responses, pick one at random

        if len(resps)>0:

            idx = random.randint(0, len(resps)-1)

            # apply DB overlay, if any
            ovl = solutions[idx].get(ASSERT_OVERLAY_VAR_NAME)
            if ovl:
                ovl.do_apply(AI_SERVER_MODULE, kernal.db, commit=True)

            acts = actions[idx]
            for action in acts:
                logging.debug("ACTION %s" % repr(action))

            resp = resps[idx]
            logging.debug('RESP: [%05d] %s' % (score, u' '.join(resps[idx])))

            # FIXME: score, intents/actions, ...

            msg = json.dumps({"utt": u' '.join(resp)})

            logging.info("publishing message on topic %s : %s ..." % (TOPIC_OUT, msg))

            (rc, mid) = client.publish(TOPIC_OUT, msg)

            # # reply_actions = map (lambda action: map (lambda p: unicode(p), action), abuf['actions'])

            # logging.debug("reply_actions: %s, resp: %s" % (repr(acts), repr(resp)))
            # reply = {'actions': acts, 'resp': resp }

            # self.wfile.write(json.dumps(reply))

        else:
            logging.error('no solution found for input %s' % line)

    except:

        logging.error(traceback.format_exc())

        # FIXME
        # # abufs = kernal.do_eliza(line, kernal.nlp_model.lang, trace=False)
        # # abuf = random.choice(abufs)

        # # logging.debug("abuf: %s" % repr(abuf)) 

        # self.send_response(200)
        # self.send_header('Content-Type', 'application/json')
        # self.end_headers()

        # # reply_actions = map (lambda action: map (lambda p: unicode(p), action), abuf['actions'])

        # logging.debug("ELIZA")
        # # logging.debug("reply_actions: %s" % repr(reply_actions)) 
        # reply = {'actions': 'FIXME' }

        # self.wfile.write(json.dumps(reply))

DEFAULTS = {
            'broker_host'   : 'localhost',
            'broker_port'   : '1883',
            'broker_user'   : '',
            'broker_pw'     : '',
           }

CLIENT_NAME = 'Zamia AI MQTT Server'

if __name__ == '__main__':

    config = misc.load_config('.airc', defaults = DEFAULTS)

    broker_host   = model.config.get   ("semantics", "broker_host")
    broker_port   = model.config.getint("semantics", "broker_port")
    broker_user   = model.config.get   ("semantics", "broker_user")
    broker_pw     = model.config.get   ("semantics", "broker_pw")

    setproctitle (PROC_TITLE)

    #
    # commandline
    #

    parser = OptionParser("usage: %prog [options] model")

    parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                       help="verbose output")

    parser.add_option ("-H", "--host", dest="host", type = "string", default=broker_host,
                       help="MQTT broker host, default: %s" % broker_host)

    parser.add_option ("-p", "--port", dest="port", type = "int", default=broker_port,
                       help="MQTT broker port, default: %d" % broker_port)

    parser.add_option ("-s", "--global-step", dest="global_step", type = "int", default=0,
                       help="global step to load, default: 0 (latest)")

    (options, args) = parser.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
        debug=True
    else:
        logging.basicConfig(level=logging.INFO)
        debug=False

    if len(args) != 1:
        parser.print_help()
        sys.exit(42)

    #
    # setup nlp kernal
    #

    kernal = AIKernal()
    for mn2 in kernal.all_modules:
        kernal.load_module (mn2)
        kernal.init_module (mn2)
    kernal.setup_tf_model ('decode', True, args[0], global_step=options.global_step)

    print "connecting..."

    client = paho.Client(CLIENT_NAME)
    if broker_user:
        client.username_pw_set(broker_user, broker_pw)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_host, broker_port)

    print "connected."

    client.loop_forever()

