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

import sys
import re
import os
import StringIO
import ConfigParser
from os.path import expanduser
from gutils import detect_latin1, isgalnum, compress_ws, split_words, edit_distance, tex_decode, tex_encode 
import random
import datetime
import psycopg2
from phonetic_alphabets import ipa2xsampa, xsampa2ipa, xsampa2xarpabet
import locale
import curses
import curses.textpad
import traceback

#
# interactively align prompts of audiobook part
#

REALIGN_JITTER = 20

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

wdir      = config.get("speech", "workdir") 
workdir   = config.get("speech", "workdir") + "/align"
abook_dir = config.get("speech", "abookdir")
audiodir  = config.get("speech", "audiodir")

#
# init
#

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

#
# command line
#

if len(sys.argv) != 3:
    print "usage: %s title partnum" % sys.argv[0]
    sys.exit(1)

abook_title  = sys.argv[1]
abook_part   = int(sys.argv[2])

promptfn = '%s/%s/prompts/part%02d.txt' % (abook_dir, abook_title, abook_part)

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# fetch cfn for this abook part from db
#

cur.execute ('SELECT cfn FROM abooks WHERE title=%s AND partnum=%s', (abook_title, abook_part))
row = cur.fetchone()

dir_name = row[0].decode('utf8')
dir_path = '%s/%s' % (audiodir, dir_name)

promptsfn  = "%s/etc/PROMPTS" % (dir_path)
opromptsfn = "%s/etc/prompts-original" % (dir_path)

#
# read all lines from prompts file, create long list of words
#

print "reading %s ..." % promptfn

words = []

promptf = open (promptfn)
for line in promptf:
    prompt = line.decode('UTF8').rstrip()
    ws = split_words(prompt)
    for word in ws:
        words.append(word)

promptf.close()

print "done. %d words." % len(words)

cur_cut = 0
cur_wav = -1

def next_wav():
    global cur_cut, cur_wav, cur, words, cur_len, cur_prompt
    global wfn, wavfn, cur_cfn

    while True:
        cur_wav += 1

        cur.execute ('SELECT audiofn, reviewed, prompt, cfn FROM submissions WHERE dir=%s ORDER BY cfn ASC LIMIT 1 OFFSET %s', (dir_name, cur_wav))
        row = cur.fetchone()

        if not row:
            return False    

        audiofn  = row[0].decode('utf8')
        reviewed = row[1]
        prompt   = row[2].decode('utf8')
        cur_cfn  = row[3].decode('utf8')

        print "next_wav: %3d %s" % (cur_wav, audiofn)

        if reviewed:

            # adjust base_offset, allow for minor deviations
    
            p1 = split_words(prompt)
            min_dist = 10000
            min_offset = cur_cut
            for offset in range (cur_cut - REALIGN_JITTER, cur_cut + REALIGN_JITTER):
                if offset<0:
                    continue
    
                p2 = words[offset:offset+len(p1)]
                dist = edit_distance(p1, p2)
                if dist<min_dist:
                    min_dist = dist
                    min_offset = offset
    
                print "offset adjustment: %5d %s vs %s" % (dist, ' '.join(p1), ' '.join(p2))
    
            cur_cut = min_offset + len(p1)

            continue

        wfn = audiofn + ".wav"
        wavfn = '%s/wav/%s' % (dir_path, wfn)

        cur_len    = 1
        cur_prompt = ' '.join(words[cur_cut:cur_cut+cur_len])


        break

    return True


if not next_wav():
    print "No non-reviewed submissions found. Exiting."
    print
    sys.exit(1)

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

c = 0

try:
    while True:
   
        #
        # repaint screen
        #
    
        stdscr.clear()
    
        s = u"%2d %-50s %d : abook-align V 0.1" % (cur_wav+1, wfn, c)
    
        stdscr.addstr(0, 0, s.encode('UTF8') )

        stdscr.addstr(3, 0, 'current prompt:' )
        stdscr.addstr(4, 5, cur_prompt.encode('UTF8') )

        stdscr.addstr(7, 0, 'next words:' )
        nw = ' '.join(words[cur_cut+cur_len:cur_cut+cur_len+5])
        stdscr.addstr(8, 5, nw.encode('UTF8') )

    
        stdscr.addstr(20, 0, "Q:Quit  P:Play  E:Edit  Space:Add  R:Remove  N:Next  B:Back" )
        stdscr.refresh()
    
    
        #
        # handle command
        #
    
        c = stdscr.getch()
        if c == ord('q'):
            break  
        
        elif c == ord('p'):
            os.system ('play -q %s &' % wavfn)
   
        elif c == ord(' '):
            if cur_cut+cur_len < len(words):
                cur_len += 1
            cur_prompt = ' '.join(words[cur_cut:cur_cut+cur_len])

        elif c == ord('r'):
            if cur_len > 1:
                cur_len -= 1
            cur_prompt = ' '.join(words[cur_cut:cur_cut+cur_len])

        elif c == ord('n'):

            cur.execute ('UPDATE submissions SET prompt=%s WHERE cfn=%s', (cur_prompt, cur_cfn))
            conn.commit()
            cur = conn.cursor()

            cur_cut += cur_len
            cur_len  = 1

            if not next_wav():
                break

            os.system ('play -q %s &' % wavfn)
  
        elif c == ord('e'):
            stdscr.addstr(14, 0, "Edit prompt:" )

            tstr = tex_encode(cur_prompt)

            win = curses.newwin(1, len(tstr)+12, 15, 0)
            tb = curses.textpad.Textbox(win, insert_mode=True)

            win.addstr (0, 0, tstr)
            stdscr.refresh()

            cur_prompt = tex_decode(tb.edit())

        elif c == ord(','):
            if cur_cut > 0 :
                cur_cut -= 1

            cur_prompt = ' '.join(words[cur_cut:cur_cut+cur_len])

        elif c == ord('.'):
            if cur_cut < len(words) :
                cur_cut += 1

            cur_prompt = ' '.join(words[cur_cut:cur_cut+cur_len])

    #
    # fini
    #

    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()
 
except:
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()

    print u"*** ERROR: Unexpected error:", sys.exc_info()[0]
    traceback.print_exc()
    #raise

