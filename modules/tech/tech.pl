% prolog

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

nlp_gen(en, '@SELF_ADDRESS_EN:LABEL (do you know|what is) @PROGRAMMING_LANGUAGE_EN:LABEL?',
            context_push(topic, programming), context_push(topic, "@PROGRAMMING_LANGUAGE_EN:NAME"), say_eoa(en, 'Yes, that is a programming language')).
nlp_gen(de, '@SELF_ADDRESS_DE:LABEL (kennst Du|was ist) @PROGRAMMING_LANGUAGE_DE:LABEL?',
            context_push(topic, programming), context_push(topic, "@PROGRAMMING_LANGUAGE_DE:NAME"), say_eoa(de, 'Ja, das ist eine Programmiersprache')).

nlp_test(en,
         ivr(in('do you know prolog?'),
             out("Yes that is a programming language")),
         ivr(in('what was our topic, again?'),
             out("We were talking about prolog."))).
nlp_test(de,
         ivr(in('kennst du prolog?'),
             out('Ja, das ist eine Programmiersprache')),
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

nlp_gen(en, '@SELF_ADDRESS_EN:LABEL (do you know|what is) @HOME_COMPUTER_EN:LABEL?',
            context_push(topic, home_computer), context_push(topic, "@HOME_COMPUTER_EN:NAME"), say_eoa(en, 'Yes, that was a home computer')).
nlp_gen(de, '@SELF_ADDRESS_DE:LABEL (kennst Du|was ist) @HOME_COMPUTER_DE:LABEL?',
            context_push(topic, home_computer), context_push(topic, "@HOME_COMPUTER_DE:NAME"), say_eoa(de, 'Ja, das ist ein Heimcomputer')).

nlp_test(en,
         ivr(in('do you know commodore 64?'),
             out("Yes that was a home computer")),
         ivr(in('what was our topic, again?'),
             out("We were talking about Commodore 64."))).
nlp_test(de,
         ivr(in('kennst du sinclair ql?'),
             out('Ja, das ist ein Heimcomputer')),
         ivr(in('Worüber hatten wir gesprochen?'),
             out("Wir hatten über Sinclair QL gesprochen."))).

%
% random / misc
%

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL bill gates',
             'What do you think about Bill Gates?').
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL bill gates',
             'Wie denkst Du über Bill Gates?').

