% prolog

%! module weather-nlp

nlp_macro('TIMESPEC',  map(w('')            , p('context(time, T); near_future(weather, T, EvT)')),
                       map(w('heute')       , p('EvT is today')),
                       map(w('morgen')      , p('EvT is tomorrow')),
                       map(w('übermorgen')  , p('EvT is dayAfterTomorrow'))).

nlp_macro('HELLO',     map(w(''          )),
                       map(w('Computer, ')),
                       map(w('HAL, '     )),
                       map(w('Hi, '      )),
                       map(w('Hallo, '   ))).

nlp_macro('PLACE',     map(w('')               , p('context(place, P)')),
                       map(w('in Stuttgart')   , p('P is stuttgart')),
                       map(w('in Freudental')  , p('P is freudental'))).

nlp_macro('TIMESPECF', map(w('')               , p('context(time, T); near_future(weather, T, EvT)')),
                       map(w('für heute')      , p('EvT is today')),
                       map(w('für morgen')     , p('EvT is tomorrow')),
                       map(w('für übermorgen') , p('EvT is dayAfterTomorrow'))).

nlp_macro('PLACEF'  ,  map(w('')               , p('context(place, P)')),
                       map(w('für Stuttgart')  , p('P is stuttgart')),
                       map(w('für Freudental') , p('P is freudental'))).

% dies ist ein prolog kommentar


nlp_gen('@HELLO:w wird es @TIMESPEC:w @PLACE:w regnen?',
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen('@HELLO:w wird es @TIMESPEC:w @PLACE:w Regen geben?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen('@HELLO:w wie groß ist die Wahrscheinlichkeit für Regen @TIMESPEC:w @PLACE:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen('@HELLO:w wie wahrscheinlich ist es, dass es @TIMESPEC:w @PLACE:w regnen wird?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen('@HELLO:w wie wird @TIMESPEC:w @PLACE:w das Wetter?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen('@HELLO:w scheint @TIMESPEC:w @PLACE:w die Sonne?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen('@HELLO:w regnet es @TIMESPEC:w @PLACE:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen('@HELLO:w kommt @TIMESPEC:w noch Regen @PLACE:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen('@HELLO:w wie warm wird es @TIMESPEC:w @PLACE:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen('@HELLO:w wie warm wird es @TIMESPEC:w @PLACE:w werden ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen('@HELLO:w wie wird das Wetter @TIMESPEC:w @PLACE:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen('@HELLO:w wie wird das Wetter @PLACE:w @TIMESPEC:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen('@HELLO:w wie kalt wird es @TIMESPEC:w @PLACE:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen('@HELLO:w wie kalt wird es @TIMESPEC:w @PLACE:w werden ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen('@HELLO:w was sagt der Wetterbericht @TIMESPECF:w @PLACEF:w ?', 
        'context(place, P); @TIMESPECF:p; @PLACEF:p; answer (weather, de, EvT, P)').

nlp_gen('@HELLO:w was sagt die Wettervorhersage @TIMESPECF:w @PLACEF:w ?', 
        'context(place, P); @TIMESPECF:p; @PLACEF:p; answer (weather, de, EvT, P)').

nlp_gen('@HELLO:w wie sind die Wetteraussichten @TIMESPECF:w @PLACEF:w ?', 
        'context(place, P); @TIMESPECF:p; @PLACEF:p; answer (weather, de, EvT, P)').



% FIXME: needs more context
% Und in den kommenden Tagen?
% Wie wird es naechste Woche werden?


% FIXME: sunset time missing in DB
% Wann geht die Sonne unter?

