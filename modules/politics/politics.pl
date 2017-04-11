%prolog

answer(topic, en) :-
    context_score(topic, politics, 100, SCORE), say_eoa(en, 'We were talking about politics.', SCORE).
answer(topic, de) :-
    context_score(topic, politics, 100, SCORE), say_eoa(de, 'Politik war unser Thema.', SCORE).

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

nlp_macro ('KNOWN_CHANCELLORS_EN', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:FederalChancellorOfGermany,
         filter (lang(LABEL) = 'en')).
nlp_macro ('KNOWN_CHANCELLORS_DE', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:FederalChancellorOfGermany,
         filter (lang(LABEL) = 'de')).

answer (knownPerson, en, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    is_german_chancellor(PERSON),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Isn't he chancellor in germany right now?", SCORE).
answer (knownPerson, de, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    is_german_chancellor(PERSON),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Der ist doch gerade Bundeskanzler!', SCORE).

answer (knownPerson, en, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    is_german_chancellor(PERSON),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Isn't she chancellor in germany right now?", SCORE).
answer (knownPerson, de, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    is_german_chancellor(PERSON),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Die ist doch gerade Bundeskanzlerin!', SCORE).

answer (knownPerson, en, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    was_german_chancellor(PERSON), 
    not (is_german_chancellor(PERSON)),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Wasn't he a german chancellor?", SCORE).
answer (knownPerson, de, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    was_german_chancellor(PERSON), 
    not (is_german_chancellor(PERSON)),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Der war doch mal Bundeskanzler.', SCORE).

answer (knownPerson, en, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    was_german_chancellor(PERSON), 
    not (is_german_chancellor(PERSON)),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(en, "Wasn't she a german chancellor?", SCORE).
answer (knownPerson, de, PERSON, LABEL) :-
    SCORE is 10,
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


answer (germanChancellorPredecessor, en, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany,
        OFFICE_STMT, wdpq:Replaces,     PREDECESSOR,
        PREDECESSOR, rdfs:label,        PLABEL,
        filter (lang(PLABEL) = 'en', PERSON \= PREDECESSOR)),
    context_push(topic, politics),
    context_push(topic, PERSON),
    context_push(topic, PREDECESSOR),
    say_eoa(en, format_str('The predecessor of %s was %s.', LABEL, PLABEL), SCORE).

answer (germanChancellorPredecessor, de, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany,
        OFFICE_STMT, wdpq:Replaces,     PREDECESSOR,
        PREDECESSOR, rdfs:label,        PLABEL,
        filter (lang(PLABEL) = 'de', PERSON \= PREDECESSOR)),
    context_push(topic, politics),
    context_push(topic, PERSON),
    context_push(topic, PREDECESSOR),
    is_male(PREDECESSOR),
    say_eoa(de, format_str('Vorgänger von %s war %s.', LABEL, PLABEL), SCORE).

answer (germanChancellorPredecessor, de, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany,
        OFFICE_STMT, wdps:Replaces,     PREDECESSOR,
        PREDECESSOR, rdfs:label,        PLABEL,
        filter (lang(PLABEL) = 'de', PERSON \= PREDECESSOR)),
    context_push(topic, politics),
    context_push(topic, PERSON),
    context_push(topic, PREDECESSOR),
    is_female(PREDECESSOR),
    say_eoa(de, format_str('Vorgängerin von %s war %s.', LABEL, PLABEL), SCORE).


nlp_gen (en, '@SELF_ADDRESS_EN:LABEL who (is|was|happened to be) the predecessor of @KNOWN_CHANCELLORS_EN:LABEL (by the way|) ?',
             answer(germanChancellorPredecessor, en, '@KNOWN_CHANCELLORS_EN:PERSON', "@KNOWN_CHANCELLORS_EN:LABEL")). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL wer (ist|war) (eigentlich|) (die vorgängerin|der vorgänger) von @KNOWN_CHANCELLORS_DE:LABEL ?',
             answer(germanChancellorPredecessor, de, '@KNOWN_CHANCELLORS_DE:PERSON', "@KNOWN_CHANCELLORS_DE:LABEL")). 

nlp_test(en,
         ivr(in('who happened to be the predecessor of Helmut Kohl?'),
             out('The predecessor of Helmut Kohl was Helmut Schmidt.'))).
nlp_test(de,
         ivr(in('wer war eigentlich der vorgänger von Helmut Kohl?'),
             out('Vorgänger von Helmut Kohl war Helmut Schmidt.'))).

answer (germanChancellorSuccessor, en, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany,
        OFFICE_STMT, wdpq:ReplacedBy,   SUCCESSOR,
        SUCCESSOR,   rdfs:label,        PLABEL,
        filter (lang(PLABEL) = 'en', PERSON \= SUCCESSOR)),
    context_push(topic, politics),
    context_push(topic, PERSON),
    context_push(topic, SUCCESSOR),
    say_eoa(en, format_str('The successor of %s is %s.', LABEL, PLABEL), SCORE).

answer (germanChancellorSuccessor, de, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany,
        OFFICE_STMT, wdpq:ReplacedBy,   SUCCESSOR,
        SUCCESSOR,   rdfs:label,        PLABEL,
        filter (lang(PLABEL) = 'de', PERSON \= SUCCESSOR)),
    context_push(topic, politics),
    context_push(topic, PERSON),
    context_push(topic, SUCCESSOR),
    is_male(SUCCESSOR),
    say_eoa(de, format_str('Nachfolger von %s ist %s.', LABEL, PLABEL), SCORE).

answer (germanChancellorSuccessor, de, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany,
        OFFICE_STMT, wdps:ReplacedBy,   SUCCESSOR,
        SUCCESSOR,   rdfs:label,        PLABEL,
        filter (lang(PLABEL) = 'de', PERSON \= SUCCESSOR)),
    context_push(topic, politics),
    context_push(topic, PERSON),
    context_push(topic, SUCCESSOR),
    is_female(SUCCESSOR),
    say_eoa(de, format_str('Nachfolgerin von %s ist %s.', LABEL, PLABEL), SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL who (is|was|happened to be) the successor of @KNOWN_CHANCELLORS_EN:LABEL (by the way|) ?',
             answer(germanChancellorSuccessor, en, '@KNOWN_CHANCELLORS_EN:PERSON', "@KNOWN_CHANCELLORS_EN:LABEL")). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL wer (ist|war) (eigentlich|) (die nachfolgerin|der nachfolger) von @KNOWN_CHANCELLORS_DE:LABEL ?',
             answer(germanChancellorSuccessor, de, '@KNOWN_CHANCELLORS_DE:PERSON', "@KNOWN_CHANCELLORS_DE:LABEL")). 

nlp_test(en,
         ivr(in('who happened to be the successor of Helmut Kohl?'),
             out('The successor of Helmut Kohl is Gerhard Schröder.'))).
nlp_test(de,
         ivr(in('wer war eigentlich der nachfolger von Helmut Kohl?'),
             out('Nachfolger von Helmut Kohl ist Gerhard Schröder.'))).

