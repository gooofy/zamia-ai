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

import unittest
import logging
import codecs

from nltools                   import misc

from sqlalchemy.orm            import sessionmaker
from zamiaai                   import model

from zamiaprolog.logicdb       import LogicDB
from aiprolog.runtime          import AIPrologRuntime
from aiprolog.parser           import AIPrologParser

UNITTEST_MODULE  = 'unittests'
UNITTEST_CONTEXT = 'unittests'

class TestAIProlog (unittest.TestCase):

    def setUp(self):

        config = misc.load_config('.airc')

        #
        # logic DB
        #

        self.db = LogicDB(model.url)

        #
        # aiprolog environment setup
        #

        self.prolog_rt = AIPrologRuntime(self.db)
        self.parser    = AIPrologParser(self.db)

        self.prolog_rt.set_trace(True)

        self.db.clear_module(UNITTEST_MODULE)

    # @unittest.skip("temporarily disabled")
    def test_tokenize(self):

        clause = self.parser.parse_line_clause_body("tokenize (de, 'hallo, welt!', X)")
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 1)
        self.assertEqual (len(solutions[0]['X'].l), 2)

    # @unittest.skip("temporarily disabled")
    def test_edit_distance(self):

        clause = self.parser.parse_line_clause_body("edit_distance (['hallo', 'welt'], ['hallo', 'springfield'], X)")
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 1)
        self.assertEqual (solutions[0]['X'].f, 1.0)


# class TestMacroEngine (unittest.TestCase):
# 
#     def setUp(self):
#         Session = sessionmaker(bind=model.engine)
#         self.session = Session()
# 
#     def testLocalMacros(self):
# 
#         me = NLPMacroEngine(self.session)
#         discourses = me.macro_expand('de', u'(HAL,|Computer,|Du,|) (Ich bin|Ich fühle mich|Man bin ich|Da bin ich) (zufrieden|so zufrieden|glücklich|so glücklich|froh|so froh)', u'', None)
# 
#         self.assertEqual(len(discourses), 96)
# 
#     def testMacroTokens(self):
# 
#         me = NLPMacroEngine(self.session)
#         discourses = me.macro_expand('de', u'hallo (HAL|Computer|Du|lieber computer|) wie geht es dir (heute|)', 
#                                            u'foo @MACRO_0:TSTART_W_0 bar @MACRO_0:TEND_W_0 @MACRO_0:W baz @MACRO_1:TEND_W_0?', None)
# 
#         self.assertEqual(len(discourses), 10)
#         self.assertEqual(discourses[0][1], u'foo 1 bar 2 HAL baz 7?')
# 
#         discourses = me.macro_expand('de', u'foobar what is the full name of (foo|donald trump)', 
#                                            u'foo @MACRO_0:TSTART_W_0 bar @MACRO_0:TEND_W_0', None)
# 
#         self.assertEqual(len(discourses), 2)
#         self.assertEqual(discourses[0][1], u'foo 7 bar 8')
#         self.assertEqual(discourses[1][1], u'foo 7 bar 9')


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
   
    unittest.main()

