%prolog

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

nlp_macro ('KNOWN_CHANCELLORS', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:FederalChancellorOfGermany,
         filter (lang(LABEL) = 'de')).

answer (knownPerson, de, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    is_german_chancellor(PERSON),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Der ist doch gerade Bundeskanzler!', SCORE).

answer (knownPerson, de, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    is_german_chancellor(PERSON),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Die ist doch gerade Bundeskanzlerin!', SCORE).

answer (knownPerson, de, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    was_german_chancellor(PERSON), 
    not (is_german_chancellor(PERSON)),
    is_male(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Der war doch mal Bundeskanzler.', SCORE).

answer (knownPerson, de, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, politics, 100, SCORE),
    was_german_chancellor(PERSON), 
    not (is_german_chancellor(PERSON)),
    is_female(PERSON),
    context_push(topic, politics),
    context_push(topic, PERSON),
    say_eoa(de, 'Die war doch mal Bundeskanzlerin.', SCORE).

nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Angela Merkel?'),
             out('die ist doch gerade bundeskanzlerin'))).

nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Helmut Kohl?'),
             out('der war doch mal Bundeskanzler.'))).


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


nlp_gen (de, '(HAL,|Computer,|) wer (ist|war) (eigentlich|) (die vorgängerin|der vorgänger) von @KNOWN_CHANCELLORS:LABEL ?',
             answer(germanChancellorPredecessor, de, '@KNOWN_CHANCELLORS:PERSON', "@KNOWN_CHANCELLORS:LABEL")). 

nlp_test(de,
         ivr(in('wer war eigentlich der vorgänger von Helmut Kohl?'),
             out('Vorgänger von Helmut Kohl war Helmut Schmidt.'))).

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
    say_eoa(de, format_str('Nachfolger von %s war %s.', LABEL, PLABEL), SCORE).

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
    say_eoa(de, format_str('Nachfolgerin von %s war %s.', LABEL, PLABEL), SCORE).

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

