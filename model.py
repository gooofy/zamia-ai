#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017 Guenter Bartsch
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
from sqlalchemy import Column, Integer, String, Text, Unicode, UnicodeText, Enum, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from nltools import misc

config = misc.load_config('.airc')

# db_server = config.get("semantics", "dbserver")
# db_name   = config.get("semantics", "dbname")
# db_user   = config.get("semantics", "dbuser")
# db_pass   = config.get("semantics", "dbpass")
# 
# # We connect with the help of the PostgreSQL URL
# # postgresql://federer:grandestslam@localhost:5432/tennis
# url = 'postgresql://{}:{}@{}:{}/{}'
# url = url.format(db_user, db_pass, db_server, 5432, db_name)

url = config.get("db", "url")

#engine = create_engine(url, echo=True)
engine = create_engine(url)

Base = declarative_base()

#
# NLP stuff
#

class DiscourseRound(Base):

    __tablename__ = 'discourse_rounds'

    id                = Column(Integer, primary_key=True)

    lang              = Column(String(2), index=True)
    module            = Column(String(255), index=True)

    inp               = Column(UnicodeText, index=True)
    resp              = Column(UnicodeText)

    loc_fn            = Column(String(255))
    loc_line          = Column(Integer)
    loc_col           = Column(Integer)

    __table_args__    = (Index('idx_dr_inp_lang', "inp", "lang"), )


class Cronjob(Base):

    __tablename__ = 'cronjobs'

    id                = Column(Integer, primary_key=True)

    module            = Column(String, index=True)
    name              = Column(String, index=True)
    last_run          = Column(Integer, index=True)

class NLPTest(Base):

    __tablename__ = 'nlp_tests'

    id                = Column(Integer, primary_key=True)

    module            = Column(String(255), index=True)
    name              = Column(String(255), index=True)

    clause            = Column(Text)

class NLPMacro(Base):

    __tablename__ = 'nlp_macros'

    id                = Column(Integer, primary_key=True)

    module            = Column(String(255), index=True)
    lang              = Column(String(2),   index=True)
    name              = Column(String(255), index=True)

    mappings          = Column(Text)
    location          = Column(String(255), index=True)

Base.metadata.create_all(engine)

