%prolog

is_person(ENTITY) :- rdf (ENTITY, wdpd:InstanceOf, wde:Human).

is_male(PERSON) :- rdf (PERSON, wdpd:SexOrGender, wde:Male).
is_female(PERSON) :- rdf (PERSON, wdpd:SexOrGender, wde:Female). 

%
% named entity recognition (NER)
%

%
% ner_person_score: this is meant to be overloaded by 
% other modules in order to prioritize certain matches 
% (possibly limited to certain contexts)
%
% i.e. known persons, persons relevant to the current topic, etc.
%
ner_score (person, PERSON, 100) :- is_person(PERSON).

ner_person(LANG, NAME_TOKENS, PERSON, LABEL) :-

    atom_chars(LANG, LSTR),

    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         filter (lang(LABEL) = LSTR)),

    tokenize (LANG, LABEL, LABEL_TOKENS),

    NAME_TOKENS = LABEL_TOKENS.

ner_person(LANG, NAME_TOKENS, PERSON, LABEL) :-

    atom_chars(LANG, LSTR),

    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:FamilyName,   FN,
         FN,     rdfs:label,        FAMILY_NAME,
         filter (lang(LABEL) = LSTR),
         filter (lang(FAMILY_NAME) = LSTR)),

    tokenize (LANG, FAMILY_NAME, FN_TOKENS),

    NAME_TOKENS = FN_TOKENS.

ner(LANG, person, TSTART, TEND, PERSON, LABEL, SCORE) :-

    rdf(ai:curin, ai:tokens, TOKENS),
    list_slice(TSTART, TEND, TOKENS, NAME_TOKENS),
   
    ner_person(LANG, NAME_TOKENS, PERSON, LABEL),

    % edit_distance (NAME_TOKENS, LABEL_TOKENS, ED),

    % ED < list_len(NAME_TOKENS),

    ner_score (person, PERSON, SCORE).

    %SCORE is PS - ED*10. 

%
% macros listing all known persons with their LABELs
% we have _FN variants here that list family names as well,
% but since wikidata doesn't have family names for many
% entries, we need both at least for the time being
%

nlp_macro ('KNOWN_PERSONS_EN', PERSON, LABEL, LABELS) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'en')),
    LABELS is format_str("%s's", LABEL).

nlp_macro ('KNOWN_PERSONS_FN_EN', PERSON, LABEL, FAMILY_NAME, FAMILY_NAMES) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:FamilyName,   FN,
         FN,     rdfs:label,        FAMILY_NAME,
         filter (lang(LABEL) = 'en'),
         filter (lang(FAMILY_NAME) = 'en')),
    FAMILY_NAMES is format_str("%s's", FAMILY_NAME).

nlp_macro ('KNOWN_PERSONS_DE', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')).

nlp_macro ('KNOWN_PERSONS_FN_DE', PERSON, LABEL, FAMILY_NAME) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:FamilyName,   FN,
         FN,     rdfs:label,        FAMILY_NAME,
         filter (lang(LABEL) = 'de'),
         filter (lang(FAMILY_NAME) = 'de')).

%
% questions about persons known
%

answer(topic, en) :-
    context_score(topic, people, 20, S), say_eoa(en, 'We were talking about people.', S).
answer(topic, de) :-
    context_score(topic, people, 20, S), say_eoa(de, 'Wir hatten es von den Menschen.', S).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_push(topic, people),
    context_push(topic, PERSON),
    say_eoa(en, 'That name sounds familiar.', SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_push(topic, people),
    context_push(topic, PERSON),
    say_eoa(de, 'Ja, der Name ist mir bekannt.').

answer (knownPersonTokens, en, TSTART, TEND) :-
    ner(en, person, TSTART, TEND, PERSON, LABEL, SCORE),
    answer(knownPerson, en, PERSON, LABEL, SCORE).
answer (knownPersonTokens, de, TSTART, TEND) :-
    ner(de, person, TSTART, TEND, PERSON, LABEL, SCORE),
    answer(knownPerson, de, PERSON, LABEL, SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (what about | do you know | do you happen to know | who is|what is) @KNOWN_PERSONS_EN:LABEL',
             answer(knownPersonTokens, en, @KNOWN_PERSONS_EN:TSTART_LABEL_0, @KNOWN_PERSONS_EN:TEND_LABEL_0)). 
nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (what about | do you know | do you happen to know | who is|what is) @KNOWN_PERSONS_FN_EN:FAMILY_NAME',
             answer(knownPersonTokens, en, @KNOWN_PERSONS_EN:TSTART_FAMILY_NAME_0, @KNOWN_PERSONS_EN:TEND_FAMILY_NAME_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (kennst du|kennst du eigentlich|wer ist|wer ist eigentlich|was ist mit|was ist eigentlich mit|was weisst du über|was weisst du eigentlich über) @KNOWN_PERSONS_DE:LABEL',
             answer(knownPersonTokens, de, @KNOWN_PERSONS_DE:TSTART_LABEL_0, @KNOWN_PERSONS_DE:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (kennst du|kennst du eigentlich|wer ist|wer ist eigentlich|was ist mit|was ist eigentlich mit|was weisst du über|was weisst du eigentlich über) @KNOWN_PERSONS_FN_DE:FAMILY_NAME',
             answer(knownPersonTokens, de, @KNOWN_PERSONS_FN_DE:TSTART_FAMILY_NAME_0, @KNOWN_PERSONS_FN_DE:TEND_FAMILY_NAME_0)). 

nlp_test(de,
         ivr(in('Kennst Du Angela Merkel?'),
             out('Ja, der Name ist mir bekannt'))).
nlp_test(en,
         ivr(in('What about Angela Merkel?'),
             out('That name sounds familiar'))).

%
% birthplace and birtdate questions
%

answer (birthplacePerson, en, PERSON, PERSON_LABEL, SCORE) :-
    rdf (distinct, limit(1),
         PERSON,     wdpd:PlaceOfBirth, BIRTHPLACE,
         BIRTHPLACE, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'en')),
    context_push(topic, people),
    context_push(topic, PERSON),
    context_push(topic, BIRTHPLACE),
    say_eoa(en, format_str('%s was born in %s.', PERSON_LABEL, LABEL), SCORE).

answer (birthplacePerson, de, PERSON, PERSON_LABEL, SCORE) :-
    rdf (distinct, limit(1),
         PERSON,     wdpd:PlaceOfBirth, BIRTHPLACE,
         BIRTHPLACE, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')),
    context_push(topic, people),
    context_push(topic, PERSON),
    context_push(topic, BIRTHPLACE),
    say_eoa(de, format_str('%s wurde in %s geboren.', PERSON_LABEL, LABEL), SCORE).

answer (birthplacePersonTokens, en, TSTART, TEND) :-
    ner(en, person, TSTART, TEND, PERSON, PERSON_LABEL, SCORE),
    answer (birthplacePerson, en, PERSON, PERSON_LABEL, SCORE).
answer (birthplacePersonTokens, de, TSTART, TEND) :-
    ner(de, person, TSTART, TEND, PERSON, PERSON_LABEL, SCORE),
    answer (birthplacePerson, de, PERSON, PERSON_LABEL, SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (where|in which town|in which city) (was|is) @KNOWN_PERSONS_EN:LABEL born?',
             answer(birthplacePersonTokens, en, @KNOWN_PERSONS_EN:TSTART_LABEL_0, @KNOWN_PERSONS_EN:TEND_LABEL_0)). 
nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (where|in which town|in which city) (was|is) @KNOWN_PERSONS_FN_EN:FAMILY_NAME born?',
             answer(birthplacePersonTokens, en, @KNOWN_PERSONS_FN_EN:TSTART_FAMILY_NAME_0, @KNOWN_PERSONS_FN_EN:TEND_FAMILY_NAME_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (wo|in welcher stadt) (wurde|ist) (eigentlich|) @KNOWN_PERSONS_DE:LABEL geboren?',
             answer(birthplacePersonTokens, de, @KNOWN_PERSONS_DE:TSTART_LABEL_0, @KNOWN_PERSONS_DE:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (wo|in welcher stadt) (wurde|ist) (eigentlich|) @KNOWN_PERSONS_FN_DE:FAMILY_NAME geboren?',
             answer(birthplacePersonTokens, de, @KNOWN_PERSONS_FN_DE:TSTART_FAMILY_NAME_0, @KNOWN_PERSONS_FN_DE:TEND_FAMILY_NAME_0)). 

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL which is (the birthplace|place of birth) of @KNOWN_PERSONS_EN:LABEL?',
             answer(birthplacePersonTokens, en, @KNOWN_PERSONS_EN:TSTART_LABEL_0, @KNOWN_PERSONS_EN:TEND_LABEL_0)). 
nlp_gen (en, '@SELF_ADDRESS_EN:LABEL which is (the birthplace|place of birth) of @KNOWN_PERSONS_FN_EN:FAMILY_NAME?',
             answer(birthplacePersonTokens, en, @KNOWN_PERSONS_FN_EN:TSTART_FAMILY_NAME_0, @KNOWN_PERSONS_FN_EN:TEND_FAMILY_NAME_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL welches ist (eigentlich|) (der Geburtsort|die Geburtsstadt) von @KNOWN_PERSONS_DE:LABEL?',
             answer(birthplacePersonTokens, de, @KNOWN_PERSONS_DE:TSTART_LABEL_0, @KNOWN_PERSONS_DE:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL welches ist (eigentlich|) (der Geburtsort|die Geburtsstadt) von @KNOWN_PERSONS_FN_DE:FAMILY_NAME?',
             answer(birthplacePersonTokens, de, @KNOWN_PERSONS_FN_DE:TSTART_FAMILY_NAME_0, @KNOWN_PERSONS_FN_DE:TEND_FAMILY_NAME_0)). 

answer (birthplacePersonContext, en) :-
    context_score(topic, PERSON, 100, SCORE),
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'en')),
    answer (birthplacePerson, en, PERSON, LABEL, SCORE).
answer (birthplacePersonContext, de) :-
    context_score(topic, PERSON, 100, SCORE),
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')),
    answer (birthplacePerson, de, PERSON, LABEL, SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (and|) (where|in which town|in which city) (was|is) (she|he) born (again|)?',
             answer(birthplacePersonContext, en)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (und|) (wo|in welcher stadt) (wurde|ist) (eigentlich|) (er|sie) (nochmal|) geboren?',
             answer(birthplacePersonContext, de)). 

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (and|) which is (the birthplace|place of birth) of (him|her) (again|)?',
             answer(birthplacePersonContext, en)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (und|) welches ist (eigentlich|nochmal|) (der Geburtsort|die Geburtsstadt) von (ihm|ihr)?',
             answer(birthplacePersonContext, de)). 

nlp_test(en,
         ivr(in('Where was Angela Merkel born?'),
             out('angela merkel was born in barmbek-nord')),
         ivr(in('What were we talking about?'),
             out('we were talking about barmbek-nord.')),
         ivr(in('and where was she born again?'),
             out('angela merkel was born in barmbek-nord'))).
nlp_test(de,
         ivr(in('Wo wurde Angela Merkel geboren?'),
             out('angela merkel wurde in barmbek-nord geboren')),
         ivr(in('Welches Thema hatten wir?'),
             out('wir hatten über barmbek-nord gesprochen.')),
         ivr(in('und wo wurde sie nochmal geboren?'),
             out('angela merkel wurde in barmbek-nord geboren'))).

answer (birthdatePerson, en, PERSON, PERSON_LABEL, SCORE) :-
    rdf (distinct, limit(1),
         PERSON,     wdpd:DateOfBirth, TS),
    transcribe_date(en, dativ, TS, TS_SCRIPT),
    context_push(topic, people),
    context_push(topic, birthday),
    context_push(topic, PERSON),
    say_eoa(en, format_str('%s was born on %s.', PERSON_LABEL, TS_SCRIPT), SCORE).
answer (birthdatePerson, de, PERSON, PERSON_LABEL, SCORE) :-
    rdf (distinct, limit(1),
         PERSON,     wdpd:DateOfBirth, TS),
    transcribe_date(de, dativ, TS, TS_SCRIPT),
    context_push(topic, people),
    context_push(topic, birthday),
    context_push(topic, PERSON),
    say_eoa(de, format_str('%s wurde am %s geboren.', PERSON_LABEL, TS_SCRIPT), SCORE).

answer (birthdatePersonTokens, en, TSTART, TEND) :-
    ner(en, person, TSTART, TEND, PERSON, PERSON_LABEL, SCORE),
    answer (birthdatePerson, en, PERSON, PERSON_LABEL, SCORE).
answer (birthdatePersonTokens, de, TSTART, TEND) :-
    ner(de, person, TSTART, TEND, PERSON, PERSON_LABEL, SCORE),
    answer (birthdatePerson, de, PERSON, PERSON_LABEL, SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (when|in which year) (was|is) @KNOWN_PERSONS_EN:LABEL born?',
             answer(birthdatePersonTokens, en, @KNOWN_PERSONS_EN:TSTART_LABEL_0, @KNOWN_PERSONS_EN:TEND_LABEL_0)). 
nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (when|in which year) (was|is) @KNOWN_PERSONS_FN_EN:FAMILY_NAME born?',
             answer(birthdatePersonTokens, en, @KNOWN_PERSONS_FN_EN:TSTART_FAMILY_NAME_0, @KNOWN_PERSONS_FN_EN:TEND_FAMILY_NAME_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (wann|in welchem Jahr) (wurde|ist) (eigentlich|) @KNOWN_PERSONS_DE:LABEL geboren?',
             answer(birthdatePersonTokens, de, @KNOWN_PERSONS_DE:TSTART_LABEL_0, @KNOWN_PERSONS_DE:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (wann|in welchem Jahr) (wurde|ist) (eigentlich|) @KNOWN_PERSONS_FN_DE:FAMILY_NAME geboren?',
             answer(birthdatePersonTokens, de, @KNOWN_PERSONS_FN_DE:TSTART_FAMILY_NAME_0, @KNOWN_PERSONS_FN_DE:TEND_FAMILY_NAME_0)). 

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (when is|on what day is) @KNOWN_PERSONS_EN:LABELS birthday?",
             answer(birthdatePersonTokens, en, @KNOWN_PERSONS_EN:TSTART_LABEL_0, @KNOWN_PERSONS_EN:TEND_LABEL_0)). 
nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (when is|on what day is) @KNOWN_PERSONS_FN_EN:FAMILY_NAMES birthday?",
             answer(birthdatePersonTokens, en, @KNOWN_PERSONS_FN_EN:TSTART_FAMILY_NAME_0, @KNOWN_PERSONS_FN_EN:TEND_FAMILY_NAME_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (wann hat|an welchem Tag hat) (eigentlich|) @KNOWN_PERSONS_DE:LABEL Geburtstag?',
             answer(birthdatePersonTokens, de, @KNOWN_PERSONS_DE:TSTART_LABEL_0, @KNOWN_PERSONS_DE:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (wann hat|an welchem Tag hat) (eigentlich|) @KNOWN_PERSONS_FN_DE:FAMILY_NAME Geburtstag?',
             answer(birthdatePersonTokens, de, @KNOWN_PERSONS_FN_DE:TSTART_FAMILY_NAME_0, @KNOWN_PERSONS_FN_DE:TEND_FAMILY_NAME_0)). 

answer (birthdatePersonContext, en) :-
    context_score(topic, PERSON, 100, SCORE),
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'en')),
    answer (birthdatePerson, en, PERSON, LABEL, SCORE).
answer (birthdatePersonContext, de) :-
    context_score(topic, PERSON, 100, SCORE),
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')),
    answer (birthdatePerson, de, PERSON, LABEL, SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (and|) (when|in which year) (was|is) (he|she) born (again|)?',
             answer(birthdatePersonContext, en)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (und|) (wann|in welchem Jahr) (wurde|ist) (eigentlich|) (sie|er) (nochmal|) geboren?',
             answer(birthdatePersonContext, de)). 

nlp_test(en,
         ivr(in('When was Merkel born?'),
             out('Angela Merkel was born on july seventeen, 1954.')),
         ivr(in('What were we talking about?'),
             out('we were talking about angela merkel.')),
         ivr(in('and when was she born?'),
             out('Angela Merkel was born on july seventeen, 1954.'))
        ).

nlp_test(de,
         ivr(in('Wann wurde Merkel geboren?'),
             out('Angela Merkel wurde am siebzehnten juli 1954 geboren.')),
         ivr(in('Welches Thema hatten wir?'),
             out('wir hatten über angela merkel gesprochen.')),
         ivr(in('und wann wurde sie nochmal geboren?'),
             out('Angela Merkel wurde am siebzehnten juli 1954 geboren.'))
        ).

