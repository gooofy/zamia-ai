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
import os
import ConfigParser
import errno
import shutil
import subprocess
import curses
import curses.textpad

from os.path import expanduser

def load_config():

    home_path = expanduser("~")

    config = ConfigParser.RawConfigParser()
    config.read("%s/%s" % (home_path, ".nlprc"))

    return config

def compress_ws (s):

    vc = True

    res = ''

    for c in s:

        if c == ' ':
            vc = False
        else:
            if vc:
                res = res + c
            else:
                res = res + ' ' + c
            vc = True

    return res

# FIXME: remove here (moved to speech_tokenizer)
# def tokenize (s):
# 
#     # FIXME: very crude.
# 
#     tokens = []
#     for t in s.replace('?', ' ').replace('!', ' ').replace(',', ' ').replace('.', ' ').lower().split(' '):
#         if len(t) == 0:
#             continue
#         tokens.append(t)
# 
#     return tokens

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

def symlink(targetfn, linkfn):
    try:
        os.symlink(targetfn, linkfn)
    except OSError, e:
        if e.errno == errno.EEXIST:
            print 'symlink', targetfn, '->', linkfn, 'already exists'

def mkdirs(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def copy_file (src, dst):
    print "copying %s to %s" % (src, dst)
    shutil.copy(src, dst)

def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def edit_distance (s, t):
    # https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm

    # for all i and j, d[i,j] will hold the Levenshtein distance between
    # the first i words of s and the first j words of t;
    # note that d has (m+1)x(n+1) values
    
    m = len(s)
    n = len(t)

    d = [[0 for i in range(n+1)] for j in range(m+1)]

    for i in range (m+1):
        d[i][0] = i                        # the distance of any first seq to an empty second seq
    for j in range (n+1):
        d[0][j] = j                         # the distance of any second seq to an empty first seq
  
    for j in range (1, n+1):
        for i in range (1, m+1):

            if s[i-1] == t[j-1]:
                d[i][j] = d[i-1][j-1]       # no operation required
            else:
                d[i][j] = min ([
                            d[i-1][j] + 1,       # a deletion
                            d[i][j-1] + 1,       # an insertion
                            d[i-1][j-1] + 1      # a substitution
                         ])
  
    return d[m][n]

#
# curses utils
#

def edit_popup (stdscr, title, s):

    my, mx = stdscr.getmaxyx()

    ww = mx * 9 / 10
    wh = 3

    wox = mx / 2 - ww/2
    woy = my / 2 - wh/2

    win = curses.newwin(wh, ww, woy, wox)
    win.box()
    win.addstr(0, 3, title)

    win.refresh()

    swin = win.derwin (1, ww-4, 1, 2)

    tb = curses.textpad.Textbox(swin, insert_mode=True)

    swin.insstr (0, 0, tex_encode(s))

    swin.refresh()

    s = tex_decode(tb.edit())

    return s.rstrip()

