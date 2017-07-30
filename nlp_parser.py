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

SYM_EOF          = 0

SYM_LPAREN       = 1
SYM_RPAREN       = 2
SYM_COMMA        = 3
SYM_NAME         = 4
SYM_STRING       = 5
SYM_LINE         = 6
SYM_EQUALS       = 7
SYM_COLON        = 8

SYM_MACRO        = 10
SYM_TRAIN        = 11
SYM_TEST         = 12
SYM_CONTEXT      = 13
SYM_BEGIN        = 14
SYM_END          = 15
SYM_INCLUDE      = 16
SYM_PREFIX       = 17

SYM_PROC         = 20
SYM_SET          = 21
SYM_TOKENS       = 22
SYM_RDF          = 23
SYM_INLINE       = 24
SYM_TSTART       = 25
SYM_TEND         = 26
SYM_SPJ          = 27
SYM_ACTION       = 28
SYM_IF           = 29
SYM_ELSE         = 30
SYM_ENDIF        = 31

class NLPLexer(object):

    NAME_CHARS = u"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"

    def __init__(self, inputf):

        self.inputf       = inputf
        self.linecnt      = 1
        self.cur_c        = None
        self.cur_sym      = None

    def report_error(self, msg):
        logging.error('%s:%d: %s' % (self.inputf.name, self.linecnt, msg))
        sys.exit(2)

    def getc(self):
        self.cur_c = self.inputf.read(1)
        if self.cur_c == '\n':
            self.linecnt += 1

    def getsym(self):

        # skip comments, whitespace
        seen_nl = False
        ws      = u''
        while self.cur_c and (self.cur_c.isspace() or self.cur_c==u'#'):
            if self.cur_c == u'#':
                while self.cur_c and self.cur_c != '\n':
                    self.getc()
            else:
                if self.cur_c == '\n':
                    seen_nl = True
                    ws      = u''
                else:
                    ws     += self.cur_c
                self.getc()

        if not self.cur_c:
            self.cur_sym = SYM_EOF
            return
      
        if seen_nl and self.cur_c != '@':
            self.cur_s = ws
            while self.cur_c != '\n':
                self.cur_s += self.cur_c
                self.getc()
            self.cur_sym = SYM_LINE
            return

        if self.cur_c == u'@':
            self.getc()
            self.cur_s = u''
            while self.cur_c and (self.cur_c in self.NAME_CHARS) :
                self.cur_s += self.cur_c
                self.getc()

            if self.cur_s == 'macro':
                self.cur_sym = SYM_MACRO
            elif self.cur_s == 'train':
                self.cur_sym = SYM_TRAIN
            elif self.cur_s == 'test':
                self.cur_sym = SYM_TEST
            elif self.cur_s == 'context':
                self.cur_sym = SYM_CONTEXT
            elif self.cur_s == 'begin':
                self.cur_sym = SYM_BEGIN
            elif self.cur_s == 'end':
                self.cur_sym = SYM_END
            elif self.cur_s == 'include':
                self.cur_sym = SYM_INCLUDE
            elif self.cur_s == 'proc':
                self.cur_sym = SYM_PROC
            elif self.cur_s == 'set':
                self.cur_sym = SYM_SET
            elif self.cur_s == 'tokens':
                self.cur_sym = SYM_TOKENS
            elif self.cur_s == 'rdf':
                self.cur_sym = SYM_RDF
            elif self.cur_s == 'inline':
                self.cur_sym = SYM_INLINE
            elif self.cur_s == 'tstart':
                self.cur_sym = SYM_TSTART
            elif self.cur_s == 'tend':
                self.cur_sym = SYM_TEND
            elif self.cur_s == 'spj':
                self.cur_sym = SYM_SPJ
            elif self.cur_s == 'prefix':
                self.cur_sym = SYM_PREFIX
            elif self.cur_s == 'action':
                self.cur_sym = SYM_ACTION
            elif self.cur_s == 'if':
                self.cur_sym = SYM_IF
            elif self.cur_s == 'else':
                self.cur_sym = SYM_ELSE
            elif self.cur_s == 'endif':
                self.cur_sym = SYM_ENDIF
            else:
                self.report_error ('unknown keyword @%s found.' % self.cur_s)

        elif self.cur_c == u'(':
            self.cur_sym = SYM_LPAREN
            self.getc()
        elif self.cur_c == u')':
            self.cur_sym = SYM_RPAREN
            self.getc()
        elif self.cur_c == u',':
            self.cur_sym = SYM_COMMA
            self.getc()
        elif self.cur_c == u'=':
            self.cur_sym = SYM_EQUALS
            self.getc()
        elif self.cur_c == u':':
            self.cur_sym = SYM_COLON
            self.getc()

        elif self.cur_c == u"'":
            self.cur_sym = SYM_STRING
            self.cur_s   = u''
            self.getc()
            while self.cur_c and (self.cur_c !="'"):
                if self.cur_c == '\n':
                    self.report_error ('lexer error: unterminated string literal')
                self.cur_s += self.cur_c
                self.getc()
            self.getc()

        elif self.cur_c in self.NAME_CHARS:

            self.cur_sym = SYM_NAME
            self.cur_s   = u''
            while self.cur_c and (self.cur_c in self.NAME_CHARS):
                self.cur_s += self.cur_c
                self.getc()

        else:
            self.report_error ('FIXME: lexer error, unexpected char: %s' % repr(self.cur_c))


class NLPParser(object):


    def __init__(self, kernal):
        self.kernal = kernal
        self.reset()

    def reset(self):
        self.named_macros = {}
        self.procs        = {}
        self.ds           = []
        self.tests        = []

    def _expand_macros (self, lang, txt, lx):

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
                    lx.report_error (') missing')
                j += i

                # extract macro

                macro_s = txt[i+1:j+1]

                # print "macro_s: %s" % macro_s

                macro_name = 'MACRO_%d' % len(implicit_macros)

                implicit_macros[macro_name] = []
                for s in macro_s.split('|'):
                    sub_parts = tokenize(s, lang=lang, keep_punctuation=True)
                    implicit_macros[macro_name].append({'W': sub_parts})

                txt2 += '{' + macro_name + ':W}'

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

        todo = [ (parts, 0, [], {}) ]

        while len(todo)>0:

            parts1, cnt, r, mpos = todo.pop()

            if cnt >= len(parts1):
                done.append((r, mpos))
                continue

            p1 = parts1[cnt]

            if cnt % 2 == 1:
                
                sub_parts = p1.split(':')
                name = sub_parts[0]

                if name == 'empty':
                    r  = copy(r)
                    todo.append((parts, cnt+1, r, mpos))
                else:

                    vn    = sub_parts[1]

                    macro = None

                    if lang in self.named_macros:
                        macro = self.named_macros[lang].get(name, None)
                    if not macro:
                        macro = implicit_macros.get(name, None)
                    if not macro:
                        lx.report_error ('unknown macro "%s"[%s] called' % (name, lang))

                    for r3 in macro:
                        r1    = copy(r)
                        mpos1 = copy(mpos)

                        # take care of multiple invocactions of the same macro
        
                        mpnn = 0
                        while True:
                            mpn = '%s_%d_start' % (name, mpnn)
                            if not mpn in mpos1:
                                break
                            mpnn += 1

                        mpos1['%s_%d_start' % (name, mpnn)] = len(r1)
                        r1.extend(r3[vn])
                        mpos1['%s_%d_end' % (name, mpnn)]   = len(r1)
                        todo.append((parts, cnt+1, r1, mpos1))
                        
            else:

                sub_parts = tokenize(p1, lang=lang, keep_punctuation=True)

                r  = copy(r)
                r.extend(sub_parts)

                todo.append((parts, cnt+1, r, mpos))

        return done

    def _parse_context(self, lx):
        lx.getsym()
        
        if lx.cur_sym != SYM_LPAREN:
            self.report_error('( expected.')
        lx.getsym()

        if lx.cur_sym != SYM_STRING:
            self.report_error('field name expected.')
        f = lx.cur_s
        lx.getsym()

        if lx.cur_sym != SYM_COMMA:
            self.report_error(', expected.')
        lx.getsym()

        if lx.cur_sym != SYM_STRING:
            self.report_error('value expected.')
        v = lx.cur_s
        lx.getsym()

        if lx.cur_sym != SYM_RPAREN:
            self.report_error('@context: ) expected.')
        lx.getsym()

        return (f,v)

    def _compile_expr (self, expr, mpos, lx):

        res = u''

        if expr[0] == u'tokens':

            t0 = self._compile_expr(expr[1], mpos, lx)
            t1 = self._compile_expr(expr[2], mpos, lx)

            res = u"context['tokens'][%s:%s]" % (t0, t1)

        elif expr[0] == u'tstart':

            mn = expr[1]
            mi = expr[2] if len(expr)>2 else 0

            mpn = '%s_%d_start' % (mn, mi)
            if not mpn in mpos:
                lx.report_error('failed to find tstart of macro %s idx %d' % (mn, mi))

            res = unicode(mpos[mpn])

        elif expr[0] == u'tend':

            mn = expr[1]
            mi = expr[2] if len(expr)>2 else 0

            mpn = '%s_%d_end' % (mn, mi)
            if not mpn in mpos:
                lx.report_error('failed to find tend of macro %s idx %d' % (mn, mi))

            res = unicode(mpos[mpn])

        elif expr[0] == u'spj':

            t = self._compile_expr(expr[1], mpos, lx)
            res = u"u' '.join(%s)" % t

        elif expr[0] == u'local':

            res = expr[1]

        elif expr[0] == u'rdf':

            res = u"rdf_get_single('%s', '%s'" % (expr[1], expr[2])
            if expr[3]:
                res += u", langfilter='%s'" % expr[3]
            res += u")"

        elif expr[0] == 'ref':

            if expr[1] == 'user':

                res = u"rdf_get_single(context['user'], 'ai:%s')" % (expr[2])

            else :
                raise Exception ('FIXME: URI scheme %s not implemented yet.' % repr(expr))

        else:

            raise Exception ('FIXME: expr node type %s not implemented yet.' % repr(expr[0]))

        return res

    def _compile_code (self, code, mpos, indent, lx, lang):

        pcode = []

        for c in code:

            if c[0] == 'set':

                t = self._compile_expr (c[2], mpos, lx)

                if c[1][0] == 'ref':

                    if c[1][1] == 'user':

                        pcode.append(u"%srdf_retractall (context['user_uri'], 'ai:%s')" % (indent, c[1][2]))
                        pcode.append(u"%srdf_assert     (context['user_uri'], 'ai:%s', %s)" % (indent, c[1][2], t))

                    else :
                        raise Exception ('FIXME: URI scheme %s not implemented yet.' % repr(c[1]))

                elif c[1][0] == 'local':

                    pcode.append(u"%s%s = %s" % (indent, c[1][1], t))

                else:
                    raise Exception ('FIXME: target %s not implemented yet.' % repr(c[1]))

            elif c[0] == 'line':

                pcode.append(u"%sr_bor(context)" % indent)

                parts = []
                for p1 in c[1].split('{'):
                    for p2 in p1.split('}'):
                        parts.append(p2)

                cnt = 0
                for part in parts:

                    if cnt % 2 == 1:
                        pcode.append(u"%sr_sayv('%s')" % (indent, part))

                    else:

                        for t in tokenize(part, lang=lang, keep_punctuation=True):
                            pcode.append(u"%sr_say(u\"%s\")" % (indent, t.replace('"', "'")))

                    cnt += 1

            elif c[0] == 'action':

                s = u"%sr_action(%s)" % (indent, repr(list(c[1:])))

                pcode.append(s)

            elif c[0] == 'if':

                t = self._compile_expr (c[1], mpos, lx)

                pcode.append(u"%sif %s :" % (indent, t))

                pcode.extend(self._compile_code (c[2], mpos, indent + '    ', lx, lang))

                if c[3]:
                    pcode.append(u"%selse:" % indent)
                pcode.extend(self._compile_code (c[3], mpos, indent + '    ', lx, lang))

            else:
                raise Exception ('FIXME: command %s not implemented yet.' % repr(c[0]))

        return pcode


    def _parse_train(self, lx):

        lx.getsym()
        if lx.cur_sym != SYM_LPAREN:
            self.report_error('( expected.')
        lx.getsym()

        if lx.cur_sym != SYM_NAME:
            self.report_error('language name expected.')
        lang = lx.cur_s
        lx.getsym()

        if lx.cur_sym != SYM_RPAREN:
            self.report_error('@train: ) expected.')
        lx.getsym()

        contexts = []
        while lx.cur_sym == SYM_CONTEXT:
            contexts.append(self._parse_context(lx))

        if lx.cur_sym != SYM_LINE:
            self.report_error('input line expected.')
        inp = lx.cur_s
        lx.getsym()

        code = self._parse_code (lx, [], lang)

        for d, mpos in self._expand_macros(lang, inp, lx):

            r = self._compile_code (code, mpos, '', lx, lang)

            # get rid of punctuation for the input, prepend context
            utt = u' '.join(d)
            u = tokenize(utt, lang=lang, keep_punctuation=False)

            logging.debug( '%s -> %s' % (repr(u), repr(r)))

            self.ds.append((lang, contexts, u, r))

    def _parse_begin(self, lx):

        lx.getsym()

        code = []

        num_spaces = -1

        while lx.cur_sym == SYM_LINE:

            if num_spaces < 0:
                num_spaces = 0
                while (num_spaces < len(lx.cur_s)) and lx.cur_s[num_spaces].isspace():
                    num_spaces += 1

            code.append(lx.cur_s[num_spaces:])
            lx.getsym()

        if lx.cur_sym != SYM_END:
            self.report_error('@end expected.')
        lx.getsym()

        # import pdb; pdb.set_trace()
        return code

    def _parse_macro(self, lx):

        lx.getsym()
        if lx.cur_sym != SYM_LPAREN:
            self.report_error('( expected.')
        lx.getsym()

        if lx.cur_sym != SYM_NAME:
            self.report_error('language name expected.')
        lang = lx.cur_s
        lx.getsym()

        if lx.cur_sym != SYM_COMMA:
            self.report_error(', expected.')
        lx.getsym()

        if lx.cur_sym != SYM_NAME:
            self.report_error('macro name expected.')
        name = lx.cur_s
        lx.getsym()

        vs = []
        while lx.cur_sym == SYM_COMMA:
            lx.getsym()
            if lx.cur_sym != SYM_NAME:
                self.report_error('variable name expected.')
            vs.append(lx.cur_s)
            lx.getsym()

        if lx.cur_sym != SYM_RPAREN:
            self.report_error('@macro: ) expected.')
        lx.getsym()

        if lx.cur_sym == SYM_BEGIN:

            code = self._parse_begin(lx)
            code_s = u'\n'.join(code)

            env_locals = { 'rdf'   : rdf,
                           'lang'  : lang,
                           'kernal': self.kernal,
                           'kb'    : self.kernal.kb }

            exec code_s in env_locals

            resps = []
            for r in env_locals['data']:
                r2 = {}
                for vn in r:    
                    r2[vn]= tokenize(r[vn], lang=lang, keep_punctuation=True)
                resps.append(r2)

        elif lx.cur_sym == SYM_LINE:

            # vs   = self.cur_line.split(':')[3:]

            # self.next_line()

            resps = []

            while lx.cur_sym == SYM_LINE:

            # while self.cur_line and (self.cur_line[0] != '@'):

                line_parts = lx.cur_s.split('@')

                for el, empos in self._expand_macros (lang, line_parts[0], lx):

                    r = {vs[0] : el}

                    for vn, val in zip (vs, line_parts)[1:]:
                        r[vn] = val

                    resps.append(r)

                lx.getsym()

        else:
            self.report_error ('FIXME: unexpected symbol in macro')

        if not lang in self.named_macros:
            self.named_macros[lang] = {}

        self.named_macros[lang][name] = resps

        logging.debug ('new named macro defined: %s -> %s' % (name, repr(resps)))

    def _parse_test(self, lx):

        lx.getsym()
        if lx.cur_sym != SYM_LPAREN:
            lx.report_error('( expected.')
        lx.getsym()

        if lx.cur_sym != SYM_NAME:
            lx.report_error('language name expected.')
        lang = lx.cur_s
        lx.getsym()

        if lx.cur_sym != SYM_COMMA:
            lx.report_error(', expected.')
        lx.getsym()

        if lx.cur_sym != SYM_NAME:
            lx.report_error('test name expected.')
        name = lx.cur_s
        lx.getsym()

        if lx.cur_sym != SYM_RPAREN:
            lx.report_error('@test: ) expected (sym %d found instead).' % lx.cur_sym)
        lx.getsym()

        rounds = []

        while lx.cur_sym == SYM_LINE:
            inp, mpos = self._expand_macros(lang, lx.cur_s, lx)[0]
            lx.getsym()
            if lx.cur_sym != SYM_LINE:
                lx.report_error('test response expected.')
            r, mpos = self._expand_macros(lang, lx.cur_s, lx)[0]
            lx.getsym()

            # filter words vs actions
            resp    = []
            actions = []
            for rs in r:
                if isinstance(rs, basestring):
                    resp.append(rs)
                else:
                    actions.append(rs)
            

            rounds.append((inp, resp, actions))

        self.tests.append((name, lang, rounds))

        logging.debug ('added test: %s' % repr(rounds))
  
    def _parse_name (self, lx, args):
        if lx.cur_sym != SYM_NAME:
            lx.report_error('name expected')
        n = lx.cur_s
        lx.getsym()
        if lx.cur_sym == SYM_COLON:
            lx.getsym()
            if lx.cur_sym != SYM_NAME:
                lx.report_error('name expected')
            n2 = lx.cur_s
            lx.getsym()

            return ('ref', n, n2)
        else:
            if n in args:
                return ('arg', n)
            else:
                return ('local', n)

    def _parse_tokens(self, lx, args):

        lx.getsym()
        if lx.cur_sym != SYM_LPAREN:
            lx.report_error('( expected.')
        lx.getsym()

        ts = self._parse_expression(lx, args)

        if lx.cur_sym != SYM_COMMA:
            lx.report_error(', expected.')
        lx.getsym()

        te = self._parse_expression(lx, args)

        if lx.cur_sym != SYM_RPAREN:
            lx.report_error('@tokens: ) expected (sym %d found instead).' % lx.cur_sym)
        lx.getsym()

        return ('tokens', ts, te)

    def _parse_rdf(self, lx, args):

        lx.getsym()
        if lx.cur_sym != SYM_LPAREN:
            lx.report_error('( expected.')
        lx.getsym()

        n1 = self._parse_name(lx, args)

        if n1[0] != 'ref':
            lx.report_error('rdf: URI shorthand "prefix:l" expected')

        if lx.cur_sym != SYM_COMMA:
            lx.report_error(', expected.')
        lx.getsym()

        n2 = self._parse_name(lx, args)
        if n2[0] != 'ref':
            lx.report_error('rdf: URI shorthand "prefix:l" expected')

        if lx.cur_sym == SYM_COMMA:
            lx.getsym()

            if lx.cur_sym != SYM_NAME:
                lx.report_error('@rdf: language filter name expected.')
            n3 = lx.cur_s
            lx.getsym()

        else:
            n3 = None

        if lx.cur_sym != SYM_RPAREN:
            lx.report_error('@rdf: ) expected (sym %d found instead).' % lx.cur_sym)
        lx.getsym()

        return ('rdf', '%s:%s' % (n1[1], n1[2]), '%s:%s' % (n2[1], n2[2]), n3)

    def _parse_tstart(self, lx, args):

        lx.getsym()
        if lx.cur_sym != SYM_LPAREN:
            lx.report_error('( expected.')
        lx.getsym()

        if lx.cur_sym != SYM_NAME:
            lx.report_error('macro name expected.')
        ts = lx.cur_s
        lx.getsym()

        if lx.cur_sym != SYM_RPAREN:
            lx.report_error('@tstart: ) expected (sym %d found instead).' % lx.cur_sym)
        lx.getsym()

        return ('tstart', ts)

    def _parse_tend(self, lx, args):

        lx.getsym()
        if lx.cur_sym != SYM_LPAREN:
            lx.report_error('( expected.')
        lx.getsym()

        if lx.cur_sym != SYM_NAME:
            lx.report_error('macro name expected.')
        ts = lx.cur_s
        lx.getsym()

        if lx.cur_sym != SYM_RPAREN:
            lx.report_error('@tend: ) expected (sym %d found instead).' % lx.cur_sym)
        lx.getsym()

        return ('tend', ts)

    def _parse_spj(self, lx, args):

        lx.getsym()
        if lx.cur_sym != SYM_LPAREN:
            lx.report_error('@spj: ( expected.')
        lx.getsym()

        e = self._parse_expression(lx, args)

        if lx.cur_sym != SYM_RPAREN:
            lx.report_error('@spj: ) expected (sym %d found instead).' % lx.cur_sym)
        lx.getsym()

        return ('spj', e)

    def _parse_expression (self, lx, args):
        
        if lx.cur_sym == SYM_NAME:
            return self._parse_name(lx, args)
        elif lx.cur_sym == SYM_TOKENS:
            return self._parse_tokens(lx, args)
        elif lx.cur_sym == SYM_RDF:
            return self._parse_rdf(lx, args)
        elif lx.cur_sym == SYM_TSTART:
            return self._parse_tstart(lx, args)
        elif lx.cur_sym == SYM_TEND:
            return self._parse_tend(lx, args)
        elif lx.cur_sym == SYM_SPJ:
            return self._parse_spj(lx, args)
        else:
            lx.report_error('expression expected, sym %d found instead.' % lx.cur_sym)

    def _parse_set (self, lx, args):
        
        lx.getsym()
        dst = self._parse_name (lx, args)

        if lx.cur_sym != SYM_EQUALS:
            lx.report_error('set: = expected')

        lx.getsym()

        src = self._parse_expression (lx, args)

        return ('set', dst, src)

    def _parse_action (self, lx, args):
        
        lx.getsym()
        if lx.cur_sym != SYM_LPAREN:
            lx.report_error('action: ( expected')
        lx.getsym()

        res = ['action']

        while lx.cur_sym and lx.cur_sym != SYM_RPAREN:
            if lx.cur_sym != SYM_NAME:
                lx.report_error('action: name expected')
            res.append(lx.cur_s)
            lx.getsym()

            if lx.cur_sym == SYM_COMMA:
                lx.getsym()

        if lx.cur_sym != SYM_RPAREN:
            lx.report_error('action: ) expected')
        lx.getsym()

        return tuple(res)

    def _apply_bindings (self, node, bindings):
        
        if not isinstance (node, tuple):
            return node

        if node[0] == 'arg':
            if node[1] in bindings:
                return bindings[node[1]]
            else:
                return node

        n2 = [node[0]]
        for n3 in node[1:]:
            n2.append(self._apply_bindings (n3, bindings))

        return tuple(n2)

    def _parse_code(self, lx, args, lang):

        code = []

        while True:

            if lx.cur_sym == SYM_SET:
                code.append(self._parse_set(lx, args))

            elif lx.cur_sym == SYM_LINE:
                code.append(('line', lx.cur_s))
                lx.getsym()

            elif lx.cur_sym == SYM_ACTION:
                code.append(self._parse_action(lx, args))

            elif lx.cur_sym == SYM_IF:
                lx.getsym()

                cond = self._parse_expression(lx, args)

                t = self._parse_code(lx, args, lang)

                if lx.cur_sym == SYM_ELSE:
                    lx.getsym()
                    e = self._parse_code(lx, args, lang)
                else:
                    e = None

                if lx.cur_sym != SYM_ENDIF:
                    lx.report_error('@endif expected')
                lx.getsym()

                code.append(('if', cond, t, e))

            elif lx.cur_sym == SYM_INLINE:
                lx.getsym()

                if lx.cur_sym != SYM_LPAREN:
                    lx.report_error ('@inline: ( expected.')
                lx.getsym()

                if lx.cur_sym != SYM_NAME:
                    lx.report_error ('@inline: proc name expected.')
                name = lx.cur_s
                if not name in self.procs[lang]:
                    lx.report_error ('@inline: unknown proc "%s".' % name)
                pa, pc = self.procs[lang][name]
                lx.getsym()

                i = 0
                bindings = {}
                while lx.cur_sym == SYM_COMMA:
                    lx.getsym()

                    if i >= len(pa):
                        lx.report_error ('@inline: %d args expected.' % len(pa))

                    x = self._parse_expression(lx, args)
                    bindings[pa[i]] = x
                    i += 1

                if lx.cur_sym != SYM_RPAREN:
                    lx.report_error ('@inline: ) expected.')
                lx.getsym()

                for c in pc:
                    code.append(self._apply_bindings(c, bindings))

            else:
                break

        return code


    def _parse_proc(self, lx):

        lx.getsym()
        if lx.cur_sym != SYM_LPAREN:
            lx.report_error('( expected.')
        lx.getsym()

        if lx.cur_sym != SYM_NAME:
            lx.report_error('language name expected.')
        lang = lx.cur_s
        lx.getsym()

        if lx.cur_sym != SYM_COMMA:
            lx.report_error(', expected.')
        lx.getsym()

        if lx.cur_sym != SYM_NAME:
            lx.report_error('proc name expected.')
        name = lx.cur_s
        lx.getsym()

        args = []
        while lx.cur_sym == SYM_COMMA:
            lx.getsym()
            if lx.cur_sym != SYM_NAME:
                lx.report_error('arg name expected.')
            args.append(lx.cur_s)
            lx.getsym()

        if lx.cur_sym != SYM_RPAREN:
            lx.report_error('@proc: ) expected (sym %d found instead).' % lx.cur_sym)
        lx.getsym()

        code = self._parse_code(lx, args, lang)

        if not lang in self.procs:
            self.procs[lang] = {}

        self.procs[lang][name] = (args, code)

        logging.debug ('added proc: %s' % name)
    
    def _parse_file(self, lx):

        while lx.cur_sym and lx.cur_sym != SYM_EOF:

            if lx.cur_sym == SYM_MACRO:
                self._parse_macro(lx)
            elif lx.cur_sym == SYM_TRAIN:
                self._parse_train(lx)
            elif lx.cur_sym == SYM_TEST:
                self._parse_test(lx)
            elif lx.cur_sym == SYM_INCLUDE:
                self._parse_include(lx)
            elif lx.cur_sym == SYM_PROC:
                self._parse_proc(lx)
            else:
                lx.report_error ('@macro/@train/@test/@include/@proc expected.')
    
    def _parse_include(self, lx):

        lx.getsym()
        if lx.cur_sym != SYM_LPAREN:
            lx.report_error('( expected.')
        lx.getsym()

        if lx.cur_sym != SYM_STRING:
            lx.report_error('include filename / path expected.')
        inputfn = lx.cur_s
        lx.getsym()

        if lx.cur_sym != SYM_RPAREN:
            lx.report_error('@test: ) expected (sym %d found instead).' % lx.cur_sym)
        lx.getsym()

        with codecs.open('modules/%s' % inputfn, 'r', 'utf8', errors='ignore') as inputf:

            lx2 = NLPLexer(inputf)
            lx2.getc()
            lx2.getsym()

            self._parse_file(lx2)

    def parse(self, inputfn):

        logging.info('processing %s ...' % inputfn)

        with codecs.open(inputfn, 'r', 'utf8', errors='ignore') as inputf:

            self.reset()

            lx = NLPLexer(inputf)
            lx.getc()
            lx.getsym()

            self._parse_file(lx)

        return self.ds, self.tests

