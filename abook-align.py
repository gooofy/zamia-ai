#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2014 Guenter Bartsch
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
from gutils import detect_latin1, isgalnum, compress_ws, split_words
import random
import datetime
import curses
import curses.textpad
import locale
import traceback
from phonetic_alphabets import ipa2xsampa, xsampa2ipa, xsampa2xarpabet

tex_umlaut_map = { u'ä': '"a', u'ü': '"u', u'ö': '"o', u'Ä':'"A', u'Ü':'"U', u'Ö':'"O', u'ß':'"s' }

def tex_encode (u):

    s = ''

    for c in u:

        if c in tex_umlaut_map:
            s += tex_umlaut_map[c]
        else:
            s += str(c)

    return s

def tex_decode (s):

    u = ''

    pos = 0
    while (pos < len(s)):

        found = False

        for umlaut in tex_umlaut_map:
            v = tex_umlaut_map[umlaut]
            if s[pos:].startswith(v):
                u += umlaut
                pos += len(v)
                found = True
                break

        if not found:
            u += unicode(s[pos])
            pos += 1

    return u

#
# command line
#

if len(sys.argv) != 3:
    print "usage: %s dir prompt.txt" % sys.argv[0]
    sys.exit(1)

dir_path = sys.argv[1]
dir_name = os.path.basename(dir_path)

promptfn = sys.argv[2]

#
# read existing prompts, init history
#

promptsfn  = "%s/etc/PROMPTS" % (dir_path)
opromptsfn = "%s/etc/prompts-original" % (dir_path)

cur_cut = 0
cur_wav = 0

history = []

if os.path.isfile(opromptsfn):
    for line in open(opromptsfn, 'r'):

        l = line.decode('utf8').rstrip()

        p = l[9:]

        print cur_cut, repr(split_words(p))

        history.append ( (cur_cut, p) )

        cur_cut += len (split_words(p))
        cur_wav += 1

promptsf  = open(promptsfn, 'a')
opromptsf = open(opromptsfn, 'a')

#
# ordered list of words from prompt file
#

words = []

for line in open (promptfn):
    for w in split_words(line.decode('utf8')):
        words.append(w)

#print repr(words)

#
# ordered list of wav files to work on
#

wav_files = sorted(os.listdir('%s/wav/' % dir_path))


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

cur_len    = 1

cur_prompt = ' '.join(words[cur_cut:cur_cut+cur_len])

c = 0

try:
    while cur_wav < len(wav_files):
   
        wfn = wav_files[cur_wav] 
        wavfn = '%s/wav/%s' % (dir_path, wfn)

        #
        # repaint screen
        #
    
        stdscr.clear()
    
        s = u"%2d/%2d %-50s %d : abook-align V 0.1" % (cur_wav+1, len(wav_files), wfn, c)
    
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

            promptsf.write ( (u'%s/mfc/%s %s\n' % (dir_name, wfn[0:len(wfn)-4], cur_prompt) ).encode('utf8') )
            promptsf.flush()

            opromptsf.write ( (u'%s %s\n' % (wfn[0:len(wfn)-4], cur_prompt) ).encode('utf8') )
            opromptsf.flush()

            history.append ( (cur_cut, cur_prompt) )

            cur_wav   +=1

            if cur_wav >= len(wav_files):
                break

            cur_cut   += cur_len
            cur_len    = 1
            cur_prompt = ' '.join(words[cur_cut:cur_cut+cur_len])

            wfn = wav_files[cur_wav] 
            wavfn = '%s/wav/%s' % (dir_path, wfn)

            os.system ('play -q %s &' % wavfn)
  
        elif c == ord('b'):

            if cur_wav > 0:
                cur_wav   -= 1

                prev_cut = history[cur_wav][0]

                cur_len  = cur_cut - prev_cut
                cur_cut -= cur_len

                cur_prompt = ' '.join(words[cur_cut:cur_cut+cur_len])
                history.pop()
                
            # re-write prompts files
            promptsf.close()
            promptsf  = open(promptsfn, 'w')
            opromptsf.close()
            opromptsf  = open(opromptsfn, 'w')

            for i in range (cur_wav):

                wfn = wav_files[i] 
                p   = history[i][1]

                promptsf.write ( (u'%s/mfc/%s %s\n' % (dir_name, wfn[0:len(wfn)-4], p) ).encode('utf8') )
                promptsf.flush()

                opromptsf.write ( (u'%s %s\n' % (wfn[0:len(wfn)-4], p) ).encode('utf8') )
                opromptsf.flush()

        elif c == ord('e'):
            stdscr.addstr(14, 0, "Edit prompt:" )
            win = curses.newwin(1, 180, 15, 0)
            tb = curses.textpad.Textbox(win, insert_mode=True)

            win.addstr (0, 0, tex_encode(cur_prompt))
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


