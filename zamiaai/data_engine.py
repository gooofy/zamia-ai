#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016, 2017, 2018 Guenter Bartsch
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
# data engine
#
# controller sitting between zamia ai modules and the database
#
# maintains dict of named macros for various languages
# contains utility functions that expand macros to produce
# training data input
#

import os
import sys
import logging
import codecs
import re
import json
import codegen
import hashlib
import ast
import inspect

from copy                import copy, deepcopy
from io                  import StringIO

from nltools.tokenizer   import tokenize
from zamiaai             import model

class DataEngine(object):

    def __init__(self, session):
        self.session           = session

        self.prefixes          = []
        self.data_module_name  = None
        self.source_location   = ('unknown', 0)

        self.cnt_dt            = 0
        self.cnt_ts            = 0

    def get_stats(self):
        return self.cnt_dt, self.cnt_ts

    def report_error(self, s):
        raise Exception ("%s: error in line %d: %s" % (self.source_location[0], self.source_location[1], s))

    def prepare_compilation (self, module_name):
        self.clean(module_name)
        self.data_module_name = module_name

    def compute_named_macros(self):
        self.named_macros = {}
        for module in self.named_macros_mod:
            for lang in self.named_macros_mod[module]:
                if not lang in self.named_macros:
                    self.named_macros[lang] = {}
                for n in self.named_macros_mod[module][lang]:
                    if not n in self.named_macros[lang]:
                        self.named_macros[lang][n] = []
                    self.named_macros[lang][n].extend(self.named_macros_mod[module][lang][n])

    def clean (self, module_name):

        logging.debug("Clearing %s ..." % module_name)
        self.session.query(model.TrainingData).filter(model.TrainingData.module==module_name).delete()
        self.session.query(model.Code).filter(model.Code.module==module_name).delete()
        self.session.query(model.TestCase).filter(model.TestCase.module==module_name).delete()
        self.session.query(model.NERData).filter(model.NERData.module==module_name).delete()
        self.session.query(model.NamedMacro).filter(model.NamedMacro.module==module_name).delete()
        logging.debug("Clearing %s ... done." % module_name)

        self.cnt_dt = 0
        self.cnt_ts = 0

    def commit(self):
        self.session.commit()

    def store_code(self, code_src, code_fn):
        md5 = hashlib.md5()
        md5.update (code_src)
        md5s = md5.hexdigest()

        if not self.session.query(model.Code).filter(model.Code.md5s==md5s).first():
            cd = model.Code(md5s=md5s, module=self.data_module_name, code=code_src, fn=code_fn)
            self.session.add(cd)
        return md5s

    def lookup_code(self, md5s):
        cd = self.session.query(model.Code).filter(model.Code.md5s==md5s).first()
        if not cd:
            raise Exception ('Code %s not found.' % md5s)
        return cd.fn, cd.code

    def lookup_data_train(self, inp, lang):
        res = []

        for td in self.session.query(model.TrainingData).filter(model.TrainingData.lang==lang).filter(model.TrainingData.inp==inp):
            res.append( (lang, inp, td.md5s, json.loads(td.args), td.loc_fn, td.loc_line) )

        return res

    def macro(self, lang, name, soln):

        # import pdb; pdb.set_trace()

        nm = model.NamedMacro(lang   = lang,
                              module = self.data_module_name,
                              name   = name,
                              soln   = json.dumps(soln))
        self.session.add(nm)

    def lookup_named_macro (self, lang, name):

        res = []

        for nm in self.session.query(model.NamedMacro).filter(model.NamedMacro.lang==lang).filter(model.NamedMacro.name==name):
            res.append(json.loads(nm.soln))

        return res

    def _expand_macros (self, lang, txt):

        logging.debug(u"expand macros  : %s" % txt)

        implicit_macros = {}

        txt2 = ''

        i = 0
        while i<len(txt):

            if txt[i] == '(':

                j = txt[i+1:].find(')')
                if j<0:
                    self.report_error (') missing')
                j += i

                # extract macro

                macro_s = txt[i+1:j+1]

                # print "macro_s: %s" % macro_s

                macro_name = 'MACRO_%d' % len(implicit_macros)

                implicit_macros[macro_name] = []
                for s in macro_s.split('|'):
                    sub_parts = tokenize(s, lang=lang, keep_punctuation=False)
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

        todo = [ (parts, 0, [], {}, {}) ]

        # import pdb; pdb.set_trace()
        while len(todo)>0:

            parts1, cnt, r, mpos, macro_rs = todo.pop()

            if cnt >= len(parts1):
                done.append((r, mpos))
                continue

            p1 = parts1[cnt]

            if cnt % 2 == 1:
                
                sub_parts = p1.split(':')

                if len(sub_parts) != 2:
                    self.report_error ('syntax error in macro call %s' % repr(p1))

                name = sub_parts[0]

                if name == 'empty':
                    todo.append((parts, cnt+1, copy(r), mpos, copy(macro_rs)))
                else:

                    vn    = sub_parts[1]

                    if name in macro_rs:
                        macro = [ macro_rs[name] ]
                    else:
                        macro = self.lookup_named_macro(lang, name)
                        if not macro:
                            macro = implicit_macros.get(name, None)
                        if not macro:
                            self.report_error ('unknown macro "%s"[%s] called' % (name, lang))

                    for r3 in macro:
                        r1        = copy(r)
                        mpos1     = copy(mpos)
                        macro_rs1 = copy(macro_rs)

                        macro_rs1[name] = r3

                        # take care of multiple invocactions of the same macro
        
                        mpnn = 0
                        while True:
                            mpn = '%s_%d_start' % (name, mpnn)
                            if not mpn in mpos1:
                                break
                            mpnn += 1

                        mpos1['%s_%d_start' % (name, mpnn)] = len(r1)
                        s3 = r3[vn]
                        if isinstance (s3, basestring):
                            s3 = tokenize (s3, lang=lang)
                            r3[vn] = s3
                        r1.extend(r3[vn])
                        mpos1['%s_%d_end' % (name, mpnn)]   = len(r1)

                        for vn3 in r3:
                            mpos1['%s_%d_%s' % (name, mpnn, vn3.lower())] = r3[vn3]

                        todo.append((parts, cnt+1, r1, mpos1, macro_rs1))
                        
                        # if name == 'home_locations':
                        #     import pdb; pdb.set_trace()

            else:

                sub_parts = tokenize(p1, lang=lang, keep_punctuation=False)

                r  = copy(r)
                r.extend(sub_parts)

                todo.append((parts, cnt+1, r, mpos, macro_rs))

        return done

    def set_prefixes (self, prefixes):
        self.prefixes = prefixes

    def generate_training_data (self, lang, inps, md5s, code_fn, args):

        prefixes = self.prefixes if self.prefixes else [u'']

        for prefix in prefixes:

            for inp in inps:

                pinp = prefix + inp

                for d, mpos in self._expand_macros(lang, pinp):

                    d_inps = u' '.join(d)
                    # if d_inps == u'subtract five from eleven':
                    #     import pdb; pdb.set_trace()
                    # logging.info(repr(mpos))

                    if args:
                        d_args = map(lambda x: mpos[x] if x in mpos else x, args)
                    else:
                        d_args = None

                    td = model.TrainingData(lang     = lang, 
                                            module   = self.data_module_name, 
                                            inp      = d_inps, 
                                            md5s     = md5s,
                                            args     = json.dumps(d_args),
                                            loc_fn   = self.src_location[0], 
                                            loc_line = self.src_location[1])
                    self.session.add(td)

                    self.cnt_dt += 1
                    if self.cnt_dt % 100 == 0:
                        logging.info ('%6d training samples extracted so far...' % self.cnt_dt)

    def _unindent(self, code):
        lines = code.split('\n')
        indent_len = 0
        for line in lines:
            stripped = line.strip()
            if stripped:
                indent_len = line.index(stripped[0])
                break
        if indent_len == 0:
            return code

        new_lines = []
        for line in lines:
            if line.strip():
                line = line[indent_len:]
            new_lines.append(line)
        return u'\n'.join(new_lines)

    def dt(self, lang, inps, resp, args=None):

        if isinstance (inps, basestring):
            inps = [ inps ]
            
        # transform response(s) to a python code snipped, has it + put in db

        if isinstance (resp, list):
            code_src = "def _resp(c):\n"
            for r in resp:
                code_src += "    c.resp(u\"%s\", 0.0, [])\n" % r
            code_fn  = '_resp'

        elif isinstance (resp, basestring):
            code_src = "def _resp(c):\n"
            code_src += "    c.resp(u\"%s\", 0.0, [])\n" % resp
            code_fn  = '_resp'
            
        else:

            code_src = inspect.getsource(resp)
            code_src = self._unindent(code_src)
            logging.debug('dte: code_src=%s' % code_src)
            code_ast = ast.parse(code_src)

            for node in ast.walk(code_ast):
                if isinstance(node, ast.FunctionDef):
                    code_fn  = node.name
                    code_src = codegen.to_source(node)
                    break
        
        md5s = self.store_code(code_src, code_fn)
 
        # caller's source location:

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)

        self.src_location = (calframe[1][1], calframe[1][2])

        # use macro engine to generate input strings

        self.generate_training_data (lang, inps, md5s, code_fn, args)

        # import pdb; pdb.set_trace()
 
    def ts (self, lang, test_name, rounds, prep=None):

        # import pdb; pdb.set_trace()

        # caller's source location:

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)

        self.src_location = (calframe[1][1], calframe[1][2])

        # normalize rounds by tokenizing inp/resp
        rs = []
        for r in rounds:

            md5s = None
            arg  = None
            if len(r)>2:
                code     = r[2]
                if code:
                    code_src = inspect.getsource(code)
                    code_src = self._unindent(code_src)
                    code_ast = ast.parse(code_src)

                    for node in ast.walk(code_ast):
                        if isinstance(node, ast.FunctionDef):
                            code_fn  = node.name
                            code_src = codegen.to_source(node)
                            md5s = self.store_code(code_src, code_fn)
                            break
                if len(r)>3:
                    arg = r[3]

            rs.append((u' '.join(tokenize(r[0], lang=lang)),
                       u' '.join(tokenize(r[1], lang=lang)),
                       md5s, arg))

        # extract prep code, if any

        if prep:
            src_txt = inspect.getsource(prep)

            src_txt = self._unindent(src_txt)

            src_ast = ast.parse(src_txt)

            code_ast = None

            for node in ast.walk(src_ast):
                if isinstance(node, ast.FunctionDef):
                    prep_ast = node
                    prep_fn  = node.name
                    break

            if prep_ast:
                prep_code = codegen.to_source(prep_ast)

        else:
            prep_code = None 
            prep_fn   = None

        tc = model.TestCase(lang      = lang,
                            module    = self.data_module_name,
                            name      = test_name,
                            prep_code = prep_code,
                            prep_fn   = prep_fn,
                            rounds    = json.dumps(rs),
                            loc_fn    = self.src_location[0], 
                            loc_line  = self.src_location[1])
        self.session.add(tc)

        self.cnt_ts += 1

    def lookup_tests (self, module_name):

        data_ts = []
        
        for ts in self.session.query(model.TestCase).filter(model.TestCase.module==module_name).order_by(model.TestCase.name).all():

            data_ts.append( (ts.name, ts.lang, ts.prep_code, ts.prep_fn, json.loads(ts.rounds), ts.loc_fn, ts.loc_line) )

        return data_ts

    def ner (self, lang, cls, entity, label):

        l_tok = u' '.join(tokenize(label, lang=lang))

        nd = model.NERData(lang   = lang,
                           module = self.data_module_name,
                           cls    = cls,
                           entity = entity,
                           label  = l_tok)
        self.session.add(nd)

