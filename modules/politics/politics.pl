%prolog

answer(topic, de) :-
    score_context(topic, politics, 100), say_eoa(de, 'Politik war unser Thema.').

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

nlp_macro ('KNOWN_CHANCELLORS', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:FederalChancellorOfGermany,
         filter (lang(LABEL) = 'de')).

answer (knownPerson, de, PERSON, LABEL) :-
    score_add(10),
    score_context_add (topic, politics, 100),
    is_german_chancellor(PERSON),
    is_male(PERSON),
    push_context(topic, politics),
    push_context(topic, PERSON),
    say_eoa(de, 'Der ist doch gerade Bundeskanzler!').

answer (knownPerson, de, PERSON, LABEL) :-
    score_add(10),
    score_context_add (topic, politics, 100),
    is_german_chancellor(PERSON),
    is_female(PERSON),
    push_context(topic, politics),
    push_context(topic, PERSON),
    say_eoa(de, 'Die ist doch gerade Bundeskanzlerin!').

answer (knownPerson, de, PERSON, LABEL) :-
    score_add(10),
    score_context_add (topic, politics, 100),
    was_german_chancellor(PERSON), 
    not (is_german_chancellor(PERSON)),
    is_male(PERSON),
    push_context(topic, politics),
    push_context(topic, PERSON),
    say_eoa(de, 'Der war doch mal Bundeskanzler.').

answer (knownPerson, de, PERSON, LABEL) :-
    score_add(10),
    score_context_add (topic, politics, 100),
    was_german_chancellor(PERSON), 
    not (is_german_chancellor(PERSON)),
    is_female(PERSON),
    push_context(topic, politics),
    push_context(topic, PERSON),
    say_eoa(de, 'Die war doch mal Bundeskanzlerin.').

nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Angela Merkel?'),
             out('die ist doch gerade bundeskanzlerin'))).

nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Helmut Kohl?'),
             out('der war doch mal Bundeskanzler.'))).


answer (germanChancellorPredecessor, de, PERSON, LABEL) :-
    score_add(10),
    score_context_add (topic, politics, 100),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany,
        OFFICE_STMT, wdpq:Replaces,     PREDECESSOR,
        PREDECESSOR, rdfs:label,        PLABEL,
        filter (lang(PLABEL) = 'de', PERSON \= PREDECESSOR)),
    push_context(topic, politics),
    push_context(topic, PERSON),
    push_context(topic, PREDECESSOR),
    is_male(PREDECESSOR),
    say_eoa(de, format_str('Vorgänger von %s war %s.', LABEL, PLABEL)).

answer (germanChancellorPredecessor, de, PERSON, LABEL) :-
    score_add(10),
    score_context_add (topic, politics, 100),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany,
        OFFICE_STMT, wdps:Replaces,     PREDECESSOR,
        PREDECESSOR, rdfs:label,        PLABEL,
        filter (lang(PLABEL) = 'de', PERSON \= PREDECESSOR)),
    push_context(topic, politics),
    push_context(topic, PERSON),
    push_context(topic, PREDECESSOR),
    is_female(PREDECESSOR),
    say_eoa(de, format_str('Vorgängerin von %s war %s.', LABEL, PLABEL)).


nlp_gen (de, '(HAL,|Computer,|) wer (ist|war) (eigentlich|) (die vorgängerin|der vorgänger) von @KNOWN_CHANCELLORS:LABEL ?',
             answer(germanChancellorPredecessor, de, '@KNOWN_CHANCELLORS:PERSON', "@KNOWN_CHANCELLORS:LABEL")). 

nlp_test(de,
         ivr(in('wer war eigentlich der vorgänger von Helmut Kohl?'),
             out('Vorgänger von Helmut Kohl war Helmut Schmidt.'))).

answer (germanChancellorSuccessor, de, PERSON, LABEL) :-
    score_add(10),
    score_context_add (topic, politics, 100),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany,
        OFFICE_STMT, wdpq:ReplacedBy,   SUCCESSOR,
        SUCCESSOR,   rdfs:label,        PLABEL,
        filter (lang(PLABEL) = 'de', PERSON \= SUCCESSOR)),
    push_context(topic, politics),
    push_context(topic, PERSON),
    push_context(topic, SUCCESSOR),
    is_male(SUCCESSOR),
    say_eoa(de, format_str('Nachfolger von %s war %s.', LABEL, PLABEL)).

answer (germanChancellorSuccessor, de, PERSON, LABEL) :-
    score_add(10),
    score_context_add (topic, politics, 100),
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany,
        OFFICE_STMT, wdps:ReplacedBy,   SUCCESSOR,
        SUCCESSOR,   rdfs:label,        PLABEL,
        filter (lang(PLABEL) = 'de', PERSON \= SUCCESSOR)),
    push_context(topic, politics),
    push_context(topic, PERSON),
    push_context(topic, SUCCESSOR),
    is_female(SUCCESSOR),
    say_eoa(de, format_str('Nachfolgerin von %s war %s.', LABEL, PLABEL)).

nlp_gen (de, '(HAL,|Computer,|) wer (ist|war) (eigentlich|) (die nachfolgerin|der nachfolger) von @KNOWN_CHANCELLORS:LABEL ?',
             answer(germanChancellorSuccessor, de, '@KNOWN_CHANCELLORS:PERSON', "@KNOWN_CHANCELLORS:LABEL")). 

nlp_test(de,
         ivr(in('wer war eigentlich der nachfolger von Helmut Kohl?'),
             out('Nachfolger von Helmut Kohl war Gerhard Schröder.'))).

% nlp_gen (de, '(HAL,|Computer,|) ueber aussenpolitik',
%              'Politik interessiert mich nicht sonderlich.').
% 
% nlp_gen (de, '(HAL,|Computer,|) kennst du dich mit politik aus',
%              'Ich schaue mir manchmal eine Bundestagsdebatte an, wenn ich etwas zum Lachen haben will...').

% nlp_gen (de, '(HAL,|Computer,|) * SPENDENAFFAEHRE',
%              'Ich möchte nicht wissen, was die SPD jetzt gerade für krumme Dinger dreht...').

