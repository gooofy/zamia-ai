% prolog

is_computer_scientist(PERSON) :- rdf (PERSON, wdpd:Occupation, wde:ComputerScientist).

%
% named entity recognition (NER) stuff: extra points for computer scientists, programming language and home computer NER
% FIXME: NER for operating systems, ...
%

ner_score (person, PERSON, 200) :- is_computer_scientist(PERSON).

ner_score (programming_language, PROGRAMMING_LANGUAGE, 100). % FIXME: we should probably score by popularity or smth

ner_programming_language(LANG, TITLE_TOKENS, PROGRAMMING_LANGUAGE, LABEL) :-

    atom_chars(LANG, LSTR),

    rdf (distinct,
         PROGRAMMING_LANGUAGE, wdpd:InstanceOf,   wde:ProgrammingLanguage,
         PROGRAMMING_LANGUAGE, rdfs:label,        LABEL,
         filter (lang(LABEL) = LSTR)),

    tokenize (LANG, LABEL, LABEL_TOKENS),

    TITLE_TOKENS = LABEL_TOKENS.

ner(LANG, programming_language, TSTART, TEND, PROGRAMMING_LANGUAGE, LABEL, SCORE) :-

    rdf(ai:curin, ai:tokens, TOKENS),
    list_slice(TSTART, TEND, TOKENS, NAME_TOKENS),
   
    ner_programming_language(LANG, NAME_TOKENS, PROGRAMMING_LANGUAGE, LABEL),

    ner_score (programming_language, PROGRAMMING_LANGUAGE, SCORE).

ner_score (home_computer, HOME_COMPUTER, 100). % FIXME: we should probably score by popularity or smth

ner_home_computer(LANG, TITLE_TOKENS, HOME_COMPUTER, LABEL) :-

    atom_chars(LANG, LSTR),

    rdf (distinct,
         HOME_COMPUTER, wdpd:InstanceOf,   wde:HomeComputer,
         HOME_COMPUTER, rdfs:label,        LABEL,
         filter (lang(LABEL) = LSTR)),

    tokenize (LANG, LABEL, LABEL_TOKENS),

    TITLE_TOKENS = LABEL_TOKENS.

ner(LANG, home_computer, TSTART, TEND, HOME_COMPUTER, LABEL, SCORE) :-

    rdf(ai:curin, ai:tokens, TOKENS),
    list_slice(TSTART, TEND, TOKENS, NAME_TOKENS),
   
    ner_home_computer(LANG, NAME_TOKENS, HOME_COMPUTER, LABEL),

    ner_score (home_computer, HOME_COMPUTER, SCORE).

answer(topic, en) :-
    context_score(topic, computers, 100, SCORE), say_eoa(en, 'We were talking about computers and machines.', SCORE).
answer(topic, de) :-
    context_score(topic, computers, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Computer und Maschinen.', SCORE).

answer(topic, en) :-
    context_score(topic, artificial_intelligence, 100, SCORE), say_eoa(en, 'We were talking about artificial intelligence.', SCORE).
answer(topic, de) :-
    context_score(topic, artificial_intelligence, 100, SCORE), say_eoa(de, 'Wir hatten über künstliche Intelligenz gesprochen.', SCORE).

answer(topic, en) :-
    context_score(topic, programming, 100, SCORE), say_eoa(en, 'We were talking about programming.', SCORE).
answer(topic, de) :-
    context_score(topic, programming, 100, SCORE), say_eoa(de, 'Wir hatten über Programmierung gesprochen.', SCORE).

answer(topic, en) :-
    context_score(topic, home_computer, 100, SCORE), say_eoa(en, 'We were talking about home computers.', SCORE).
answer(topic, de) :-
    context_score(topic, home_computer, 100, SCORE), say_eoa(de, 'Wir hatten über Heimcomputer gesprochen.', SCORE).

answer(topic, en) :-
    context_score(topic, computer_science, 100, SCORE), say_eoa(en, 'We were talking about computer science.', SCORE).
answer(topic, de) :-
    context_score(topic, computer_science, 100, SCORE), say_eoa(de, 'Wir hatten über Informatik gesprochen.', SCORE).

answer(topic, en) :-
    context_score(topic, linux, 100, SCORE), say_eoa(en, 'We were talking about Linux.', SCORE).
answer(topic, de) :-
    context_score(topic, linux, 100, SCORE), say_eoa(de, 'Wir hatten über Linux gesprochen.', SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (do you know|what do you think about|have you tried|do you run|do you like) Linux',
             context_push(topic, linux), say_eoa(en, 'Hey, Linux is my operating system, it is very cool.')).
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (kennst du|was hältst du von|was denkst du über|läufst du unter|magst du) Linux',
             context_push(topic, linux), say_eoa(en, 'Hey, Linux ist mein Betriebssystem, das ist richtig cool.')).

nlp_test(en,
         ivr(in('do you know linux?'),
             out("Hey, Linux is my operating system, it is very cool."))).
nlp_test(de,
         ivr(in('magst du linux?'),
             out('Hey, Linux ist mein Betriebssystem, das ist richtig cool.'))).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, computer_science, 100, SCORE),
    is_computer_scientist(PERSON),
    is_male(PERSON),
    context_push(topic, computer_science),
    context_push(topic, PERSON),
    say_eoa(en, 'He is a computer scientist.', SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, computer_science, 100, SCORE),
    is_computer_scientist(PERSON),
    is_male(PERSON),
    context_push(topic, computer_science),
    context_push(topic, PERSON),
    say_eoa(de, 'Er ist ein Informatiker.', SCORE).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, computer_science, 100, SCORE),
    is_computer_scientist(PERSON),
    is_female(PERSON),
    context_push(topic, computer_science),
    context_push(topic, PERSON),
    say_eoa(en, 'She is a computer scientist.', SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, computer_science, 100, SCORE),
    is_computer_scientist(PERSON),
    is_female(PERSON),
    context_push(topic, computer_science),
    context_push(topic, PERSON),
    say_eoa(de, 'Sie ist eine Informatikerin.', SCORE).

nlp_test(en,
         ivr(in('Who is Niklaus Wirth?'),
             out('He is a computer scientist.'))).
nlp_test(de,
         ivr(in('wer ist Niklaus Wirth?'),
             out('Er ist ein Informatiker.'))).

nlp_macro('PROGRAMMING_LANGUAGE_EN', NAME, LABEL) :- 
    rdf(distinct,
        NAME, wdpd:InstanceOf, wde:ProgrammingLanguage,
        NAME, rdfs:label, LABEL,
        filter(lang(LABEL) = 'en')).
nlp_macro('PROGRAMMING_LANGUAGE_DE', NAME, LABEL) :- 
    rdf(distinct,
        NAME, wdpd:InstanceOf, wde:ProgrammingLanguage,
        NAME, rdfs:label, LABEL,
        filter(lang(LABEL) = 'de')).

answer (knownProgrammingLanguage, en, PROGRAMMING_LANGUAGE, PROGRAMMING_LANGUAGE_LABEL, SCORE) :-
    context_push(topic, programming),
    context_push(topic, PROGRAMMING_LANGUAGE),
    say_eoa(en, format_str('%s is a programming language.', PROGRAMMING_LANGUAGE_LABEL), SCORE).
answer (knownProgrammingLanguage, de, PROGRAMMING_LANGUAGE, PROGRAMMING_LANGUAGE_LABEL, SCORE) :-
    context_push(topic, programming),
    context_push(topic, PROGRAMMING_LANGUAGE),
    say_eoa(de, format_str('%s ist eine Programmiersprache.', PROGRAMMING_LANGUAGE_LABEL), SCORE).

answer (knownProgrammingLanguageTokens, en, TSTART, TEND) :-
    ner(en, programming_language, TSTART, TEND, PROGRAMMING_LANGUAGE, PROGRAMMING_LANGUAGE_LABEL, SCORE),
    answer (knownProgrammingLanguage, en, PROGRAMMING_LANGUAGE, PROGRAMMING_LANGUAGE_LABEL, SCORE).
answer (knownProgrammingLanguageTokens, de, TSTART, TEND) :-
    ner(de, programming_language, TSTART, TEND, PROGRAMMING_LANGUAGE, PROGRAMMING_LANGUAGE_LABEL, SCORE),
    answer (knownProgrammingLanguage, de, PROGRAMMING_LANGUAGE, PROGRAMMING_LANGUAGE_LABEL, SCORE).

nlp_gen(en, '@SELF_ADDRESS_EN:LABEL (do you know|what is) @PROGRAMMING_LANGUAGE_EN:LABEL?',
             answer(knownProgrammingLanguageTokens, en, @PROGRAMMING_LANGUAGE_EN:TSTART_LABEL_0, @PROGRAMMING_LANGUAGE_EN:TEND_LABEL_0)). 
nlp_gen(de, '@SELF_ADDRESS_DE:LABEL (kennst Du|was ist) @PROGRAMMING_LANGUAGE_DE:LABEL?',
             answer(knownProgrammingLanguageTokens, de, @PROGRAMMING_LANGUAGE_DE:TSTART_LABEL_0, @PROGRAMMING_LANGUAGE_DE:TEND_LABEL_0)). 

nlp_test(en,
         ivr(in('do you know prolog?'),
             out("Prolog is a programming language")),
         ivr(in('what was our topic, again?'),
             out("We were talking about prolog."))).
nlp_test(de,
         ivr(in('kennst du prolog?'),
             out('Prolog ist eine Programmiersprache')),
         ivr(in('Worüber hatten wir gesprochen?'),
             out("Wir hatten über prolog gesprochen."))).

nlp_macro('HOME_COMPUTER_EN', NAME, LABEL) :- 
    rdf(distinct,
        NAME, wdpd:InstanceOf, wde:HomeComputer,
        NAME, rdfs:label, LABEL,
        filter(lang(LABEL) = 'en')).
nlp_macro('HOME_COMPUTER_DE', NAME, LABEL) :- 
    rdf(distinct,
        NAME, wdpd:InstanceOf, wde:HomeComputer,
        NAME, rdfs:label, LABEL,
        filter(lang(LABEL) = 'de')).

answer (knownHomeComputer, en, HOME_COMPUTER, HOME_COMPUTER_LABEL, SCORE) :-
    context_push(topic, programming),
    context_push(topic, HOME_COMPUTER),
    say_eoa(en, format_str('The %s is a home computer.', HOME_COMPUTER_LABEL), SCORE).
answer (knownHomeComputer, de, HOME_COMPUTER, HOME_COMPUTER_LABEL, SCORE) :-
    context_push(topic, programming),
    context_push(topic, HOME_COMPUTER),
    say_eoa(de, format_str('Der %s ist ein Heimcomputer.', HOME_COMPUTER_LABEL), SCORE).

answer (knownHomeComputerTokens, en, TSTART, TEND) :-
    ner(en, home_computer, TSTART, TEND, HOME_COMPUTER, HOME_COMPUTER_LABEL, SCORE),
    answer (knownHomeComputer, en, HOME_COMPUTER, HOME_COMPUTER_LABEL, SCORE).
answer (knownHomeComputerTokens, de, TSTART, TEND) :-
    ner(de, home_computer, TSTART, TEND, HOME_COMPUTER, HOME_COMPUTER_LABEL, SCORE),
    answer (knownHomeComputer, de, HOME_COMPUTER, HOME_COMPUTER_LABEL, SCORE).

nlp_gen(en, '@SELF_ADDRESS_EN:LABEL (do you know|what is) @HOME_COMPUTER_EN:LABEL?',
            answer(knownHomeComputerTokens, en, @HOME_COMPUTER_EN:TSTART_LABEL_0, @HOME_COMPUTER_EN:TEND_LABEL_0)). 
nlp_gen(de, '@SELF_ADDRESS_DE:LABEL (kennst Du|was ist) @HOME_COMPUTER_DE:LABEL?',
            answer(knownHomeComputerTokens, de, @HOME_COMPUTER_DE:TSTART_LABEL_0, @HOME_COMPUTER_DE:TEND_LABEL_0)). 

nlp_test(en,
         ivr(in('do you know commodore 64?'),
             out("The Commodore 64 is a home computer")),
         ivr(in('what was our topic, again?'),
             out("We were talking about Commodore 64."))).
nlp_test(de,
         ivr(in('kennst du sinclair ql?'),
             out('Der Sinclair QL ist ein Heimcomputer')),
         ivr(in('Worüber hatten wir gesprochen?'),
             out("Wir hatten über Sinclair QL gesprochen."))).

%
% random / misc
%

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL bill gates',
             'What do you think about Bill Gates?').
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL bill gates',
             'Wie denkst Du über Bill Gates?').

