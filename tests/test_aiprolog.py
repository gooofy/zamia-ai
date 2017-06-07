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

from nltools import misc

from sqlalchemy.orm import sessionmaker
import model

from zamiaprolog.logicdb       import LogicDB
from aiprolog.runtime          import AIPrologRuntime
from aiprolog.parser           import AIPrologParser
from aiprolog.nlp_macro_engine import NLPMacroEngine

from kb import AIKB

UNITTEST_MODULE  = 'unittests'
UNITTEST_CONTEXT = 'unittests'

COMMON_PREFIXES = {
            'rdf':     'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs':    'http://www.w3.org/2000/01/rdf-schema#',
            'ai':      'http://ai.zamia.org/kb/',
            'aiu':     'http://ai.zamia.org/kb/user/',
            'aiup':    'http://ai.zamia.org/kb/user/prop/',
            'dbo':     'http://dbpedia.org/ontology/',
            'dbr':     'http://dbpedia.org/resource/',
            'dbp':     'http://dbpedia.org/property/',
            'xml':     'http://www.w3.org/XML/1998/namespace',
            'xsd':     'http://www.w3.org/2001/XMLSchema#',
            'geo':     'http://www.opengis.net/ont/geosparql#',
            'geo1':    'http://www.w3.org/2003/01/geo/wgs84_pos#',
            'geof':    'http://www.opengis.net/def/function/geosparql/',
            'owl':     'http://www.w3.org/2002/07/owl#',
            'schema':  'http://schema.org/',
            'wde':     'http://www.wikidata.org/entity/',
            'wdes':    'http://www.wikidata.org/entity/statement',
            'wdpd':    'http://www.wikidata.org/prop/direct/',
            'wdps':    'http://www.wikidata.org/prop/statement/',
            'wdpq':    'http://www.wikidata.org/prop/qualifier/',
            'wdp':     'http://www.wikidata.org/prop/',
    }

class TestAIProlog (unittest.TestCase):

    def setUp(self):

        config = misc.load_config('.airc')

        #
        # logic DB
        #

        self.db = LogicDB(model.url)

        #
        # knowledge base
        #

        self.kb = AIKB(UNITTEST_MODULE)

        for prefix in COMMON_PREFIXES:
            self.kb.register_prefix(prefix, COMMON_PREFIXES[prefix])

        self.kb.clear_all_graphs()

        self.kb.parse_file (UNITTEST_CONTEXT, 'n3', 'tests/chancellors.n3')
        self.kb.parse_file (UNITTEST_CONTEXT, 'n3', 'tests/wev.n3')

        #
        # aiprolog environment setup
        #

        self.prolog_rt = AIPrologRuntime(self.db, self.kb)
        self.parser    = AIPrologParser()

        self.prolog_rt.set_trace(True)

        self.db.clear_module(UNITTEST_MODULE)

    # @unittest.skip("temporarily disabled")
    def test_rdf_results(self):

        self.parser.compile_file('tests/chancellors_rdf.pl', UNITTEST_MODULE, self.db, self.kb)

        clause = self.parser.parse_line_clause_body('chancellor(X)')
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 2)

    # @unittest.skip("temporarily disabled")
    def test_rdf_exists(self):

        clause = self.parser.parse_line_clause_body("rdf ('http://www.wikidata.org/entity/Q567', 'http://www.wikidata.org/prop/direct/P21', 'http://www.wikidata.org/entity/Q6581072')")
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 1)

    # @unittest.skip("temporarily disabled")
    def test_rdf_optional(self):

        self.parser.compile_file('tests/chancellors_rdf.pl', UNITTEST_MODULE, self.db, self.kb)

        clause = self.parser.parse_line_clause_body("is_current_chancellor (X)")
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 1)

    # @unittest.skip("temporarily disabled")
    def test_rdf_filter(self):

        self.parser.compile_file('tests/chancellors_rdf.pl', UNITTEST_MODULE, self.db, self.kb)

        clause = self.parser.parse_line_clause_body("chancellor_labels (X, Y)")
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 2)

    # @unittest.skip("temporarily disabled")
    def test_rdf_filter_expr(self):

        clause = self.parser.parse_line_clause_body('rdf (X, dbp:termEnd, TE, filter(and(TE =< "1998-10-27", TE >= "1998-10-27")))')
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 1)

        clause = self.parser.parse_line_clause_body('rdf (X, dbp:termEnd, TE, filter(or(TE =< "1998-10-27", TE >= "1998-10-27")))')
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 2)

        clause = self.parser.parse_line_clause_body('rdf (X, dbp:termEnd, TE, filter(TE =< "1998-10-27", TE =< "1998-10-27", TE >= "1998-10-27"))')
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 1)

    # @unittest.skip("temporarily disabled")
    def test_rdf_joins(self):

        clause = self.parser.parse_line_clause_body("""
         uriref(wde:Q61656, P),
         Lang is de,
         atom_chars(Lang, L2),
         date_time_stamp(date(2016,12,6,0,0,0,\'local\'), EvTS),
         date_time_stamp(date(2016,12,7,0,0,0,\'local\'), EvTE),
         rdf (distinct,
              WEV, ai:dt_end,        DT_END,
              WEV, ai:dt_start,      DT_START,
              WEV, ai:location,      P,
              P,   rdfs:label,        Label,
              WEV, ai:temp_min,      TempMin,
              WEV, ai:temp_max,      TempMax,
              WEV, ai:precipitation, Precipitation,
              WEV, ai:clouds,        Clouds,
              WEV, ai:icon,          Icon,
              filter (DT_START >= EvTS,
                      DT_END   =< EvTE,
                      lang(Label) = L2)
              )
         """)

        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 7)

    # FIXME: this needs to be ported to new assertz based approach
    @unittest.skip("temporarily disabled")
    def test_rdf_assert(self):

        clause = self.parser.parse_line_clause_body('rdf(aiu:Alice, X, Y).')
        solutions = self.prolog_rt.search(clause)
        self.assertEqual (len(solutions), 0)

        clause = self.parser.parse_line_clause_body('rdf_assert (aiu:Alice, aiup:name, "Alice Green"), eoa.')
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))

        actions = self.prolog_rt.get_actions()
        logging.debug('actions: %s' % repr(actions))

        self.assertEqual (len(actions), 1)

        self.prolog_rt.execute_builtin_actions(actions[0])

        clause = self.parser.parse_line_clause_body('rdf(aiu:Alice, X, Y).')
        solutions = self.prolog_rt.search(clause)
        self.assertEqual (len(solutions), 1)
        self.assertEqual (solutions[0]['X'].s, u'http://ai.zamia.org/kb/user/prop/name')
        self.assertEqual (solutions[0]['Y'].s, u'Alice Green')

    # FIXME: this needs to be ported to new assertz based approach
    @unittest.skip("temporarily disabled")
    def test_rdf_assert_list(self):

        clause = self.parser.parse_line_clause_body('rdf_assert (aiu:Alice, aiup:topic, [1, "abc", wde:42]), eoa.')
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))

        actions = self.prolog_rt.get_actions()
        logging.debug('actions: %s' % repr(actions))

        self.assertEqual (len(actions), 1)

        self.prolog_rt.execute_builtin_actions(actions[0])

        clause = self.parser.parse_line_clause_body('rdf(aiu:Alice, aiup:topic, Y).')
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))

        self.assertEqual (len(solutions), 1)
        self.assertEqual (len(solutions[0]['Y'].l), 3)
        self.assertEqual (solutions[0]['Y'].l[0].f, 1.0)
        self.assertEqual (solutions[0]['Y'].l[1].s, u'abc')
        self.assertEqual (solutions[0]['Y'].l[2].name, u'wde:42')

class TestMacroEngine (unittest.TestCase):

    def setUp(self):
        Session = sessionmaker(bind=model.engine)
        self.session = Session()

    def testLocalMacros(self):

        me = NLPMacroEngine(self.session)
        discourses = me.macro_expand('de', u'(HAL,|Computer,|Du,|) (Ich bin|Ich fühle mich|Man bin ich|Da bin ich) (zufrieden|so zufrieden|glücklich|so glücklich|froh|so froh)', u'', None)

        self.assertEqual(len(discourses), 96)

    def testMacroTokens(self):

        me = NLPMacroEngine(self.session)
        discourses = me.macro_expand('de', u'hallo (HAL|Computer|Du|lieber computer|) wie geht es dir (heute|)', 
                                           u'foo @MACRO_0:TSTART_W_0 bar @MACRO_0:TEND_W_0 @MACRO_0:W baz @MACRO_1:TEND_W_0?', None)

        self.assertEqual(len(discourses), 10)
        self.assertEqual(discourses[0][1], u'foo 1 bar 2 HAL baz 7?')

        discourses = me.macro_expand('de', u'foobar what is the full name of (foo|donald trump)', 
                                           u'foo @MACRO_0:TSTART_W_0 bar @MACRO_0:TEND_W_0', None)

        self.assertEqual(len(discourses), 2)
        self.assertEqual(discourses[0][1], u'foo 7 bar 8')
        self.assertEqual(discourses[1][1], u'foo 7 bar 9')


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
   
    unittest.main()

