#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2013, 2014 Guenter Bartsch
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

import StringIO
import re
import sys
import locale

import xml.etree.ElementTree as ET
import httplib, urllib
import psycopg2
import ConfigParser

from os.path import expanduser

from phonetic_alphabets import ipa2xsampa, xsampa2ipa, mary2ipa, ipa2mary
from maryclient import maryclient

#
# feed back correct pronounciations from our db to Mary TTS via userdict
#
# 2013 by G. Bartsch. License: LGPLv3
#
#
# Usage:
#
# - stop mary tts
# - put in empty $MARYTTS/user-dictionaries/userdict-de.txt
# - start mary tts
# - run this script
# - stop mary tts
# - cp output/userdict-de.txt to $MARYTTS/user-dictionaries/userdict-de.txt
# - start mary tts


#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

db_server = config.get("speech", "dbserver")
db_name   = config.get("speech", "dbname")
db_user   = config.get("speech", "dbuser")
db_pass   = config.get("speech", "dbpass")

OUTFILENAME = "output/userdict-de.txt"

def compress_ws (str):

        vc = False

        res = ''

        for c in str:

                if c == ' ':
                        vc = False
                else:
                        if vc:
                                res = res + c
                        else:
                                res = res + ' ' + c
                        vc = True

        return res 

def mary_gather_ph (parent):

	res = ""

	for child in parent:
		r = mary_gather_ph (child)
		if len(r) > 0:
			res += r + " "

	if 'ph' in parent.attrib:
		res += parent.attrib['ph'] + " "

	return compress_ws(res)

def mary_strip_phonemes (mph):

    stripped = re.sub(u"^ \?", "", re.sub(u"^ ' \?", "'", mph))
    stripped = re.sub(u"^\?", "", re.sub(u"^'\?", "'", stripped))

    #print "strip: %s => %s" % (repr(mph), repr(stripped))

    return stripped


def mary_gen_phonemes (word):

    global mclient

    mclient.set_input_type ("TEXT")
    mclient.set_output_type ("PHONEMES")

    xmls = mclient.generate(word.lower())

    #print "Got: For %s %s" % (graph.encode('utf-8'), xmls)

    root = ET.fromstring(xmls)

    #print "ROOT: %s" % repr(root)

    mph = mary_gather_ph (root)

    return mary_strip_phonemes (mph)


#
# main
#

#
# Mary / pulse init
#

mclient = maryclient()
mclient.set_locale ("de")
mclient.set_voice ("bits3")
#mclient.set_locale ("en")
#mclient.set_locale ("dfki-spike")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

#
# iterate over all existing pronounciations in db
# compare to mary-generated pronounciations
# when different, add correct pronounciation to user dict
#

cur = conn.cursor()
cur.execute ("SELECT phonemes, grapheme_id FROM pronounciations WHERE points>5")

out = open (OUTFILENAME, 'w')

# single pre-existing entry
out.write ('Sathish | \' s a - t I S\n')

count = 0
diffs = 0

rows = cur.fetchall()
for row in rows:

    count += 1

    ipa = row[0].decode('UTF8')
    gid = row[1]

    cur.execute ("SELECT grapheme FROM graphemes WHERE id = %s", (gid,))

    row2 = cur.fetchone()

    if not row2:
        continue

    word = row2[0].decode('UTF8')

    mary_gen = mary_gen_phonemes (word)

    # strip formatting/ws
    mary_gen = ipa2mary(word, mary2ipa (word, mary_gen))

    mary_conv = mary_strip_phonemes(ipa2mary (word, ipa))

    if mary_gen == mary_conv:
        #print "%3d%% %-16s SAME" % (count * 100 / len(rows), word)
        continue

    print "%3d%% %-16s DB   %s " % (count * 100 / len(rows), word, mary_conv)
    print "                      MARY %s " % (mary_gen)

    out.write ("%s | %s\n" % (word.lower().encode('UTF8'), mary_conv))
    diffs +=1

out.close()

print
print "%s: %d entries written." % (OUTFILENAME, diffs)
print

