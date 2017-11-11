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

