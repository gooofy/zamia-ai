#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Heiko Schaefer, Guenter Bartsch
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
# zamia-ai nlp format parser / processor
#

import os
import sys
import re
import traceback
import codecs
import logging

from copy              import copy
from nltools           import misc
from nltools.tokenizer import tokenize
from kb                import AIKB
from rdf               import rdf

class NLPParser(object):

    def __init__(self, kernal):
        self.kernal = kernal
        self.reset()

    def reset(self):
        self.linecnt      = 0
        self.named_macros = {}
        self.ds           = []

    #
    # line parser support functions
    #

    def report_error(self, msg):
        logging.error('Error in line %d: %s' % (self.linecnt, msg))
        sys.exit(2)

    def next_line(self):

        while True:

            self.cur_line = self.inputf.readline()
            if not self.cur_line:
                return

            self.cur_line = self.cur_line.strip()
            self.linecnt += 1
           
            # skip empty lines, comments
            if len(self.cur_line)==0 or self.cur_line[0] == '#':
                continue

            break

    def _expand_macros (self, lang, txt):

        logging.debug(u"expand macros  : %s" % txt)

        implicit_macros = {}

        if not lang in self.named_macros:
            self.named_macros[lang] = {}

        txt2 = ''

        i = 0
        while i<len(txt):

            if txt[i] == '(':

                j = txt[i+1:].find(')')
                if j<0:
                    raise Exception (') missing')
                j += i

                # extract macro

                macro_s = txt[i+1:j+1]

                # print "macro_s: %s" % macro_s

                macro_name = 'MACRO_%d' % len(implicit_macros)

                implicit_macros[macro_name] = []
                for s in macro_s.split('|'):
                    sub_parts = tokenize(s, lang=lang, keep_punctuation=True)
                    implicit_macros[macro_name].append({'W': sub_parts})

                txt2 += '{macro:' + macro_name + ':W}'

                i = j+2
            else:

                txt2 += txt[i]
                i+=1

        logging.debug ( "implicit macros: %s" % repr(implicit_macros) )
        logging.debug ( "txt2           : %s" % txt2 )

        parts = []
        for p1 in txt2.split('{'):
            for p2 in p1.split('}'):
                parts.append(p2)

        done = []

        todo = [ (parts, 0, []) ]

        while len(todo)>0:

            parts1, cnt, r = todo.pop()

            if cnt >= len(parts1):
                done.append(r)
                continue

            p1 = parts1[cnt]

            if cnt % 2 == 1:
                
                sub_parts = p1.split(':')

                if sub_parts[0] == 'macro':

                    name = sub_parts[1]
                    vn   = sub_parts[2]

                    if name in self.named_macros[lang]:
                        for r3 in self.named_macros[lang][name]:
                            r1  = copy(r)
                            r1.extend(r3[vn])
                            todo.append((parts, cnt+1, r1))

                    else:
                        if not name in implicit_macros:
                            raise Exception ('unknown macro "%s" called' % name)

                        for r3 in implicit_macros[name]:
                            r1  = copy(r)
                            r1.extend(r3[vn])
                            todo.append((parts, cnt+1, r1))
                        
                elif sub_parts[0] == 'empty':
                    r  = copy(r)
                    todo.append((parts, cnt+1, r))

                else:

                    r  = copy(r)
                    r.append(sub_parts)
                    todo.append((parts, cnt+1, r))

            else:

                sub_parts = tokenize(p1, lang=lang, keep_punctuation=True)

                r  = copy(r)
                r.extend(sub_parts)

                todo.append((parts, cnt+1, r))

        return done

    def _says (self, lang, r, txt, bor=False):

        r1 = copy(r)

        for r2 in self._expand_macros(lang, txt):

            if bor:
                r1.append(u"r_bor(ias)")

            response = []
            for r3 in r2:

                if isinstance (r3, basestring):
                    response.append(u"r_say(ias, u'%s')" % r3.replace("'", "\\'"))
                elif r3[0] == 'action':
                    response.append(u"r_action(ias, %s)" % repr(r3[1:]))
                else:
                    raise Exception ('unknown brace command "%s"' % r3[0])

            r1.extend(response)

        return r1

    def _parse_start(self):

        lang = self.cur_line.split(':')[1]

        self.next_line()

        inp = self.cur_line
        self.next_line()

        resps = []

        while self.cur_line and (self.cur_line[0] != '@'):
            resps.append(self.cur_line)
            self.next_line()

        for d in self._expand_macros(lang, inp):

            # print repr(d)

            r = []

            for resp in resps:
                r = self._says(lang, r, resp, bor=True)

            # get rid of punctuation for the input
            utt = u' '.join(d)
            u = tokenize(utt, lang=lang, keep_punctuation=False)

            logging.debug( '%s -> %s' % (repr(u), repr(r)))

            self.ds.append((lang, [[], u, r]))
    
    def _parse_macro(self):

        lang = self.cur_line.split(':')[1]
        name = self.cur_line.split(':')[2]
        vs   = self.cur_line.split(':')[3:]

        self.next_line()

        resps = []

        while self.cur_line and (self.cur_line[0] != '@'):

            line_parts = self.cur_line.split('@')


            for el in self._expand_macros (lang, line_parts[0]):

                r = {vs[0] : el}

                for vn, val in zip (vs, line_parts)[1:]:
                    r[vn] = val

                resps.append(r)

            self.next_line()


        if not lang in self.named_macros:
            self.named_macros[lang] = {}

        self.named_macros[lang][name] = resps

        logging.debug ('new named macro defined: %s -> %s' % (name, repr(resps)))

    def _parse_rdf(self):

        lang = self.cur_line.split(':')[1]
        name = self.cur_line.split(':')[2]

        self.next_line()

        triples = []
        limit   = 0
        filters = []

        while self.cur_line and (self.cur_line[0] != '@'):

            if self.cur_line.startswith('limit'):
                limit = int(self.cur_line.split(':')[1])

            elif self.cur_line.startswith('lang'):
                parts = self.cur_line.split(':')
                filters.append( ('=', ('lang', parts[1]), parts[2]) )

            else:

                triples.append(self.cur_line.split(','))

            self.next_line()

        res = rdf(self.kernal.kb, triples=triples, limit=limit, filters=filters)

        if not lang in self.named_macros:
            self.named_macros[lang] = {}

        resps = []
        for r in res:
            r2 = {}
            for vn in r:    
                r2[vn]= tokenize(r[vn], lang=lang, keep_punctuation=True)
            resps.append(r2)

        self.named_macros[lang][name] = resps

        logging.debug ('new named macro defined: %s -> %s' % (name, repr(resps)))

    def parse(self, inputfn):

        self.inputfn = inputfn

        logging.info('processing %s ...' % inputfn)

        with codecs.open(self.inputfn, 'r', 'utf8', errors='ignore') as self.inputf:

            self.reset()

            self.next_line()

            while self.cur_line:

                if self.cur_line.startswith('@start'):
                    self._parse_start()
                elif self.cur_line.startswith('@macro'):
                    self._parse_macro()
                elif self.cur_line.startswith('@rdf'):
                    self._parse_rdf()
                else:
                    self.report_error ('syntax error')

        return self.ds

