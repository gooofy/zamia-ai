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

nlp_macro('GREETING',  map(w('guten morgen')     , p('answer (greeting, de, S)')),
                       map(w('hallo')            , p('answer (greeting, de, S)')),
                       map(w('hi')               , p('answer (greeting, de, S)')),
                       map(w('guten tag')        , p('answer (greeting, de, S)')),
                       map(w('tag')              , p('answer (greeting, de, S)')),
                       map(w('morgen')           , p('answer (greeting, de, S)')),
                       map(w('guten abend')      , p('answer (greeting, de, S)')),
                       map(w('gute nacht')       , p('answer (greeting, de, S)')),
                       map(w('huhu')             , p('answer (greeting, de, S)')),
                       map(w('auf wiedersehen')  , p('answer (goodbye,  de, S)')),
                       map(w('tschüss')          , p('answer (goodbye,  de, S)')),
                       map(w('ciao')             , p('answer (goodbye,  de, S)')),
                       map(w('ade')              , p('answer (goodbye,  de, S)'))).

nlp_macro('ADDRESSEE', map(w('Computer '), p('S is personal')),
                       map(w('HAL '     ), p('S is personal'))).

nlp_gen(de,'@GREETING:w',
           'S is anonymous; @GREETING:p').

nlp_gen(de,'@GREETING:w @ADDRESSEE:w',
           '@ADDRESSEE:p; @GREETING:p').

nlp_gen(de,'@ADDRESSEE:w @GREETING:w',
           '@ADDRESSEE:p; @GREETING:p').

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

nlp_macro('ADDRESSEE2', map(w('')),
                        map(w('Computer ')),
                        map(w('HAL '     ))).

answer(howdy, de) :-
    say_eou(de, "Sehr gut, danke. Und selber?"),
    say_eou(de, "Gut, danke. Wie geht es Dir?"),
    say_eou(de, "Mir geht's prima, und Dir?"),
    say_eou(de, "Mir geht's gut, und selber?"),
    say_eou(de, "Super, wie immer!"),
    say_eou(de, "Gut, danke der Nachfrage. Wie geht es Dir?").

nlp_gen(de,'@ADDRESSEE2:w wie geht es dir?',
           'answer (howdy, de)').

nlp_gen(de,'@ADDRESSEE2:w wie gehts',
           'answer (howdy, de)').

nlp_gen(de,'@ADDRESSEE2:w was geht',
           'answer (howdy, de)').

nlp_gen(de,'@ADDRESSEE2:w wie fühlst du dich',
           'answer (howdy, de)').

