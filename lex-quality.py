#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import re
import os
import StringIO
import ConfigParser
from os.path import expanduser
import subprocess
import psycopg2
import traceback

from phonetic_alphabets import ipa2xsampa, xsampa2ipa, xsampa2xarpabet, mary2ipa
from gutils import split_words

from maryclient import mary_say_phonemes, mary_gather_ph, mary_gen_phonemes, mary_init, mary_set_voice
from espeakclient import espeak_gen_ipa
from phonetisaurusclient import phonetisaurus_gen_ipa

#
# check lexicon entries, generate a list of those that do not meet our standards. 
# Each entry must contain:
#  
# - at least one emphasis marker (')
# - at least one hyphen unless the whole entry is shorter than 6 phonemes


#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

webroot   = config.get("speech", "webroot")

db_server = config.get("speech", "dbserver")
db_name   = config.get("speech", "dbname")
db_user   = config.get("speech", "dbuser")
db_pass   = config.get("speech", "dbpass")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

cur.execute ("SELECT phonemes,word,words.id,pronounciations.id FROM pronounciations,words WHERE pronounciations.wid=words.id AND pronounciations.points < 11 ORDER BY word ASC")
rows = cur.fetchall()
for row in rows:

    ipas = row[0].decode('UTF8')
    word = row[1].decode('UTF8')
    wid  = row[2]
    pid  = row[3]

    if ( (ipas.count(u'-') > 0) or (len(ipas)<4) ) and (ipas.count(u"'") > 0):
        continue

    #print wid, pid, ipas
    #print ipas.count(u'-')

    print (u"%s " % word).encode('utf8'),

