#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2018 Guenter Bartsch
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

