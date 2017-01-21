#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016, 2017 Guenter Bartsch
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
# store and retrieve logic clauses to and from our relational db
#

import os
import logging

import model

from logic  import *
from prolog_parser import PrologParser

class LogicDB(object):

    def __init__(self, session):

        self.session         = session
        self.parser          = PrologParser()

        
    def clear_module(self, module):

        logging.info("Clearing %s ..." % module)
        self.session.query(model.ORMClause).filter(model.ORMClause.module==module).delete()
        self.session.query(model.ORMPredicateDoc).filter(model.ORMPredicateDoc.module==module).delete()
        logging.info("Clearing %s ... done." % module)

    def clear_all_modules(self):

        logging.info("Clearing all modules ...")
        self.session.query(model.ORMClause).delete()
        self.session.query(model.ORMPredicateDoc).delete()
        self.session.query(model.Context).delete()
        logging.info("Clearing all modules ... done.")
        

    def store (self, module, clause):

        ormc = model.ORMClause(module    = module,
                               arity     = len(clause.head.args), 
                               head      = clause.head.name, 
                               prolog    = unicode(clause))

        # print unicode(clause)

        self.session.add(ormc)
       
    def store_doc (self, module, name, doc):

        ormd = model.ORMPredicateDoc(module = module,
                                     name   = name,
                                     doc    = doc)
        self.session.add(ormd)

    def lookup (self, name):

        # FIXME: caching ?

        # if name in self.clauses:
        #     return self.clauses[name]

        res = []

        for ormc in self.session.query(model.ORMClause).filter(model.ORMClause.head==name).all():

            for c in self.parser.parse_line_clauses(ormc.prolog):
                res.append (c)
        
        return res

    #
    # manage stored contexts in db
    #

    def read_context (self, name, key):

        ctx = self.session.query(model.Context).filter(model.Context.name==name, model.Context.key==key).first()
        if not ctx:
            return None

        return self.parser.parse_line_clause_body(ctx.value)

    def write_context (self, name, key, value):

        v = unicode(value)

        ctx = self.session.query(model.Context).filter(model.Context.name==name, model.Context.key==key).first()
        if not ctx:
            ctx = model.Context(name=name, key=key, value=v, default_value=v)
            self.session.add(ctx)
        else:
            ctx.value = v

    def set_context_default(self, name, key, value):

        ctx = self.session.query(model.Context).filter(model.Context.name==name, model.Context.key==key).first()

        if not ctx:
            ctx = model.Context(name=name, key=key, value=value, default_value=value)
            self.session.add(ctx)
        else:
            ctx.default_value = value

    def reset_context(self, name):

        for ctx in self.session.query(model.Context).filter(model.Context.name==name).all():
            ctx.value = ctx.default_value
        
# class LogicMemDB(object):
# 
#     def __init__(self):
#         self.clauses = {}
# 
#     def store (self, clause):
#         if clause.head.name in self.clauses:
#             self.clauses[clause.head.name].append (clause)
#         else:
#             self.clauses[clause.head.name] = [clause]
#        
#     def lookup (self, name):
#         if name in self.clauses:
#             return self.clauses[name]
#         return []

