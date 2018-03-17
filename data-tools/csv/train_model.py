#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2018 Guenter Bartsch
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
# train keras module alignment model
#

import os
import sys
import traceback
import codecs
import logging
import time
import numpy as np

from optparse               import OptionParser
from zamiaai                import model
from nltools                import misc
from nltools.tokenizer      import tokenize
from sqlalchemy.orm         import sessionmaker
from align_model            import AlignModel

#
# init, cmdline
#

misc.init_app('train_model')

parser = OptionParser("usage: %prog [options]")

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

#
# db
#

Session = sessionmaker(bind=model.engine)
session = Session()

#
# train
#

align_model = AlignModel(session)
align_model.train(100000, False)

