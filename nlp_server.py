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
# nlp wsgi server
#
# usage:
#
# curl -i http://hal:8302/nlp/process?line=hallo%20hal
#

import os
import sys
import logging
import readline
import atexit
import traceback

from optparse import OptionParser

import model

from nlp_engine import NLPEngine

import tensorflow as tf

from flask import Flask, jsonify, request, abort, send_file, Markup, render_template, send_from_directory

app = Flask(__name__)

#
# commandline
#

parser = OptionParser("usage: %prog [options] ")

parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                  help="verbose output")

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
    debug=True
else:
    logging.basicConfig(level=logging.INFO)
    debug=False

#
# setup nlp engine, tensorflow session
#

# setup config to use BFC allocator
config = tf.ConfigProto()  
config.gpu_options.allocator_type = 'BFC'

tf_session = tf.Session(config=config) 

nlp_engine = NLPEngine(tf_session)

@app.route('/nlp/process', methods=['GET'])
def process_line():

    global nlp_engine

    if not 'line' in request.args:
        return jsonify({'message': 'missing "line" argument.'}), 400
    line    = request.args['line']

    try:
        utts, actions = nlp_engine.process_line(line)

        logging.debug("utts: %s" % repr(utts)) 
        logging.debug("actions: %s" % repr(actions)) 

        return jsonify({'utts': utts, 'actions': map(lambda p: unicode(p), actions)}), 201

    except:

        print >>sys.stderr, traceback.format_exc()
        print >>sys.stderr, 'process_line failed for line=%s' % repr(line)

    abort(400)


if __name__ == '__main__':

    server_host   = model.config.get("semantics", "server_host")
    server_port   = model.config.get("semantics", "server_port")

    app.run(debug=debug, host = server_host, port=int(server_port))

