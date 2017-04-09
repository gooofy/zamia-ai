%prolog

is_person(ENTITY) :- rdf (ENTITY, wdpd:InstanceOf, wde:Human).

is_male(PERSON) :- rdf (PERSON, wdpd:SexOrGender, wde:Male).
is_female(PERSON) :- rdf (PERSON, wdpd:SexOrGender, wde:Female). 

nlp_macro ('KNOWN_PERSONS_EN', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'en')).

nlp_macro ('KNOWN_PERSONS_DE', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')).

answer(topic, en) :-
    context_score(topic, people, 20, S), say_eoa(en, 'We were talking about people.', S).
answer(topic, de) :-
    context_score(topic, people, 20, S), say_eoa(de, 'Wir hatten es von den Menschen.', S).

answer (knownPerson, en, PERSON, LABEL) :-
    say_eoa(en, 'That name sounds familiar.').
answer (knownPerson, de, PERSON, LABEL) :-
    say_eoa(de, 'Ja, der Name ist mir bekannt.').

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (do you know|do you happen to know|who is) @KNOWN_PERSONS_EN:LABEL',
             answer(knownPerson, en, '@KNOWN_PERSONS_EN:PERSON', "@KNOWN_PERSONS_EN:LABEL")). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (kennst du|wer ist) (eigentlich|) @KNOWN_PERSONS_DE:LABEL',
             answer(knownPerson, de, '@KNOWN_PERSONS_DE:PERSON', "@KNOWN_PERSONS_DE:LABEL")). 

answer (birthplacePerson, en, PERSON, PERSON_LABEL) :-
    rdf (distinct, limit(1),
         PERSON,     wdpd:PlaceOfBirth, BIRTHPLACE,
         BIRTHPLACE, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'en')),
    context_push(topic, people),
    context_push(topic, PERSON),
    context_push(topic, BIRTHPLACE),
    say_eoa(en, format_str('%s was born in %s.', PERSON_LABEL, LABEL)).

answer (birthplacePerson, de, PERSON, PERSON_LABEL) :-
    rdf (distinct, limit(1),
         PERSON,     wdpd:PlaceOfBirth, BIRTHPLACE,
         BIRTHPLACE, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')),
    context_push(topic, people),
    context_push(topic, PERSON),
    context_push(topic, BIRTHPLACE),
    say_eoa(de, format_str('%s wurde in %s geboren.', PERSON_LABEL, LABEL)).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (where|in which town|in which city) (was|is) @KNOWN_PERSONS_EN:LABEL born?',
             answer(birthplacePerson, en, '@KNOWN_PERSONS_EN:PERSON', "@KNOWN_PERSONS_EN:LABEL")). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (wo|in welcher stadt) (wurde|ist) (eigentlich|) @KNOWN_PERSONS_DE:LABEL geboren?',
             answer(birthplacePerson, de, '@KNOWN_PERSONS_DE:PERSON', "@KNOWN_PERSONS_DE:LABEL")). 

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL which is (the birthplace|place of birth) of @KNOWN_PERSONS_EN:LABEL?',
             answer(birthplacePerson, en, '@KNOWN_PERSONS_EN:PERSON', "@KNOWN_PERSONS_EN:LABEL")). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL welches ist (eigentlich|) (der Geburtsort|die Geburtsstadt) von @KNOWN_PERSONS_DE:LABEL?',
             answer(birthplacePerson, de, '@KNOWN_PERSONS_DE:PERSON', "@KNOWN_PERSONS_DE:LABEL")). 

nlp_test(de,
         ivr(in('Wo wurde Angela Merkel geboren?'),
             out('angela merkel wurde in barmbek-nord geboren'))).
nlp_test(en,
         ivr(in('Where was Angela Merkel born?'),
             out('angela merkel was born in barmbek-nord'))).

answer (birthdatePerson, en, PERSON, PERSON_LABEL) :-
    rdf (distinct, limit(1),
         PERSON,     wdpd:DateOfBirth, TS),
    transcribe_date(en, dativ, TS, TS_SCRIPT),
    context_push(topic, people),
    context_push(topic, birthday),
    context_push(topic, PERSON),
    say_eoa(en, format_str('%s was born on %s.', PERSON_LABEL, TS_SCRIPT)).

answer (birthdatePerson, de, PERSON, PERSON_LABEL) :-
    rdf (distinct, limit(1),
         PERSON,     wdpd:DateOfBirth, TS),
    transcribe_date(de, dativ, TS, TS_SCRIPT),
    context_push(topic, people),
    context_push(topic, birthday),
    context_push(topic, PERSON),
    say_eoa(de, format_str('%s wurde am %s geboren.', PERSON_LABEL, TS_SCRIPT)).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (when|in which year) (was|is) @KNOWN_PERSONS_EN:LABEL born?',
             answer(birthdatePerson, en, '@KNOWN_PERSONS_EN:PERSON', "@KNOWN_PERSONS_EN:LABEL")). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (wann|in welchem Jahr) (wurde|ist) (eigentlich|) @KNOWN_PERSONS_DE:LABEL geboren?',
             answer(birthdatePerson, de, '@KNOWN_PERSONS_DE:PERSON', "@KNOWN_PERSONS_DE:LABEL")). 

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (when is|on what day is) @KNOWN_PERSONS_EN:LABEL's birthday?",
             answer(birthdatePerson, en, '@KNOWN_PERSONS_EN:PERSON', "@KNOWN_PERSONS_EN:LABEL")). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (wann hat|an welchem Tag hat) (eigentlich|) @KNOWN_PERSONS_DE:LABEL Geburtstag?',
             answer(birthdatePerson, de, '@KNOWN_PERSONS_DE:PERSON', "@KNOWN_PERSONS_DE:LABEL")). 

nlp_test(en,
         ivr(in('When was Angela Merkel born?'),
             out('Angela Merkel was born on july seventeen, 1954.')),
         ivr(in('What were we talking about?'),
             out('we were talking about angela merkel.'))
        ).

nlp_test(de,
         ivr(in('Wann wurde Angela Merkel geboren?'),
             out('Angela Merkel wurde am siebzehnten juli 1954 geboren.')),
         ivr(in('Welches Thema hatten wir?'),
             out('wir hatten über angela merkel gesprochen.'))
        ).

