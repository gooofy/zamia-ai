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
# macro-engine
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

from copy                import copy
from io                  import StringIO

from nltools.tokenizer   import tokenize

# class RewriteName(NodeTransformer):
# 
#     def visit_Name(self, node):
#         return copy_location(Subscript(value = Name(id='data', ctx=Load()),
#                                        slice = Index(value=Str(s=node.id)),
#                                        ctx   = node.ctx), 
#                              node)

class DataEngine(object):

    def __init__(self):

        self.md5               = hashlib.md5()

        self.prefixes          = []
        self.named_macros      = {}
        self.named_macros_mod  = {}
        self.code_map          = {}
        self.code_map_mod      = {}

        self.module_name       = None
        self.source_location   = ('unknown', 0)

    def report_error(self, s):
        raise Exception ("%s: error in line %d: %s" % (self.source_location[0], self.source_location[1], s))

    def prepare_compilation (self, module_name):
        self.clear(module_name)

        self.data_module_name = module_name
        self.data_train       = []
        self.data_test        = []
        self.data_ner         = {}
        self.data_pfx         = ""

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

    def compute_code_map(self):
        self.code_map = {}
        for module in self.code_map_mod:
            for n in self.code_map_mod[module]:
                if not n in self.code_map:
                    self.code_map[n] = []
                self.code_map[n].extend(self.code_map_mod[module][n])

    def clear (self, module_name):
        if module_name in self.named_macros_mod:
            del self.named_macros_mod[module_name]
        if module_name in self.code_map_mod:
            del self.code_map_mod[module_name]
        self.compute_named_macros()
        self.compute_code_map()
  
    def load (self, module_name):

        self.clear(module_name)

        fn = 'modules/%s/_macros.json' % module_name
        if os.path.exists(fn):
            with open(fn, 'r') as of:
                nmm = json.load(of)

                self.named_macros_mod[module_name] = nmm
                self.compute_named_macros()

    def save (self, module_name):
        fn = 'modules/%s/_macros.json' % module_name
        if module_name in self.named_macros_mod:
            with open(fn, 'w') as of:
                json.dump(self.named_macros_mod[module_name], of, indent=2)
        else:
            if os.path.exists(fn):
                os.unlink(fn)

        fn = 'modules/%s/_data.json' % module_name
        if module_name in self.code_map_mod:
            with open(fn, 'w') as of:
                json.dump(self.code_map_mod[module_name], of, indent=2)
        else:
            if os.path.exists(fn):
                os.unlink(fn)
 
    def macro(self, lang, name, soln):
        # import pdb; pdb.set_trace()
        if not lang in self.named_macros:
            self.named_macros[lang] = {}
        if not name in self.named_macros[lang]:
            self.named_macros[lang][name] = []

        self.named_macros[lang][name].append(soln)

        if not self.data_module_name in self.named_macros_mod:
            self.named_macros_mod[self.data_module_name] = {}
        if not lang in self.named_macros_mod[self.data_module_name]:
            self.named_macros_mod[self.data_module_name][lang] = {}
        if not name in self.named_macros_mod[self.data_module_name][lang]:
            self.named_macros_mod[self.data_module_name][lang][name] = []

        self.named_macros_mod[self.data_module_name][lang][name].append(soln)
 
    ###############################################
    #
    # training data extraction 
    #
    ###############################################

    def fetch_named_macro (self, lang, name):

        if not lang in self.named_macros:
            self.named_macros[lang] = {}

        if name in self.named_macros[lang]:
            return self.named_macros[lang][name]

        return None

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
                        macro = self.fetch_named_macro(lang, name)
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


    def _generate_training_code (self, lang, code_ast, mpos):

        # import pdb; pdb.set_trace()

        # FIXME:
        # use ast NodeTransformer to replace tstart / tend / mvar occurences

        # if a.name == 'tstart':

        #     if len(a.args) == 1:
        #         occ = 0
        #         tname = a.args[0]
        #     elif len(a.args) == 2:
        #         occ   = int(a.args[1].f)
        #         tname = a.args[0]
        #     else:
        #         self.report_error ('tstart: one or two args expected, found "%s" instead' % unicode(a))

        #     k = '%s_%d_start' % (tname, occ)
        #     if not k in mpos:
        #         self.report_error ('tstart: could not determine "%s"' % unicode(a))

        #     return NumberLiteral(mpos[k])

        # elif a.name == 'tend':

        #     if len(a.args) == 1:
        #         occ = 0
        #         tname = a.args[0]
        #     elif len(a.args) == 2:
        #         occ   = int(a.args[1].f)
        #         tname = a.args[0]
        #     else:
        #         self.report_error ('tend: one or two args expected, found "%s" instead' % unicode(a))

        #     k = '%s_%d_end' % (tname, occ)
        #     if not k in mpos:
        #         self.report_error ('tend: could not determine "%s"' % unicode(a))

        #     return NumberLiteral(mpos[k])

        # elif a.name == 'mvar':

        #     # import pdb; pdb.set_trace()
        #     if len(a.args) == 2:
        #         tname = a.args[0]
        #         vname = a.args[1]
        #         occ = 0
        #     elif len(a.args) == 3:
        #         tname = a.args[0]
        #         vname = a.args[1]
        #         occ   = int(a.args[2].f)
        #     else:
        #         self.report_error ('mvar: one or two args expected, found "%s" instead' % unicode(a))

        #     k = '%s_%d_%s' % (tname, occ, vname)
        #     if not k in mpos:
        #         self.report_error ('mvar: could not determine "%s"' % unicode(a))

        #     return mpos[k

        resp_code = codegen.to_source(code_ast)
        # print (resp_code)

        return resp_code

    def set_prefixes (self, prefixes):
        self.prefixes = prefixes

    def generate_training_data (self, lang, inps, code_ast):

        prefixes = self.prefixes if self.prefixes else [u'']
        if not self.data_module_name in self.code_map_mod:
            self.code_map_mod[self.data_module_name] = {}

        for prefix in prefixes:

            for inp in inps:

                pinp = prefix + inp

                for d, mpos in self._expand_macros(lang, pinp):

                    r = self._generate_training_code (lang, code_ast, mpos)

                    logging.debug( '%s -> %s' % (repr(d), repr(r)))

                    self.md5.update (r)
                    md5s = self.md5.hexdigest()
                    self.code_map[md5s]             = r
                    self.code_map_mod[self.data_module_name][md5s] = r

                    self.data_train.append((lang, d, md5s, self.src_location[0], self.src_location[1]))

                    if len(self.data_train) % 100 == 0:
                        logging.info ('%6d training samples extracted so far...' % len(self.data_train))

    # def extract_test_data (self, clause):

    #     if len(clause.head.args) != 2:
    #         self.report_error ('test: 2 arguments (lang, test_name) expected')

    #     self.lang = clause.head.args[0].name
    #     test_name = clause.head.args[1].name

    #     if not clause.body or clause.body.name != 'and':
    #         self.report_error ('test: flat (and) body expected')

    #     prep    = []
    #     rounds  = []

    #     inp     = None
    #     resp    = None
    #     actions = []
    #     cnt     = 0

    #     for a in clause.body.args:

    #         # import pdb; pdb.set_trace()
    #         if isinstance (a, StringLiteral):

    #             if cnt % 2 == 0:
    #                 if inp:
    #                     rounds.append ((inp, resp, actions))
    #                 inp     = tokenize(a.s, lang=self.lang, keep_punctuation = False)
    #                 resp    = None
    #                 actions = []

    #             else:
    #                 resp    = tokenize(a.s, lang=self.lang, keep_punctuation = False)

    #             cnt += 1
    #         else:

    #             if not inp:
    #                 prep.append(a)
    #             else:
    #                 if not isinstance(a, Predicate) or a.name != 'action':
    #                     self.report_error('only action predicates allowed here.')
    #                 actions.append(list(map (lambda x: unicode(x), a.args)))


    #     if inp:
    #         rounds.append ((inp, resp, actions))

    #     self.ts.append((test_name, self.lang, prep, rounds, clause.location.fn, clause.location.line, clause.location.col))

    # def extract_ner_training (self, clause):

    #     if len(clause.head.args) != 4:
    #         self.report_error ('train_ner: 4 arguments (+Lang, +Class, -Entity, -Label) expected')

    #     arg_Lang   = clause.head.args[0].name
    #     arg_Cls    = clause.head.args[1].name
    #     arg_Entity = clause.head.args[2].name
    #     arg_Label  = clause.head.args[3].name

    #     logging.info ('computing NER training data for %s [%s] ...' % (arg_Cls, arg_Lang))

    #     # cProfile.run('self.rt.search(clause)', 'mestats')
    #     # self.rt.set_trace(True)
    #     solutions = self.rt.search(clause)

    #     if not arg_Lang in self.ner:
    #         self.ner[arg_Lang] = {}

    #     if not arg_Cls in self.ner[arg_Lang]:
    #         self.ner[arg_Lang][arg_Cls] = {}
    #         
    #     ner = self.ner[arg_Lang][arg_Cls]

    #     cnt = 0
    #     for s in solutions:
    #         entity = s[arg_Entity].name
    #         label  = s[arg_Label].s

    #         ner[entity] = label
    #         cnt += 1

    #     logging.info ('computing NER training data for %s [%s] ... done. %d entries processed.' % (arg_Cls, arg_Lang, cnt))

    def dt_set_prefixes(self, prefixes):
        self.me.set_prefixes(prefixes)

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

    def dt(self, lang, inps, resp):

        if isinstance (inps, basestring):
            inps = [ inps ]
            
        # transform response(s)

        if isinstance (resp, list):
            src_txt = "def _resp(c):\n"
            for r in resp:
                src_txt += "    c.response(u\"%s\", 0.0, [])\n" % r
            code_ast = ast.parse(src_txt)

        elif isinstance (resp, basestring):
            src_txt = "def _resp(c):\n"
            src_txt += "    c.response(u\"%s\", 0.0, [])\n" % resp
            code_ast = ast.parse(src_txt)
            
        else:
            src_txt = inspect.getsource(resp)

            src_txt = self._unindent(src_txt)

            src_ast = ast.parse(src_txt)

            code_ast = None

            for node in ast.walk(src_ast):
                if isinstance(node, ast.FunctionDef):
                    code_ast = node
                    break
          
        # caller's source location:

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)

        self.src_location = (calframe[1][1], calframe[1][2])

        # use macro engine to generate input strings

        self.generate_training_data (lang, inps, code_ast)

        # import pdb; pdb.set_trace()
 
