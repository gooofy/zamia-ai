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

#
# NLP stuff
#

class Document(Base):

    __tablename__ = 'documents'

    ref               = Column(String(255), primary_key=True)
    
    name              = Column(Unicode(255), index=True)
    doctype           = Column(Enum('col', 'doc', 'dlg', name='doctypes'), default='col', index=True)

    segments          = relationship("Segment", back_populates="doc", cascade="all, delete-orphan")

    def __unicode__(self):
        return self.name

class Segment(Base):

    __tablename__ = 'segments'

    id                = Column(Integer, primary_key=True)
    
    txt               = Column(UnicodeText, index=True)
    lang              = Column(String(2), index=True)
    participant       = Column(Integer, index=True) # for dialogs

    doc_ref           = Column(String(255), ForeignKey('documents.ref'))
    doc               = relationship("Document")

    ssms              = relationship("SegmentSemanticMap", back_populates="segment", cascade="all, delete-orphan")

# Semantics

class SemanticTerm(Base):

    __tablename__ = 'semantic_terms'

    term              = Column(String(255), primary_key=True)
    comment           = Column(UnicodeText)

class SegmentSemanticMap(Base):

    __tablename__ = 'seg_sem_map'

    id                = Column(Integer, primary_key=True)
    
    segment_id        = Column(Integer, ForeignKey('segments.id'))
    segment           = relationship("Segment")
    term_term         = Column(String(255), ForeignKey('semantic_terms.term'))
    term              = relationship("SemanticTerm")

# Speech
# 
# class Pronounciation(Base):
# 
#     __tablename__ = 'pronounciations'
# 
#     id                = Column(Integer, primary_key=True)
#     
#     token_txt         = Column(String(255), ForeignKey('tokens.txt'))
#     token             = relationship("Token")
#     ipa               = Column(Unicode(255))
#     priority          = Column(Integer)
#     lang              = Column(String(2))
# 
# class Speaker(Base):
# 
#     __tablename__ = 'speakers'
# 
#     name              = Column(Unicode(255), primary_key=True)
#     gender            = Column(Enum('male', 'female', 'unknown', name='genders'), default='unknown', index=True)
#     accent            = Column(Enum('none', 'mild', 'strong', 'unknown', name='accents'), default='unknown', index=True)
# 
# class Recording(Base):
# 
#     __tablename__ = 'recordings'
# 
#     fileref           = Column(String(255), primary_key=True)
# 
#     segment_id        = Column(Integer, ForeignKey('segments.id'))
#     segment           = relationship("Segment")
#     speaker_name      = Column(Unicode(255), ForeignKey('speakers.name'))
#     speaker           = relationship("Speaker")
# 
#     quality           = Column(Enum('high', 'low', 'bad', 'unknown', name='qualities'), default='unknown', index=True)
# 
# class RecordingPronounciationMap(Base):
# 
#     __tablename__ = 'rec_prn_map'
# 
#     id                = Column(Integer, primary_key=True)
#     
#     recording_id      = Column(String(255), ForeignKey('recordings.fileref'))
#     recording         = relationship("Recording")
#     idx               = Column(Integer)
#     pronounciation_id = Column(Integer, ForeignKey('pronounciations.id'))
#     pronounciation    = relationship("Pronounciation")

Base.metadata.create_all(engine)

def store_doc (session, ref, name, delete = True):

    doc = session.query(Document).filter(Document.ref==ref).first()

    if not doc:
        doc = Document (ref=ref, name=name)
        session.add(doc)

    else:

        if delete:

            session.delete(doc)

            doc = Document (ref=ref, name=name)
            session.add(doc)

    return doc

term_cache = {}

def add_segment (session, doc, txt, terms):

    global term_cache

    segment = Segment (txt=txt, lang='de', participant=0, doc=doc)
    session.add(segment)

    for t in terms:

        if not t in term_cache:

            term = session.query(SemanticTerm).filter(SemanticTerm.term == t).first()

            if not term:
                term = SemanticTerm(term=t)
                session.add(term)

            term_cache[t] = term
        else:
            term = term_cache[t]

        ssm = SegmentSemanticMap(segment=segment, term=term)
        session.add(ssm)

    return segment

