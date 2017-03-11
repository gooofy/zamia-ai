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

from zamiaprolog.logicdb import LogicDB
from aiprolog.runtime    import AIPrologRuntime
from aiprolog.parser     import AIPrologParser

from kb import HALKB

UNITTEST_MODULE  = 'unittests'
UNITTEST_CONTEXT = 'unittests'

COMMON_PREFIXES = {
            'rdf':     'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs':    'http://www.w3.org/2000/01/rdf-schema#',
            'hal':     'http://hal.zamia.org/kb/',
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

        self.kb = HALKB(UNITTEST_MODULE)

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
              WEV, hal:dt_end,        DT_END,
              WEV, hal:dt_start,      DT_START,
              WEV, hal:location,      P,
              P,   rdfs:label,        Label,
              WEV, hal:temp_min,      TempMin,
              WEV, hal:temp_max,      TempMax,
              WEV, hal:precipitation, Precipitation,
              WEV, hal:clouds,        Clouds,
              WEV, hal:icon,          Icon,
              filter (DT_START >= isoformat(EvTS, 'local'),
                      DT_END   =< isoformat(EvTE, 'local'),
                      lang(Label) = L2)
              )
         """)

        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 7)



if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    unittest.main()

