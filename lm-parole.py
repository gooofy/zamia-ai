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

#
# extract sentences from german parole corpus (http://ota.ahds.ac.uk/desc/2467)
#

import sys
import re
import os
import traceback
import nltk
import pickle
from os.path import expanduser
import StringIO
import ConfigParser
from gutils import split_words, compress_ws
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint


#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

workdir   = config.get("speech", "lmworkdir")
parole    = config.get("speech", "parole-de")

MIN_PAR_LEN = 12

def collect_sentences (parent):

    if parent.tag == 'head':
        print "Head: %s" % parent.text

    for child in parent:
        collect_sentences (parent)
        
class ParoleParser(HTMLParser):
    def __init__  (self):
        HTMLParser.__init__  (self)
        self.in_par = False

    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag
        if tag == 'p':
            self.in_par = True
            self.buf = u""

    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_par = False
            #print (u"PAR: %s" % self.buf).encode('UTF8')

            text = compress_ws(self.buf.replace('\n', ' '))

            sentences = sent_detector.tokenize(text, realign_boundaries=True)
            for sentence in sentences:

                # split sentence into words and put it back together 
                # again using single spaces so we get rid of all non-word
                # characters in a uniform way 

                s = ' '.join(split_words(sentence.upper()))

                if len(s)<MIN_PAR_LEN:
                    continue

                outf.write((u"%s\n" % s).encode('UTF8'))


    def handle_data(self, data):
        if self.in_par and len(data)>0:
            #print "About to add: %s" % repr(data)
            self.buf += data.decode('UTF8', 'ignore')

    def handle_entityref (self, name):
        if self.in_par:
            c = ''
            if name == 'star':
                c = u'*'
            elif name == 'bquot':
                c = u'"'
            elif name == 'equot':
                c = u'"'
            elif name == 'lowbar':
                c = u'_'
            elif name == 'parole.tax':
                c = u''
            else:
                if name in name2codepoint:
                    c = unichr(name2codepoint[name])
                else: 
                    print "unknown entityref: %s" % name
                    c = ''
            #print "Named ent:", c
            self.buf += c

def crawl_sgms (path):

    files = os.listdir (path)
    for file in files:

        p = "%s/%s" % (path, file)

        if os.path.isdir(p):
            crawl_sgms(p)
            continue
        
        if not p.endswith ('.sgm'):
            continue

        print "found sgm: %s" % p

        try:
            pp = ParoleParser()

            inf = open (p)
            while True:
                sgmldata = inf.read(1024)
                if not sgmldata:
                    break
                pp.feed(sgmldata)
            pp.close()
            inf.close()
        except:
            print "*** ERROR: unexpected error:", sys.exc_info()[0]
            traceback.print_exc()


#
# main
#

#
# load german sentence segmenter
#

with open('de_punkt.pickle', mode='rb') as f:
    sent_detector = pickle.load(f)

outfn = '%s/parole.sent' % workdir
outf = open (outfn, 'w')

crawl_sgms (parole)

outf.close()

print
print "%s written." % outfn
print 




