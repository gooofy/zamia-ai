% prolog

%! module radio-nlp

nlp_macro('ADDRESSEE', map(w(''         )),
                       map(w('Computer' )),
                       map(w('HAL'      ))).

nlp_macro('PLEASE'   , map(w(''         )),
                       map(w('bitte'    ))).

nlp_macro('VERB',      map(w('schalte'   ), v('ein'), p('turn_on(W)')),
                       map(w('mach '     ), v('an'),  p('turn_on(W)')),
                       map(w('mach '     ), v('aus'), p('turn_off(W)')),
                       map(w('schalte '  ), v('aus'), p('turn_off(W)'))).

nlp_macro('WHAT',      map(w('Musik'           ), p('W is music')),
                       map(w('das Radio '      ), p('W is radio')),
                       map(w('B5 aktuell'      ), p('W is b5aktuell')),
                       map(w('Deutschlandfunk' ), p('W is dlf')),
                       map(w('SWR Info'        ), p('W is swrinfo')),
                       map(w('SWR 3'           ), p('W is swr3')),
                       map(w('Aktuelles'       ), p('W is news')),
                       map(w('Newstalk'        ), p('W is newstalk')),
                       map(w('Power Hit Radio' ), p('W is powerhitradio')),
                       map(w('RTL'             ), p('W is rtl')),
                       map(w('NEW ROCK'        ), p('W is newrock')),
                       map(w('ROCK'            ), p('W is rock')),
                       map(w('POP'             ), p('W is pop')),
                       map(w('DANCE'           ), p('W is dance')),
                       map(w('Tech News'       ), p('W is technews')),
                       map(w('Workout'         ), p('W is workout'))).

nlp_gen('@ADDRESSEE:w @VERB:w @PLEASE:w @WHAT:w @VERB:v',
        '@WHAT:p; @VERB:p').

