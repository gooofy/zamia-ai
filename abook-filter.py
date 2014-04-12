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

import sys
import os
from gutils import split_words

#
# simple tool which transfers a formattet text file into a long list of whitespace sperated words
#

if len(sys.argv) != 2:
    print "usage: %s foo.txt" % sys.argv[0]
    sys.exit(1)

inf = open (sys.argv[1])

for line in inf:

    s = ' '.join(split_words(line.decode('utf8')))
    print s,







