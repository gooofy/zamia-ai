%prolog

% answer(topic, en) :-
%     context_score(topic, politics, 100, SCORE), say_eoa(en, 'We were talking about politics.', SCORE).
% answer(topic, de) :-
%     context_score(topic, politics, 100, SCORE), say_eoa(de, 'Politik war unser Thema.', SCORE).

%
% all politicians we know of
%

nlp_macro (en, 'KNOWN_POLITICIANS', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:PresidentOfTheUnitedStatesOfAmerica,
         filter (lang(LABEL) = 'en')).
nlp_macro (de, 'KNOWN_POLITICIANS', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:PresidentOfTheUnitedStatesOfAmerica,
         filter (lang(LABEL) = 'de')).
nlp_macro (en, 'KNOWN_POLITICIANS', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:PresidentOfGermany,
         filter (lang(LABEL) = 'en')).
nlp_macro (de, 'KNOWN_POLITICIANS', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:PresidentOfGermany,
         filter (lang(LABEL) = 'de')).
nlp_macro (en, 'KNOWN_POLITICIANS', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:FederalChancellorOfGermany,
         filter (lang(LABEL) = 'en')).
nlp_macro (de, 'KNOWN_POLITICIANS', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:FederalChancellorOfGermany,
         filter (lang(LABEL) = 'de')).

%
% US presidents
%

is_us_president(PERSON) :- 
    rdf(PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:PresidentOfTheUnitedStatesOfAmerica, 
        optional(OFFICE_STMT, wdpq:EndTime, END_TIME),
        filter(END_TIME is []), limit(1)).

was_us_president(PERSON) :- 
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:PresidentOfTheUnitedStatesOfAmerica).

person_political_status(PERSON, STATUS) :- 
    was_us_president(PERSON), 
    not (is_us_president(PERSON)),
    STATUS is former_us_president.
person_political_status(PERSON, STATUS) :- 
    is_us_president(PERSON),
    STATUS is current_us_president.

l3proc (I, F, fnQuestioning) :-

    frame (F, top,      general_info),
    frame (F, ent,      HUMAN),
    frame (F, entclass, human),

    was_us_president(HUMAN),

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user about person's status)
    
    CAT is uriref (wde:PresidentOfTheUnitedStatesOfAmerica),

    list_append(VMC, fe(cat,   CAT)),
    list_append(VMC, fe(item,  HUMAN)),
    list_append(VMC, frame(fnCategorization)),

    list_append(VMC, fe(msg,   vm_frame_pop)),
    list_append(VMC, fe(top,   category)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,   USER)),
    list_append(VMC, fe(spkr,  uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 150),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    l4proc (I).

nlp_test(en,
         ivr(in('Computer, do you know Donald Trump?'),
             out("yes i know donald trump"))).
nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Donald Trump?'),
             out('ja donald trump ist mir ein begriff'))).

nlp_test(en,
         ivr(in('Computer, who is Ronald Reagan?'),
             out("ronald reagan is categorized as president of the united states of america"))).
nlp_test(de,
         ivr(in('Computer, wer ist Ronald Reagan?'),
             out('ronald reagan ist in der kategorie präsident der vereinigten staaten'))).
%
% german chancellors
%

is_german_chancellor(PERSON) :- 
    rdf(PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany, 
        optional(OFFICE_STMT, wdpq:EndTime, END_TIME),
        filter(END_TIME is []), limit(1)).

was_german_chancellor(PERSON) :- 
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany).

l3proc (I, F, fnQuestioning) :-

    frame (F, top,      general_info),
    frame (F, ent,      HUMAN),
    frame (F, entclass, human),

    was_german_chancellor(HUMAN),

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user about person's status)
    
    CAT is uriref (wde:FederalChancellorOfGermany),

    list_append(VMC, fe(cat,   CAT)),
    list_append(VMC, fe(item,  HUMAN)),
    list_append(VMC, frame(fnCategorization)),

    list_append(VMC, fe(msg,   vm_frame_pop)),
    list_append(VMC, fe(top,   category)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,   USER)),
    list_append(VMC, fe(spkr,  uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 150),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    l4proc (I).

nlp_test(en,
         ivr(in('Computer, do you know Angela Merkel?'),
             out("yes i know angela merkel"))).
nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Angela Merkel?'),
             out('ja ich kenne angela merkel'))).

nlp_test(en,
         ivr(in('Computer, who is Helmut Kohl?'),
             out("helmut kohl is categorized as federal chancellor of germany"))).
nlp_test(de,
         ivr(in('Computer, wer ist Helmut Kohl?'),
             out('helmut kohl ist in der kategorie bundeskanzler'))).

%
% german presidents
%

is_german_president(PERSON) :- 
    rdf(PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:PresidentOfGermany, 
        optional(OFFICE_STMT, wdpq:EndTime, END_TIME),
        filter(END_TIME is []), limit(1)).

was_german_president(PERSON) :- 
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:PresidentOfGermany).

l3proc (I, F, fnQuestioning) :-

    frame (F, top,      general_info),
    frame (F, ent,      HUMAN),
    frame (F, entclass, human),

    was_german_president(HUMAN),

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user about person's status)
    
    CAT is uriref (wde:PresidentOfGermany),

    list_append(VMC, fe(cat,   CAT)),
    list_append(VMC, fe(item,  HUMAN)),
    list_append(VMC, frame(fnCategorization)),

    list_append(VMC, fe(msg,   vm_frame_pop)),
    list_append(VMC, fe(top,   category)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,   USER)),
    list_append(VMC, fe(spkr,  uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 150),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    l4proc (I).

nlp_test(en,
         ivr(in('Computer, do you know Frank-Walter Steinmeier?'),
             out("yes i know frank walter steinmeier"))).
nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Frank-Walter Steinmeier?'),
             out('ja ich kenne frank walter steinmeier'))).

nlp_test(en,
         ivr(in('Computer, who is Joachim Gauck?'),
             out("joachim gauck is categorized as president of germany"))).
nlp_test(de,
         ivr(in('Computer, wer ist Joachim Gauck?'),
             out('joachim gauck ist in der kategorie bundespräsident'))).

%
% successors / predecessors in office
%

answerz (I, en, politicalPredecessor, P_LABEL, S_LABEL, R_LABEL) :- sayz(I, en, format_str("Predecessor of %s in the role %s was %s", S_LABEL, R_LABEL, P_LABEL)).
answerz (I, de, politicalPredecessor, P_LABEL, S_LABEL, R_LABEL) :- sayz(I, de, format_str("Vorgänger von %s in der Rolle %s war %s", S_LABEL, R_LABEL, P_LABEL)).

l4proc (I, F, fnTelling, ldr_o, MSGF, fnChangeOfLeadership) :-

    frame (MSGF, ldr_o, PREDECESSOR),
    frame (MSGF, ldr_n, SUCCESSOR),
    frame (MSGF, role,  ROLE),    

    ias (I, uttLang, LANG),

    % entity_gender(HUMAN, GENDER),

    entity_label(LANG, PREDECESSOR, P_LABEL),
    entity_label(LANG, SUCCESSOR,   S_LABEL),
    entity_label(LANG, ROLE,        R_LABEL),

    answerz (I, LANG, politicalPredecessor, P_LABEL, S_LABEL, R_LABEL).

political_predecessor (I, ROLE, PERSON, PREDECESSOR) :- 
    ROLE is uriref (wde:PresidentOfTheUnitedStatesOfAmerica),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, ROLE,
        OFFICE_STMT, wdpq:Replaces,     PREDECESSOR,
        filter (PERSON \= PREDECESSOR)),
    scorez (I, 100).

political_predecessor (I, ROLE, PERSON, PREDECESSOR) :- 
    ROLE is uriref (wde:FederalChancellorOfGermany),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, ROLE,
        OFFICE_STMT, wdpq:Replaces,     PREDECESSOR,
        filter (PERSON \= PREDECESSOR)),
    scorez (I, 100).

political_predecessor (I, ROLE, PERSON, PREDECESSOR) :- 
    ROLE is uriref (wde:PresidentOfGermany),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, ROLE,
        OFFICE_STMT, wdpq:Replaces,     PREDECESSOR,
        filter (PERSON \= PREDECESSOR)),
    scorez (I, 100).

l3proc (I, F, fnQuestioning, MSGF, fnChangeOfLeadership) :-

    log (debug, 'l3proc: fnTelling (ldr_o) -> fnChangeOfLeadership'),

    frame (F,    top,      ldr_o),
    frame (MSGF, ldr_n,    SUCCESSOR),

    ignore (frame(MSGF, role, ROLE)),

    assertz(ias(I, uframe, F)),

    political_predecessor (I, ROLE, SUCCESSOR, PREDECESSOR),

    % produce response frame graph (here: tell user about person's predecessor)
    
    list_append(VMC, fe(ldr_n, SUCCESSOR)),
    list_append(VMC, fe(ldr_o, PREDECESSOR)),
    list_append(VMC, fe(role,  ROLE)),
    list_append(VMC, frame(fnChangeOfLeadership)),

    list_append(VMC, fe(msg,   vm_frame_pop)),
    list_append(VMC, fe(top,   ldr_o)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,   USER)),
    list_append(VMC, fe(spkr,  uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 150),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    log (debug, 'l3proc: fnTelling (ldr_o) -> fnChangeOfLeadership ldr_n =', PREDECESSOR, ', role = ', ROLE),

    % generate response actions
    
    l4proc (I).


l2proc_politicianPredecessorTokens(LANG) :-

    ner(LANG, I, human, @KNOWN_POLITICIANS:TSTART_LABEL_0, @KNOWN_POLITICIANS:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(ldr_n, NER1ENTITY)),
    list_append(VMC, frame(fnChangeOfLeadership)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  ldr_o)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    log (debug, 'l2proc: fnQuestioning (ldr_o) -> fnChangeOfLeadership ldr_n =', NER1ENTITY),

    fnvm_exec (I, VMC).
   
nlp_gen (en, '@SELF_ADDRESS:LABEL who (is|was|happened to be) the predecessor of @KNOWN_POLITICIANS:LABEL (by the way|) ?',
         inline(l2proc_politicianPredecessorTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL wer (ist|war) (eigentlich|) (die vorgängerin|der vorgänger) von @KNOWN_POLITICIANS:LABEL ?',
         inline(l2proc_politicianPredecessorTokens, en)).

nlp_test(en,
         ivr(in('who happened to be the predecessor of Ronald Reagan?'),
             out('predecessor of ronald reagan in the role president of the united states of america was jimmy carter'))).
nlp_test(de,
         ivr(in('wer war eigentlich der vorgänger von Ronald Reagan?'),
             out('vorgänger von ronald reagan in der rolle präsident der vereinigten staaten war jimmy carter'))).
nlp_test(en,
         ivr(in('who happened to be the predecessor of Helmut Kohl?'),
             out('predecessor of helmut kohl in the role federal chancellor of germany was helmut schmidt'))).
nlp_test(de,
         ivr(in('wer war eigentlich der vorgänger von Helmut Kohl?'),
             out('vorgänger von helmut kohl in der rolle bundeskanzler war helmut schmidt'))).
nlp_test(en,
         ivr(in('who happened to be the predecessor of Richard von Weizsäcker?'),
             out('predecessor of richard von weizsäcker in the role president of germany was karl carstens'))).
nlp_test(de,
         ivr(in('wer war eigentlich der vorgänger von Richard von Weizsäcker?'),
             out('vorgänger von richard von weizsäcker in der rolle bundespräsident war karl carstens'))).

answerz (I, en, politicalSuccessor, P_LABEL, S_LABEL, R_LABEL) :- sayz(I, en, format_str("Successor of %s in the role %s was %s", P_LABEL, R_LABEL, S_LABEL)).
answerz (I, de, politicalSuccessor, P_LABEL, S_LABEL, R_LABEL) :- sayz(I, de, format_str("Nachfolger von %s in der Rolle %s war %s", P_LABEL, R_LABEL, S_LABEL)).

l4proc (I, F, fnTelling, ldr_n, MSGF, fnChangeOfLeadership) :-

    frame (MSGF, ldr_o, PREDECESSOR),
    frame (MSGF, ldr_n, SUCCESSOR),
    frame (MSGF, role,  ROLE),    

    ias (I, uttLang, LANG),

    % entity_gender(HUMAN, GENDER),

    entity_label(LANG, PREDECESSOR, P_LABEL),
    entity_label(LANG, SUCCESSOR,   S_LABEL),
    entity_label(LANG, ROLE,        R_LABEL),

    answerz (I, LANG, politicalSuccessor, P_LABEL, S_LABEL, R_LABEL).

political_successor (I, ROLE, PERSON, SUCCESSOR) :- 
    ROLE is uriref (wde:PresidentOfTheUnitedStatesOfAmerica),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, ROLE,
        OFFICE_STMT, wdpq:ReplacedBy,   SUCCESSOR,
        filter (PERSON \= SUCCESSOR)),
    scorez (I, 100).

political_successor (I, ROLE, PERSON, SUCCESSOR) :- 
    ROLE is uriref (wde:FederalChancellorOfGermany),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, ROLE,
        OFFICE_STMT, wdpq:ReplacedBy,   SUCCESSOR,
        filter (PERSON \= SUCCESSOR)),
    scorez (I, 100).

political_successor (I, ROLE, PERSON, SUCCESSOR) :- 
    ROLE is uriref (wde:PresidentOfGermany),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, ROLE,
        OFFICE_STMT, wdpq:ReplacedBy,   SUCCESSOR,
        filter (PERSON \= SUCCESSOR)),
    scorez (I, 100).

l3proc (I, F, fnQuestioning, MSGF, fnChangeOfLeadership) :-

    log (debug, 'l3proc: fnTelling (ldr_n) -> fnChangeOfLeadership'),

    frame (F,    top,      ldr_n),
    frame (MSGF, ldr_o,    PREDECESSOR),

    ignore (frame(MSGF, role, ROLE)),

    assertz(ias(I, uframe, F)),

    political_successor (I, ROLE, PREDECESSOR, SUCCESSOR),

    % produce response frame graph (here: tell user about person's successor)
    
    list_append(VMC, fe(ldr_n, SUCCESSOR)),
    list_append(VMC, fe(ldr_o, PREDECESSOR)),
    list_append(VMC, fe(role,  ROLE)),
    list_append(VMC, frame(fnChangeOfLeadership)),

    list_append(VMC, fe(msg,   vm_frame_pop)),
    list_append(VMC, fe(top,   ldr_n)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,   USER)),
    list_append(VMC, fe(spkr,  uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 150),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    log (debug, 'l3proc: fnTelling (ldr_n) -> fnChangeOfLeadership ldr_o =', PREDECESSOR, ', role = ', ROLE),

    % generate response actions
    
    l4proc (I).


l2proc_politicianSuccessorTokens(LANG) :-

    ner(LANG, I, human, @KNOWN_POLITICIANS:TSTART_LABEL_0, @KNOWN_POLITICIANS:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(ldr_o, NER1ENTITY)),
    list_append(VMC, frame(fnChangeOfLeadership)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  ldr_n)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    log (debug, 'l2proc: fnQuestioning (ldr_o) -> fnChangeOfLeadership ldr_n =', NER1ENTITY),

    fnvm_exec (I, VMC).
   
nlp_gen (en, '@SELF_ADDRESS:LABEL who (is|was|happened to be) the successor of @KNOWN_POLITICIANS:LABEL (by the way|) ?',
         inline(l2proc_politicianSuccessorTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL wer (ist|war) (eigentlich|) (die nachfolgerin|der nachfolger) von @KNOWN_POLITICIANS:LABEL ?',
         inline(l2proc_politicianSuccessorTokens, de)).

nlp_test(en,
         ivr(in('who happened to be the successor of Ronald Reagan?'),
             out('successor of ronald reagan in the role president of the united states of america was george h w bush'))).
nlp_test(de,
         ivr(in('wer war eigentlich der nachfolger von Ronald Reagan?'),
             out('nachfolger von ronald reagan in der rolle präsident der vereinigten staaten war george h w bush'))).
nlp_test(en,
         ivr(in('who happened to be the successor of Helmut Kohl?'),
             out('successor of helmut kohl in the role federal chancellor of germany was gerhard schröder'))).
nlp_test(de,
         ivr(in('wer war eigentlich der nachfolger von Helmut Kohl?'),
             out('nachfolger von helmut kohl in der rolle bundeskanzler war gerhard schröder'))).
nlp_test(en,
         ivr(in('who happened to be the successor of Richard von Weizsäcker?'),
             out('successor of richard von weizsäcker in the role president of germany was roman herzog'))).
nlp_test(de,
         ivr(in('wer war eigentlich der nachfolger von Richard von Weizsäcker?'),
             out('nachfolger von richard von weizsäcker in der rolle bundespräsident war roman herzog.'))).

% FIXME: context-based follow-up style questions

