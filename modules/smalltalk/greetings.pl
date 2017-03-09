% prolog

%
% test setup and context
%

set_context_default('test', time, today).
set_context_default('test', currentTime, T) :- date_time_stamp(date(2016,12,06,13,28,6,'local'), T).

answer(greeting, de, personal) :-
    say_eou(de, "Hallo!"),
    say_eou(de, "Hi!"),
    say_eou(de, "Grüß Dich!"),
    say_eou(de, "Hey!"),
    action(attention,on).

answer(greeting, de, anonymous) :-
    context(currentTime, TS),
    before_noon(TS),
    say_eou(de, "Guten Morgen!"),
    action(attention,on).

answer(greeting, de, anonymous) :-
    context(currentTime, TS),
    before_evening(TS),
    after_noon(TS),
    say_eou(de, "Guten Tag!"),
    say_eou(de, "Hallo!"),
    action(attention,on).

answer(greeting, de, anonymous) :-
    context(currentTime, TS),
    after_evening(TS),
    say_eou(de, "Guten Abend!"),
    action(attention,on).

answer(goodbye, de, anonymous) :-
    say_eou(de, "Auf Wiedersehen!"),
    action(attention,off).

answer(goodbye, de, personal) :-
    say_eou(de, "Ade"),
    say_eou(de, "Tschüss"),
    say_eou(de, "Ciao"),
    action(attention,off).

nlp_macro('GREETING', W, P) :- W is 'guten morgen'     , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'hallo'            , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'hi'               , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'guten tag'        , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'tag'              , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'morgen'           , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'guten abend'      , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'gute nacht'       , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'huhu'             , P is 'answer (greeting, de, S)'.
nlp_macro('GREETING', W, P) :- W is 'auf wiedersehen'  , P is 'answer (goodbye,  de, S)'.
nlp_macro('GREETING', W, P) :- W is 'tschüss'          , P is 'answer (goodbye,  de, S)'.
nlp_macro('GREETING', W, P) :- W is 'ciao'             , P is 'answer (goodbye,  de, S)'.
nlp_macro('GREETING', W, P) :- W is 'ade'              , P is 'answer (goodbye,  de, S)'.

nlp_macro('ADDRESSEE', W, P) :- W is 'Computer ', P is 'S is personal'.
nlp_macro('ADDRESSEE', W, P) :- W is 'HAL '     , P is 'S is personal'.

nlp_gen(de,'@GREETING:W',
           S is anonymous, @GREETING:P).

nlp_gen(de,'@GREETING:W @ADDRESSEE:W',
           @ADDRESSEE:P, @GREETING:P).

nlp_gen(de,'@ADDRESSEE:W @GREETING:W',
           @ADDRESSEE:P, @GREETING:P).

set_context_default('test', currentTime, T) :- date_time_stamp(date(2016,12,06,10,28,6,'local'), T).
nlp_test(de,
         ivr(in('hallo'),
             out('Guten Morgen!'))).

set_context_default('test', currentTime, T) :- date_time_stamp(date(2016,12,06,13,28,6,'local'), T).
nlp_test(de,
         ivr(in('hi'),
             out('Guten Tag!'))).
nlp_test(de,
         ivr(in('hi'),
             out('Hallo!'))).

set_context_default('test', currentTime, T) :- date_time_stamp(date(2016,12,06,19,28,6,'local'), T).
nlp_test(de,
         ivr(in('guten abend'),
             out('Guten Abend!'))).

nlp_test(de,
         ivr(in('hallo computer'),
             out('Hi!'))).

nlp_test(de,
         ivr(in('Tschüss computer'),
             out('Tschüss!'))).

nlp_test(de,
         ivr(in('Ciao'),
             out('Auf Wiedersehen!'))).

nlp_macro('ADDRESSEE2', W) :- W is ''.
nlp_macro('ADDRESSEE2', W) :- W is 'Computer '.
nlp_macro('ADDRESSEE2', W) :- W is 'HAL '.

answer(howdy, de) :-
    say_eou(de, "Sehr gut, danke. Und selber?"),
    say_eou(de, "Gut, danke. Wie geht es Dir?"),
    say_eou(de, "Mir geht's prima, und Dir?"),
    say_eou(de, "Mir geht's gut, und selber?"),
    say_eou(de, "Super, wie immer!"),
    say_eou(de, "Gut, danke der Nachfrage. Wie geht es Dir?").

nlp_gen(de,'@ADDRESSEE2:W wie geht es dir?',
           answer (howdy, de)).

nlp_gen(de,'@ADDRESSEE2:W wie gehts',
           answer (howdy, de)).

nlp_gen(de,'@ADDRESSEE2:W was geht',
           answer (howdy, de)).

nlp_gen(de,'@ADDRESSEE2:W wie fühlst du dich',
           answer (howdy, de)).

