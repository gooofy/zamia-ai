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
import ConfigParser
from os.path import expanduser
from gutils import run_command
from phonetic_alphabets import ipa2xsampa, xsampa2ipa

#
# A simple phonetisaurus interface for phoneme generation
#

def phonetisaurus_gen_ipa (s):

    xs = ''

    for line in run_command ( ['phonetisaurus-g2p', '--model=%s' % psmodel, '--nbest=1', '--input=%s' % s.encode('utf8')] ):
        print line,
        xs = line.decode('utf8').lstrip().rstrip()

    parts = xs.split('\t')[1].split(' ')
    print repr(parts)
    xs = ''
    for p in parts:
        xs = xs + p

    ipa = xsampa2ipa(s, xs)

    return ipa

#
# load config from ~/.airc
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

psmodel = config.get("speech", "psmodel")

if __name__ == "__main__":

    for word in [u'GELBSEIDENEN', u'UNMUTE', u'GESCHIRRSCHEUERN', u'DÜSTRE', u'EINGANGE', 
                 u'AUSSCHLÄGEN', u'NACHHÄNGEND', u'HAUPTSTRAßEN', u'HOCHWEISEN', u'DICKER']:

        ipa = phonetisaurus_gen_ipa (word)
        print (u'%-12s: %s %s' % (word, ipa, repr(ipa))).encode('utf8')

        xs = ipa2xsampa (word, ipa)
        print "    X-SAMPA: %s" % xs


