%prolog

is_person(ENTITY) :- rdf (ENTITY, wdpd:InstanceOf, wde:Human).

is_male(PERSON) :- rdf (PERSON, wdpd:SexOrGender, wde:Male).
is_female(PERSON) :- rdf (PERSON, wdpd:SexOrGender, wde:Female). 

nlp_macro ('KNOWN_PERSONS', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')).

answer(topic, de) :-
    context_score(topic, people, 20, S), say_eoa(de, 'Wir hatten es von den Menschen.', S).

answer (knownPerson, de, PERSON, LABEL) :-
    say_eoa(de, 'Ja, der Name ist mir bekannt.').

nlp_gen (de, '(HAL,|Computer,|) (kennst du|wer ist) (eigentlich|) @KNOWN_PERSONS:LABEL',
             answer(knownPerson, de, '@KNOWN_PERSONS:PERSON', "@KNOWN_PERSONS:LABEL")). 

answer (birthplacePerson, de, PERSON, PERSON_LABEL) :-
    rdf (distinct, limit(1),
         PERSON,     wdpd:PlaceOfBirth, BIRTHPLACE,
         BIRTHPLACE, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')),
    context_push(topic, people),
    context_push(topic, PERSON),
    context_push(topic, BIRTHPLACE),
    say_eoa(de, format_str('%s wurde in %s geboren.', PERSON_LABEL, LABEL)).

nlp_gen (de, '(HAL,|Computer,|) (wo|in welcher stadt) (wurde|ist) (eigentlich|) @KNOWN_PERSONS:LABEL geboren?',
             answer(birthplacePerson, de, '@KNOWN_PERSONS:PERSON', "@KNOWN_PERSONS:LABEL")). 

nlp_gen (de, '(HAL,|Computer,|) welches ist (eigentlich|) (der Geburtsort|die Geburtsstadt) von @KNOWN_PERSONS:LABEL?',
             answer(birthplacePerson, de, '@KNOWN_PERSONS:PERSON', "@KNOWN_PERSONS:LABEL")). 

nlp_test(de,
         ivr(in('Wo wurde Angela Merkel geboren?'),
             out('angela merkel wurde in barmbek-nord geboren'))).

answer (birthdatePerson, de, PERSON, PERSON_LABEL) :-
    rdf (distinct, limit(1),
         PERSON,     wdpd:DateOfBirth, TS),
    transcribe_date(de, dativ, TS, TS_SCRIPT),
    context_push(topic, people),
    context_push(topic, birthday),
    context_push(topic, PERSON),
    say_eoa(de, format_str('%s wurde am %s geboren.', PERSON_LABEL, TS_SCRIPT)).

nlp_gen (de, '(HAL,|Computer,|) (wann|in welchem Jahr) (wurde|ist) (eigentlich|) @KNOWN_PERSONS:LABEL geboren?',
             answer(birthdatePerson, de, '@KNOWN_PERSONS:PERSON', "@KNOWN_PERSONS:LABEL")). 

nlp_gen (de, '(HAL,|Computer,|) (wann hat|an welchem Tag hat) (eigentlich|) @KNOWN_PERSONS:LABEL Geburtstag?',
             answer(birthdatePerson, de, '@KNOWN_PERSONS:PERSON', "@KNOWN_PERSONS:LABEL")). 

nlp_test(de,
         ivr(in('Wann wurde Angela Merkel geboren?'),
             out('Angela Merkel wurde am siebzehnten juli 1954 geboren.')),
         ivr(in('Welches Thema hatten wir?'),
             out('wir hatten über angela merkel gesprochen.'))
        ).

