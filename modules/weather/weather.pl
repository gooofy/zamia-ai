% prolog

%
% test setup and context
%

set_context_default('test', place, 'dbr:Stuttgart').
set_context_default('test', time, today).
set_context_default('test', currentTime, T) :- date_time_stamp(date(2016,12,06,13,28,6,'local'), T).

%
% weather reasoning / common sense
%

near_future(weather, today) :-
    context(currentTime, TS),
    before_evening(TS).

near_future(weather, tomorrow) :-
    context(currentTime, TS),
    after_evening(TS).

%
% weather answers 
%

answerWeather(de, Code, Precipitation, TempMin, TempMax, DeP, DeEvT) :-
    Code is "01", say_eou(de, format_str("%s wird es der Himmel klar sein in %s und es wird zwischen %d und %d Grad warm.", DeEvT, DeP, TempMin, TempMax)).

answerWeather(de, Code, Precipitation, TempMin, TempMax, DeP, DeEvT) :-
    Code is "02", say_eou(de, format_str("%s wird es wenige Wolken geben in %s und es wird zwischen %d und %d Grad warm.", DeEvT, DeP, TempMin, TempMax)).

answerWeather(de, Code, Precipitation, TempMin, TempMax, DeP, DeEvT) :-
    Code is "03", say_eou(de, format_str("%s wird es lockere Wolken geben in %s und es wird zwischen %d und %d Grad warm.", DeEvT, DeP, TempMin, TempMax)).

answerWeather(de, Code, Precipitation, TempMin, TempMax, DeP, DeEvT) :-
    Code is "04", say_eou(de, format_str("%s zeigt sich ab und an die Sonne in %s und es wird zwischen %d und %d Grad warm.", DeEvT, DeP, TempMin, TempMax)).

answerWeather(de, Code, Precipitation, TempMin, TempMax, DeP, DeEvT) :-
    Code is "09", say_eou(de, format_str("%s wird es %d Millimeter Schauer geben in %s und es wird zwischen %d und %d Grad warm.", DeEvT, Precipitation, DeP, TempMin, TempMax)).

answerWeather(de, Code, Precipitation, TempMin, TempMax, DeP, DeEvT) :-
    Code is "10", say_eou(de, format_str("%s regnet es %d Millimeter in %s und es wird zwischen %d und %d Grad warm.", DeEvT, Precipitation, DeP, TempMin, TempMax)).

answerWeather(de, Code, Precipitation, TempMin, TempMax, DeP, DeEvT) :-
    Code is "11", say_eou(de, format_str("%s wird es Gewitter geben mit %d Millimeter Niederschlag in %s und es wird zwischen %d und %d Grad warm.", DeEvT, Precipitation, DeP, TempMin, TempMax)).

answerWeather(de, Code, Precipitation, TempMin, TempMax, DeP, DeEvT) :-
    Code is "13", say_eou(de, format_str("%s schneit es %d Millimeter in %s und es wird zwischen %d und %d Grad kalt.", DeEvT, Precipitation, DeP, TempMin, TempMax)).

answerWeather(de, Code, Precipitation, TempMin, TempMax, DeP, DeEvT) :-
    Code is "50", say_eou(de, format_str("%s wird es neblich in %s und es wird zwischen %d und %d Grad geben.", DeEvT, DeP, TempMin, TempMax)).

weather_data(Lang, EvT, P, Code, Precipitation, TempMin, TempMax, Clouds, PLoc, EvTLoc) :-
    time_span(EvT, EvTS, EvTE),

    sparql_query (format_str(
                      "SELECT ?temp_min ?temp_max ?precipitation ?clouds ?icon
                       WHERE {
                           ?wev hal:dt_end ?dt_end. 
                           ?wev hal:dt_start ?dt_start.
                           ?wev hal:location %s.
                           ?wev hal:temp_min ?temp_min   .
                           ?wev hal:temp_max ?temp_max   .
                           ?wev hal:precipitation ?precipitation .
                           ?wev hal:clouds ?clouds .
                           ?wev hal:icon ?icon .
                           FILTER (?dt_start >= \"%s\"^^xsd:dateTime && 
                                   ?dt_end   <= \"%s\"^^xsd:dateTime)
                       }", 
                       P,
                       isoformat(EvTS, 'local'), 
                       isoformat(EvTE, 'local')
                  ), 
                  TempMin, TempMax, Precipitation, Clouds, Icon
                 ),
    time_str(Lang, EvT, EvTLoc),
    place_str(Lang, P, PLoc),
    sub_string (list_max(Icon), 0, 2, _, Code).

answer(weather, Lang, EvT, P) :-
    weather_data(Lang, EvT, P, Code, Precipitation, TempMin, TempMax, Clouds, PLoc, EvTLoc),
    answerWeather(Lang, Code, list_sum(Precipitation), list_min(TempMin), list_max(TempMax), PLoc, EvTLoc).

answer(weatherPrecCloud, Lang, EvT, P) :-
    weather_data(Lang, EvT, P, Code, Precipitation, TempMin, TempMax, Clouds, PLoc, EvTLoc),
    answerWeatherPrecCloud(Lang, list_sum(Precipitation), list_avg(Clouds), EvTLoc, PLoc).

answerWeatherPrecCloud(de, PREC, CLDS, DeEvT, DeP) :-
    PREC < 0.5,
    CLDS < 50,
    say_eou(de, format_str("%s scheint in %s überwiegend die Sonne und es wird kaum Niederschlag geben.", DeEvT, DeP)).

answerWeatherPrecCloud(de, PREC, CLDS, DeEvT, DeP) :-
    PREC >= 0.5,
    CLDS < 50,
    say_eou(de, format_str("%s scheint in %s oft die Sonne, aber es gibt auch %d Millimeter Niederschlag.", DeEvT, DeP, PREC)).

answerWeatherPrecCloud(de, PREC, CLDS, DeEvT, DeP) :-
    PREC < 0.5,
    CLDS >= 50,
    say_eou(de, format_str("%s ist es in %s überwiegend bewölkt, aber es gibt wenig Niederschlag.", DeEvT, DeP)).

answerWeatherPrecCloud(de, PREC, CLDS, DeEvT, DeP) :-
    PREC >= 0.5,
    CLDS >= 50,
    say_eou(de, format_str("%s ist es in %s überwiegend bewölkt, und es gibt %d Millimeter Niederschlag.", DeEvT, DeP, PREC)).

%
% nlp processing (german)
%

nlp_macro('TIMESPEC',  map(w('')            , p('near_future(weather, EvT)')),
                       map(w('heute')       , p('EvT is today')), 
                       map(w('morgen')      , p('EvT is tomorrow')), 
                       map(w('übermorgen')  , p('EvT is dayAfterTomorrow'))).

nlp_macro('HELLO',     map(w(''          )),
                       map(w('Computer, ')),
                       map(w('HAL, '     )),
                       map(w('Hi, '      )),
                       map(w('Hallo, '   ))).

% all places we mirror from dbpedia, for now
nlp_macro('PLACE',     map(w('')                 , p('context(place, P)')),
                       map(w('in Stuttgart')     , p('P is "dbr:Stuttgart"')),
                       map(w('in Freudental')    , p('P is "dbr:Freudental"')),
                       map(w('in Tallinn')       , p('P is "dbr:Tallinn"')),
                       map(w('in San Francisco') , p('P is "dbr:San_Francisco"')),
                       map(w('in Los Angeles')   , p('P is "dbr:Los_Angeles"')),
                       map(w('in New York')      , p('P is "dbr:New_York_City"')),
                       map(w('in London')        , p('P is "dbr:London"')),
                       map(w('in Paris')         , p('P is "dbr:Paris"')),
                       map(w('in Reykjavík')     , p('P is "dbr:Reykjavík"')),
                       map(w('in Oberwiesenthal'), p('P is "dbr:Oberwiesenthal"')),
                       map(w('in Arnstorf')      , p('P is "dbr:Arnstorf"')),
                       map(w('in Hamburg')       , p('P is "dbr:Hamburg"')),
                       map(w('in Washington')    , p('P is "<http://dbpedia.org/resource/Washington,_D.C.>"')),
                       map(w('in Alaska')        , p('P is "<http://dbpedia.org/resource/Fairbanks,_Alaska>"')),
                       map(w('in Brackenheim')   , p('P is "dbr:Brackenheim"')),
                       map(w('in Heilbronn')     , p('P is "dbr:Heilbronn"')),
                       map(w('in Biberach')      , p('P is "dbr:Biberach_an_der_Riss"'))).

nlp_macro('TIMESPECF', map(w('')               , p('context(time, T); near_future(weather, T, EvTS, EvTE)')),
                       map(w('für heute')      , p('EvT is today')),
                       map(w('für morgen')     , p('EvT is tomorrow')),
                       map(w('für übermorgen') , p('EvT is dayAfterTomorrow'))).

nlp_macro('PLACEF',    map(w('')                  , p('context(place, P)')),
                       map(w('für Stuttgart')     , p('P is "dbr:Stuttgart"')),
                       map(w('für Freudental')    , p('P is "dbr:Freudental"')),
                       map(w('für Tallinn')       , p('P is "dbr:Tallinn"')),
                       map(w('für San Francisco') , p('P is "dbr:San_Francisco"')),
                       map(w('für Los Angeles')   , p('P is "dbr:Los_Angeles"')),
                       map(w('für New York')      , p('P is "dbr:New_York_City"')),
                       map(w('für London')        , p('P is "dbr:London"')),
                       map(w('für Paris')         , p('P is "dbr:Paris"')),
                       map(w('für Reykjavík')     , p('P is "dbr:Reykjavík"')),
                       map(w('für Oberwiesenthal'), p('P is "dbr:Oberwiesenthal"')),
                       map(w('für Arnstorf')      , p('P is "dbr:Arnstorf"')),
                       map(w('für Hamburg')       , p('P is "dbr:Hamburg"')),
                       map(w('für Washington')    , p('P is "<http://dbpedia.org/resource/Washington,_D.C.>"')),
                       map(w('für Alaska')        , p('P is "<http://dbpedia.org/resource/Fairbanks,_Alaska>"')),
                       map(w('für Brackenheim')   , p('P is "dbr:Brackenheim"')),
                       map(w('für Heilbronn')     , p('P is "dbr:Heilbronn"')),
                       map(w('für Biberach')      , p('P is "dbr:Biberach_an_der_Riss"'))).

nlp_gen(de,
        '@HELLO:w wird es @TIMESPEC:w @PLACE:w regnen?',
        @TIMESPEC:p, @PLACE:p, answer (weatherPrecCloud, de, EvT, P), set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hi, wird es morgen in Freudental regnen?'),
             out('morgen ist es in Freudental überwiegend bewölkt, aber es gibt wenig Niederschlag.'))).

nlp_gen(de,
        '@HELLO:w wird es @TIMESPEC:w @PLACE:w Regen geben?', 
        @TIMESPEC:p, @PLACE:p, answer (weatherPrecCloud, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Computer, wird es heute in Tallinn regnen?'),
             out('heute scheint in tallinn überwiegend die sonne und es wird kaum niederschlag geben.'))).

nlp_gen(de,
        '@HELLO:w wie groß ist die Wahrscheinlichkeit für Regen @TIMESPEC:w @PLACE:w ?', 
        @TIMESPEC:p, @PLACE:p, answer (weatherPrecCloud, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('wie groß ist die Wahrscheinlichkeit für Regen übermorgen in San Francisco?'),
             out('übermorgen ist es in san francisco überwiegend bewölkt und es gibt sieben millimeter niederschlag'))).

nlp_gen(de,
        '@HELLO:w wie wahrscheinlich ist es, dass es @TIMESPEC:w @PLACE:w regnen wird?', 
        @TIMESPEC:p, @PLACE:p, answer (weatherPrecCloud, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('HAL, wie wahrscheinlich ist es, dass es heute in Los Angeles regnen wird?'),
             out('heute scheint in los angeles überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(de,
        '@HELLO:w wie wird @TIMESPEC:w @PLACE:w das Wetter?', 
        @TIMESPEC:p, @PLACE:p, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hi, wie wird morgen in New York das Wetter?'),
             out('morgen regnet es 10 millimeter in new york und es wird zwischen fünf und sechs grad warm'))).

nlp_gen(de,
        '@HELLO:w scheint @TIMESPEC:w @PLACE:w die Sonne?', 
        @TIMESPEC:p, @PLACE:p, answer (weatherPrecCloud, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hallo, scheint übermorgen in London die Sonne?'),
             out('übermorgen ist es in london überwiegend bewölkt und es gibt 0 millimeter niederschlag'))).

nlp_gen(de,
        '@HELLO:w regnet es @TIMESPEC:w @PLACE:w ?', 
        @TIMESPEC:p, @PLACE:p, answer (weatherPrecCloud, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Regnet es in Paris?'),
             out('heute scheint in paris überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(de,
        '@HELLO:w kommt @TIMESPEC:w noch Regen @PLACE:w ?', 
        @TIMESPEC:p, @PLACE:p, answer (weatherPrecCloud, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Computer, kommt morgen noch Regen in Reykjavík?'),
             out('morgen ist es in reykjavík überwiegend bewölkt und es gibt 15 millimeter niederschlag'))).

nlp_gen(de,
        '@HELLO:w wie warm wird es @TIMESPEC:w @PLACE:w ?', 
        @TIMESPEC:p, @PLACE:p, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('HAL, wie warm wird es übermorgen in Oberwiesenthal?'),
             out('übermorgen zeigt sich ab und an die sonne in oberwiesenthal und es wird zwischen -11 und 0 grad warm'))).

nlp_gen(de,
        '@HELLO:w wie warm wird es @TIMESPEC:w @PLACE:w werden ?', 
        @TIMESPEC:p, @PLACE:p, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hi, wie warm wird es in Arnstorf werden?'),
             out('heute zeigt sich ab und an die sonne in arnstorf und es wird zwischen -8 und -2 grad warm'))).

nlp_gen(de,
        '@HELLO:w wie wird das Wetter @TIMESPEC:w @PLACE:w ?', 
        @TIMESPEC:p, @PLACE:p, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hallo, wie wird das Wetter heute in Hamburg?'),
             out('heute regnet es null millimeter in hamburg und es wird zwischen minus zwei und null grad warm'))).

nlp_gen(de,
        '@HELLO:w wie wird das Wetter @PLACE:w @TIMESPEC:w ?', 
        @TIMESPEC:p, @PLACE:p, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('wie wird das Wetter in Washington morgen?'),
             out('morgen regnet es vier millimeter in washington und es wird zwischen fünf und sieben grad warm'))).

nlp_gen(de,
        '@HELLO:w wie kalt wird es @TIMESPEC:w @PLACE:w ?', 
        @TIMESPEC:p, @PLACE:p, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Computer, wie kalt wird es übermorgen in Alaska?'),
             out('übermorgen wird es der himmel klar sein in alaska und es wird zwischen -36 und -34 grad warm'))).

nlp_gen(de,
        '@HELLO:w wie kalt wird es @TIMESPEC:w @PLACE:w werden ?', 
        @TIMESPEC:p, @PLACE:p, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('HAL, wie kalt wird es in Brackenheim?'),
             out('heute wird es wenige wolken geben in brackenheim und es wird zwischen -7 und 2 grad warm'))).

nlp_gen(de,
        '@HELLO:w was sagt der Wetterbericht @TIMESPECF:w @PLACEF:w ?', 
        @TIMESPECF:p, @PLACEF:p, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hi, was sagt der Wetterbericht für heute für Heilbronn?'),
             out('heute wird es wenige wolken geben in heilbronn und es wird zwischen minus sieben und zwei grad warm'))).

nlp_gen(de,
        '@HELLO:w was sagt die Wettervorhersage @TIMESPECF:w @PLACEF:w ?', 
        @TIMESPECF:p, @PLACEF:p, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hallo, was sagt die Wettervorhersage für morgen für Biberach?'),
             out('morgen wird es lockere wolken geben in biberach und es wird zwischen -8 und 1 grad warm'))).

nlp_gen(de, 
        '@HELLO:w wie sind die Wetteraussichten @TIMESPECF:w @PLACEF:w ?', 
        @TIMESPECF:p, @PLACEF:p, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Wie sind die Wetteraussichten für übermorgen?'),
             out('übermorgen zeigt sich ab und an die sonne in stuttgart und es wird zwischen -9 und 1 grad warm'))).

% multiple iteraction steps
% FIXME: many more examples needed

nlp_gen(de,
        '@HELLO:w wie wird das Wetter @PLACE:w ?', 
        near_future(weather, EvT), @PLACE:p, answer (weather, de, EvT, P), set_context(place, P), set_context(time, EvT), nnr,
        'und in den nächsten Tagen?',
        EvT is nextThreeDays, context(place, P), answer (weather, de, EvT, P), set_context(time, EvT), nnr,
        'und in Freudental?',
        context(time, EvT), P is "dbr:Freudental", answer (weather, de, EvT, P), set_context(playe, P) 
        ).

%
% tests (german)
%

nlp_test(de,
         ivr(in('computer, wie wird das wetter?'),
             out('heute wird es wenige Wolken geben in Stuttgart und es wird zwischen -7 und 3 Grad warm.')),
         ivr(in('und in den nächsten Tagen?'),
             out('in den nächsten drei Tagen zeigt sich ab und an die Sonne in Stuttgart und es wird zwischen -9 und 3 Grad warm.')),
         ivr(in('und in Freudental?'),
             out('in den nächsten drei Tagen zeigt sich ab und an die Sonne in Freudental und es wird zwischen -7 und 5 Grad warm.'))). 


% FIXME: sunset time missing in DB
% Wann geht die Sonne unter?

