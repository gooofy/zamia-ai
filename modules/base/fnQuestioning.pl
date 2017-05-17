%prolog

%
% if we do not have a msg frame, use a previous one
%
l3proc (I, F, fnQuestioning) :-

    uriref (aiu:self, SELF),
    frame (F, add, SELF),
    not (frame (F, msg, MSGF)),

    log (info, "l3proc looking for fnQuestioning msg frame..."),

    context_search_l2(I, I, 100, 25, uframe, fnQuestioning, L1FRAME, msg, MSGFT, MSGF),

    log (info, "l3proc looking for fnQuestioning msg frame... found one."),

    assertz(frame(F, msg, MSGF)),

    l3proc (I, F, fnQuestioning, MSGF, MSGFT).

%
% map question with known msg frame to 2-layer l3proc search
%

l3proc (I, F, fnQuestioning) :-

    uriref (aiu:self, SELF),
    frame (F, add, SELF),

    % look for message frame + type, run l3proc on it

    frame(F, msg, MSGF),
    frame(MSGF, type, MSGFT),

    l3proc (I, F, fnQuestioning, MSGF, MSGFT).

%
% low score don't know answer to all questions
%

l3proc (I, F, fnQuestioning) :-

    uriref (aiu:self, SELF),
    frame (F, add, SELF),

    % remember our utterance interpretation

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user we don't know)
    
    list_append(VMC, fe(degr, none)),
    list_append(VMC, fe(cog,  uriref(aiu:self))),
    list_append(VMC, frame(fnAwareness)),

    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  topic)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,  USER)),
    list_append(VMC, fe(spkr, uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    % log (info, 'fnQuestioning basic answer'),
    % trace(on),

    l4proc (I).

l2proc_andWhereContext :-
    list_append(VMC, fe(top,  place)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    fnvm_exec (I, VMC) .

nlp_gen (en, '(and|) (where|in which place|in which town) (again|)?',
         inline(l2proc_andWhereContext)).

nlp_gen (de, '(und|) (wo|an welchem ort|in welcher stadt) (nochmal|)?',
         inline(l2proc_andWhereContext)).

