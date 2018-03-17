#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# generate AI-Prolog of given names
#

import codecs

from nltools import misc

misc.init_app ('names_aip')

def name2pred(name):

    res = u''
    for c in name:
        if c.isalpha():
            res += c

    return 'name' + res

for gender in ['Female', 'Male']:

    with codecs.open('%s20.txt' % gender, 'r', 'utf8') as f:

        for line in f:

            name = line.strip()

            print u'rdfsLabel(%s, de, "%s").' % (name2pred(name), name)
            print u'rdfsLabel(%s, en, "%s").' % (name2pred(name), name)
            print u'wdpdSexOrGender(%s, wde%s).' % (name2pred(name), gender)
            print u'wdpdInstanceOf(%s, wde%sGivenName).' % (name2pred(name), gender)
            print

