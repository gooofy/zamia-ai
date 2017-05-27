%prolog

%
% if we do not have a msg frame, use a previous one
%
l3proc (I, F, fnQuestioning) :-

    uriref (aiu:self, SELF),
    frame (F, add, SELF),
    not (frame (F, msg, MSGF)),

    log (debug, "l3proc looking for fnQuestioning msg frame..."),

    context_search_l2(I, I, 100, 25, uframe, fnQuestioning, L1FRAME, msg, MSGFT, MSGF),

    log (debug, "l3proc looking for fnQuestioning msg frame... found one."),

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

%
% re-run previous question while changing some aspect of it
%

l3proc (I, F, fnQuestioning, MSGF, zfQuestionAspect) :-

    uriref (aiu:self, SELF),
    frame (F, add, SELF),

    % log (info, "l3proc looking for previous fnQuestioning msg frame..."),

    context_search_l2(I, I, 100, 25, uframe, fnQuestioning, OL1F, msg, MSGFT, OMSGF),

    % log (info, "l3proc looking for previous fnQuestioning msg frame... found one."),

    % trace(on),

    ignore (
        or (
            and (
                frame (MSGF, place, PLACE), frame_modify (OMSGF, place, PLACE, TMSGF), scorez(I, 100)
                ),
            TMSGF is OMSGF
           )   
        ),
    ignore (
        or (
            and (
                frame (MSGF, time, TIME), frame_modify (TMSGF, time, TIME, NMSGF), scorez(I, 100)
                ),
            NMSGF is TMSGF
           )   
        ),
    %ignore (and (frame (MSGF, time, TIME), frame_modify (OMSGF, time, TIME, NMSGF))),

    frame_modify (OL1F, msg, NMSGF, NL1F),

    % trace(off),

    % assertz(frame(F, msg, NMSGF)),

    l3proc (I, NL1F, fnQuestioning, NMSGF, MSGFT).

l2proc_andWhereContext :-
    list_append(VMC, fe(top,  place)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    fnvm_exec (I, VMC) .

nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) (where|in which place|in which town) (again|)?',
         inline(l2proc_andWhereContext)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) (wo|an welchem ort|in welcher stadt) (nochmal|)?',
         inline(l2proc_andWhereContext)).

l2proc_andInLocationTokens(LANG) :-

    ner(LANG, I, geo_location, @GEO_LOCATION:TSTART_LABEL_0, @GEO_LOCATION:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(place, NER1ENTITY)),
    list_append(VMC, frame(zfQuestionAspect)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),

    fnvm_exec (I, VMC).
   
nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) (for|in|) @GEO_LOCATION:LABEL (again|)?',
         inline(l2proc_andInLocationTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) (für|in|) @GEO_LOCATION:LABEL (nochmal|)?',
         inline(l2proc_andInLocationTokens, de)).

l2proc_andInTimespecTokens :-

    list_append(VMC, fe(time, @TIMESPEC:TIME)),
    list_append(VMC, frame(zfQuestionAspect)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),

    fnvm_exec (I, VMC).
   
nlp_gen (en, '(and|) (for|in|) @TIMESPEC:W (again|)?',
         inline(l2proc_andInTimespecTokens)).
nlp_gen (de, '(und|) (für|in|) @TIMESPEC:W (nochmal|)?',
         inline(l2proc_andInTimespecTokens)).

l2proc_andInLocationTimespecTokens(LANG) :-

    % trace(on),

    ner(LANG, I, geo_location, @GEO_LOCATION:TSTART_LABEL_0, @GEO_LOCATION:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(place, NER1ENTITY)),
    list_append(VMC, fe(time, @TIMESPEC:TIME)),
    list_append(VMC, frame(zfQuestionAspect)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),

    fnvm_exec (I, VMC).
   
nlp_gen (en, '(and|) (for|in|) @TIMESPEC:W (and|) (for|in|) @GEO_LOCATION:LABEL (again|)?',
         inline(l2proc_andInLocationTimespecTokens, en)).
nlp_gen (de, '(und|) (für|in|) @TIMESPEC:W (und|) (für|in|) @GEO_LOCATION:LABEL (nochmal|)?',
         inline(l2proc_andInLocationTimespecTokens, de)).

nlp_gen (en, '(and|) (for|in|) @GEO_LOCATION:LABEL (and|) (for|in|) @TIMESPEC:W (again|)?',
         inline(l2proc_andInLocationTimespecTokens, en)).
nlp_gen (de, '(und|) (für|in|) @GEO_LOCATION:LABEL (und|) (für|in|) @TIMESPEC:W (nochmal|)?',
         inline(l2proc_andInLocationTimespecTokens, de)).

