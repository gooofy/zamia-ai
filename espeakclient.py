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

import StringIO
import sys
from gutils import run_command
from phonetic_alphabets import ipa2xsampa, xsampa2ipa

#
# A simple espeak interface for phone generation and TTS output
#

def espeak_gen_ipa (s):

    ipa = ''

    for line in run_command ( ['espeak', '-x', '--ipa=2', '-v', 'de', '-q', s] ):
        ipa = line.decode('utf8').lstrip().rstrip()

    # filter out phonemes we do not handle but translating to X-SAMPA and back:

    xs = ipa2xsampa (s, ipa)
    xs = xs.replace ('r','R').replace('3','6').replace('A','a')
    ipa = xsampa2ipa (s, xs)

    return ipa

def espeak_say (s):

    phonemes = ''

    run_command ( ['espeak', '-v', 'de', s] )


if __name__ == "__main__":

    for word in [u'GELBSEIDENEN', u'UNMUTE', u'GESCHIRRSCHEUERN', u'DÜSTRE', u'EINGANGE', 
                 u'AUSSCHLÄGEN', u'NACHHÄNGEND', u'HAUPTSTRAßEN', u'HOCHWEISEN', u'DICKER']:

        ipa = espeak_gen_ipa (word)
        print (u'%12s: %s %s' % (word, ipa, repr(ipa))).encode('utf8')

        xs = ipa2xsampa (word, ipa)
        print "    X-SAMPA: %s" % xs


    espeak_say ("Hallo")

