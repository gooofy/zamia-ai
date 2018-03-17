#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Guenter Bartsch, Heiko Schaefer
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
# benchmark prolog compiler+runtime through kernal
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

from zamiaprolog.logic         import Predicate
from zamiaprolog.errors        import PrologError, PrologRuntimeError
from ai_kernal                 import AIKernal
from nltools                   import misc

def _bench_fn():

    kernal.compile_module_multi (['humans'], run_trace=False, print_utterances=False)


logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

kernal = AIKernal()


cProfile.run('_bench_fn()', 'mestats')

p = pstats.Stats('mestats')
# p.strip_dirs().sort_stats(-1).print_stats()
p.sort_stats('cumulative').print_stats(10)

