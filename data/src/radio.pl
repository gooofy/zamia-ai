% prolog

%! module radio

%
% context setup
%

context(channel, b5aktuell).

%
% natural language part
%

nlp_macro('HI',        map(w(''         )),
                       map(w('Hallo' )),
                       map(w('Hi' ))).

nlp_macro('ADDRESSEE', map(w(''         )),
                       map(w('Computer' )),
                       map(w('HAL'      ))).

nlp_macro('PLEASE'   , map(w(''         )),
                       map(w('bitte'    ))).

nlp_macro('MAL'      , map(w(''         )),
                       map(w('mal'      ))).

nlp_macro('VERB',      map(w('schalte'   ), v('ein'), p('set_context(channel, C); action(media, tune, C)')),
                       map(w('mach '     ), v('an'),  p('set_context(channel, C); action(media, tune, C)')),
                       map(w('mach '     ), v('aus'), p('action(media, off)')),
                       map(w('schalte '  ), v('aus'), p('action(media, off)'))).

nlp_macro('WHAT',      map(w('Musik'           ), p('C is music')),
                       map(w('das Radio '      ), p('context(channel, C)')),
                       map(w('B5 aktuell'      ), p('C is b5aktuell')),
                       map(w('Deutschlandfunk' ), p('C is dlf')),
                       map(w('SWR Info'        ), p('C is swrinfo')),
                       map(w('SWR 3'           ), p('C is swr3')),
                       map(w('Aktuelles'       ), p('C is news')),
                       map(w('Newstalk'        ), p('C is newstalk')),
                       map(w('Power Hit Radio' ), p('C is powerhitradio')),
                       map(w('RTL'             ), p('C is rtl')),
                       map(w('NEW ROCK'        ), p('C is newrock')),
                       map(w('ROCK'            ), p('C is rock')),
                       map(w('POP'             ), p('C is pop')),
                       map(w('DANCE'           ), p('C is dance')),
                       map(w('Tech News'       ), p('C is technews')),
                       map(w('Workout'         ), p('C is workout'))).

nlp_gen('@HI:w @ADDRESSEE:w @VERB:w @PLEASE:w @MAL:w @WHAT:w @VERB:v',
        '@WHAT:p; @VERB:p').

nlp_test(ivr(in('computer schalte bitte new rock ein'),
             action(media, tune, newrock)),
         ivr(in('hal mach das radio aus'),
             action(media, off)),
         ivr(in('schalte bitte das radio ein'),
             action(media, tune, newrock))). 

