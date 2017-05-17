%prolog

%
% basic implementation of the BeingBorn frame
%

fill_blanks (I, F, fnBeingBorn, child) :- frame(F, child, C).
fill_blanks (I, F, fnBeingBorn, child) :- 
    not(frame(F, child, C)), 
    ias(I, prevIAS, PREVI),
    context_search_l2(I, PREVI, 100, 25, URFRAME, L1FRAMETYPE, L1FRAME, L1FE, L2FRAMETYPE, L2FRAME, L2FE, CHILD),
    is_human(CHILD), % FIXME: animals and maybe other creatures are born, too
    assertz(frame(F, child, CHILD)).

fill_blanks (I, F, fnBeingBorn, time) :- frame(F, time, T).
fill_blanks (I, F, fnBeingBorn, time) :- 
    frame(F, child, HUMAN), 
    rdf (distinct, limit(1),
         HUMAN,   wdpd:DateOfBirth,  BIRTHDATE),
    assertz(frame(F, time, BIRTHDATE)).

fill_blanks (I, F, fnBeingBorn, place) :- frame(F, place, P).
fill_blanks (I, F, fnBeingBorn, place) :- 
    frame(F, child, HUMAN), 
    rdf (distinct, limit(1),
         HUMAN,   wdpd:PlaceOfBirth,  BIRTHPLACE),
    assertz(frame(F, place, BIRTHPLACE)).

fill_blanks (I, F, fnBeingBorn) :-
    fill_blanks (I, F, fnBeingBorn, child),
    fill_blanks (I, F, fnBeingBorn, place),
    fill_blanks (I, F, fnBeingBorn, time).

answerz (I, en, personBeenBornWhen, LABEL, BD_SCRIPT, GENDER) :- sayz(I, en, format_str("%s was born on %s", LABEL, BD_SCRIPT)).
answerz (I, en, personBeenBornWhen, LABEL, BD_SCRIPT, male)   :- sayz(I, en, format_str("he was born on %s", BD_SCRIPT)).
answerz (I, en, personBeenBornWhen, LABEL, BD_SCRIPT, female) :- sayz(I, en, format_str("she was born on %s", BD_SCRIPT)).

answerz (I, de, personBeenBornWhen, LABEL, BD_SCRIPT, GENDER) :- sayz(I, de, format_str("%s wurde am %s geboren", LABEL, BD_SCRIPT)).
answerz (I, de, personBeenBornWhen, LABEL, BD_SCRIPT, male)   :- sayz(I, de, format_str("er wurde am %s geboren", BD_SCRIPT)).
answerz (I, de, personBeenBornWhen, LABEL, BD_SCRIPT, female) :- sayz(I, de, format_str("sie wurde am %s geboren", BD_SCRIPT)).

l4proc (I, F, fnTelling, time, MSGF, fnBeingBorn) :-

    frame (MSGF, child, HUMAN),
    frame (MSGF, time, BD),    

    ias (I, uttLang, LANG),

    transcribe_date(LANG, dativ, BD, BD_SCRIPT),
    % BD_SCRIPT is BD,
    entity_gender(HUMAN, GENDER),

    entity_label(LANG, HUMAN, LABEL),

    answerz (I, LANG, personBeenBornWhen, LABEL, BD_SCRIPT, GENDER).


l3proc (I, F, fnQuestioning, MSGF, fnBeingBorn) :-

    frame (F, top, time),

    fill_blanks (I, MSGF),

    % remember our utterance interpretation

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user about birth time)
    
    list_append(VMC, fe(msg,  MSGF)),
    list_append(VMC, fe(top,  time)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,  USER)),
    list_append(VMC, fe(spkr, uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 100),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    l4proc (I).

answerz (I, en, personBeenBornWhere, LABEL, BP_LABEL, GENDER) :- sayz(I, en, format_str("%s was born in %s", LABEL, BP_LABEL)).
answerz (I, en, personBeenBornWhere, LABEL, BP_LABEL, male)   :- sayz(I, en, format_str("he was born in %s", BP_LABEL)).
answerz (I, en, personBeenBornWhere, LABEL, BP_LABEL, female) :- sayz(I, en, format_str("she was born in %s", BP_LABEL)).

answerz (I, de, personBeenBornWhere, LABEL, BP_LABEL, GENDER) :- sayz(I, de, format_str("%s wurde in %s geboren", LABEL, BP_LABEL)).
answerz (I, de, personBeenBornWhere, LABEL, BP_LABEL, male)   :- sayz(I, de, format_str("er wurde in %s geboren", BP_LABEL)).
answerz (I, de, personBeenBornWhere, LABEL, BP_LABEL, female) :- sayz(I, de, format_str("sie wurde in %s geboren", BP_LABEL)).

l4proc (I, F, fnTelling, place, MSGF, fnBeingBorn) :-

    frame (MSGF, child, HUMAN),
    frame (MSGF, place, BP),    

    entity_gender(HUMAN, GENDER),

    ias (I, uttLang, LANG),

    entity_label(LANG, HUMAN, LABEL),
    entity_label(LANG, BP, BP_LABEL),

    answerz (I, LANG, personBeenBornWhere, LABEL, BP_LABEL, GENDER).

l3proc (I, F, fnQuestioning, MSGF, fnBeingBorn) :-

    frame (F, top, place),

    fill_blanks (I, MSGF),

    % remember our utterance interpretation

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user about birth time)
    
    list_append(VMC, fe(msg,  MSGF)),
    list_append(VMC, fe(top,  place)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,  USER)),
    list_append(VMC, fe(spkr, uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 100),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    l4proc (I).

%
% tell user topic of fnBeingBorn frame
%

answerz (I, en, topicOfBeingBornFrame, LABEL) :- sayz(I, en, format_str("%s's birthday", LABEL)).
answerz (I, en, topicOfBeingBornFrame, LABEL) :- sayz(I, en, format_str("%s's birth", LABEL)).
answerz (I, de, topicOfBeingBornFrame, LABEL) :- sayz(I, de, format_str("%ss Geburtstag", LABEL)).
answerz (I, de, topicOfBeingBornFrame, LABEL) :- sayz(I, de, format_str("%ss Geburt", LABEL)).

l4proc (I, F, fnTelling, topic, MSGF, fnBeingBorn) :-

    frame (MSGF, child, HUMAN),

    ias (I, uttLang, LANG),

    entity_label(LANG, HUMAN, LABEL),

    answerz (I, LANG, topicOfBeingBornFrame, LABEL).

