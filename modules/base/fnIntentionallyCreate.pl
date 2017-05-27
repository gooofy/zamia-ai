%prolog

l2proc_whenWasEntityCreatedContext :-

    log (debug, 'l2 whenWasEntityCreatedContext ...'),

    list_append(VMC, frame(fnIntentionallyCreate)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  time)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    log (debug, 'l2 whenWasEntityCreatedContext done '),
    fnvm_exec (I, VMC).
   
nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) do you (happen to|) know when it was (made|produced) (by the way|)?',
         inline(l2proc_whenWasEntityCreatedContext)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) weisst du (eigentlich|) wann er (gedreht|gemacht) wurde?',
         inline(l2proc_whenWasEntityCreatedContext)).

answerz (I, en, whenWasEntityCreated, E_LABEL, Y)   :- sayz(I, en, format_str("%s was created in %s", E_LABEL, Y)).
answerz (I, de, whenWasEntityCreated, E_LABEL, Y)   :- sayz(I, de, format_str("%s ist aus %s",        E_LABEL, Y)).

l4proc (I, F, fnTelling, time, MSGF, fnIntentionallyCreate) :-

    frame (MSGF, ent,  ENTITY),
    frame (MSGF, time, TIME),

    ias (I, uttLang, LANG),

    entity_label(LANG, ENTITY, E_LABEL),
    stamp_date_time(TIME, date(Y,M,D,H,Mn,S,'local')),

    answerz (I, LANG, whenWasEntityCreated, E_LABEL, Y).

l2proc_whoCreatedEntityContext :-

    log (debug, 'l2 whoCreatedEntity ...'),

    list_append(VMC, frame(fnIntentionallyCreate)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  creator)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    log (debug, 'l2 whoCreatedEntity done '),
    fnvm_exec (I, VMC).
   
nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) do you (happen to|) know who (made|produced|created) it (by the way|)?',
         inline(l2proc_whoCreatedEntityContext)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) weisst du (eigentlich|) wer (es|ihn|das|den) (gedreht|gemacht|produziert) hat?',
         inline(l2proc_whoCreatedEntityContext)).

l3proc (I, F, fnQuestioning, MSGF, fnIntentionallyCreate) :-

    log (debug, 'l3 fnQuestioning:fnIntentionallyCreate 1 ...'),

    frame (F,    top,  TOP),

    % if there is no entity given, we have to find one in previous frames

    or (
        frame (MSGF, ent,  ENTITY),
        context_search_l2(I, I, 100, 25, URFRAME, L1FRAMETYPE, L1FRAME, L1FE, L2FRAMETYPE, L2FRAME, ent, ENTITY)
       ),

    % remember our utterance interpretation

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user about some aspect of that entity's creation)

    % trace(on),

    lookup_entity_creation_info (ENTITY, CREATOR, TIME),

    list_append(VMC, fe(ent,      ENTITY)),
    list_append(VMC, fe(creator,  CREATOR)),
    list_append(VMC, fe(time,     TIME)),
    list_append(VMC, frame(fnIntentionallyCreate)),

    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  TOP)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,  USER)),
    list_append(VMC, fe(spkr, uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    % trace(off),

    scorez(I, 100),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    log (debug, 'l3 fnQuestioning:fnIntentionallyCreate 1 done'),

    % generate response actions
    
    l4proc (I).

answerz (I, en, entityCreatedBy, E_LABEL, C_LABEL) :- sayz(I, en, format_str("%s was created by %s", E_LABEL, C_LABEL)).
answerz (I, de, entityCreatedBy, E_LABEL, C_LABEL) :- sayz(I, de, format_str("%s wurde von %s gemacht", E_LABEL, C_LABEL)).

l4proc (I, F, fnTelling, creator, MSGF, fnIntentionallyCreate) :-

    frame (MSGF, ent,     ENTITY),
    frame (MSGF, creator, CREATOR),

    ias (I, uttLang, LANG),

    entity_label(LANG, ENTITY,  E_LABEL),
    entity_label(LANG, CREATOR, C_LABEL),

    answerz (I, LANG, entityCreatedBy, E_LABEL, C_LABEL).

