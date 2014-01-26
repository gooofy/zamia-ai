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

import curses
import pulseclient
import ctypes
import struct
import wave
import array
import re
import sys
import locale

def t_c (b):
    if b < 128:
        return b
    return -256 + b

def paint_wf():

    global recbuf_len, recbuf, stdscr

    # ASCII-paint waveform
   
    if recbuf_len > 0: 
        sx = 120.0 / (recbuf_len / 2)

        ox = -1
        min_s = 100000
        max_s = -100000

        for si in range (0, recbuf_len/2):

            lb = ord(recbuf[si*2    ])
            hb = ord(recbuf[si*2 + 1])
            sample = (t_c(hb) * 256 + t_c(lb))

            #logf.write ('lb: %02x, hb: %02x, sample: %d\n' % (lb, hb, sample))
            #logf.flush()

            if sample > max_s:
                max_s = sample
            if sample < min_s:
                min_s = sample

            x = int(si * sx)
            if x > ox:

                #stdscr.addstr ( 15, x, '-' )

                #logf.write ('max_s: %d, min_s: %d\n' % (max_s, min_s))
                #logf.flush()

                stdscr.addstr ( 15 + max_s / 3000, x, '*' )
                stdscr.addstr ( 15 + min_s / 3000, x, '*' )

                min_s = 100000
                max_s = -100000
                ox = x

if len(sys.argv) != 2:
    print 'usage: %s audiodir' % sys.argv[0]
    sys.exit(1)

audiodir = sys.argv[1]

#
# init curses
#

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
#locale.setlocale(locale.LC_ALL,"")

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

recorder = pulseclient.pulserecorder("HAL 9000")
player = pulseclient.pulseplayer("HAL 9000")

# 4 minutes max recording time
REC_BUF_LEN = 4 * 60 * 4800 *16

recbuf = ctypes.create_string_buffer(REC_BUF_LEN)
recbuf_len = 0

# bytes to skip at beginning and end of recording (eliminiate keyboard clicks)
TO_SKIP = 48000/5 * 2 # 1/5th of a second

# count lines

total_lines = 0
fp = open ("%s/etc/prompts-original" % audiodir)
for line in fp:
    total_lines += 1
fp.close()

#logf = open ('/tmp/t.log', 'w')

lc = 1
fp = open ("%s/etc/prompts-original" % audiodir)
for line in fp:
    
    m = re.match (r"^(\S+)\s+(.+)$", line.decode('utf8'))

    if not m:
        print u"ERROR: failed to parse line '%s'" % line
        sys.exit(1)
    
    fn = "%s/wav/%s.wav" % (audiodir, m.group(1))

    prompt = m.group(2)

    while True:

        stdscr.clear()
        stdscr.addstr (0, 0, "%3d/%3d : %-60s" % (lc, total_lines, fn), curses.A_NORMAL)
        stdscr.addstr (2, 10, prompt.encode('utf8'), curses.A_BOLD)

        paint_wf()

        stdscr.addstr (30, 0, "%-120s" % " R record   P playback   N next   Q quit", curses. A_REVERSE)
        stdscr.refresh()

        c = stdscr.getch()

        if c == ord('r'):

            stdscr.nodelay(1)

            recorder.start()

            recbuf_len = 0
            skip = TO_SKIP

            while True:

                res = recorder.record()

                if skip > 0:
                    skip -= res[0]
                    #stdscr.addstr (30,10, "    WAIT ... %8d                                               " % skip, curses.A_BOLD)
                    #stdscr.refresh ()
                    continue

                for i in range (res[0]):
                    recbuf[i + recbuf_len] = res[1][i]

                recbuf_len += res[0]

                seconds = recbuf_len / 48000 / 2

                stdscr.addstr (30,10, "    REC TIME: %03d s    ***  ANY KEY TO STOP RECORDING  ***    " % seconds, curses.A_BOLD)
                stdscr.refresh ()

                c = stdscr.getch()  
                if c != curses.ERR:
                    break

            stdscr.nodelay(0)
            recorder.stop()

            recbuf_len -= TO_SKIP
            if recbuf_len < 0:
                recbuf_len = 0

        elif c == ord('p'):

            player.play (recbuf, recbuf_len)


        elif c == ord('n'):

            if recbuf_len < 25:
                continue

            wav_file = wave.open(fn, "w")

            num_frames = recbuf_len 

            wav_file.setparams((1, 2, 48000, num_frames, 'NONE', 'not compressed'))

            samples = array.array('h')
            samples.fromstring (recbuf)

            #print "Number of samples total: %d, will write: %d" % (len(samples), num_frames)

            samples = samples [0:num_frames]

            wav_file.writeframes (samples)
            wav_file.close()

            #print "wav file written."
            #stdscr.getch()

            lc += 1
            recbuf_len = 0

            break

        elif c == ord('q'):
            curses.nocbreak(); stdscr.keypad(0); curses.echo()
            curses.endwin()

            print "Goodbye."
            print

            sys.exit(0)

curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()


