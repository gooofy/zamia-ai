%prolog

answer(topic, en) :-
    context_score(topic, politics, 100, SCORE), say_eoa(en, 'We were talking about politics.', SCORE).
answer(topic, de) :-
    context_score(topic, politics, 100, SCORE), say_eoa(de, 'Politik war unser Thema.', SCORE).

%
% all politicians we know of
%

nlp_macro ('KNOWN_POLITICIANS_EN', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:PresidentOfTheUnitedStatesOfAmerica,
         filter (lang(LABEL) = 'en')).
nlp_macro ('KNOWN_POLITICIANS_DE', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:PresidentOfTheUnitedStatesOfAmerica,
         filter (lang(LABEL) = 'de')).
nlp_macro ('KNOWN_POLITICIANS_EN', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:PresidentOfGermany,
         filter (lang(LABEL) = 'en')).
nlp_macro ('KNOWN_POLITICIANS_DE', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:PresidentOfGermany,
         filter (lang(LABEL) = 'de')).
nlp_macro ('KNOWN_POLITICIANS_EN', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:FederalChancellorOfGermany,
         filter (lang(LABEL) = 'en')).
nlp_macro ('KNOWN_POLITICIANS_DE', PERSON, LABEL) :-
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

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    is_us_president(PERSON),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Isn't he the US president right now?", SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    is_us_president(PERSON),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Der ist doch gerade US Präsident!', SCORE).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    is_us_president(PERSON),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Isn't she the US president right now?", SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    is_us_president(PERSON),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Die ist doch gerade US Präsidentin!', SCORE).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    was_us_president(PERSON), 
    not (is_us_president(PERSON)),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Wasn't he a US president?", SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    was_us_president(PERSON), 
    not (is_us_president(PERSON)),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Der war doch mal US Präsident.', SCORE).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    was_us_president(PERSON), 
    not (is_us_president(PERSON)),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Wasn't she a US president?", SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    was_us_president(PERSON), 
    not (is_us_president(PERSON)),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Die war doch mal US Präsidentin.', SCORE).

nlp_test(en,
         ivr(in('Computer, do you know Donald Trump?'),
             out("Isn't he the US president right now?"))).
nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Donald Trump?'),
             out('der ist doch gerade US Präsident'))).

nlp_test(en,
         ivr(in('Computer, do you happen to know Ronald Reagan?'),
             out("Wasn't he a US president?"))).
nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Ronald Reagan?'),
             out('der war doch mal US Präsident.'))).
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

% FIXME: unused
% nlp_macro ('KNOWN_CHANCELLORS_EN', PERSON, LABEL) :-
%     rdf (distinct,
%          PERSON, wdpd:InstanceOf,   wde:Human,
%          PERSON, rdfs:label,        LABEL,
%          PERSON, wdpd:PositionHeld, wde:FederalChancellorOfGermany,
%          filter (lang(LABEL) = 'en')).
% nlp_macro ('KNOWN_CHANCELLORS_DE', PERSON, LABEL) :-
%     rdf (distinct,
%          PERSON, wdpd:InstanceOf,   wde:Human,
%          PERSON, rdfs:label,        LABEL,
%          PERSON, wdpd:PositionHeld, wde:FederalChancellorOfGermany,
%          filter (lang(LABEL) = 'de')).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    is_german_chancellor(PERSON),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Isn't he chancellor in germany right now?", SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    is_german_chancellor(PERSON),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Der ist doch gerade Bundeskanzler!', SCORE).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    is_german_chancellor(PERSON),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Isn't she chancellor in germany right now?", SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    is_german_chancellor(PERSON),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Die ist doch gerade Bundeskanzlerin!', SCORE).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    was_german_chancellor(PERSON), 
    not (is_german_chancellor(PERSON)),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Wasn't he a german chancellor?", SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    was_german_chancellor(PERSON), 
    not (is_german_chancellor(PERSON)),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Der war doch mal Bundeskanzler.', SCORE).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    was_german_chancellor(PERSON), 
    not (is_german_chancellor(PERSON)),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Wasn't she a german chancellor?", SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    was_german_chancellor(PERSON), 
    not (is_german_chancellor(PERSON)),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Die war doch mal Bundeskanzlerin.', SCORE).

nlp_test(en,
         ivr(in('Computer, do you know Angela Merkel?'),
             out("Isn't she chancellor in germany right now?"))).
nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Angela Merkel?'),
             out('die ist doch gerade bundeskanzlerin'))).

nlp_test(en,
         ivr(in('Computer, do you happen to know Helmut Kohl?'),
             out("Wasn't he a german chancellor?"))).
nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Helmut Kohl?'),
             out('der war doch mal Bundeskanzler.'))).

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

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    is_german_president(PERSON),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Isn't he the german president right now?", SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    is_german_president(PERSON),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Der ist doch gerade Bundespräsident!', SCORE).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    is_german_president(PERSON),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Isn't she the german president right now?", SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    is_german_president(PERSON),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Die ist doch gerade Bundespräsidentin!', SCORE).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    was_german_president(PERSON), 
    not (is_german_president(PERSON)),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Wasn't he a german president?", SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    was_german_president(PERSON), 
    not (is_german_president(PERSON)),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Der war doch mal Bundespräsident.', SCORE).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    was_german_president(PERSON), 
    not (is_german_president(PERSON)),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Wasn't she a german president?", SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    was_german_president(PERSON), 
    not (is_german_president(PERSON)),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Die war doch mal Bundespräsidentin.', SCORE).

nlp_test(en,
         ivr(in('Computer, do you know Frank-Walter Steinmeier?'),
             out("Isn't he the german president right now?"))).
nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Frank-Walter Steinmeier?'),
             out('der ist doch gerade Bundespräsident'))).

nlp_test(en,
         ivr(in('Computer, do you happen to know Joachim Gauck?'),
             out("Wasn't he a german president?"))).
nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Joachim Gauck?'),
             out('der war doch mal Bundespräsident.'))).
%
% successors / predecessors in office
%

say_answer(en, LABEL, wdpq:Replaces, PREDECESSOR, PLABEL, SCORE) :- 
    say_eoa(en, format_str('The predecessor of %s was %s.', LABEL, PLABEL), SCORE).
say_answer(de, LABEL, wdpq:Replaces, PREDECESSOR, PLABEL, SCORE) :- 
    is_male(PREDECESSOR),
    say_eoa(de, format_str('Vorgänger von %s war %s.', LABEL, PLABEL), SCORE).
say_answer(de, LABEL, wdpq:Replaces, PREDECESSOR, PLABEL, SCORE) :- 
    is_female(PREDECESSOR),
    say_eoa(de, format_str('Vorgängerin von %s war %s.', LABEL, PLABEL), SCORE).

say_answer(en, LABEL, wdpq:ReplacedBy, SUCCESSOR, PLABEL, SCORE) :- 
    say_eoa(en, format_str('The successor of %s is %s.', LABEL, PLABEL), SCORE).
say_answer(de, LABEL, wdpq:ReplacedBy, SUCCESSOR, PLABEL, SCORE) :- 
    is_male(SUCCESSOR),
    say_eoa(de, format_str('Nachfolger von %s ist %s.', LABEL, PLABEL), SCORE).
say_answer(de, LABEL, wdpq:ReplacedBy, SUCCESSOR, PLABEL, SCORE) :- 
    is_female(SUCCESSOR),
    say_eoa(de, format_str('Nachfolgerin von %s ist %s.', LABEL, PLABEL), SCORE).

answer (politicianPredSucc, LANG, POSITION, RELATION, PERSON, LABEL, SCORE) :-
    context_score (topic, politics, 100, SCORE),
    atom_chars(LANG, LSTR),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, POSITION,
        OFFICE_STMT, RELATION,          PREDSUCC,
        PREDSUCC,    rdfs:label,        PLABEL,
        filter (lang(PLABEL) = LSTR, PERSON \= PREDSUCC)),
    context_push(topic, politics),
    context_push(topic, PERSON),
    context_push(topic, PREDSUCC),
    say_answer(LANG, LABEL, RELATION, PREDSUCC, PLABEL, SCORE).

answer (politicianPredecessor, LANG, PERSON, LABEL, SCORE) :-
    answer (politicianPredSucc, LANG, wde:PresidentOfTheUnitedStatesOfAmerica, wdpq:Replaces, PERSON, LABEL, SCORE).
answer (politicianPredecessor, LANG, PERSON, LABEL, SCORE) :-
    answer (politicianPredSucc, LANG, wde:PresidentOfGermany, wdpq:Replaces, PERSON, LABEL, SCORE).
answer (politicianPredecessor, LANG, PERSON, LABEL, SCORE) :-
    answer (politicianPredSucc, LANG, wde:FederalChancellorOfGermany, wdpq:Replaces, PERSON, LABEL, SCORE).

answer (politicianSuccessor, LANG, PERSON, LABEL, SCORE) :-
    answer (politicianPredSucc, LANG, wde:PresidentOfTheUnitedStatesOfAmerica, wdpq:ReplacedBy, PERSON, LABEL, SCORE).
answer (politicianSuccessor, LANG, PERSON, LABEL, SCORE) :-
    answer (politicianPredSucc, LANG, wde:PresidentOfGermany, wdpq:ReplacedBy, PERSON, LABEL, SCORE).
answer (politicianSuccessor, LANG, PERSON, LABEL, SCORE) :-
    answer (politicianPredSucc, LANG, wde:FederalChancellorOfGermany, wdpq:ReplacedBy, PERSON, LABEL, SCORE).

answer (politicianPredecessorTokens, en, TSTART, TEND) :-
    ner(en, person, TSTART, TEND, PERSON, LABEL, SCORE),
    answer(politicianPredecessor, en, PERSON, LABEL, SCORE).
answer (politicianPredecessorTokens, de, TSTART, TEND) :-
    ner(de, person, TSTART, TEND, PERSON, LABEL, SCORE),
    answer(politicianPredecessor, de, PERSON, LABEL, SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL who (is|was|happened to be) the predecessor of @KNOWN_POLITICIANS_EN:LABEL (by the way|) ?',
             answer(politicianPredecessorTokens, en, @KNOWN_POLITICIANS_EN:TSTART_LABEL_0, @KNOWN_POLITICIANS_EN:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL wer (ist|war) (eigentlich|) (die vorgängerin|der vorgänger) von @KNOWN_POLITICIANS_DE:LABEL ?',
             answer(politicianPredecessorTokens, de, @KNOWN_POLITICIANS_DE:TSTART_LABEL_0, @KNOWN_POLITICIANS_DE:TEND_LABEL_0)). 

nlp_test(en,
         ivr(in('who happened to be the predecessor of Ronald Reagan?'),
             out('The predecessor of Ronald Reagan was Jimmy Carter.'))).
nlp_test(de,
         ivr(in('wer war eigentlich der vorgänger von Ronald Reagan?'),
             out('Vorgänger von Ronald Reagan war Jimmy Carter.'))).
nlp_test(en,
         ivr(in('who happened to be the predecessor of Helmut Kohl?'),
             out('The predecessor of Helmut Kohl was Helmut Schmidt.'))).
nlp_test(de,
         ivr(in('wer war eigentlich der vorgänger von Helmut Kohl?'),
             out('Vorgänger von Helmut Kohl war Helmut Schmidt.'))).
nlp_test(en,
         ivr(in('who happened to be the predecessor of Richard von Weizsäcker?'),
             out('The predecessor of Richard von Weizsäcker was Karl Carstens.'))).
nlp_test(de,
         ivr(in('wer war eigentlich der vorgänger von Richard von Weizsäcker?'),
             out('Vorgänger von Richard von Weizsäcker war Karl Carstens.'))).

answer (politicianSuccessorTokens, en, TSTART, TEND) :-
    ner(en, person, TSTART, TEND, PERSON, LABEL, SCORE),
    answer(politicianSuccessor, en, PERSON, LABEL, SCORE).
answer (politicianSuccessorTokens, de, TSTART, TEND) :-
    ner(de, person, TSTART, TEND, PERSON, LABEL, SCORE),
    answer(politicianSuccessor, de, PERSON, LABEL, SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL who (is|was|happened to be) the successor of @KNOWN_POLITICIANS_EN:LABEL (by the way|) ?',
             answer(politicianSuccessorTokens, en, @KNOWN_POLITICIANS_EN:TSTART_LABEL_0, @KNOWN_POLITICIANS_EN:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL wer (ist|war) (eigentlich|) (die nachfolgerin|der nachfolger) von @KNOWN_POLITICIANS_DE:LABEL ?',
             answer(politicianSuccessorTokens, de, @KNOWN_POLITICIANS_DE:TSTART_LABEL_0, @KNOWN_POLITICIANS_DE:TEND_LABEL_0)). 

nlp_test(en,
         ivr(in('who happened to be the successor of Ronald Reagan?'),
             out('The successor of Ronald Reagan is george h w bush.'))).
nlp_test(de,
         ivr(in('wer war eigentlich der nachfolger von Ronald Reagan?'),
             out('Nachfolger von Ronald Reagan ist george h w bush.'))).
nlp_test(en,
         ivr(in('who happened to be the successor of Helmut Kohl?'),
             out('The successor of Helmut Kohl is Gerhard Schröder.'))).
nlp_test(de,
         ivr(in('wer war eigentlich der nachfolger von Helmut Kohl?'),
             out('Nachfolger von Helmut Kohl ist Gerhard Schröder.'))).
nlp_test(en,
         ivr(in('who happened to be the successor of Richard von Weizsäcker?'),
             out('The successor of Richard von Weizsäcker is roman herzog.'))).
nlp_test(de,
         ivr(in('wer war eigentlich der nachfolger von Richard von Weizsäcker?'),
             out('Nachfolger von Richard von Weizsäcker ist roman herzog.'))).

