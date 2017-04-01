% prolog

%
% test setup and context
%

answer(greeting, de, personal) :-
    action(attention, on),
    say_eoa(de, "Hallo!"),

    action(attention, on),
    say_eoa(de, "Hi!"),

    action(attention, on),
    say_eoa(de, "Grüß Dich!"),

    action(attention, on),
    say_eoa(de, "Hey!").

answer(greeting, de, anonymous) :-
    rdf(ai:curin, ai:currentTime, TS),
    before_noon(TS),
    action(attention, on),
    say_eoa(de, "Guten Morgen!").

answer(greeting, de, anonymous) :-
    rdf(ai:curin, ai:currentTime, TS),
    before_evening(TS),
    after_noon(TS),
    action(attention, on),
    say_eoa(de, "Guten Tag!"),
    action(attention, on),
    say_eoa(de, "Hallo!").

answer(greeting, de, anonymous) :-
    rdf(ai:curin, ai:currentTime, TS),
    after_evening(TS),
    action(attention, on),
    say_eoa(de, "Guten Abend!").

answer(goodbye, de, anonymous) :-
    action(attention,off),
    say_eoa(de, "Auf Wiedersehen!").

answer(goodbye, de, personal) :-
    action(attention, off),
    say_eoa(de, "Ade"),
    action(attention, off),
    say_eoa(de, "Tschüss"),
    action(attention, off),
    say_eoa(de, "Bis bald"),
    action(attention, off),
    say_eoa(de, "Ciao").

nlp_macro('GREETING', W, P) :- W is 'guten morgen'        , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'hallo'               , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'hi'                  , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'guten tag'           , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'tag'                 , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'morgen'              , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'guten abend'         , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'gute nacht'          , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'huhu'                , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'auf wiedersehen'     , P is 'answer (goodbye,  de, S)'.
nlp_macro('GREETING', W, P) :- W is 'tschüss'             , P is 'answer (goodbye,  de, S)'.
nlp_macro('GREETING', W, P) :- W is 'ciao'                , P is 'answer (goodbye,  de, S)'.
nlp_macro('GREETING', W, P) :- W is 'ade'                 , P is 'answer (goodbye,  de, S)'.
nlp_macro('GREETING', W, P) :- W is 'bye'                 , P is 'answer (goodbye,  de, S)'.
nlp_macro('GREETING', W, P) :- W is 'cu'                  , P is 'answer (goodbye,  de, S)'.
nlp_macro('GREETING', W, P) :- W is 'bis bald'            , P is 'answer (goodbye,  de, S)'.
nlp_macro('GREETING', W, P) :- W is 'bis zum nächsten mal', P is 'answer (goodbye,  de, S)'.

nlp_macro('ADDRESSEE', W, P) :- W is 'Computer ', P is 'S is personal'.
nlp_macro('ADDRESSEE', W, P) :- W is 'HAL '     , P is 'S is personal'.

nlp_gen(de,'@GREETING:W',
           S is anonymous, @GREETING:P).

nlp_gen(de,'@GREETING:W @ADDRESSEE:W',
           @ADDRESSEE:P, @GREETING:P).

nlp_gen(de,'@ADDRESSEE:W @GREETING:W',
           @ADDRESSEE:P, @GREETING:P).

nlp_test(de,
         ivr(in('hi'),
             out('Guten Tag!'),
             action(attention, on))).
nlp_test(de,
         ivr(in('hi'),
             out('Hallo!'),
             action(attention, on))).

nlp_test(de,
         ivr(in('hallo computer'),
             out('Hi!'),
             action(attention, on))).

nlp_test(de,
         ivr(in('Tschüss computer'),
             out('Tschüss!'),
             action(attention, off))).

nlp_test(de,
         ivr(in('Ciao'),
             out('Auf Wiedersehen!'),
             action(attention, off))).

nlp_macro('ADDRESSEE2', W) :- W is ''.
nlp_macro('ADDRESSEE2', W) :- W is 'Computer '.
nlp_macro('ADDRESSEE2', W) :- W is 'HAL '.

answer(howdy, de) :-
    say_eoa(de, "Sehr gut, danke. Und selber?"),
    say_eoa(de, "Gut, danke. Wie geht es Dir?"),
    say_eoa(de, "Mir geht's prima, und Dir?"),
    say_eoa(de, "Mir geht's gut, und selber?"),
    say_eoa(de, "Super, wie immer!"),
    say_eoa(de, "Gut, danke der Nachfrage. Wie geht es Dir?").

nlp_gen(de,'@ADDRESSEE2:W wie geht es dir?',
           answer (howdy, de)).

nlp_gen(de,'@ADDRESSEE2:W wie gehts',
           answer (howdy, de)).

nlp_gen(de,'@ADDRESSEE2:W was geht',
           answer (howdy, de)).

nlp_gen(de,'@ADDRESSEE2:W wie fühlst du dich',
           answer (howdy, de)).

