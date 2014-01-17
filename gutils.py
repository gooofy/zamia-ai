#!/usr/bin/env python
# -*- coding: utf-8 -*- 

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


class TestGUtils (unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_latin1(self):
        self.assertTrue (detect_latin1('/home/ai/voxforge/de/audio/ralfherzog-20071220-de34/etc/prompts-original'))
        self.assertFalse (detect_latin1('/home/ai/voxforge/de/audio/mjw-20110527-dyg/etc/prompts-original'))

    def test_ws(self):
        self.assertEqual (compress_ws('   ws   foo bar'), ' ws foo bar')

if __name__ == "__main__":

    unittest.main()

