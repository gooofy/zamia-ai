#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import logging
import rdflib
from rdflib.plugins.sparql.parserutils import CompValue

from zamiaprolog.errors import PrologRuntimeError
from aiprolog.runtime   import build_algebra
from nltools.tokenizer  import tokenize
from aiprolog.pl2rdf    import rdf_to_pl

#     atom_chars(LANG, LSTR),
# 
#     rdf (distinct,
#          PERSON, wdpd:InstanceOf,   wde:Human,
#          PERSON, rdfs:label,        LABEL,
#          PERSON, wdpd:FamilyName,   FN,
#          FN,     rdfs:label,        FAMILY_NAME,
#          filter (lang(LABEL) = LSTR),
#          filter (lang(FAMILY_NAME) = LSTR)),
# 
#     tokenize (LANG, FAMILY_NAME, FN_TOKENS),
# 
#     NAME_TOKENS = FN_TOKENS.

def builtin_ner_person(g, pe):

    """ ner_person ( +Lang, +Name_Tokens, -Person, -Label ) """

    pe._trace ('CALLED BUILTIN ner_person', g)

    pred = g.terms[g.inx]
    args = pred.args

    if len(args) != 4:
        raise PrologRuntimeError('ner_person: 4 args ( +Lang, +Name_Tokens, -Person, -Label ) expected.', g.location)

    arg_Lang        = pe.prolog_get_constant(args[0], g.env, g.location)
    arg_Name_Tokens = pe.prolog_get_list(args[1], g.env, g.location)
    name            = u' '.join(arg_Name_Tokens.l)
    arg_Person      = pe.prolog_get_variable(args[2], g.env, g.location)
    arg_Label       = pe.prolog_get_variable(args[3], g.env, g.location)

    res_bindings    = []

    print arg_Lang, arg_Name_Tokens

    #  rdf (distinct,
    #       PERSON, wdpd:InstanceOf,   wde:Human,
    #       PERSON, rdfs:label,        LABEL,
    #       filter (lang(LABEL) = LSTR)),

    #  tokenize (LANG, LABEL, LABEL_TOKENS),

    #  NAME_TOKENS = LABEL_TOKENS.

    var_map = { 
                'PERSON'      : rdflib.term.Variable('PERSON'),
                'LABEL'       : rdflib.term.Variable('LABEL'), 
              }

    triples = [
                (var_map['PERSON'], 
                 rdflib.term.URIRef(pe.kb.resolve_aliases_prefixes('wdpd:InstanceOf')), 
                 rdflib.term.URIRef(pe.kb.resolve_aliases_prefixes('wde:Human')) 
                ),
                (var_map['PERSON'], 
                 rdflib.term.URIRef(pe.kb.resolve_aliases_prefixes('rdfs:label')), 
                 var_map['LABEL'] 
                ),
              ]

    # filter (lang(LABEL) = LSTR),
    # filter (lang(FAMILY_NAME) = LSTR)),
    filters = [ 
                CompValue ('RelationalExpression', 
                           op    = '=', 
                           expr  = CompValue ('Builtin_LANG', 
                                              arg = var_map['LABEL'],
                                              _vars = set(var_map.values())),
                           other = rdflib.term.Literal(arg_Lang),
                           _vars = set(var_map.values())),
              ]
    algebra = build_algebra(var_map, triples, filters=filters, distinct=True)
    
    logging.debug ('algebra: %s' % (repr(algebra)))

    result = pe.kb.query_algebra (algebra)

    logging.debug ('result (len: %d): %s' % (len(result), repr(result)))

    # filter, turn result into list of bindings

    for binding in result:

        tokens = tokenize(unicode(binding['LABEL']))

        label = u' '.join(tokens)
        if label != name:
            continue

        res_binding = { 
                        arg_Person: rdf_to_pl(binding['PERSON']),
                        arg_Label : rdf_to_pl(binding['LABEL' ])
                      }

        logging.debug ('binding: %s LABEL: %s %s, binding: %s' % (binding, binding['LABEL'], repr(tokens), repr(res_binding)))
        # import pdb; pdb.set_trace()
    
        res_bindings.append(res_binding)

    #  rdf (distinct,
    #       PERSON, wdpd:InstanceOf,   wde:Human,
    #       PERSON, rdfs:label,        LABEL,
    #       PERSON, wdpd:FamilyName,   FN,
    #       FN,     rdfs:label,        FAMILY_NAME,
    #       filter (lang(LABEL) = LSTR),
    #       filter (lang(FAMILY_NAME) = LSTR)),
    # 
    #  tokenize (LANG, FAMILY_NAME, FN_TOKENS),
    # 
    #  NAME_TOKENS = FN_TOKENS.
    
    var_map = { 
                'PERSON'      : rdflib.term.Variable('PERSON'),
                'LABEL'       : rdflib.term.Variable('LABEL'), 
                'FN'          : rdflib.term.Variable('FN'),
                'FAMILY_NAME' : rdflib.term.Variable('FAMILY_NAME') 
              }

    triples = [
                (var_map['PERSON'], 
                 rdflib.term.URIRef(pe.kb.resolve_aliases_prefixes('wdpd:InstanceOf')), 
                 rdflib.term.URIRef(pe.kb.resolve_aliases_prefixes('wde:Human')) 
                ),
                (var_map['PERSON'], 
                 rdflib.term.URIRef(pe.kb.resolve_aliases_prefixes('rdfs:label')), 
                 var_map['LABEL'] 
                ),
                (var_map['PERSON'], 
                 rdflib.term.URIRef(pe.kb.resolve_aliases_prefixes('wdpd:FamilyName')), 
                 var_map['FN'] 
                ),
                (var_map['FN'], 
                 rdflib.term.URIRef(pe.kb.resolve_aliases_prefixes('rdfs:label')), 
                 var_map['FAMILY_NAME'] 
                ),
              ]

    # filter (lang(LABEL) = LSTR),
    # filter (lang(FAMILY_NAME) = LSTR)),
    filters = [ 
                CompValue ('RelationalExpression', 
                           op    = '=', 
                           expr  = CompValue ('Builtin_LANG', 
                                              arg = var_map['LABEL'],
                                              _vars = set(var_map.values())),
                           other = rdflib.term.Literal(arg_Lang),
                           _vars = set(var_map.values())),
                CompValue ('RelationalExpression', 
                           op    = '=', 
                           expr  = CompValue ('Builtin_LANG', 
                                              arg = var_map['FAMILY_NAME'],
                                              _vars = set(var_map.values())),
                           other = rdflib.term.Literal(arg_Lang),
                           _vars = set(var_map.values())),
              ]
    algebra = build_algebra(var_map, triples, filters=filters, distinct=True)
    
    logging.debug ('algebra: %s' % (repr(algebra)))

    result = pe.kb.query_algebra (algebra)

    logging.debug ('result (len: %d): %s' % (len(result), repr(result)))

    # filter, turn result into list of bindings

    for binding in result:

        tokens = tokenize(unicode(binding['FAMILY_NAME']))

        family_name = u' '.join(tokens)
        if family_name != name:
            continue

        res_binding = { 
                        arg_Person: rdf_to_pl(binding['PERSON']),
                        arg_Label : rdf_to_pl(binding['LABEL' ])
                      }

        logging.debug ('binding: %s FAMILY_NAME: %s %s, binding: %s' % (binding, binding['FAMILY_NAME'], repr(tokens), repr(res_binding)))
        # import pdb; pdb.set_trace()
    
        res_bindings.append(res_binding)

    logging.debug ('res_bindings: %s' % repr(res_bindings))

    return res_bindings

