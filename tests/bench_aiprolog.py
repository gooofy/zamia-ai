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
# benchmark the macro engine
#

import logging
import codecs
import cProfile, pstats

from nltools import misc

from sqlalchemy.orm import sessionmaker
import model

from zamiaprolog.logicdb       import LogicDB
from aiprolog.runtime          import AIPrologRuntime
from aiprolog.parser           import AIPrologParser
from aiprolog.nlp_macro_engine import NLPMacroEngine

def _bench_fn():

    Session = sessionmaker(bind=model.engine)
    session = Session()
    me = NLPMacroEngine(session)

    discourses = me.macro_expand("de", u"(a|b|c|d|e|f) (a|b|c|d|e|f) (a|b|c|d|e|f) (a|b|c|d|e|f) (a|b|c|d|e|f) (a|b|c|d|e|f)", u"foo @MACRO_0:TSTART_W_0 @MACRO_1:TEND_W_0?", None)


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

cProfile.run('_bench_fn()', 'mestats')

p = pstats.Stats('mestats')
# p.strip_dirs().sort_stats(-1).print_stats()
p.sort_stats('cumulative').print_stats(10)

