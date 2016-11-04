#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2015, 2016 Guenter Bartsch
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
# HAL-PROLOG engine
#
# based on http://openbookproject.net/py4fun/prolog/prolog3.html by Chris Meyers
#

import os
import sys
import logging
import codecs
import re
import copy

from logic import *

class PrologRuntimeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def prolog_unary_plus  (a) : return NumberLiteral(a)
def prolog_unary_minus (a) : return NumberLiteral(-a)

unary_operators = {'+': prolog_unary_plus, 
                   '-': prolog_unary_minus}

def prolog_binary_add (a,b) : return NumberLiteral(a + b)
def prolog_binary_sub (a,b) : return NumberLiteral(a - b)
def prolog_binary_mul (a,b) : return NumberLiteral(a * b)

binary_operators = {'+': prolog_binary_add, 
                    '-': prolog_binary_sub, 
                    '*': prolog_binary_mul}

def prolog_eval (term, env):      # eval all variables within a term to constants

    if isinstance(term, Predicate):
        if len(term.args) == 1:
            op = unary_operators.get(term.name)
            if op:

                a = prolog_eval(term.args[0],env)

                if not isinstance (a, NumberLiteral):
                    return None

                return op(a.f)

        op = binary_operators.get(term.name)
        if op:
            if len(term.args) != 2:
                return None

            a = prolog_eval(term.args[0],env)

            if not isinstance (a, NumberLiteral):
                return None

            b = prolog_eval(term.args[1],env)

            if not isinstance (b, NumberLiteral):
                return None

            return op(a.f, b.f)

    if isinstance (term, Literal):
        return term
    if isinstance (term, Variable):
        ans = env.get(term.name)
        if not ans:
            return None
        else: 
            return prolog_eval(ans,env)
    args = []
    for arg in term.args : 
        a = prolog_eval(arg,env)
        if not a: 
            return None
        args.append(a)
    return Predicate(term.name, args)

# helper functions (used by builtin predicates)
def prolog_get_int(term, env):

    t = prolog_eval (term, env)

    if not isinstance (t, NumberLiteral):
        raise PrologRuntimeError('Integer expected, %s found instead.' % term.__class__)
    return int(t.f)

def prolog_get_float(term, env):

    t = prolog_eval (term, env)

    if not isinstance (t, NumberLiteral):
        raise PrologRuntimeError('Float expected, %s found instead.' % term.__class__)
    return t.f

def prolog_get_string(term, env):

    t = prolog_eval (term, env)

    if not isinstance (t, StringLiteral):
        raise PrologRuntimeError('String expected, %s found instead.' % t.__class__)
    return t.s

def prolog_get_literal(term, env):

    t = prolog_eval (term, env)

    if not isinstance (t, Literal):
        raise PrologRuntimeError('Literal expected, %s found instead.' % t.__class__)
    return t.get_literal()

def prolog_get_bool(term, env):

    t = prolog_eval (term, env)

    if not isinstance(t, Predicate):
        raise PrologRuntimeError('Boolean expected, %s found instead.' % term.__class__)
    return t.name == 'true'

def prolog_get_variable(term, env):

    if not isinstance(term, Variable):
        raise PrologRuntimeError('Variable expected, %s found instead.' % term.__class__)
    return term.name


class PrologGoal:

    def __init__ (self, clause, parent=None, env={}) :

        self.clause = clause
        self.parent = parent
        self.env    = copy.deepcopy(env)
        self.inx    = 0      # start search with 1st subgoal

    def __str__ (self) :
        return "Goal clause=%s inx=%d env=%s" % (self.clause, self.inx, self.env)

    def get_depth (self):
        if not self.parent:
            return 0
        return self.parent.get_depth() + 1

class PrologEngine(object):

    def register_builtin (self, name, builtin):
        self.builtins[name] = builtin

    def set_trace(self, trace):
        self.trace = trace

    def __init__(self, db):
        self.db           = db
        self.builtins     = {}
        self.context_name = 'test'
        self.trace        = False

    # A Goal is a rule in at a certain point in its computation. 
    # env contains definitions (so far), inx indexes the current term
    # being satisfied, parent is another Goal which spawned this one
    # and which we will unify back to when this Goal is complete.

    def _unify (self, src, srcEnv, dest, destEnv) :
        "update dest env from src. return true if unification succeeds"
        # logging.debug("Unify %s %s to %s %s" % (src, srcEnv, dest, destEnv))

        # FIXME: ?!? if src.pred == '_' or dest.pred == '_' : return sts(1,"Wildcard")

        if isinstance (src, Variable):
            srcVal = prolog_eval(src, srcEnv)
            if not srcVal: 
                return True 
            else: 
                return self._unify(srcVal, srcEnv, dest, destEnv)

        if isinstance (dest, Variable):
            destVal = prolog_eval(dest, destEnv)     # evaluate destination
            if destVal: 
                return self._unify(src, srcEnv, destVal, destEnv)
            else:
                destEnv[dest.name] = prolog_eval(src, srcEnv)
                return True                         # unifies. destination updated

        elif isinstance (src, Literal):
            srcVal = prolog_eval(src, srcEnv)
            destVal = prolog_eval(dest, destEnv)
            return srcVal == destVal
            
        elif isinstance (dest, Literal):
            return False

        elif src.name != dest.name:
            return False
        elif len(src.args) != len(dest.args): 
            return False
        else:
            dde = copy.deepcopy(destEnv)
            for i in range(len(src.args)):
                if not self._unify(src.args[i],srcEnv,dest.args[i],dde):
                    return False
            destEnv.update(dde)
            return True

    def _trace (self, label, goal):

        if not self.trace:
            return

        depth = goal.get_depth()
        ind = depth * '  ' + len(label) * ' '

        if goal.inx < len(goal.clause.body):
            print u"%s %s: %s" % (depth*'  ', label, unicode(goal.clause.body[goal.inx]))
            print u"%s : %s" % (ind, unicode(goal.clause))
        else:
            print u"%s %s: %s" % (depth*'  ', label, unicode(goal.clause))

        print "%s : %s" % (ind, repr(goal.env))



    def search (self, clause):

        queue     = [ PrologGoal (clause) ]
        solutions = []

        while queue :
            g = queue.pop()                         # Next goal to consider

            self._trace ('CONSIDER', g)

            # logging.debug ('g=%s' % str(g))
            if g.inx >= len(g.clause.body) :        # Is this one finished?
                self._trace ('SUCCESS ', g)
                # logging.debug ('finished: ' + str(g))
                if g.parent == None :               # Yes. Our original goal?
                    solutions.append(g.env)         # Record solution
                    continue
                parent = copy.deepcopy(g.parent)    # Otherwise resume parent goal
                self._unify (g.clause.head, g.env,
                             parent.clause.body[parent.inx], parent.env)
                parent.inx = parent.inx+1           # advance to next goal in body
                queue.insert(0,parent)              # let it wait its turn
                # logging.debug ("queue: %s" % str(parent))
                continue

            # No. more to do with this goal.
            pred = g.clause.body[g.inx]             # What we want to solve

            name = pred.name
            if name in ['is', 'cut', 'fail'] :
                if name == 'is' :
                    ques = prolog_eval(pred.args[0], g.env)
                    ans  = prolog_eval(pred.args[1], g.env)
                    if ques == None :
                        g.env[pred.args[0].name] = ans  # Set variable
                    elif ques.name != ans.name :
                        self._trace ('FAIL    ', g)
                        continue                # Mismatch, fail
                elif name == 'cut' : queue = [] # Zap the competition
                elif name == 'fail':            # Dont succeed
                    self._trace ('FAIL    ', g)
                    continue
                g.inx = g.inx + 1               # Succeed. resume self.
                queue.insert(0, g)
                continue

            # builtin predicate ?

            if pred.name in self.builtins:
                if self.builtins[pred.name](g, self):
                    self._trace ('BUILTIN ', g)
                    g.inx = g.inx + 1
                    queue.insert (0, g)
                else:
                    self._trace ('FAIL    ', g)
                continue

            # Not special. look up in rule database

            clauses = self.db.lookup(pred.name)

            if len(clauses) == 0:
                raise PrologRuntimeError ('Failed to find predicate "%s" !' % pred.name)

            for clause in clauses:

                if len(clause.head.args) != len(pred.args): 
                    continue

                child = PrologGoal(clause, g)       # A possible subgoal

                ans = self._unify (pred, g.env, clause.head, child.env)
                if ans:                             # if unifies, queue it up
                    queue.insert(0, child)
                    # logging.debug ("Queue %s" % str(child))

        return solutions

