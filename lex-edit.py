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
import curses
import curses.textpad
import locale
import ConfigParser
from os.path import expanduser
from optparse import OptionParser
import xml.etree.ElementTree as ET
import httplib, urllib
import psycopg2
import traceback 

from phonetic_alphabets import ipa2xsampa, xsampa2ipa, mary2ipa, ipa2mary
from maryclient import maryclient, pulseplayer
from espeakclient import espeak_gen_ipa
from phonetisaurusclient import phonetisaurus_gen_ipa

#
# A simple, db-based lexicon editor
#
# based on Code from Hugh Sasse (maryclient-http.py)
#
# 2013, 2014 by G. Bartsch. License: LGPLv3
#

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

def mary_say_phonemes (phonemes):

    global mclient, player

    try:
        s = '<maryxml xmlns="http://mary.dfki.de/2002/MaryXML" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="0.5" xml:lang="de"><p><s><t g2p_method="lexicon" ph="%s" pos="NE"></t></s></p></maryxml>' % phonemes

        mclient.set_input_type("PHONEMES")
        mclient.set_output_type("AUDIO")
        wav = mclient.generate(s)

        player.play(wav)
    except:
        print "*** ERROR: unexpected error:", sys.exc_info()[0]
        traceback.print_exc()

def mary_gather_ph (parent):

	res = ""

	for child in parent:
		r = mary_gather_ph (child)
		if len(r) > 0:
			res += r + " "

	if 'ph' in parent.attrib:
		res += parent.attrib['ph'] + " "

	return compress_ws(res)


def mary_gen_phonemes (word):

    global mclient

    mclient.set_input_type ("TEXT")
    mclient.set_output_type ("PHONEMES")

    xmls = mclient.generate(word.lower())

    #print "Got: For %s %s" % (graph.encode('utf-8'), xmls)

    root = ET.fromstring(xmls)

    #print "ROOT: %s" % repr(root)

    mph = mary_gather_ph (root)

    return re.sub(u"^ \?", "", re.sub(u"^ ' \?", "'", mph))

def load_entry (word):

    global conn

    entry = { 'id': 0, 'word': word, 'occurences': 0, 'phonemes': [] }

    cur = conn.cursor()
    cur.execute ("SELECT id, occurences FROM words WHERE word=%s", (word,))

    row = cur.fetchone()
    if row:

        entry['id'] = row[0]    
        entry['occurences'] = row[1]

        cur.execute ("SELECT id, phonemes, probability, points FROM pronounciations WHERE wid=%s", (entry['id'],))

        rows = cur.fetchall()
        for row in rows:
            
            entry['phonemes'].append ( { 'id': row[0], 'phonemes': row[1].decode('UTF8'), 'probability': row[2], 'points': row[3] })

    cur.close()
         
    return entry
    
def store_entry (entry):

    global conn

    cur = conn.cursor()

    if entry['id'] == 0:
        cur.execute ("INSERT INTO words (word, occurences) VALUES (%s, 1) RETURNING id", (entry['word'],))
        entry['id'] = cur.fetchone()[0]

    for ph in entry['phonemes']:

        if ph['id'] == 0:
            cur.execute ("INSERT INTO pronounciations (phonemes, probability, points, wid) VALUES (%s,%s,%s,%s)", 
                         (ph['phonemes'], ph['probability'], ph['points'], entry['id']))
        else:
            cur.execute ("UPDATE pronounciations SET phonemes=%s, probability=%s, points=%s WHERE id=%s", 
                         (ph['phonemes'], ph['probability'], ph['points'], ph['id']))

    conn.commit()

    cur.close()


#
# main
#

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

#
# command line
#

parser = OptionParser("usage: %prog [options] word ...)")

#parser.add_option("-f", "--file", dest="filename",
#                  help="write report to FILE", metavar="FILE")

(options, args) = parser.parse_args()

if len(args)==0:
    print "ERROR: need at least one word!"
    print
    sys.exit(1)
    

#
# Mary / pulse init
#

mclient = maryclient()
mclient.set_locale ("de")
mclient.set_voice ("bits3")
#mclient.set_locale ("en")
#mclient.set_locale ("dfki-spike")

player = pulseplayer("HAL 9000")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

#
# curses
#

locale.setlocale(locale.LC_ALL,"")

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

#
# main loop
#

cur_word = 0
cur_phi = 0
word = args[cur_word].decode('UTF8').upper()
entry = load_entry (word)

def repaint_main():

    global stdscr, entry, cur_word, args, word

    stdscr.clear()

    s = u"%2d/%2d %-50s : lex-edit V 0.1" % (cur_word+1, len(args), word)

    stdscr.addstr(0, 0, s.encode('UTF8') )
    stdscr.addstr(1, 45, "    word id : %d" % entry['id'])
    stdscr.addstr(2, 45, " occurences : %d" % entry['occurences'])

    stdscr.addstr (4, 2, " #   Prob  Points  IPA                       MARY")
    phi = 0
    for ph in entry['phonemes']:
        
        y = phi + 5

        s = u"%2d: %4d%% %7d  %-25s %-25s" % (phi+1, ph['probability'], ph['points'], ph['phonemes'], ipa2xsampa(entry['word'], ph['phonemes']))
        stdscr.addstr (y, 2, s.encode("utf-8"))

        if phi == cur_phi:
            stdscr.addstr (y, 0, "**")

        phi += 1

    stdscr.addstr(20, 0, "Q:Quit  P:Play (unitsel)  O:Play (hsmm)  E:Edit  G:Gen(mary)  H:Gen(espeak)  J:Gen(saurus)  A: Add  1-9: Select  N:Next" )
    stdscr.refresh()

while 1:

    repaint_main()

    c = stdscr.getch()
    if c == ord('q'):
        break  

    elif c >= ord('1') and c <= ord('0') + len(entry['phonemes']):

        cur_phi = c - ord('1')

    elif c == ord('a'):
        
        mp = mary_gen_phonemes (entry['word'])
        #mary_say_phonemes (mp)

        #print "mp: %s" % mp

        ipas = mary2ipa(word, mp)

        entry['phonemes'].append ( { 'id': 0, 'phonemes': ipas, 'probability': 100, 'points': 10 }  )

        n = len(entry['phonemes'])

        p = 100 / n
        for e in entry['phonemes']:
            e['probability'] = p

    elif c == ord('g'):
        
        mp = mary_gen_phonemes (entry['word'])
        mary_say_phonemes (mp)

        #print "mp: %s" % mp

        ipas = mary2ipa(word, mp)

        if len(entry['phonemes']) == 0:

            entry['phonemes'].append ( { 'id': 0, 'phonemes': ipas, 'probability': 100, 'points': 10 }  )

        else:

            entry['phonemes'][cur_phi]['phonemes'] = ipas
            entry['phonemes'][cur_phi]['points'] = 10

    elif c == ord('h'):
        
        ipas = espeak_gen_ipa (entry['word'])
        mp = ipa2mary (entry['word'], ipas)
        mary_say_phonemes (mp)

        if len(entry['phonemes']) == 0:

            entry['phonemes'].append ( { 'id': 0, 'phonemes': ipas, 'probability': 100, 'points': 10 }  )

        else:

            entry['phonemes'][cur_phi]['phonemes'] = ipas
            entry['phonemes'][cur_phi]['points'] = 10

    elif c == ord('j'):
        
        ipas = phonetisaurus_gen_ipa (entry['word'])
        mp = ipa2mary (entry['word'], ipas)
        mary_say_phonemes (mp)

        if len(entry['phonemes']) == 0:

            entry['phonemes'].append ( { 'id': 0, 'phonemes': ipas, 'probability': 100, 'points': 10 }  )

        else:

            entry['phonemes'][cur_phi]['phonemes'] = ipas
            entry['phonemes'][cur_phi]['points'] = 10

    elif c == ord('p'):

        if len(entry['phonemes']) == 0:
            continue

        ipas = entry['phonemes'][cur_phi]['phonemes']

        xs = ipa2mary (word, ipas)

        mclient.set_voice ("bits3")
        mary_say_phonemes (xs)

    elif c == ord('o'):

        if len(entry['phonemes']) == 0:
            continue

        ipas = entry['phonemes'][cur_phi]['phonemes']

        xs = ipa2mary (word, ipas)

        mclient.set_voice ("dfki-pavoque-neutral-hsmm")
        mary_say_phonemes (xs)

    elif c == ord('n'):

        entry['phonemes'][cur_phi]['points'] = 10

        store_entry (entry)

        cur_word += 1
        if cur_word >= len(args):
            break
        else:
            word = args[cur_word].decode('UTF8').upper()
            cur_phi = 0
            entry = load_entry (word)

            if len(entry['phonemes']) == 0:

                # default: espeak
                ipas = espeak_gen_ipa (entry['word'])
                mp = ipa2mary (entry['word'], ipas)

                #mp = mary_gen_phonemes (entry['word'])
                #ipas = mary2ipa(word, mp)

                entry['phonemes'].append ({ 'id': 0, 'phonemes': ipas, 'probability': 100, 'points': 10 }  )
                repaint_main()

                mary_say_phonemes (mp)

    elif c == ord('e'):

        if len(entry['phonemes']) == 0:
            continue

        stdscr.addstr(14, 5, "X-Sampa:" )
        win = curses.newwin(1, 60, 15, 5)
        tb = curses.textpad.Textbox(win, insert_mode=True)

        xs = ipa2xsampa (word, entry['phonemes'][cur_phi]['phonemes'])
        win.addstr (0, 0, xs)
        stdscr.refresh()

        xs = tb.edit()

        ipas = xsampa2ipa (word, xs)

        entry['phonemes'][cur_phi]['phonemes'] = ipas


#
# fini
#

curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()


