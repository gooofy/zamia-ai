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

