#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
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
# a very simple console chatbot zamia ai demo
#

import os
import sys
import traceback
import logging
import datetime
import codecs
import readline 
 
from builtins               import input
from optparse               import OptionParser
from zamiaai.ai_kernal      import AIKernal, AIContext, USER_PREFIX, LANGUAGES
from nltools                import misc
from nltools.tokenizer      import tokenize

PROC_TITLE        = 'chatbot'

#
# init 
#

misc.init_app(PROC_TITLE)

#
# command line
#

parser = OptionParser("usage: %prog [options])")

parser.add_option("-v", "--verbose", action="store_true", dest="verbose", 
                  help="enable debug output")

(options, args) = parser.parse_args()

#
# logger
#

if options.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)
else:
    logging.basicConfig(level=logging.INFO)


#
# setup AI DB, Kernal and Context
#

kernal = AIKernal.from_ini_file()
for mn2 in kernal.all_modules:
    kernal.consult_module (mn2)
kernal.setup_tf_model()
ctx  = kernal.create_context()
logging.debug ('AI kernal initialized.')

#
# main loop
#

print(chr(27) + "[2J")
while True:

    user_utt = input ('> ')

    ai_utt, score, action = kernal.process_input(ctx, user_utt)

    print('AI : %s' % ai_utt)

    if action:
        print('     %s' % repr(action))

    print
    
