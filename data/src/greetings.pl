% prolog

%! module greetings-nlp
%! requires common-sense

%
% test setup and context
%

set_context_default('test', place, 'dbr:Stuttgart').
set_context_default('test', time, today).
set_context_default('test', currentTime, T) :- date_time_stamp(date(2016,12,06,13,28,6,'local'), T).

nlp_test_setup(context('test')).


answer(greeting, de, personal) :-
    say_eou(de, "Hallo!"),
    say_eou(de, "Hi!"),
    say_eou(de, "Grüß Dich!"),
    say_eou(de, "Huhu!").

answer(greeting, de, anonymous) :-
    context(currentTime, TS),
    before_noon(TS),
    say_eou(de, "Guten Morgen!").

answer(greeting, de, anonymous) :-
    context(currentTime, TS),
    before_evening(TS),
    after_noon(TS),
    say_eou(de, "Guten Tag!"),
    say_eou(de, "Hallo!").

answer(greeting, de, anonymous) :-
    context(currentTime, TS),
    after_evening(TS),
    say_eou(de, "Guten Abend!").

answer(goodbye, de, anonymous) :-
    say_eou(de, "Auf Wiedersehen!").

answer(goodbye, de, personal) :-
    say_eou(de, "Ade"),
    say_eou(de, "Tschüss"),
    say_eou(de, "Ciao").

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
                       map(w('ciao')          , p('answer (goodbye,  de, S)')),
                       map(w('ade')              , p('answer (goodbye,  de, S)'))).

nlp_macro('ADDRESSEE', map(w(''         ), p('S is anonymous')),
                       map(w('Computer '), p('S is personal')),
                       map(w('HAL '     ), p('S is personal'))).

nlp_gen(de,'@GREETING:w @ADDRESSEE:w',
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

