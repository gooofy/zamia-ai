#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Guenter Bartsch, Heiko Schaefer
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
# benchmark prolog runtime through the kernal
#

import sys
import logging
import codecs
import cProfile, pstats
from time import time

from sqlalchemy.orm import sessionmaker
import model

from zamiaprolog.logicdb       import LogicDB
from aiprolog.runtime          import AIPrologRuntime, USER_PREFIX
from aiprolog.parser           import AIPrologParser
from aiprolog.nlp_macro_engine import NLPMacroEngine

from zamiaprolog.logic         import Predicate
from zamiaprolog.errors        import PrologError, PrologRuntimeError
from ai_kernal                 import AIKernal
from nltools                   import misc

def _bench_fn():

    user_uri = USER_PREFIX + 'benchmark'

    start_time = time()

    abufs = kernal.process_input(line, 'en', user_uri, test_mode=True, trace=False)

    logging.info ('process_input took %fs' % (time()-start_time))

    for abuf in abufs:
        logging.debug ("abuf: %s" % repr(abuf))


logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

kernal = AIKernal()

line = u'exp do you know obama'

# MODEL = 'models/200ksteps_2_1024_de.ini'

for mn2 in kernal.all_modules:
    kernal.load_module (mn2)

kernal.init_module ('exp', run_trace=False)
# kernal.setup_tf_model(True, True, MODEL)

                
cProfile.run('_bench_fn()', 'mestats')

p = pstats.Stats('mestats')
# p.strip_dirs().sort_stats(-1).print_stats()
p.sort_stats('cumulative').print_stats(10)

