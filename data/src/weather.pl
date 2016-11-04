% prolog

%! module weather
%! requires common-sense

%
% weather reasoning / common sense
%

near_future(weather, T, today)    :- before_evening(T).
near_future(weather, T, tomorrow) :- after_evening(T).

%
% weather answers 
%

answerWeatherDe(weatherCondRain, DeP, DeEvT, TMIN, TMAX):-
    say_eou(de, "%s regnet es in %s und es wird zwischen %d und %d Grad warm.", DeEvT, DeP, TMIN, TMAX).

answerWeatherDe(weatherCondScatteredClouds, DeP, DeEvT, TMIN, TMAX):-
    say_eou(de, "%s ist es in %s aufgelockert bewölkt und es wird zwischen %d und %d Grad warm.", DeEvT, DeP, TMIN, TMAX).

answer(weather, de, EvT, P) :-
    time(E, EvT), 
    place(E, P), 
    weatherDesc(E, DESC),
    tempMin(E, TMIN),
    tempMax(E, TMAX),
    precipitation (E, PREC),
    timeStrDe(EvT, DeEvT),
    placeStrDe(P, DeP),
    answerWeatherDe(DESC, DeP, DeEvT, TMIN, TMAX).

answer(weatherPrecCloud, de, EvT, P) :-
    time(E, EvT), 
    place(E, P), 
    precipitation (E, PREC),
    cloudiness (E, CLDS),
    timeStrDe(EvT, DeEvT),
    placeStrDe(P, DeP),
    answerWeatherPrecCloudDe(PREC, CLDS, DeEvT, DeP).

answerWeatherPrecCloudDe(PREC, CLDS, DeEvT, DeP) :-
    PREC < 0.5,
    CLDS < 50,
    say_eou(de, "%s scheint in %s überwiegend die Sonne und es wird kaum Niederschlag geben.", DeEvT, DeP).

answerWeatherPrecCloudDe(PREC, CLDS, DeEvT, DeP) :-
    PREC >= 0.5,
    CLDS < 50,
    say_eou(de,"%s scheint in %s oft die Sonne, aber es gibt auch %d Millimeter Niederschlag.", DeEvT, DeP, PREC).

answerWeatherPrecCloudDe(PREC, CLDS, DeEvT, DeP) :-
    PREC < 0.5,
    CLDS >= 50,
    say_eou(de,"%s ist es in %s überwiegend bewölkt, aber es gibt wenig Niederschlag.", DeEvT, DeP).

answerWeatherPrecCloudDe(PREC, CLDS, DeEvT, DeP) :-
    PREC >= 0.5,
    CLDS >= 50,
    say_eou(de,"%s ist es in %s überwiegend bewölkt, und es gibt %d Millimeter Niederschlag.", DeEvT, DeP, PREC).

%
% nlp processing (german)
%

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

nlp_gen(de,
        '@HELLO:w wird es @TIMESPEC:w @PLACE:w regnen?',
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w wird es @TIMESPEC:w @PLACE:w Regen geben?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w wie groß ist die Wahrscheinlichkeit für Regen @TIMESPEC:w @PLACE:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w wie wahrscheinlich ist es, dass es @TIMESPEC:w @PLACE:w regnen wird?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w wie wird @TIMESPEC:w @PLACE:w das Wetter?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w scheint @TIMESPEC:w @PLACE:w die Sonne?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w regnet es @TIMESPEC:w @PLACE:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w kommt @TIMESPEC:w noch Regen @PLACE:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weatherPrecCloud, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w wie warm wird es @TIMESPEC:w @PLACE:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w wie warm wird es @TIMESPEC:w @PLACE:w werden ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w wie wird das Wetter @TIMESPEC:w @PLACE:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w wie wird das Wetter @PLACE:w @TIMESPEC:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w wie kalt wird es @TIMESPEC:w @PLACE:w ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w wie kalt wird es @TIMESPEC:w @PLACE:w werden ?', 
        'context(place, P); @TIMESPEC:p; @PLACE:p; answer (weather, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w was sagt der Wetterbericht @TIMESPECF:w @PLACEF:w ?', 
        'context(place, P); @TIMESPECF:p; @PLACEF:p; answer (weather, de, EvT, P)').

nlp_gen(de,
        '@HELLO:w was sagt die Wettervorhersage @TIMESPECF:w @PLACEF:w ?', 
        'context(place, P); @TIMESPECF:p; @PLACEF:p; answer (weather, de, EvT, P)').

nlp_gen(de, 
        '@HELLO:w wie sind die Wetteraussichten @TIMESPECF:w @PLACEF:w ?', 
        'context(place, P); @TIMESPECF:p; @PLACEF:p; answer (weather, de, EvT, P)').

% multiple iteraction steps
% FIXME: many more examples needed

nlp_gen(de,
        '@HELLO:w wie wird das Wetter @PLACE:w ?', 
        'context(time, T); near_future(weather, T, EvT); @PLACE:p; answer (weather, de, EvT, P); set_context(place, P)',
        'und in den nächsten Tagen?',
        'EvT is nextThreeDays, context(place, P); answer (weather, de, EvT, P)',
        'wie wird es nächste Woche werden?',
        '"Das weiss ich nicht."' % FIXME
        ).

%
% test setup and context
%

set_context_default('test', place, stuttgart).
set_context_default('test', time, T) :- date_time_stamp(date(2016,10,30,13,28,6,'local'), T).

nlp_test_setup(requires('weather-data-test'), context('test')).

%
% tests (german)
%

nlp_test(de,
         ivr(in('computer, wie wird das wetter?'),
             out('heute ist es in Stuttgart aufgelockert bewölkt und es wird zwischen 10 und 21 Grad warm.')),
         ivr(in('und in den nächsten Tagen?'),
             out('in den nächsten drei Tagen regnet es in Stuttgart und es wird zwischen 6 und 24 Grad warm.')),
         ivr(in('wie wird es nächste Woche werden?'),
             action(media, tune, newrock))). 


% FIXME: sunset time missing in DB
% Wann geht die Sonne unter?

