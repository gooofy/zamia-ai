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

