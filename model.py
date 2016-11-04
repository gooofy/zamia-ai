#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016 Guenter Bartsch
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

import sys
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, Unicode, UnicodeText, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import utils

config = utils.load_config()

db_server = config.get("semantics", "dbserver")
db_name   = config.get("semantics", "dbname")
db_user   = config.get("semantics", "dbuser")
db_pass   = config.get("semantics", "dbpass")

# We connect with the help of the PostgreSQL URL
# postgresql://federer:grandestslam@localhost:5432/tennis
url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format(db_user, db_pass, db_server, 5432, db_name)

#engine = create_engine(url, echo=True)
engine = create_engine(url)

Base = declarative_base()

#
# knowledge / reasoning
#

class ORMClause(Base):

    __tablename__ = 'clauses'

    id                = Column(Integer, primary_key=True)

    module            = Column(String(255), index=True)
    head              = Column(String(255), index=True)
    arity             = Column(Integer, index=True) 
    prolog            = Column(UnicodeText)
  
class ORMPredicateDoc(Base):

    __tablename__ = 'predicate_docs'

    module            = Column(String(255), index=True)
    name              = Column(String(255), primary_key=True)

    doc               = Column(UnicodeText)

class ModuleDependency(Base):

    __tablename__ = 'module_dependencies'

    id                = Column(Integer, primary_key=True)

    module            = Column(String(255), index=True)
    requires          = Column(String(255), index=True)

#
# NLP stuff
#

class Source(Base):

    __tablename__ = 'sources'

    ref               = Column(String(255), primary_key=True)
    
    name              = Column(Unicode(255), index=True)

    discourses        = relationship("Discourse", backref="src", passive_deletes=True)

    def __unicode__(self):
        return self.name

class Discourse(Base):

    __tablename__ = 'discourses'

    id                = Column(Integer, primary_key=True)
    
    num_participants  = Column(Integer)
    lang              = Column(String(2), index=True)

    src_ref           = Column(String(255), ForeignKey('sources.ref', ondelete='CASCADE'))

    rounds            = relationship("DiscourseRound", backref="discourse", passive_deletes=True)

class DiscourseRound(Base):

    __tablename__ = 'discourse_rounds'

    id                = Column(Integer, primary_key=True)

    round_num         = Column(Integer, index=True)

    inp_raw           = Column(UnicodeText)
    inp_tokenized     = Column(UnicodeText)
    response          = Column(UnicodeText)

    discourse_id      = Column(Integer, ForeignKey('discourses.id', ondelete='CASCADE'))

class Context(Base):

    __tablename__ = 'contexts'

    id                = Column(Integer, primary_key=True)

    name              = Column(String, index=True)
    key               = Column(Unicode, index=True)
    value             = Column(UnicodeText)
    default_value     = Column(UnicodeText)

Base.metadata.create_all(engine)

# def store_doc (session, ref, name, delete = True):
# 
#     doc = session.query(Document).filter(Document.ref==ref).first()
# 
#     if not doc:
#         doc = Document (ref=ref, name=name)
#         session.add(doc)
# 
#     else:
# 
#         if delete:
# 
#             session.delete(doc)
# 
#             doc = Document (ref=ref, name=name)
#             session.add(doc)
# 
#     return doc


