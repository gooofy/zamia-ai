#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Guenter Bartsch
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
# simple conversion helper tool for AI Prolog -> Python
#

import os
import sys
import traceback
import codecs
import logging
import random
import time

from optparse import OptionParser

from zamiaprolog.parser  import PrologParser, SYM_EOF
from zamiaprolog.logic   import StringLiteral, ListLiteral, Predicate, Variable, Clause

from nltools             import misc

DEFAULT_OUTPUT = 'foo.py'

td_count = 0

# nlp_gens (en,"@SELF_ADDRESS:LABEL (all|) (men|women) are (all|) (alike|the same)",
#              "in what way?").

# STATE_NORMAL = 0
# STATE_MACRO  = 1
# STATE_CHOICE = 2
# 
# TEST_OFFSET=0
# 
# def convert_macro_string(ms):
# 
#     pos   = 0
#     state = STATE_NORMAL
#     curs  = u''
#     res   = []
#     while pos<len(ms):
# 
#         c = ms[pos]
# 
#         if state == STATE_NORMAL:
#             
#             if c=='@':
#                 if len(curs.strip())>0:
#                     res.append(StringLiteral(curs.strip()))
#                 curs = u''
#                 state = STATE_MACRO
#             elif c=='(':
#                 if len(curs.strip())>0:
#                     res.append(StringLiteral(curs.strip()))
#                 curs = u''
#                 choices = []
#                 state = STATE_CHOICE
#             else:
#                 curs += c
# 
#         elif state == STATE_MACRO:
#             if c==' ':
#                 state = STATE_NORMAL
#         elif state == STATE_CHOICE:
#             if c==')':
#                 state = STATE_NORMAL
#                 choices.append(StringLiteral(curs))
#                 curs = u''
#                 res.append(ListLiteral(choices))
#             elif c=='|':
#                 choices.append(StringLiteral(curs))
#                 curs = u''
#             else:
#                 curs += c
#         pos += 1
#        
#     if state == STATE_NORMAL:
#         if len(curs.strip())>0:
#             res.append(StringLiteral(curs.strip()))
# 
#     return ListLiteral(res)
# 
# 
# def convert_nlp_gens(pred):
# 
#     global outf
# 
#     lang  = pred.args[0].name
#     ms    = pred.args[1].s.replace(u'@SELF_ADDRESS:LABEL ', u'')
#     resps = pred.args[2:]
# 
#     # res = convert_macro_string(ms)
# 
#     outf.write(u'\n')
#     outf.write(u"train(%s) :-\n" % lang)
#     outf.write(u'    "%s",\n' % ms)
# 
#     if len(resps) == 1:
#         outf.write(u'    "%s".\n' % resps[0].s)
#     else:
#         for i, r in enumerate(resps):
#             if i == len(resps)-1:
#                 outf.write(u'       "%s").\n' %r.s)
#             elif i == 0:
#                 outf.write(u'    or("%s",\n' %r.s)
#             else:
#                 outf.write(u'       "%s",\n' %r.s)
# 
# def convert_nlp_macro(clause):
# 
#     global outf
# 
#     lang  = clause.head.args[0].name
#     name  = clause.head.args[1].s.lower()
#     mvars = clause.head.args[2:]
# 
#     outf.write(u'\n')
#     outf.write(u"macro(%s, %s" % (lang, name))
#     for v in mvars:
#         outf.write(u", %s" % v)
#     outf.write (u") :- %s.\n" % unicode(clause.body))
# 
# 
# def convert_nlp_gen(pred):
# 
#     # print "% ", unicode(pred)
# 
#     lang = pred.args[0].name
#     ms   = pred.args[1].s.replace(u'@SELF_ADDRESS:LABEL ', u'')
# 
#     outf.write(u'\n')
#     outf.write(u"train(%s) :-\n" % lang)
#     outf.write(u'    "%s",\n' % ms)
#     for i, r in enumerate(pred.args[2:]):
#         if i == len(pred.args)-3:
#             outf.write(u'    %s.\n' % unicode(r))
#         else:
#             outf.write(u'    %s,\n' % unicode(r))
# 
# def convert_answerz(c):
# 
#     pred = c.head
# 
#     lang = pred.args[1].name
#     n    = pred.args[2].name
# 
#     pred = c.body
# 
#     s    = pred.args[2].s
# 
#     head = Predicate(name='nlp_%s_r' % MODULE_NAME, args=[Predicate(name=lang), Predicate(name=n), Variable(name='R')])
# 
#     body = Predicate(name='says', args=[Predicate(name=lang), Variable(name='R'), StringLiteral(s)])
# 
#     clause = Clause (head=head, body=body)
# 
#     print unicode(clause)
# 
#     # import pdb; pdb.set_trace()
#     
# test_cnt = TEST_OFFSET
# 
# def convert_nlp_test(pred):
# 
#     global test_cnt, outf
# 
#     # print "% ", unicode(pred)
# 
#     lang      = pred.args[0].name
#     test_name = 't%04d' % test_cnt
#     test_cnt += 1
# 
#     outf.write(u'\n')
#     outf.write(u"test(%s, %s) :-\n" % (lang, test_name))
# 
#     for i, ivr in enumerate(pred.args[1:]):
#         
#         ivr_in  = ivr.args[0].args[0].s
#         ivr_out = ivr.args[1].args[0].s
# 
#         outf.write(u'    "%s",\n' % ivr_in)
#         outf.write(u'    "%s"'    % ivr_out)
# 
#         if i == len(pred.args)-2:
#             outf.write ('.\n')
#         else:
#             outf.write (',\n')
# 
#     # import pdb; pdb.set_trace()
# 
# def convert_nlp_test2(pred):
# 
#     global test_cnt, outf
# 
#     # print "% ", unicode(pred)
# 
#     lang      = pred.args[1].name
#     test_name = pred.args[2].s
# 
#     # test_name = 't%04d' % test_cnt
#     test_cnt += 1
# 
#     outf.write(u'\n')
#     outf.write(u"test(%s, %s) :-\n" % (lang, test_name))
# 
#     test_prep = pred.args[3].l
# 
#     for p in test_prep:
#         outf.write(u'    %% prep: %s,\n' % unicode(p))
# 
#     ivrs = pred.args[4].l
# 
#     offset = 0
#     while offset < len(ivrs):
#         
#         ivr_in      = ivrs[offset].s
#         ivr_out     = ivrs[offset+1].s
#         ivr_actions = ivrs[offset+2].l
# 
#         offset += 3
# 
#         outf.write(u'    "%s",\n' % ivr_in)
#         outf.write(u'    "%s"'    % ivr_out)
#         if ivr_actions:
#             outf.write(u'\n    %% actions %s'    % repr(ivr_actions))
# 
#         if offset == len(ivrs):
#             outf.write ('.\n')
#         else:
#             outf.write (',\n')
# 
#     # import pdb; pdb.set_trace()

def convert_train_prefix(pred):

    global outf

    prefix = pred.args[0].s

    outf.write(u"    k.dt_set_prefix('%s')\n" % prefix)

def convert_train(clause):

    global outf, td_count

    lang = clause.head.args[0].name

    if not isinstance(clause.body, Predicate) or clause.body.name != 'and':
        outf.write(u"#    %s\n" % unicode(clause))
        return

    if len(clause.body.args) != 2:
        outf.write(u"#    %s\n" % unicode(clause))
        return

    if isinstance(clause.body.args[0], StringLiteral):
        inp = clause.body.args[0].s
    elif isinstance(clause.body.args[0], Predicate) and clause.body.args[0].name == 'or':
        inp = []
        for a in clause.body.args[0].args:
            if not isinstance(a, StringLiteral):
                outf.write(u"#    %s\n" % unicode(clause))
                return
            inp.append(a.s)
    else:
        outf.write(u"#    %s\n" % unicode(clause))
        return

    if isinstance(clause.body.args[1], StringLiteral):
        resp = clause.body.args[1].s
    elif isinstance(clause.body.args[1], Predicate) and clause.body.args[1].name == 'or':
        resp = []
        for a in clause.body.args[1].args:
            if not isinstance(a, StringLiteral):
                outf.write(u"#    %s\n" % unicode(clause))
                return
            resp.append(a.s)
    else:
        outf.write(u"#    %s\n" % unicode(clause))
        return

    outf.write(u"    k.dt('%s', " % lang)

    if isinstance(inp,basestring) and isinstance(resp,basestring):
        outf.write(u"u\"%s\", u\"%s\")\n" % (inp, resp))
    else:
        if isinstance(inp, basestring):
            outf.write(u"u\"%s\",\n" % inp)
        else:
            if len(inp) == 0:
                outf.write(u"[],\n")
            else:
                outf.write(u"[u\"%s\"" % inp[0])
                for i in inp[1:]:
                    outf.write(u",\n")
                    outf.write(u"                u\"%s\"" % i)
                outf.write (u"],\n")

        if isinstance(resp, basestring):
            outf.write(u"               u\"%s\"" % resp)
        else:
            if len(resp) == 0:
                outf.write(u"               []")
            else:
                outf.write(u"               [u\"%s\"" % resp[0])
                for i in resp[1:]:
                    outf.write(u",\n")
                    outf.write(u"                u\"%s\"" % i)
                outf.write (u"]")

        outf.write(u")\n")

    td_count += 1
    if td_count % 2 == 0:
        outf.write("\n")

#
# init, cmdline
#

misc.init_app('aip2py')

parser = OptionParser("usage: %prog [options] foo.aip")

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")
parser.add_option ("-o", "--output", dest="outputfn", type = "string", default=DEFAULT_OUTPUT,
                   help="output file, default: %s" % DEFAULT_OUTPUT)

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if len(args) != 1:
    logging.error('exactly one input file needed.')
    parser.print_help()
    sys.exit(1)

inputfn  = args[0]
outputfn = options.outputfn

#
# main
#


db = None

parser = PrologParser(db)

with codecs.open(outputfn, 'w', 'utf8') as outf:

    outf.write('#!/usr/bin/env python\n')
    outf.write('# -*- coding: utf-8 -*-\n\n')

    outf.write('def get_data(k):\n')

    with codecs.open(inputfn, 'r', 'utf8') as f:

        parser.start(f, inputfn, module_name='foo')

        while parser.cur_sym != SYM_EOF:
            clauses = parser.clause()

            for clause in clauses:

                if clause.head.name == 'train_prefix':
                    convert_train_prefix(clause.head)
                elif clause.head.name == 'train':
                    convert_train(clause)
                    
                else:
                    outf.write(u"#    %s\n" % unicode(clause))
                    continue

logging.info ('%s written.' % outputfn)

