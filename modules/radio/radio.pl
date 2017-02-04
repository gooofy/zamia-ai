% prolog

%
% test setup and context
%

set_context_default('test', channel, 'media:B5_aktuell').

%
% natural language part
%

nlp_macro('HI',        map(w(''         )),
                       map(w('Hallo'    )),
                       map(w('Hi'       ))).

nlp_macro('ADDRESSEE', map(w(''         )),
                       map(w('Computer' )),
                       map(w('HAL'      ))).

nlp_macro('PLEASE',    map(w(''         )),
                       map(w('bitte'    ))).

nlp_macro('MAL',       map(w(''         )),
                       map(w('mal'      ))).

nlp_macro('VERB',      map(w('schalte'   ), v('ein'), p('set_context(channel, C); action(media, tune, C)')),
                       map(w('mach '     ), v('an'),  p('set_context(channel, C); action(media, tune, C)')),
                       map(w('mach '     ), v('aus'), p('action(media, off)')),
                       map(w('schalte '  ), v('aus'), p('action(media, off)'))).

nlp_macro('WHAT',      map(w('Musik'           ), p('C is "media:Music"')),
                       map(w('das Radio '      ), p('context(channel, C)')),
                       map(w('B5 aktuell'      ), p('C is "media:B5_aktuell"')),
                       map(w('Deutschlandfunk' ), p('C is "media:Deutschlandfunk"')),
                       map(w('SWR Info'        ), p('C is "media:SWRinfo"')),
                       map(w('SWR 3'           ), p('C is "media:SWR3"')),
                       map(w('Aktuelles'       ), p('C is "media:News"')),
                       map(w('Newstalk'        ), p('C is "media:NewsTalk"')),
                       map(w('Power Hit Radio' ), p('C is "media:Power_Hit_Radio"')),
                       map(w('RTL'             ), p('C is "media:104.6_RTL"')),
                       map(w('NEW ROCK'        ), p('C is "media:New_Rock"')),
                       map(w('ROCK'            ), p('C is "media:Rock"')),
                       map(w('POP'             ), p('C is "media:Pop"')),
                       map(w('DANCE'           ), p('C is "media:Dance"')),
                       map(w('Tech News'       ), p('C is "media:Tech_News"')),
                       map(w('Workout'         ), p('C is "media:Workout"'))).

nlp_gen(de, 
        '@HI:w @ADDRESSEE:w @VERB:w @PLEASE:w @MAL:w @WHAT:w @VERB:v',
        @WHAT:p, @VERB:p).

nlp_test(de,
         ivr(in('HAL, schalte bitte das Radio ein'),
             action(media, tune, 'media:B5_aktuell'))).

nlp_test(de,
         ivr(in('computer schalte bitte new rock ein'),
             action(media, tune, "media:New_Rock"))).


nlp_test(de,
         ivr(in('mach das radio aus'),
             action(media, off))).


% FIXME
% nlp_test(de,
%          ivr(in('computer schalte bitte new rock ein'),
%              action(media, tune, newrock)),
%          ivr(in('hal mach das radio aus'),
%              action(media, off)),
%          ivr(in('schalte bitte das radio ein'),
%              action(media, tune, newrock))). 

