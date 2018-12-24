#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016, 2017, 2018 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# interactive debugger shell
#

from __future__ import print_function

import os
import sys
import logging

class AIDbg(object):

    def __init__(self, kernal, user_uri, realm, verbose):

        self.kernal   = kernal
        self.user_uri = user_uri
        self.realm    = realm
        self.verbose  = verbose

        if self.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)


    def print_help(self):
        print (":h          help")
        print (":c <skills> compile <skills>")
        print (":m          show memory / context")
        print (":t          %s prolog tracing" % ('disable' if self.run_trace else 'enable'))
        print (":v          verbose logging %s" % ('off' if self.verbose else 'on'))
        print (":q          quit")

    def process_command(self, line):

        if line == ":h":
            self.print_help()

        # FIXME: we'd have to force-reload the python module
        elif line[:2] == ":c":

            parts = line.split(' ')
            if len(parts) < 2:
                logging.error('?usage')
                self.print_help()
                return

            self.kernal.compile_skill_multi (parts[1:])

        elif line == ":m":

            print ("ctx.user   = %s" % self.ctx.user)
            print ("ctx.realm  = %s" % self.ctx.realm)
            print ("ctx.lang   = %s" % self.ctx.lang)
            memd = self.kernal.mem_dump(self.ctx.realm)
            for k, v, score in memd:
                print(u'MEM(%-8s):    %-20s: %s (%f)' % (self.ctx.realm, k, v, score))
            memd = self.kernal.mem_dump(self.ctx.user)
            for k, v, score in memd:
                print(u'MEM(%-8s):    %-20s: %s (%f)' % (self.ctx.user, k, v, score))

        elif line == ":t":
            self.run_trace = not self.run_trace

        elif line == ":v":
            self.verbose = not self.verbose
            if self.verbose:
                logging.getLogger().setLevel(logging.DEBUG)
            else:
                logging.getLogger().setLevel(logging.INFO)

        else:
            logging.error("? command error ('%s')" % line)
            self.print_help()


    def run(self):
    
        self.ctx       = self.kernal.create_context(user=self.user_uri, realm=self.realm)
        self.run_trace = False

        while True:

            line = raw_input ('dbg (:h for help)> ')

            if not line:
                continue
            if len(line)<1:
                continue

            if line == ':q':
                break

            if line[0] == ':':
                self.process_command(line)
                continue

            out, score, action = self.kernal.process_input(self.ctx, line, run_trace=self.run_trace)

            if action:
                logging.info(u'RESP: [%6.1f] %s | action: %s' % (score, out, unicode(action)))
            else:
                logging.info(u'RESP: [%6.1f] %s ' % (score, out))
        
