#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2013, 2014, 2016 Guenter Bartsch
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
#
# random tokenization / nlp pre-processing related stuff
#

import sys
import re
import unittest

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


# word replacement table
wrt = { u'0'             : u'null',
        u'1'             : u'eins', 
        u'10'            : u'zehn',
        u'10%'           : u'zehn prozent',
        u'100%'          : u'hundert prozent',
        u'1000'          : u'tausend',
        u'11'            : u'elf',
        u'12'            : u'zwölf',
        u'1200'          : u'zwölfhundert',
        u'128'           : u'hundertachtundzwanzig',
        u'13'            : u'dreizehn',
        u'132'           : u'hundertzweiunddreißig',
        u'137'           : u'hundertsiebenunddreißig',
        u'14'            : u'vierzehn',
        u'15'            : u'fünfzehn',
        u'16'            : u'sechzehn',
        u'160'           : u'hundertsechzig',
        u'17'            : u'siebzehn',
        u'170'           : u'hundertsiebzig',
        u'1700'          : u'siebzehnhundert',
        u'18'            : u'achtzehn',
        u'1825'          : u'achtzehnhundertfünfundzwanzig',
        u'186'           : u'hundertsechsundachtzig',
        u'19'            : u'neunzehn',
        u'1949'          : u'neunzehnhundertneunundvierzig',
        u'1960ER'        : u'neunzehnhundertsechziger',
        u'1970ER'        : u'neunzehnhundertsiebziger',
        u'1970ERJAHREN'  : u'neunzehnhundertsiebziger jahren',
        u'1977'          : u'neunzehnhundertsiebenundsiebzig',
        u'1979'          : u'neunzehnhundertneunundsiebzig',
        u'1980ER'        : u'neunzehnhundertachtziger',
        u'1983'          : u'neunzehnhundertdreiundachtzig',
        u'1984'          : u'neunzehnhundertvierundachtzig',
        u'1989'          : u'neunzehnhundertneunundachtzig',
        u'1990'          : u'neunzehnhundertneunzig',
        u'1990ER'        : u'neunzehnhundertneunziger',
        u'1991'          : u'neunzehnhunderteinundneunzig',
        u'1993'          : u'neunzehnhundertdreiundneunzig',
        u'1998'          : u'neunzehnhundertachtundneunzig',
        u'2'             : u'zwei', 
        u'2%'            : u'zwei prozent', 
        u'20'            : u'zwanzig',
        u'200'           : u'zweihundert',
        u'2000'          : u'zweitausend',
        u'20000'         : u'zwanzigtausend',
        u'2002'          : u'zweitausendzwei',
        u'2004'          : u'zweitausendvier',
        u'2005'          : u'zweitausendfünf',
        u'2150'          : u'zweitausendeinhundertfünfzig',
        u'2310'          : u'zweitausenddreihundertzehn',
        u'204'           : u'zweihundertvier',
        u'21'            : u'einundzwanzig',
        u'226'           : u'zweihundertsechsundzwanzig',
        u'22'            : u'zweiundzwanzig',
        u'23'            : u'dreiundzwanzig',
        u'24'            : u'vierundzwanzig',
        u'242'           : u'zweihundertzweiundvierzig',
        u'25'            : u'fünfundzwanzig', 
        u'28'            : u'achtundzwanzig', 
        u'250'           : u'zweihundertfünfzig',
        u'253'           : u'zweihundertdreiundfünfzig',
        u'254'           : u'zweihundertvierundfünfzig',
        u'3'             : u'drei', 
        u'30'            : u'dreißig',
        u'300'           : u'dreihundert',
        u'32'            : u'zweiunddreißig',
        u'33'            : u'dreiunddreißig',
        u'328'           : u'dreihundertachtundzwanzig',
        u'35'            : u'fünfunddreißig',
        u'4'             : u'vier', 
        u'40%'           : u'vierzig prozent', 
        u'400'           : u'vierhundert', 
        u'4000'          : u'viertausend', 
        u'4096'          : u'viertausendsechsundneunzig', 
        u'418'           : u'vierhundertachtzehn', 
        u'42'            : u'zweiundvierzig',
        u'43'            : u'dreiundvierzig',
        u'45'            : u'fünfundvierzig', 
        u'5'             : u'fünf', 
        u'50'            : u'fünfzig', 
        u'55'            : u'fünfundfünfzig', 
        u'500000'        : u'fünfhunderttausend', 
        u'57'            : u'siebenundfünfzig', 
        u'6'             : u'sechs', 
        u'63'            : u'dreiundsechzig', 
        u'7'             : u'sieben',
        u'75'            : u'fünfundsiebzig',
        u'8'             : u'acht',
        u'80'            : u'achtzig',
        u'80%'           : u'achtzig prozent',
        u'800'           : u'achthundert',
        u'80ER'          : u'achtziger',
        u'850'           : u'achthundertfünfzig',
        u'852'           : u'achthundertzweiundfünfzig',
        u'9'             : u'neun',
        u'90'            : u'neunzig',
        u'95'            : u'fünfundneunzig',
        u'99'            : u'neunundneunzig',
        u'100'           : u'hundert',
        u'daß'           : u'dass',
        u'haß'           : u'hass',
        u'gross'         : u'groß',
        u'grosse'        : u'große',
        u'grossen'       : u'großen',
        u'grosses'       : u'großes',
        u'faßte'         : u'fasste',
        u'gefaßt'        : u'gefasst',
        u'eingefaßte'    : u'eingefasste',
        u'bißchen'       : u'bisschen',
        u'blaß'          : u'blass',
        u'blaßblauen'    : u'blassblauen',
        u'bläßlich'      : u'blässlich',
        u'entschluß'     : u'entschluss',
        u'eßstube'       : u'essstube',
        u'eßtisch'       : u'esstisch',
        u'eßzimmer'      : u'esszimmer',
        u'gepreßt'       : u'gepresst',
        u'gewiß'         : u'gewiss',
        u'küßte'         : u'küsste',
        u'küßten'        : u'küssten',
        u'laß'           : u'lass',
        u'läßt'          : u'lässt',
        u'mißvergnügt'   : u'missvergnügt',
        u'mißverständnis': u'missverständnis',
        u'müßte'         : u'müsste',
        u'paß'           : u'pass',
        u'paßt'          : u'passt',
        u'preßte'        : u'presste',
        u'photo'         : u'foto',
        u'riß'           : u'riss',
        u'schloß'        : u'schloss',
        u'schluß'        : u'schluss',
        u'telephon'      : u'telefon',
        u'totenblaß'     : u'totenblass',
        u'vermißte'      : u'vermisste',
        u'vermißt'       : u'vermisst',
        u'phantasie'     : u'fantasie',
        u'phantasieren'  : u'fantasieren',
        u'phantastereien': u'fantastereien',
        u'phantastisch'  : u'fantastisch',
        u'mikrophon'     : u'mikrofon',
        u'mikrophone'    : u'mikrofone',
        u'wüßte'         : u'wüsste',
        u'wußte'         : u'wusste',
        u'wußten'        : u'wussten',
        u'muß'           : u'muss',
        u'mußt'          : u'musst',
        u'mußte'         : u'musste',
        u'bewußt'        : u'bewusst',
        u'unbewußt'      : u'unbewusst',
        u'gewußt'        : u'gewusst',
        u'bewußte'       : u'bewusste',
        u'bewußten'      : u'bewussten',
        u'zielbewußte'   : u'zielbewusste',
        u'siegesgewiß'   : u'siegesgewiss',
        u'zerriß'        : u'zerriss',
        u'walther'       : u'walter',
        u'eur'           : u'euro',
        u'sodass'        : u'so dass',
        u'elephant'      : u'elefant',
        u'elephanten'    : u'elefanten',
        u'abschluß'      : u'abschluss',
        u'philipp'       : u'philip',
        u'millenium'     : u'millennium',
        u'stop'          : u'stopp',
        u'§'             : u'paragraph'}


symb_abbrev_norm = [
        (u'Abk.'    , u'abkürzung '),
        (u'Abk '    , u'abkürzung '),
        (u'Prof.'   , u'professor '),
        (u'Dipl.'   , u'diplom '),
        (u'Ing.'    , u'ingenieur '),
        (u'Inf.'    , u'informatiker '),
        (u'Inform.' , u'informatiker '),
        (u'Tel.'    , u'telefon '),
        (u'bzw.'    , u'beziehungsweise '),
        (u'bzw '    , u'beziehungsweise '),
        (u'bspw.'   , u'beispielsweise '),
        (u'bspw '   , u'beispielsweise '),
        (u'bzgl.'   , u'bezüglich '),
        (u'ca.'     , u'circa '),
        (u'ca '     , u'circa '),
        (u'd.h.'    , u'das heißt '),
        (u'd. h.'   , u'das heißt '),
        (u'Dr. '    , u'doktor '),
        (u'evtl.'   , u'eventuell '),
        (u'evtl '   , u'eventuell '),
        (u'geb.'    , u'geborene '),
        (u'ggf.'    , u'gegebenenfalls '),
        (u'ggf '    , u'gegebenenfalls '),
        (u'kath.'   , u'katholische '),
        (u'Hrsg.'   , u'herausgeber '),
        (u'Mr.'     , u'mister '),
        (u'Mrd.'    , u'milliarden '),
        (u'Mrs.'    , u'misses '),
        (u'Nr.'     , u'nummer '),
        (u'Nrn.'    , u'nummern '),
        (u's.a.'    , u'siehe auch '),
        (u's. a.'   , u'siehe auch '),
        (u's.o.'    , u'siehe oben '),
        (u's. o.'   , u'siehe oben '),
        (u's.u.'    , u'siehe unten '),
        (u's. u.'   , u'siehe unten '),
        (u'jr.'     , u'junior '),
        (u'Str.'    , u'strasse '),
        (u'u.a.'    , u'unter anderem '),
        (u'u. a.'   , u'unter anderem '),
        (u'u.U.'    , u'unter umständen '),
        (u'u. U.'   , u'unter umständen '),
        (u'usw.'    , u'und so weiter '),
        (u'u.s.w.'  , u'und so weiter '),
        (u'u. s. w.', u'und so weiter '),
        (u'v.a.'    , u'vor allem '),
        (u'vgl.'    , u'vergleiche '),
        (u'vgl '    , u'vergleiche '),
        (u'Wdh.'    , u'wiederholung '),
        (u'Ziff.'   , u'ziffer '),
        (u'z.B.'    , u'zum beispiel '),
        (u'z. B.'   , u'zum beispiel '),
        (u'z.T.'    , u'zum teil '),
        (u'z. T.'   , u'zum teil '),
        (u'z.Zt.'   , u'zur zeit '),
        (u'z. Zt.'  , u'zur zeit '),
        (u'GHz'     , u'gigahertz '),
        (u'\ufeff'  , u' '),
        (u'\u2019'  , u' '),
        (u'\xa0'    , u' '),
        (u'\u203a'  , u' '),
        (u'\u2039'  , u' '),
        (u'_'       , u' '),
        (u'&'       , u'und'),
        (u'-'       , u' '),
        (u'\xa020'  , u' ')
    ]


# based on code from: http://www.python-forum.de/viewtopic.php?f=11&t=22543

w1 = u"null ein zwei drei vier fünf sechs sieben acht neun zehn elf zwölf dreizehn vierzehn fünfzehn sechzehn siebzehn achtzehn neunzehn".split()
w2 = u"zwanzig dreißig vierzig fünfzig sechzig siebzig achtzig neunzig".split()
 
def zahl_in_worten(n, s=True, z=False):
    if n < 0: raise ValueError
    if n == 0 and z: return ""
    if n == 1 and s: return "eins"
    if n < 20: return w1[n]
    if n < 100:
        w = w2[(n - 20) // 10]
        if n % 10:
            w = w1[n % 10] + "und" + w
        return w
    if n < 1000:
        if n // 100 == 1:
            if z: return "einhundert" + zahl_in_worten(n % 100, z=True)
            return "hundert" + zahl_in_worten(n % 100, z=True)
        return w1[n // 100] + "hundert" + zahl_in_worten(n % 100, z=True)
    if n < 2000:
        if n < 1100:
            return  "tausend" + zahl_in_worten(n % 1000, z=True)
        return w1[n // 100] + "hundert" + zahl_in_worten(n % 100, z=True)
    if n < 1000000:
        return zahl_in_worten(n // 1000, s=False) + "tausend" + zahl_in_worten(n % 1000, z=True)
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

def tokenize (s):


    global wrt

    for san in symb_abbrev_norm:
        srch = san[0]
        repl = san[1]

        s = s.replace (srch, repl)

    res = []

    words = re.split ('\s+', s)
    for word in words:

        w = re.sub(r"[,.?+*#! ;:/\"\[\]()='»«<>|]", '', word.rstrip()).replace(u'–',u'').lower()
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

class TestTokenizer (unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    # FIXME
    # def test_latin1(self):
    #     self.assertTrue (detect_latin1('/home/ai/voxforge/de/audio/ralfherzog-20071220-de34/etc/prompts-original'))
    #     self.assertFalse (detect_latin1('/home/ai/voxforge/de/audio/mjw-20110527-dyg/etc/prompts-original'))

    def test_ws(self):
        self.assertEqual (compress_ws('   ws   foo bar'), ' ws foo bar')

    def test_split(self):
        self.assertEqual (tokenize(u"1 2 3 4"), ["EINS", "ZWEI", "DREI", "VIER"])
        self.assertEqual (tokenize(u"00 01 02 03 04"), ["NULL", "EINS", "ZWEI", "DREI", "VIER"])
        self.assertEqual (tokenize(u"z.B. u. U. Prof. Dr. Dipl. Ing."), [u'ZUM', u'BEISPIEL', u'UNTER', u'UMST\xc4NDEN', u'PROFESSOR', u'DOKTOR', u'DIPLOM', u'INGENIEUR'])

    def test_zahl_in_worten(self):

        for i in range(10000):
            u = unicode(i)
            z = zahl_in_worten(i)
            #print "%4s : %s" % (u, z)
            if u in wrt:
                self.assertEqual (z, wrt[u])

    def test_editdist(self):
        self.assertEqual (edit_distance(
                             tokenize(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT'), 
                             tokenize(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT')), 0)
        self.assertEqual (edit_distance(
                             tokenize(u'DIE LEISTUNG WURDE'), 
                             tokenize(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT')), 1)
        self.assertEqual (edit_distance(
                             tokenize(u'DIE LEISTUNG'), 
                             tokenize(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT')), 2)
        self.assertEqual (edit_distance(
                             tokenize(u'DIE'), 
                             tokenize(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT')), 3)
        self.assertEqual (edit_distance(
                             tokenize(u'DIE ZURÜCKVERLANGT'), 
                             tokenize(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT')), 2)
        self.assertEqual (edit_distance(
                             tokenize(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT'), 
                             tokenize(u'LEISTUNG WURDE ZURÜCKVERLANGT')), 1)
        self.assertEqual (edit_distance(
                             tokenize(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT'), 
                             tokenize(u'WURDE ZURÜCKVERLANGT')), 2)
        self.assertEqual (edit_distance(
                             tokenize(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT'), 
                             tokenize(u'ZURÜCKVERLANGT')), 3)
        self.assertEqual (edit_distance(
                             tokenize(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT'), 
                             tokenize(u'')), 4)
        self.assertEqual (edit_distance(
                             tokenize(u'DIE LEISTUNG WURDE ZURÜCKVERLANGT'), 
                             tokenize(u'LEISTUNG FOO ZURÜCKVERLANGT')), 2)
        self.assertEqual (edit_distance(
                             tokenize(u'SIE IST FÜR DIE LEISTUNG DANKBAR'), 
                             tokenize(u'SIE STRITTIG LEISTUNG DANKBAR')), 3)

if __name__ == "__main__":

    unittest.main()

