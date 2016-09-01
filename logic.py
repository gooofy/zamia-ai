#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015 Guenter Bartsch
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
# classes that represent basic first order and clausal logic
# plus conversion function from FOL to clausal
#

import logging
import datetime
from dateutil.tz import tzlocal

skolem_index = 0

def _next_skolem_const():
    global skolem_index
    skolem_index += 1
    return 'g'+str(skolem_index)

class Literal:

    def __unicode__(self):
        return "<LITERAL>"

    def _remove_implications(self):
        return self

    def _skolemize(self, var_map = {}, forall_vars = set()):
        return self

    def _distribute_and_over_or(self):
        return False, self

class StringLiteral(Literal):

    def __init__(self, s):
        self.s = s

    def __unicode__(self):
        return '"' + self.s + '"'

    def __eq__(self, other):
        return isinstance(other, StringLiteral) and other.s == self.s

    def get_literal(self):
        return self.s

class NumberLiteral(Literal):

    def __init__(self, f):
        self.f = f

    def __unicode__(self):
        return unicode(self.f)

    def __str__(self):
        return str(self.f)

    def __repr__(self):
        return repr(self.f)

    def __eq__(self, other):
        return isinstance(other, NumberLiteral) and other.f == self.f

    def get_literal(self):
        return self.f

class Variable(object):

    counter = 0 
    @staticmethod
    def get_unused_var():
        v = Var('_var%d' % Var.counter)
        Var.counter += 1
        return v

    def __init__(self, name, row = False):
        self.name = name
        self.row  = row
  
    def __unicode__(self):
        return '@' + self.name if self.row else self.name

    def __eq__(self, other):
        return isinstance(other, Variable) and other.name == self.name

    def __hash__(self):
        return hash(self.name)

    def _remove_implications(self):
        return self

    def _move_negation_inwards(self):
        return self

    def _skolemize(self, var_map = {}, forall_vars = set()):
        if not self.name in var_map:
            return self
        return var_map[self.name]

class Predicate:

    def __init__(self, name, args=None, uri = None):
        self.name  = name
        self.args  = args if args else []
        self.uri   = uri 
  
    def __str__(self):
        if not self.args:
            return self.name
        return '%s(%s)' % (self.name, ', '.join(map(str, self.args)))
    
    def __unicode__(self):
        if not self.args:
            return self.name
        return u'%s(%s)' % (self.name, u', '.join(map(unicode, self.args)))
        #return '(' + self.name + ' ' + ' '.join( [str(arg) for arg in self.args]) + ')'

    def __repr__(self):
        return self.__unicode__()

    def __eq__(self, other):
        return (isinstance(other, Predicate)
                and self.pred == other.pred
                and list(self.args) == list(other.args))

    def normalize(self, depth = 0):
        return self

    def _remove_implications(self):
        return self

    def _move_negation_inwards(self):
        return self

    def _skolemize(self, var_map = {}, forall_vars = set()):
        if not self.args:
            return self
        return Predicate (self.name, map(lambda a: a._skolemize(var_map, forall_vars), self.args), self.uri)

    def _flatten_and_or(self):
        return self

    def _distribute_and_over_or(self):
        return False, self

    def to_clausal_form(self):
        return Clause (self)

class Clause:

    def __init__(self, head, body=None):
        self.head = head
        self.body = body or []

    def __str__(self):
        if self.body:
            return u'%s :- %s.' % (str(self.head), ', '.join(map(str, self.body)))
        return str(self.head) + '.'

    def __unicode__(self):
        if self.body:
            return u'%s :- %s.' % (unicode(self.head), ', '.join(map(unicode, self.body)))
        return unicode(self.head) + '.'

    def __eq__(self, other):
        return (isinstance(other, Clause)
                and self.head == other.head
                and list(self.body) == list(other.body))


#############################################################################
#
# full-blown First Order Logic starts here
#
#############################################################################


FOLOP_IMPLICATION   = 'i'
FOLOP_BICONDITIONAL = 'b'
FOLOP_EQUALITY      = 'e'
FOLOP_NOT           = 'n'
FOLOP_AND           = 'a'
FOLOP_OR            = 'o'
FOLOP_EXISTS        = 'E'
FOLOP_FORALL        = 'A'

FOLOP_STR = { FOLOP_IMPLICATION   : "=>", 
              FOLOP_EQUALITY      : "=", 
              FOLOP_BICONDITIONAL : "<=>", 
              FOLOP_NOT           : "not", 
              FOLOP_AND           : "and", 
              FOLOP_OR            : "or", 
              FOLOP_EXISTS        : "exists", 
              FOLOP_FORALL        : "forall" } 


class FOLFormula:

    def __init__(self, operator, variables, ops):
        self.operator   = operator
        self.variables  = variables
        self.ops        = ops
  
    def __unicode__(self):
        if not self.variables:
            return '(' + FOLOP_STR[self.operator] + ' ' + ' '.join( [unicode(arg) for arg in self.ops]) + ')'
        return '(' + FOLOP_STR[self.operator] + ' (' + '  '.join( [unicode(v) for v in self.variables]) + ') ' + ', '.join( [unicode(arg) for arg in self.ops]) + ')'

    def _remove_implications(self):
        if self.operator == FOLOP_IMPLICATION:
            op0 = self.ops[0]._remove_implications()
            op1 = self.ops[1]._remove_implications()
            return FOLFormula (FOLOP_OR, None, [FOLFormula (FOLOP_NOT, None, [op0]), op1] )

        if self.operator == FOLOP_EQUALITY or self.operator == FOLOP_BICONDITIONAL:
            op0 = self.ops[0]._remove_implications()
            op1 = self.ops[1]._remove_implications()

            f1 = FOLFormula (FOLOP_AND, None, [op0, op1])
            f2 = FOLFormula (FOLOP_AND, None, [FOLFormula (FOLOP_NOT, None, [op0]), FOLFormula (FOLOP_NOT, None, [op1])])

            return FOLFormula (FOLOP_OR, None, [f1,f2])

        return FOLFormula (self.operator, self.variables, map(lambda o: o._remove_implications(), self.ops))

    def _move_negation_inwards(self):
        if self.operator != FOLOP_NOT:
            return FOLFormula (self.operator, self.variables, map(lambda o: o._move_negation_inwards(), self.ops))

        op0 = self.ops[0]

        if not isinstance(op0, FOLFormula):
            return FOLFormula (FOLOP_NOT, None, [op0])

        op0 = op0._move_negation_inwards()

        if op0.operator == FOLOP_AND:
            return FOLFormula (FOLOP_OR, None, map(lambda o: FOLFormula (FOLOP_NOT, None, [o])._move_negation_inwards(), op0.ops))
        if op0.operator == FOLOP_OR:
            return FOLFormula (FOLOP_AND, None, map(lambda o: FOLFormula (FOLOP_NOT, None, [o])._move_negation_inwards(), op0.ops))

        if op0.operator == FOLOP_EXISTS:
            return FOLFormula (FOLOP_FORALL, op0.variables, [ FOLFormula (FOLOP_NOT, None, [op0.ops[0]])._move_negation_inwards()])
        if op0.operator == FOLOP_FORALL:
            return FOLFormula (FOLOP_EXISTS, op0.variables, [ FOLFormula (FOLOP_NOT, None, [op0.ops[0]])._move_negation_inwards()])

        if op0.operator == FOLOP_NOT:
            return op0.ops[0]

        raise Exception ("move_negation_inwards: unsupported operation?!? " + unicode(op0.operator))

    def _skolemize(self, var_map = {}, forall_vars = set()):

        if self.operator == FOLOP_EXISTS:

            v = None
            if len(forall_vars)>0:
                v = []
                for var in forall_vars:
                    v.append(Variable(var))

            cm = var_map.copy()
            for var in self.variables:
                cm[var.name] = Predicate(_next_skolem_const(), v)

            return self.ops[0]._skolemize(cm, forall_vars)

        if self.operator == FOLOP_FORALL:
    
            cs = forall_vars.copy()
            for var in self.variables:
                cs.add(var.name)

            return self.ops[0]._skolemize(var_map, cs)
       
        return FOLFormula (self.operator, None, map(lambda o: o._skolemize(var_map, forall_vars), self.ops))
   
    def _flatten_and_or(self):

        if self.operator == FOLOP_AND or self.operator == FOLOP_OR:

            ops = []
            for op in self.ops:

                fop = op._flatten_and_or()

                if isinstance (fop, FOLFormula) and fop.operator == self.operator:
                    for cop in fop.ops:
                        ops.append(cop)
                else:
                    ops.append(fop)
            return FOLFormula (self.operator, None, ops)

        return self


    def _distribute_and_over_or(self):

        logging.debug ("_distribute_and_over_or: %s" % unicode(self))

        changed = False

        if self.operator == FOLOP_OR:

            ops = []
            for op in self.ops:
                c, o = op._distribute_and_over_or()
                ops.append(o)
                changed |= c

            first_and = None
            for op in ops:
                if isinstance (op, FOLFormula) and op.operator == FOLOP_AND:
                    first_and = op
                    break

            if not first_and:
                return changed, self

            remaining = []

            for op in ops:
                if op != first_and:
                    remaining.append(op)

            if len(remaining)>1:
                op2 = FOLFormula (FOLOP_OR, None, remaining)
            else:
                op2 = remaining[0]

            nops = []

            for op in first_and.ops:
                nops.append(FOLFormula (FOLOP_OR, None, [op, op2]))

            return True, FOLFormula (FOLOP_AND, None, nops)

        ops = []
        for op in self.ops:
            c, o = op._distribute_and_over_or()
            ops.append(o)
            changed |= c

        if changed:
            return True, FOLFormula (self.operator, self.variables, ops)

        return False, self


    def normalize(self):

        # import pdb; pdb.set_trace()

        logging.debug ("normalize             : %s" % unicode(self))
        f = self._remove_implications()
        logging.debug ("remove_implications   : %s" % unicode(f))
        f = f._move_negation_inwards()
        logging.debug ("move_negation_invwards: %s" % unicode(f))
        f = f._skolemize()
        logging.debug ("skolemize             : %s" % unicode(f))

        while True:
            c, f = f._distribute_and_over_or()
            logging.debug ("dist => %s" % unicode(f))
            f = f._flatten_and_or()
            logging.debug ("flat => %s" % unicode(f))
            if not c:
                break

        return f

    def to_clausal_form(self):

        norm = self.normalize()

        if isinstance (norm, Predicate):
            return Clause (norm)

        if not norm.operator == FOLOP_OR:
            logging.debug (" 1 NOT horn: %s" % unicode(self))
            return None

        # determine head clause
        heads = []
        body  = []
        for o in norm.ops:
            if isinstance (o, FOLFormula):
                if o.operator != FOLOP_NOT:
                    logging.debug (u" 2 NOT horn: %s" % unicode(norm))
                    return None
                body.append(o.ops[0])
            else:
                heads.append(o)
        
        if len(heads)==0:
            print "QUESTION?? %s" % unicode(self)
            return None

        if len(heads)>1:
            print "NOT horn: %s" % unicode(norm)
            return None

        return Clause (heads[0], body)

