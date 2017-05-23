#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import logging
from zamiaprolog.logic    import NumberLiteral, Predicate
from zamiaprolog.builtins import do_gensym, do_assertz_predicate

def builtin_fnvm_graph (g, pe):

    """ builtin_fnvm_graph ( +Vmc, -RootFrame ) """

    pe._trace ('CALLED BUILTIN builtin_fnvm_graph', g)

    pred = g.terms[g.inx]
    args = pred.args

    if len(args) != 2:
        raise PrologRuntimeError('builtin_fnvm_graph: 2 args ( +Vmc, -RootFrame ) expected.', g.location)

    arg_Vmc       = pe.prolog_get_list     (args[0], g.env, g.location)
    arg_RootFrame = pe.prolog_get_variable (args[1], g.env, g.location)

    stack       = []
    frames      = []
    frames_dict = {} # frame -> type

    r = {}

    for c in arg_Vmc.l:
        
        if c.name == 'fe':
            stack.append(c)
            continue

        if c.name == 'frame':

            # create new frame, fill fame elements from fe's on the stack

            framesym = do_gensym(pe, 'frame')
            r = do_assertz_predicate(g.env, 'frame', [framesym, 'type', c.args[0]], res=r)

            while len(stack)>0:
                sf = stack[len(stack)-1]
                
                if sf.name == 'fe':
                    fe = stack.pop()
                    k = fe.args[0]
                    v = fe.args[1]

                    if isinstance(v, Predicate) and v.name == 'vm_frame_pop':
                        v = frames.pop()

                    r = do_assertz_predicate(g.env, 'frame', [framesym, k, v], res=r) 

                    continue

                break

            frames.append(framesym)
            frames_dict[framesym] = c.args[0]

            continue

        raise PrologRuntimeError('unexpected FNVM command encountered: %s' % c.name, g.location)

    # import pdb; pdb.set_trace()

    # now run layer 3 processing (l3proc) on the last frame generated

    if len(frames)==0:
        raise PrologRuntimeError('no frame left on stack', g.location)
        
    last_frame = frames[len(frames)-1]

    r[arg_RootFrame] = Predicate(last_frame)

    return [r]

def builtin_frame_modify (g, pe):

    """ builtin_frame_modify ( +OldFrame, +FE, +V, -NewFrame ) """

    pe._trace ('CALLED BUILTIN builtin_frame_modify', g)

    pred = g.terms[g.inx]
    args = pred.args

    if len(args) != 4:
        raise PrologRuntimeError('builtin_frame_modify: 4 args ( +OldFrame, +FE, +V, -NewFrame ) expected.', g.location)

    arg_OldFrame  = pe.prolog_get_constant (args[0], g.env, g.location)
    arg_FE        = pe.prolog_get_constant (args[1], g.env, g.location)
    arg_V         = pe.prolog_eval         (args[2], g.env, g.location)
    arg_NewFrame  = pe.prolog_get_variable (args[3], g.env, g.location)

    solutions = pe.search_predicate('frame', [arg_OldFrame, 'FE', 'V'], env=g.env, location=g.location, err_on_missing=False)

    framesym = do_gensym(pe, 'frame')

    r = {}
    for s in solutions:
        if s['FE'].name != arg_FE:
            r = do_assertz_predicate(g.env, 'frame', [framesym, s['FE'].name, s['V']], res=r)
        else:
            r = do_assertz_predicate(g.env, 'frame', [framesym, s['FE'].name, arg_V], res=r)

    r[arg_NewFrame] = Predicate(framesym)

    return [r]

