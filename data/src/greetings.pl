% prolog

%! module greetings-nlp

nlp_macro('GREETING',  map(w('guten morgen')     , p('answer (greeting. S)')),
                       map(w('hallo')            , p('answer (greeting. S)')),
                       map(w('hi')               , p('answer (greeting. S)')),
                       map(w('guten tag')        , p('answer (greeting. S)')),
                       map(w('tag')              , p('answer (greeting. S)')),
                       map(w('morgen')           , p('answer (greeting. S)')),
                       map(w('guten abend')      , p('answer (greeting. S)')),
                       map(w('gute nacht')       , p('answer (greeting. S)')),
                       map(w('huhu')             , p('answer (greeting. S)')),
                       map(w('auf wiedersehen')  , p('answer (goodbye, S)')),
                       map(w('tschüss')          , p('answer (goodbye, S)')),
                       map(w('ade')              , p('answer (goodbye, S)'))).

nlp_macro('ADDRESSEE', map(w(''         ), p('S is anonymoys')),
                       map(w('Computer '), p('S is personal')),
                       map(w('HAL '     ), p('S is personal'))).

nlp_gen('@GREETING:w @ADDRESSEE:w',
        '@ADDRESSEE:p; @GREETING:p').

