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
# simple ai http api server
#
# WARNING: 
#     right now, this supports a single client only - needs a lot more work
#     to become (at least somewhat) scalable
#
# Process NLP input line
# ----------------------
# 
# * POST `/process`
# * args (JSON encoded dict): 
#   * "line"        : line to be processed 
# 
# Returns:
# 
# * 400 if request is invalid
# * 200 OK {"utts": [{"lang": "de", "finished": true, "utterance": "Hallo!"}], 
#           "actions": [["media", "tune", "\"media:B5_aktuell\""]]}
# 
# Example:
# 
# curl -i -H "Content-Type: application/json" -X POST \
#      -d '{"line": "computer, schalte bitte das radio ein"}' \
#      http://localhost:8302/process

import os
import sys
import logging
import traceback
import json

from time import time
from optparse import OptionParser
from setproctitle import setproctitle
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

import model

from ai_kernal import AIKernal

PROC_TITLE        = 'ai_server'

class AIHandler(BaseHTTPRequestHandler):
	
    def do_GET(self):
        self.send_error(400, 'Invalid request')

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):

        global kernal

        logging.debug("POST %s" % self.path)

        if self.path=="/process":

            try:
                data = json.loads(self.rfile.read(int(self.headers.getheader('content-length'))))

                # print data

                line        = data['line']

                utts, actions = kernal.process_line(line)

                logging.debug("utts: %s" % repr(utts)) 
                logging.debug("actions: %s" % repr(actions)) 

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

                reply_actions = map (lambda action: map (lambda p: unicode(p), action), actions)

                logging.debug("reply_actions: %s" % repr(reply_actions)) 
                reply = {'utts': utts, 'actions': reply_actions }

                self.wfile.write(json.dumps(reply))

            except:

                logging.error(traceback.format_exc())

                self.send_response(400)
                self.end_headers()

        else:
            self.send_response(400)
            self.end_headers()


if __name__ == '__main__':

    server_host   = model.config.get("semantics", "server_host")
    server_port   = int(model.config.get("semantics", "server_port"))

    setproctitle (PROC_TITLE)

    #
    # commandline
    #

    parser = OptionParser("usage: %prog [options] ")

    parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                       help="verbose output")

    parser.add_option ("-H", "--host", dest="host", type = "string", default=server_host,
                       help="host, default: %s" % server_host)

    parser.add_option ("-p", "--port", dest="port", type = "int", default=server_port,
                       help="port, default: %d" % server_port)

    (options, args) = parser.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
        debug=True
    else:
        logging.basicConfig(level=logging.INFO)
        debug=False

    #
    # setup nlp kernal
    #

    kernal = AIKernal()
    kernal.setup_tf_model (True, True)

    #
    # run HTTP server
    #

    try:
        server = HTTPServer((options.host, options.port), AIHandler)
        logging.info('listening for HTTP requests on %s:%d' % (options.host, options.port))
        
        # wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        logging.error('^C received, shutting down the web server')
        server.socket.close()

