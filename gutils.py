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
import random
import unittest
import subprocess

#
# guenters random hacks and utils
#

def detect_latin1 (fn):

    f = open(fn)

    l1ucnt = 0

    for line in f:

        for c in line:

            o = ord(c)
            if o == 0xc4 or o == 0xd6 or o == 0xdc or o == 0xe4 or o==0xf6 or o==0xfc or o==0xdf:
                l1ucnt += 1


    f.close()

    return l1ucnt > 1

def compress_ws (s):

        vc = False

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

def isgalnum (s):

    for c in s:
        if c.isalnum():
            continue

        if c == '%' or c ==u'§':
            continue

        return False

    return True


def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def split_words (s):

    res = []

    words = re.split ('\s+', s)
    for word in words:

        w = re.sub(r"[,.?\-! ;:]", '', word.rstrip()).upper()
        if len(w) > 0:
            res.append (w)

    return res

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


class TestGUtils (unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_latin1(self):
        self.assertTrue (detect_latin1('/home/ai/voxforge/de/audio/ralfherzog-20071220-de34/etc/prompts-original'))
        self.assertFalse (detect_latin1('/home/ai/voxforge/de/audio/mjw-20110527-dyg/etc/prompts-original'))

    def test_ws(self):
        self.assertEqual (compress_ws('   ws   foo bar'), ' ws foo bar')

    def test_editdist(self):
        self.assertEqual (edit_distance(
                             split_words(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT'), 
                             split_words(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT')), 0)
        self.assertEqual (edit_distance(
                             split_words(u'DIE LEISTUNG WURDE'), 
                             split_words(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT')), 1)
        self.assertEqual (edit_distance(
                             split_words(u'DIE LEISTUNG'), 
                             split_words(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT')), 2)
        self.assertEqual (edit_distance(
                             split_words(u'DIE'), 
                             split_words(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT')), 3)
        self.assertEqual (edit_distance(
                             split_words(u'DIE ZURÜCKVERLANGT'), 
                             split_words(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT')), 2)
        self.assertEqual (edit_distance(
                             split_words(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT'), 
                             split_words(u'LEISTUNG WURDE ZURÜCKVERLANGT')), 1)
        self.assertEqual (edit_distance(
                             split_words(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT'), 
                             split_words(u'WURDE ZURÜCKVERLANGT')), 2)
        self.assertEqual (edit_distance(
                             split_words(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT'), 
                             split_words(u'ZURÜCKVERLANGT')), 3)
        self.assertEqual (edit_distance(
                             split_words(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT'), 
                             split_words(u'')), 4)
        self.assertEqual (edit_distance(
                             split_words(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT'), 
                             split_words(u'LEISTUNG FOO ZURÜCKVERLANGT')), 2)
        self.assertEqual (edit_distance(
                             split_words(u'SIE IST FÜR DIE LEISTUNG DANKBAR'), 
                             split_words(u'SIE STRITTIG LEISTUNG DANKBAR')), 3)


if __name__ == "__main__":

    unittest.main()

