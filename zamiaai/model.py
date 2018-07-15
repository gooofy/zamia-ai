#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
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

import sys

from sqlalchemy                 import create_engine
from sqlalchemy                 import Column, Integer, String, Text, Unicode, UnicodeText, Enum, DateTime, ForeignKey, Index, Float
from sqlalchemy.orm             import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TrainingData(Base):

    __tablename__ = 'training_data'

    id                = Column(Integer, primary_key=True)

    lang              = Column(String(2), index=True)
    module            = Column(String(255), index=True)

    inp               = Column(UnicodeText, index=True)
    md5s              = Column(String(32))
    args              = Column(String(255))

    loc_fn            = Column(String(255))
    loc_line          = Column(Integer)

    __table_args__    = (Index('idx_td_inp_lang', "inp", "lang"), 
                         Index('idx_td_mod_lang', "module", "lang"))

class Code(Base):
    __tablename__ = "code"

    md5s              = Column(String(32), primary_key=True)

    module            = Column(String(255), index=True)

    code              = Column(Text)
    fn                = Column(String(255))

class TestCase(Base):

    __tablename__ = 'test_case'

    id                = Column(Integer, primary_key=True)

    lang              = Column(String(2), index=True)
    module            = Column(String(255), index=True)

    name              = Column(String(255), index=True)

    prep_code         = Column(Text)
    prep_fn           = Column(String(255))

    rounds            = Column(Text)

    loc_fn            = Column(String(255))
    loc_line          = Column(Integer)

    # __table_args__    = (Index('idx_tc_inp_lang', "inp", "lang"), )

class NERData(Base):

    __tablename__ = 'ner_data'

    id                = Column(Integer, primary_key=True)

    lang              = Column(String(2), index=True)
    module            = Column(String(255), index=True)

    cls               = Column(String(255))
    entity            = Column(Unicode(255))
    label             = Column(Unicode(255))

class NamedMacro(Base):

    __tablename__ = 'named_macro'

    id                = Column(Integer, primary_key=True)

    lang              = Column(String(2), index=True)
    module            = Column(String(255), index=True)

    name              = Column(String(255), index=True)

    soln              = Column(Text)

class Mem(Base):

    __tablename__ = 'mem'

    id                = Column(Integer, primary_key=True)

    realm             = Column(String(255), index=True)
    k                 = Column(String(255), index=True)
    v                 = Column(Text)
    score             = Column(Float)

    __table_args__    = (Index('idx_mem_realm_k', "realm", "k"), )


def data_engine_setup(db_url, echo=False):
    engine = create_engine(db_url, echo=echo)
    Base.metadata.create_all(engine)
    return engine

