#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017, 2018 Guenter Bartsch, Heiko Schaefer
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
# convert RDF to Prolog
#

import os
import sys
import traceback
import codecs
import logging
import random
import time
import rdflib
import dateutil.parser

from optparse    import OptionParser
from nltools     import misc
from config      import RDF_PREFIXES

DEFAULT_OUTPUT     = 'bar.pl'
DEFAULT_LOGLEVEL   = logging.INFO
LEM_FN             = 'etc/lem.csv'
LPM_FN             = 'etc/lpm.csv'
RDF_SCHEMA_LABEL   = rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#label')
LANGUAGES          = set([u'en', u'de'])
LEGAL_ENTITY_CHARS = set(u"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖÙÚÛÜÝßàáâãäåæçèéêëìíîïðñòóôõöùúûüý")

def mangle_prolog(n, start_uppercase=False):

    res = u''
    make_upper = start_uppercase # to enforce CamelCase

    for c in n:
        if not c.isalnum():
            make_upper = True
            continue
        if make_upper:
            c = c.upper()
            make_upper=False

        if c in LEGAL_ENTITY_CHARS:
            res += c
        else:
            res += u"U%d" % ord(c)
    return res

def mangle_url(s, do_exc=True):
    prefix = None
    for p, url in RDF_PREFIXES.items():
        if not s.startswith(url):
            continue
        n      = s[len(url):]
        prefix = p
        break

    if not prefix:
        if do_exc:
            raise Exception ('no prefix for %s found' % s)
        return None

    return prefix + mangle_prolog(n, start_uppercase=True)

def entity_label(s, label):

    prefix = None
    for p, url in RDF_PREFIXES.items():
        if not s.startswith(url):
            continue
        prefix = p
        break

    if not prefix:
        raise Exception ('no prefix for %s found' % s)

    l = prefix + mangle_prolog(label, start_uppercase=True)

    return l[:100]

def property2entity_mapper(p):

    up = unicode(p)

    if up.startswith('http://www.wikidata.org/prop/direct/'):
        return 'wdpd', rdflib.URIRef('http://www.wikidata.org/entity/' + p[36:])
    if up.startswith('http://www.wikidata.org/qualifier/'):
        return 'wdpq', rdflib.URIRef('http://www.wikidata.org/entity/' + p[34:])
    if up.startswith('http://www.wikidata.org/prop/statement/'):
        return 'wdps', rdflib.URIRef('http://www.wikidata.org/entity/' + p[39:])
    if up.startswith('http://www.wikidata.org/prop/'):
        return 'wdp', rdflib.URIRef('http://www.wikidata.org/entity/' + p[29:])
    return None, None

def property_label(p):

    global lpm, plm, g

    if p in plm:
        return plm[p]

    prefix, pe = property2entity_mapper(p)
    if not pe:

        l = mangle_url(p)

    else:

        triples = list(g.triples((pe, RDF_SCHEMA_LABEL, None)))

        l      = None
        for t in triples:

            s, p2, o = t

            if o.language != 'en':
                continue

            l = prefix + mangle_prolog(unicode(o), start_uppercase=True)

        if not l:
            return None
            

    # make unique

    label = l
    cnt = 1
    while label in lpm and lpm[label] != p:
        label = l + unicode(cnt)
        cnt += 1

    lpm[label] = p
    plm[p]     = label

    return label

#
# init, cmdline
#

misc.init_app('rdf2prolog')

parser = OptionParser("usage: %prog [options] foo.n3")

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")
parser.add_option ("-o", "--output", dest="outputfn", type = "string", default=DEFAULT_OUTPUT,
                   help="output file, default: %s" % DEFAULT_OUTPUT)

(options, args) = parser.parse_args()

if len(args) != 1:
    parser.print_usage()
    sys.exit(1)

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

inputfn  = args[0]
outputfn = options.outputfn

#
# get everything
#

logging.info ('parsing %s ...' % inputfn)

g = rdflib.Graph()
g.parse(inputfn, format='n3')

logging.info ('parsing %s ... extracting triples ...' % inputfn)
triples = list(g)

logging.info ('parsing %s ... extracting triples ... got %d triples.' % (inputfn, len(triples)))

#
# entity labels
#

lem = {} # label -> entity
elm = {} # entity -> label

#
# read existing entity labels
#

if os.path.isfile(LEM_FN):

    with codecs.open(LEM_FN, 'r', 'utf8') as f:

        while True:

            line = f.readline()
            if not line:
                break

            line = line.strip()
            if len(line)==0:
                continue

            if 'Unlabeled' in line:
                logging.info ('ignoring line: %s' % line)
                continue

            if 'unlabeled' in line:
                logging.info ('ignoring line: %s' % line)
                continue

            parts = line.split(',')
            elu = mangle_prolog(parts[0])
            entity = rdflib.URIRef(u','.join(parts[1:]))

            if elu in lem:
                raise Exception (u'error while parsing %s: entity label %s is not unique!' % (LEM_FN, elu))

            lem[elu]    = entity
            elm[entity] = elu

#
# generate missing entity labels from rdfsLabels
#

for t in triples:

    s, p, o = t

    if s in elm:
        continue

    label_base = None

    # 1: see if we have an rdfsLabel

    for s2, p2, o2 in g.triples((s, RDF_SCHEMA_LABEL, None)):
        if not isinstance(o2, rdflib.Literal) or o2.language != 'en':
            continue
        label_base = unicode(o2)
        break

    if label_base:
        el = entity_label (s, label_base)
    else:
        el = mangle_url(unicode(s))

    # ensure label is unique

    elu = el

    cnt = 1
    while elu in lem and lem[elu] != s:
        elu = el + unicode(cnt)
        cnt += 1
    
    lem[elu] = s
    elm[s]   = elu

    #print s, elu

logging.debug ('have unique labels for %d entities' % len(lem))

#
# load existing property labels
#

lpm = {} # label    -> property
plm = {} # property -> label

if os.path.isfile(LPM_FN):
    with codecs.open(LPM_FN, 'r', 'utf8') as f:

        while True:

            line = f.readline()
            if not line:
                break

            line = line.strip()
            if len(line)==0:
                continue

            parts = line.split(',')
            label = parts[0]
            prop  = rdflib.URIRef(u','.join(parts[1:]))

            if label in lpm:
                raise Exception (u'error while parsing %s: entity label %s is not unique!' % (LEM_FN, elu))

            lpm[label] = prop
            plm[prop]  = label

def prolog_string_escape (o):

    s = unicode(o)
    # s = s.replace('\\',' ').replace ("'", "\\'")
    s = s.replace('\\',' ').replace ('"', '\\"')

    return s

#
# generate prolog, generate and cache property labels as we encounter them
#

cnt = 0

prolog_code = []
predicate_set = set()
for elu in lem:

    entity = lem[elu]

    cnt += 1

    triples = list(g.triples((entity, None, None)))

    if len(triples)==0:
        continue

    logging.info ('%5d/%5d generating prolog code for %s ...' % (cnt, len(lem), elu))

    # f.write(u'\n%% URI: %s\n\n' % unicode(entity))

    for s, p, o in triples:

        if not s in elm:
            continue
        el = elm[s]

        try:
            el.decode('ascii')
        except UnicodeDecodeError:
            el = u"'" + el + u"'"

        pl = property_label(p)
        if not pl:
            logging.debug (u'Skipping1: %s(%s, %s).\n' % (unicode(p), el, unicode(o)))
            continue

        try:

            if isinstance(o, rdflib.term.Literal):
                if o.datatype:

                    datatype = str(o.datatype)

                    if datatype == 'http://www.w3.org/2001/XMLSchema#decimal':
                        prolog_code.append(u"%s(%s, %s).\n" % (pl, el, unicode(o)))
                        predicate_set.add(u'%s/2' % pl)
                        continue
                    elif datatype == 'http://www.w3.org/2001/XMLSchema#float':
                        prolog_code.append(u"%s(%s, %s).\n" % (pl, el, unicode(o)))
                        predicate_set.add(u'%s/2' % pl)
                        continue
                    elif datatype == 'http://www.w3.org/2001/XMLSchema#integer':
                        prolog_code.append(u"%s(%s, %s).\n" % (pl, el, unicode(o)))
                        predicate_set.add(u'%s/2' % pl)
                        continue
                    elif datatype == 'http://www.w3.org/2001/XMLSchema#dateTime':
                        dt = dateutil.parser.parse(unicode(o))
                        prolog_code.append(u'%s(%s, "%s").\n' % (pl, el, dt.isoformat()))
                        predicate_set.add(u'%s/2' % pl)
                        continue
                    elif datatype == 'http://www.w3.org/2001/XMLSchema#date':
                        dt = dateutil.parser.parse(unicode(o))
                        prolog_code.append(u'%s(%s, "%s").\n' % (pl, el, dt.isoformat()))
                        predicate_set.add(u'%s/2' % pl)
                        continue
                    elif datatype == 'http://www.opengis.net/ont/geosparql#wktLiteral':
                        # FIXME
                        prolog_code.append(u'%s(%s, "%s").\n' % (pl, el, unicode(o)))
                        predicate_set.add(u'%s/2' % pl)
                        continue
                    elif datatype == 'http://www.w3.org/1998/Math/MathML':
                        # FIXME
                        continue
                     
                    else:
                        raise Exception('unknown literal datatype %s (value: %s) .' % (datatype, unicode(o)))
                else:
                    if o.value is None:
                        prolog_code.append(u"%s(%s, []).\n" % (pl, el))
                        predicate_set.add(u'%s/2' % pl)
                        continue
                    if o.language:
                        if o.language in LANGUAGES:
                            prolog_code.append(u'%s(%s, %s, "%s").\n' % (pl, el, o.language, prolog_string_escape(o)))
                            predicate_set.add(u'%s/3' % pl)
                        continue

                    prolog_code.append(u'%s(%s, "%s").\n' % (pl, el, prolog_string_escape(o)))
                    predicate_set.add(u'%s/2' % pl)
                    continue

            elif isinstance (o, rdflib.term.URIRef):
                if o in elm:
                    ol = elm[o]
                else:
                    # ol = u"'" + unicode(o) + "'"
                    ol = mangle_url(str(o), do_exc=False)
                if not ol:
                    logging.debug (u'Skipping2: %s(%s, %s).\n' % (pl, el, unicode(o)))
                    continue

                prolog_code.append(u"%s(%s, %s).\n" % (pl, el, ol))
                predicate_set.add(u'%s/2' % pl)
            else:
                raise Exception ('unknown term: %s (%s %s)' % (unicode(o), type(o), o.__class__))
        except:
            logging.error(u'Failed to convert %s: %s' % (unicode(o), traceback.format_exc()))

with codecs.open(outputfn, 'w', 'utf8') as f:

    f.write('%prolog\n')

    for p in sorted(predicate_set):
        f.write(u':- multifile %s.\n' % p)

    f.write('\n')

    for pc in sorted(prolog_code):
        f.write(pc)

logging.info (' %s written' % outputfn)

#
# dump out all property and entity labels to keep them the same in future runs
#

with codecs.open(LPM_FN, 'w', 'utf8') as f:
    for plu in sorted(lpm):
        if 'Unlabeled' in plu:
            continue
        if 'unlabeled' in plu:
            continue
        prop = lpm[plu]
        f.write(u'%s,%s\n' % (plu, prop))

logging.info (' %s written' % LPM_FN)

with codecs.open(LEM_FN, 'w', 'utf8') as f:
    for elu in sorted(lem):
        if 'Unlabeled' in elu:
            continue
        if 'unlabeled' in elu:
            continue
        entity = lem[elu]
        f.write(u'%s,%s\n' % (elu, unicode(entity)))

logging.info (' %s written' % LEM_FN)

