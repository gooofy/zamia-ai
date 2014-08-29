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
        u'1200'  : u'ZWÖLFHUNDERT',
        u'128'   : u'HUNDERTACHTUNDZWANZIG',
        u'13'    : u'DREIZEHN',
        u'132'   : u'HUNDERTZWEIUNDDREIßIG',
        u'137'   : u'HUNDERTSIEBENUNDDREIßIG',
        u'14'    : u'VIERZEHN',
        u'15'    : u'FÜNFZEHN',
        u'16'    : u'SECHZEHN',
        u'160'   : u'HUNDERTSECHZIG',
        u'17'    : u'SIEBZEHN',
        u'170'   : u'HUNDERTSIEBZIG',
        u'1700'  : u'SIEBZEHNHUNDERT',
        u'18'    : u'ACHTZEHN',
        u'1825'  : u'ACHTZEHNHUNDERTFÜNFUNDZWANZIG',
        u'186'   : u'HUNDERTSECHSUNDACHTZIG',
        u'19'    : u'NEUNZEHN',
        u'1949'  : u'NEUNZEHNHUNDERTNEUNUNDVIERZIG',
        u'1960ER': u'NEUNZEHNHUNDERTSECHZIGER',
        u'1970ER': u'NEUNZEHNHUNDERTSIEBZIGER',
        u'1970ERJAHREN': u'NEUNZEHNHUNDERTSIEBZIGER JAHREN',
        u'1977'  : u'NEUNZEHNHUNDERTSIEBENUNDSIEBZIG',
        u'1979'  : u'NEUNZEHNHUNDERTNEUNUNDSIEBZIG',
        u'1980ER': u'NEUNZEHNHUNDERTACHTZIGER',
        u'1983'  : u'NEUNZEHNHUNDERTDREIUNDACHTZIG',
        u'1984'  : u'NEUNZEHNHUNDERTVIERUNDACHTZIG',
        u'1989'  : u'NEUNZEHNHUNDERTNEUNUNDACHTZIG',
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
        u'2150'  : u'ZWEITAUSENDEINHUNDERTFÜNFZIG',
        u'2310'  : u'ZWEITAUSENDDREIHUNDERTZEHN',
        u'204'   : u'ZWEIHUNDERTVIER',
        u'21'    : u'EINUNDZWANZIG',
        u'226'   : u'ZWEIHUNDERTSECHSUNDZWANZIG',
        u'22'    : u'ZWEIUNDZWANZIG',
        u'23'    : u'DREIUNDZWANZIG',
        u'24'    : u'VIERUNDZWANZIG',
        u'242'   : u'ZWEIHUNDERTZWEIUNDVIERZIG',
        u'25'    : u'FÜNFUNDZWANZIG', 
        u'28'    : u'ACHTUNDZWANZIG', 
        u'250'   : u'ZWEIHUNDERTFÜNFZIG',
        u'253'   : u'ZWEIHUNDERTDREIUNDFÜNFZIG',
        u'254'   : u'ZWEIHUNDERTVIERUNDFÜNFZIG',
        u'3'     : u'DREI', 
        u'30'    : u'DREIßIG',
        u'300'   : u'DREIHUNDERT',
        u'32'    : u'ZWEIUNDDREIßIG',
        u'33'    : u'DREIUNDDREIßIG',
        u'328'   : u'DREIHUNDERTACHTUNDZWANZIG',
        u'35'    : u'FÜNFUNDDREIßIG',
        u'4'     : u'VIER', 
        u'40%'   : u'VIERZIG PROZENT', 
        u'400'   : u'VIERHUNDERT', 
        u'4000'  : u'VIERTAUSEND', 
        u'4096'  : u'VIERTAUSENDSECHSUNDNEUNZIG', 
        u'418'   : u'VIERHUNDERTACHTZEHN', 
        u'42'    : u'ZWEIUNDVIERZIG',
        u'43'    : u'DREIUNDVIERZIG',
        u'45'    : u'FÜNFUNDVIERZIG', 
        u'5'     : u'FÜNF', 
        u'50'    : u'FÜNFZIG', 
        u'55'    : u'FÜNFUNDFÜNFZIG', 
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
        u'DAß'           : u'DASS',
        u'HAß'           : u'HASS',
        u'GROSS'         : u'GROß',
        u'GROSSE'        : u'GROßE',
        u'GROSSEN'       : u'GROßEN',
        u'GROSSES'       : u'GROßES',
        u'FAßTE'         : u'FASSTE',
        u'GEFAßT'        : u'GEFASST',
        u'EINGEFAßTE'    : u'EINGEFASSTE',
        u'BIßCHEN'       : u'BISSCHEN',
        u'BLAß'          : u'BLASS',
        u'BLAßBLAUEN'    : u'BLASSBLAUEN',
        u'BLÄßLICH'      : u'BLÄSSLICH',
        u'ENTSCHLUß'     : u'ENTSCHLUSS',
        u'EßSTUBE'       : u'ESSSTUBE',
        u'EßTISCH'       : u'ESSTISCH',
        u'EßZIMMER'      : u'ESSZIMMER',
        u'GEPREßT'       : u'GEPRESST',
        u'GEWIß'         : u'GEWISS',
        u'KÜßTE'         : u'KÜSSTE',
        u'KÜßTEN'        : u'KÜSSTEN',
        u'LAß'           : u'LASS',
        u'LÄßT'          : u'LÄSST',
        u'MIßVERGNÜGT'   : u'MISSVERGNÜGT',
        u'MIßVERSTÄNDNIS': u'MISSVERSTÄNDNIS',
        u'MÜßTE'         : u'MÜSSTE',
        u'PAß'           : u'PASS',
        u'PAßT'          : u'PASST',
        u'PREßTE'        : u'PRESSTE',
        u'PHOTO'         : u'FOTO',
        u'RIß'           : u'RISS',
        u'SCHLOß'        : u'SCHLOSS',
        u'SCHLUß'        : u'SCHLUSS',
        u'TELEPHON'      : u'TELEFON',
        u'TOTENBLAß'     : u'TOTENBLASS',
        u'VERMIßTE'      : u'VERMISSTE',
        u'VERMIßT'       : u'VERMISST',
        u'PHANTASIE'     : u'FANTASIE',
        u'PHANTASIEREN'  : u'FANTASIEREN',
        u'PHANTASTEREIEN': u'FANTASTEREIEN',
        u'MIKROPHON'     : u'MIKROFON',
        u'MIKROPHONE'    : u'MIKROFONE',
        u'WÜßTE'         : u'WÜSSTE',
        u'WUßTE'         : u'WUSSTE',
        u'WUßTEN'        : u'WUSSTEN',
        u'MUß'           : u'MUSS',
        u'MUßT'          : u'MUSST',
        u'MUßTE'         : u'MUSSTE',
        u'BEWUßT'        : u'BEWUSST',
        u'UNBEWUßT'      : u'UNBEWUSST',
        u'GEWUßT'        : u'GEWUSST',
        u'BEWUßTE'       : u'BEWUSSTE',
        u'BEWUßTEN'      : u'BEWUSSTEN',
        u'ZIELBEWUßTE'   : u'ZIELBEWUSSTE',
        u'SIEGESGEWIß'   : u'SIEGESGEWISS',
        u'ZERRIß'        : u'ZERRISS',
        u'§'             : u'PARAGRAPH'}


symb_abbrev_norm = [
        (u'Abk.'    , u'ABKÜRZUNG '),
        (u'Abk '    , u'ABKÜRZUNG '),
        (u'Prof.'   , u'PROFESSOR '),
        (u'Dipl.'   , u'DIPLOM '),
        (u'Ing.'    , u'INGENIEUR '),
        (u'Inf.'    , u'INFORMATIKER '),
        (u'Inform.' , u'INFORMATIKER '),
        (u'Tel.'    , u'TELEFON '),
        (u'bzw.'    , u'BEZIEHUNGSWEISE '),
        (u'bzw '    , u'BEZIEHUNGSWEISE '),
        (u'bspw.'   , u'BEISPIELSWEISE '),
        (u'bspw '   , u'BEISPIELSWEISE '),
        (u'bzgl.'   , u'BEZÜGLICH '),
        (u'ca.'     , u'CIRCA '),
        (u'ca '     , u'CIRCA '),
        (u'd.h.'    , u'DAS HEIßT '),
        (u'd. h.'   , u'DAS HEIßT '),
        (u'Dr. '    , u'DOKTOR '),
        (u'evtl.'   , u'EVENTUELL '),
        (u'evtl '   , u'EVENTUELL '),
        (u'geb.'    , u'GEBORENE '),
        (u'ggf.'    , u'GEGEBENENFALLS '),
        (u'ggf '    , u'GEGEBENENFALLS '),
        (u'kath.'   , u'KATHOLISCHE '),
        (u'Hrsg.'   , u'HERAUSGEBER '),
        (u'Mr.'     , u'MISTER '),
        (u'Mrd.'    , u'MILLIARDEN '),
        (u'Mrs.'    , u'MISSES '),
        (u'Nr.'     , u'NUMMER '),
        (u'Nrn.'    , u'NUMMERN '),
        (u's.a.'    , u'SIEHE AUCH '),
        (u's. a.'   , u'SIEHE AUCH '),
        (u's.o.'    , u'SIEHE OBEN '),
        (u's. o.'   , u'SIEHE OBEN '),
        (u's.u.'    , u'SIEHE UNTEN '),
        (u's. u.'   , u'SIEHE UNTEN '),
        (u'jr.'     , u'JUNIOR '),
        (u'Str.'    , u'STRASSE '),
        (u'u.a.'    , u'UNTER ANDEREM '),
        (u'u. a.'   , u'UNTER ANDEREM '),
        (u'u.U.'    , u'UNTER UMSTÄNDEN '),
        (u'u. U.'   , u'UNTER UMSTÄNDEN '),
        (u'usw.'    , u'UND SO WEITER '),
        (u'u.s.w.'  , u'UND SO WEITER '),
        (u'u. s. w.', u'UND SO WEITER '),
        (u'v.a.'    , u'VOR ALLEM '),
        (u'vgl.'    , u'VERGLEICHE '),
        (u'vgl '    , u'VERGLEICHE '),
        (u'Wdh.'    , u'WIEDERHOLUNG '),
        (u'Ziff.'   , u'ZIFFER '),
        (u'z.B.'    , u'ZUM BEISPIEL '),
        (u'z. B.'   , u'ZUM BEISPIEL '),
        (u'z.T.'    , u'ZUM TEIL '),
        (u'z. T.'   , u'ZUM TEIL '),
        (u'z.Zt.'   , u'ZUR ZEIT '),
        (u'z. Zt.'  , u'ZUR ZEIT '),
        (u'\ufeff'  , u' '),
        (u'\u2019'  , u' '),
        (u'\xa0'    , u' '),
        (u'\u203a'  , u' '),
        (u'\u2039'  , u' '),
        (u'_'       , u' '),
        (u'&'       , u'UND'),
        (u'-'       , u' '),
        (u'\xa020'  , u' ')
    ]


# based on code from: http://www.python-forum.de/viewtopic.php?f=11&t=22543

w1 = u"NULL EIN ZWEI DREI VIER FÜNF SECHS SIEBEN ACHT NEUN ZEHN ELF ZWÖLF DREIZEHN VIERZEHN FÜNFZEHN SECHZEHN SIEBZEHN ACHTZEHN NEUNZEHN".split()
w2 = u"ZWANZIG DREIßIG VIERZIG FÜNFZIG SECHZIG SIEBZIG ACHTZIG NEUNZIG".split()
 
def zahl_in_worten(n, s=True, z=False):
    if n < 0: raise ValueError
    if n == 0 and z: return ""
    if n == 1 and s: return "EINS"
    if n < 20: return w1[n]
    if n < 100:
        w = w2[(n - 20) // 10]
        if n % 10:
            w = w1[n % 10] + "UND" + w
        return w
    if n < 1000:
        if n // 100 == 1:
            if z: return "EINHUNDERT" + zahl_in_worten(n % 100, z=True)
            return "HUNDERT" + zahl_in_worten(n % 100, z=True)
        return w1[n // 100] + "HUNDERT" + zahl_in_worten(n % 100, z=True)
    if n < 2000:
        if n < 1100:
            return  "TAUSEND" + zahl_in_worten(n % 1000, z=True)
        return w1[n // 100] + "HUNDERT" + zahl_in_worten(n % 100, z=True)
    if n < 1000000:
        return zahl_in_worten(n // 1000, s=False) + "TAUSEND" + zahl_in_worten(n % 1000, z=True)
    raise ValueError

#
# init number replacement dict
#

for i in range(10000):
    u = unicode(i)
    if not u in wrt:
        wrt[u] = zahl_in_worten(i)
    wrt[u'0'+u] = zahl_in_worten(i)
    wrt[u'00'+u] = zahl_in_worten(i)
    wrt[u'000'+u] = zahl_in_worten(i)

def split_words (s):

    global wrt

    for san in symb_abbrev_norm:
        srch = san[0]
        repl = san[1]

        s = s.replace (srch, repl)

    res = []

    words = re.split ('\s+', s)
    for word in words:

        w = re.sub(r"[,.?+*#! ;:/\"\[\]()='»«]", '', word.rstrip()).replace(u'–',u'').upper()
        if len(w) > 0:

            if w in wrt:
                w = wrt[w]
        
                words2 = re.split('\s+', w)
                for w2 in words2:
                    res.append(w2)

            else:
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

    def test_split(self):
        self.assertEqual (split_words(u"1 2 3 4"), ["EINS", "ZWEI", "DREI", "VIER"])
        self.assertEqual (split_words(u"00 01 02 03 04"), ["NULL", "EINS", "ZWEI", "DREI", "VIER"])
        self.assertEqual (split_words(u"z.B. u. U. Prof. Dr. Dipl. Ing."), [u'ZUM', u'BEISPIEL', u'UNTER', u'UMST\xc4NDEN', u'PROFESSOR', u'DOKTOR', u'DIPLOM', u'INGENIEUR'])

    def test_zahl_in_worten(self):

        for i in range(10000):
            u = unicode(i)
            z = zahl_in_worten(i)
            #print "%4s : %s" % (u, z)
            if u in wrt:
                self.assertEqual (z, wrt[u])

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

