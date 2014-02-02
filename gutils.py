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

# word replacement table
wrt = { u'0'     : u'NULL',
        u'1'     : u'EINS', 
        u'10'    : u'ZEHN',
        u'10%'   : u'ZEHN PROZENT',
        u'100%'  : u'HUNDERT PROZENT',
        u'1000'  : u'TAUSEND',
        u'11'    : u'ELF',
        u'12'    : u'ZWÖLF',
        u'128'   : u'HUNDERTACHTUNDZWANZIG',
        u'13'    : u'DREIZEHN',
        u'132'   : u'HUNDERTZWEIUNDREIßIG',
        u'137'   : u'HUNDERTSIEBENUNDDREIßIG',
        u'14'    : u'VIERZEHN',
        u'15'    : u'FÜNFZEHN',
        u'16'    : u'SECHZEHN',
        u'160'   : u'HUNDERTSECHZIG',
        u'17'    : u'SIEBZEHN',
        u'18'    : u'ACHZEHN',
        u'186'   : u'HUNDERTSECHSUNDACHZIG',
        u'19'    : u'NEUNZEHN',
        u'1949'  : u'NEUNZEHNHUNDERTNEUNUNDVIERZIG',
        u'1960ER': u'NEUNZEHNHUNDERTSECHZIGER',
        u'1970ER': u'NEUNZEHNHUNDERTSIEBZIGER',
        u'1970ERJAHREN': u'NEUNZEHNHUNDERTSIEBZIGER JAHREN',
        u'1977'  : u'NEUNZEHNHUNDERTSIEBENUNDSIEBZIG',
        u'1979'  : u'NEUNZEHNHUNDERTNEUNUNDSIEBZIG',
        u'1980ER': u'NEUNZEHNHUNDERTACHZIGER',
        u'1983'  : u'NEUNZEHNHUNDERTDREIUNDACHZIG',
        u'1984'  : u'NEUNZEHNHUNDERTVIERUNDACHZIG',
        u'1989'  : u'NEUNZEHNHUNDERTNEUNUNDACHZIG',
        u'1990'  : u'NEUNZEHNHUNDERTNEUNZIG',
        u'1990ER': u'NEUNZEHNHUNDERTNEUNZIGER',
        u'1991'  : u'NEUNZEHNHUNDERTEINUNDNEUNZIG',
        u'1993'  : u'NEUNZEHNHUNDERTDREIUNDNEUNZIG',
        u'1998'  : u'NEUNZEHNHUNDERTACHTUNDNEUNZIG',
        u'2'     : u'ZWEI', 
        u'2%'    : u'ZWEI PROZENT', 
        u'20'    : u'ZWANZIG',
        u'200'   : u'ZWEIHUNDERT',
        u'2000'  : u'ZWEITAUSEND',
        u'20000' : u'ZWANZIGTAUSEND',
        u'2002'  : u'ZWEITAUSENDZWEI',
        u'2004'  : u'ZWEITAUSENDVIER',
        u'2005'  : u'ZWEITAUSENDFÜNF',
        u'204'   : u'ZWEIHUNDERTVIER',
        u'21'    : u'EINUNDZWANZIG',
        u'226'   : u'ZWEIHUNDERTSECHSUNDZWANZIG',
        u'23'    : u'DREIUNDZWANZIG',
        u'24'    : u'VIERUNDZWANZIG',
        u'242'   : u'ZWEIHUNDERTZWEIUNDVIERZIG',
        u'25'    : u'FÜNFUNDZWANZIG', 
        u'250'   : u'ZWEIHUNDERTFÜNFZIG',
        u'253'   : u'ZWEIHUNDERTDREIUNDFÜNFZIG',
        u'254'   : u'ZWEIHUNDERTVIERUNDFÜNFZIG',
        u'3'     : u'DREI', 
        u'30'    : u'DREIßIG',
        u'32'    : u'ZWEIUNDDREIßIG',
        u'328'   : u'DREIHUNDERTACHTUNDZWANZIG',
        u'35'    : u'FÜNFUNDDREIßIG',
        u'4'     : u'VIER', 
        u'40%'   : u'VIERZIG PROZENT', 
        u'400'   : u'VIERHUNDERT', 
        u'4096'  : u'VIERTAUSENDSECHSUNDNEUNZIG', 
        u'418'   : u'VIERHUNDERTACHTZEHN', 
        u'42'    : u'ZWEIUNDVIERZIG',
        u'43'    : u'DREIUNDVIERZIG',
        u'5'     : u'FÜNF', 
        u'50'    : u'FÜNFZIG', 
        u'500000': u'FÜNFHUNDERTTAUSEND', 
        u'57'    : u'SIEBENUNDFÜNFZIG', 
        u'6'     : u'SECHS', 
        u'63'    : u'DREIUNDSECHZIG', 
        u'7'     : u'SIEBEN',
        u'75'    : u'FÜNFUNDSIEBZIG',
        u'8'     : u'ACHT',
        u'80'    : u'ACHTZIG',
        u'80%'   : u'ACHTZIG PROZENT',
        u'800'   : u'ACHTHUNDERT',
        u'80ER'  : u'ACHTZIGER',
        u'850'   : u'ACHTHUNDERTFÜNFZIG',
        u'852'   : u'ACHTHUNDERTZWEIUNDFÜNFZIG',
        u'9'     : u'NEUN',
        u'90'    : u'NEUNZIG',
        u'95'    : u'FÜNFUNDNEUNZIG',
        u'99'    : u'NEUNUNDNEUNZIG',
        u'100'   : u'HUNDERT',
        u'§'     : u'PARAGRAPH' }

def split_words (s):

    global wrt

    res = []

    words = re.split ('\s+', s)
    for word in words:

        w = re.sub(r"[,.?\-+*#! ;:/\"\[\]()=]", '', word.rstrip()).upper()
        if len(w) > 0:

            if w in wrt:
                w = wrt[w]

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

def kill_umlauts(s):
    return s.replace(u'ß',u'SS').replace(u'Ü',u'UE').replace(u'Ö',u'OE').replace(u'Ä',u'AE').replace(u'§', 'PARAGRAPH').replace('%','PROZENT').replace('-','STRICH').replace("'",'')

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

