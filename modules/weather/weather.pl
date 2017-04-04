% prolog

%
% init / defaults
%

init ('weather') :-
    % by default, give weather forecast for location of self
    rdf (aiu:self, wdpd:P131, PLACE),
    context_set (weatherPlace, PLACE),

    % by default, give weather forecast for the near future
    context_set (weatherTime, weatherNearFuture),
    eoa.


%
% test setup and context
%

test_setup('weather') :-

    % these are the same defaults as in init above, but
    % the point here is to reset the 'test' user back to defaults
    % before each test is run (so tests will independently from 
    % each other always start with the same context)

    % by default, give weather forecast for location of self
    rdf (aiu:self, wdpd:P131, PLACE),
    context_set (weatherPlace, PLACE),

    % by default, give weather forecast for the near future
    context_set (weatherTime, weatherNearFuture),
    eoa.

%
% weather reasoning / common sense
%

time_span(weatherNearFuture, TS, TE) :-
    rdf(ai:curin, ai:currentTime, CT),
    before_evening(CT),
    time_span(today, TS, TE).

time_span(weatherNearFuture, TS, TE) :-
    rdf(ai:curin, ai:currentTime, CT),
    after_evening(CT),
    time_span(tomorrow, TS, TE).

time_str(en, weatherNearFuture, "today") :- 
    rdf(ai:curin, ai:currentTime, CT),
    before_evening(CT).
time_str(de, weatherNearFuture, "heute") :- 
    rdf(ai:curin, ai:currentTime, CT),
    before_evening(CT).

time_str(en, weatherNearFuture, "tomorrow") :- 
    rdf(ai:curin, ai:currentTime, CT),
    after_evening(CT).
time_str(de, weatherNearFuture, "morgen") :- 
    rdf(ai:curin, ai:currentTime, CT),
    after_evening(CT).

%
% weather answers 
%

weatherStr(en, "01", Precipitation, TempMin, TempMax, EnP, EnEvT, S) :- 
    S is format_str("%s will be clear skies in %s with temperatures between %d and %d degrees.", EnEvT, EnP, TempMin, TempMax).
weatherStr(en, "02", Precipitation, TempMin, TempMax, EnP, EnEvT, S) :- 
    S is format_str("%s will be mostly clear skies in %s with temperatures between %d and %d degrees.", EnEvT, EnP, TempMin, TempMax).
weatherStr(en, "03", Precipitation, TempMin, TempMax, EnP, EnEvT, S) :- 
    S is format_str("%s there will be some clouds in %s with temperatures between %d and %d degrees.", EnEvT, EnP, TempMin, TempMax).
weatherStr(en, "04", Precipitation, TempMin, TempMax, EnP, EnEvT, S) :- 
    S is format_str("%s the sun will show up occasionally in %s with temperatures between %d and %d degrees.", EnEvT, EnP, TempMin, TempMax).
weatherStr(en, "09", Precipitation, TempMin, TempMax, EnP, EnEvT, S) :- 
    S is format_str("%s there will be rain showers of %d millimeters in %s with temperatures between %d and %d degrees.", EnEvT, Precipitation, EnP, TempMin, TempMax).
weatherStr(en, "10", Precipitation, TempMin, TempMax, EnP, EnEvT, S) :- 
    Precipitation >= 1.0,
    S is format_str("%s it will rain %d millimeters in %s with temperatures between %d and %d degrees.", EnEvT, Precipitation, EnP, TempMin, TempMax).
weatherStr(en, "10", Precipitation, TempMin, TempMax, EnP, EnEvT, S) :- 
    Precipitation < 1.0,
    S is format_str("%s there might be a little rain in %s with temperatures between %d and %d degrees.", EnEvT, EnP, TempMin, TempMax).
weatherStr(en, "11", Precipitation, TempMin, TempMax, EnP, EnEvT, S) :- 
    S is format_str("%s we will have thunderstorms and %d millimeters of rain in %s with temperatures between %d and %d degrees.", EnEvT, Precipitation, EnP, TempMin, TempMax).
weatherStr(en, "13", Precipitation, TempMin, TempMax, EnP, EnEvT, S) :- 
    S is format_str("%s it will snow %d millimeters in %s with temperatures between %d and %d degrees.", EnEvT, Precipitation, EnP, TempMin, TempMax).
weatherStr(en, "50", Precipitation, TempMin, TempMax, EnP, EnEvT, S) :- 
    S is format_str("%s it will be foggy in %s with temperatures between %d and %d degrees", EnEvT, EnP, TempMin, TempMax).

weatherStr(de, "01", Precipitation, TempMin, TempMax, DeP, DeEvT, S) :- 
    S is format_str("%s wird der Himmel klar sein in %s und es wird zwischen %d und %d Grad warm.", DeEvT, DeP, TempMin, TempMax).
weatherStr(de, "02", Precipitation, TempMin, TempMax, DeP, DeEvT, S) :- 
    S is format_str("%s wird es wenige Wolken geben in %s und es wird zwischen %d und %d Grad warm.", DeEvT, DeP, TempMin, TempMax).
weatherStr(de, "03", Precipitation, TempMin, TempMax, DeP, DeEvT, S) :- 
    S is format_str("%s wird es lockere Wolken geben in %s und es wird zwischen %d und %d Grad warm.", DeEvT, DeP, TempMin, TempMax).
weatherStr(de, "04", Precipitation, TempMin, TempMax, DeP, DeEvT, S) :- 
    S is format_str("%s zeigt sich ab und an die Sonne in %s und es wird zwischen %d und %d Grad warm.", DeEvT, DeP, TempMin, TempMax).
weatherStr(de, "09", Precipitation, TempMin, TempMax, DeP, DeEvT, S) :- 
    S is format_str("%s wird es %d Millimeter Schauer geben in %s und es wird zwischen %d und %d Grad warm.", DeEvT, Precipitation, DeP, TempMin, TempMax).
weatherStr(de, "10", Precipitation, TempMin, TempMax, DeP, DeEvT, S) :- 
    Precipitation >= 1.0,
    S is format_str("%s regnet es %d Millimeter in %s und es wird zwischen %d und %d Grad warm.", DeEvT, Precipitation, DeP, TempMin, TempMax).
weatherStr(de, "10", Precipitation, TempMin, TempMax, DeP, DeEvT, S) :- 
    Precipitation < 1.0,
    S is format_str("%s kann es etwas Niederschlag geben in %s und es wird zwischen %d und %d Grad warm.", DeEvT, DeP, TempMin, TempMax).
weatherStr(de, "11", Precipitation, TempMin, TempMax, DeP, DeEvT, S) :- 
    S is format_str("%s wird es Gewitter geben mit %d Millimeter Niederschlag in %s und es wird zwischen %d und %d Grad warm.", DeEvT, Precipitation, DeP, TempMin, TempMax).
weatherStr(de, "13", Precipitation, TempMin, TempMax, DeP, DeEvT, S) :- 
    S is format_str("%s schneit es %d Millimeter in %s und es wird zwischen %d und %d Grad kalt.", DeEvT, Precipitation, DeP, TempMin, TempMax).
weatherStr(de, "50", Precipitation, TempMin, TempMax, DeP, DeEvT, S) :- 
    S is format_str("%s wird es neblich in %s und es wird zwischen %d und %d Grad geben.", DeEvT, DeP, TempMin, TempMax).

weather_data(Lang, EvT, P, Code, Precipitation, TempMin, TempMax, Clouds, PLoc, EvTLoc) :-
    time_span(EvT, EvTS, EvTE),
    atom_chars(Lang, L2),

    rdf_lists(distinct,
              WEV, ai:dt_end,        DT_END,
              WEV, ai:dt_start,      DT_START,
              WEV, ai:location,      P,
              P,   rdfs:label,        Label,
              WEV, ai:temp_min,      TempMin,
              WEV, ai:temp_max,      TempMax,
              WEV, ai:precipitation, Precipitation,
              WEV, ai:clouds,        Clouds,
              WEV, ai:icon,          Icon,
              filter (DT_START >= isoformat(EvTS, 'local'),
                      DT_END   =< isoformat(EvTE, 'local'),
                      lang(Label) = L2)
             ),

    list_nth(0, Label, PLoc),
    time_str(Lang, EvT, EvTLoc),
    sub_string (list_max(Icon), 0, 2, _, Code).

answer(weather, Lang, EvT, P, SCORE) :-
    weather_data(Lang, EvT, P, Code, Precipitation, TempMin, TempMax, Clouds, PLoc, EvTLoc),
    weatherStr(Lang, Code, list_sum(Precipitation), list_min(TempMin), list_max(TempMax), PLoc, EvTLoc, STR),
    context_push(topic, weather),
    context_set(weatherPlace, P), context_set(weatherTime, EvT),
    say_eoa(Lang, STR, SCORE).

answer(weather, Lang, EvT, P) :-
    answer(weather, Lang, EvT, P, 100).

answer(weatherPrecCloud, Lang, EvT, P) :-
    weather_data(Lang, EvT, P, Code, Precipitation, TempMin, TempMax, Clouds, PLoc, EvTLoc),
    answerWeatherPrecCloud(Lang, list_sum(Precipitation), list_avg(Clouds), EvTLoc, PLoc, P, EvT).

answerWeatherPrecCloud(en, PREC, CLDS, DeEvT, DeP, P, EvT) :-
    PREC < 0.5,
    CLDS < 50,
    context_push(topic, weather),
    context_set(weatherPlace, P), context_set(weatherTime, EvT),
    say_eoa(en, format_str("%s it will be mostly sunny in %s with little precipitation.", DeEvT, DeP)).
answerWeatherPrecCloud(de, PREC, CLDS, DeEvT, DeP, P, EvT) :-
    PREC < 0.5,
    CLDS < 50,
    context_push(topic, weather),
    context_set(weatherPlace, P), context_set(weatherTime, EvT),
    say_eoa(de, format_str("%s scheint in %s überwiegend die Sonne und es wird kaum Niederschlag geben.", DeEvT, DeP)).

answerWeatherPrecCloud(en, PREC, CLDS, DeEvT, DeP, P, EvT) :-
    PREC >= 0.5,
    CLDS < 50,
    context_push(topic, weather),
    context_set(weatherPlace, P), context_set(weatherTime, EvT),
    say_eoa(en, format_str("%s the sun will shine quite often in %s but there might be some precipitation of %d millimeters.", DeEvT, DeP, PREC)).
answerWeatherPrecCloud(de, PREC, CLDS, DeEvT, DeP, P, EvT) :-
    PREC >= 0.5,
    CLDS < 50,
    context_push(topic, weather),
    context_set(weatherPlace, P), context_set(weatherTime, EvT),
    say_eoa(de, format_str("%s scheint in %s oft die Sonne, aber es gibt auch %d Millimeter Niederschlag.", DeEvT, DeP, PREC)).

answerWeatherPrecCloud(en, PREC, CLDS, DeEvT, DeP, P, EvT) :-
    PREC < 0.5,
    CLDS >= 50,
    context_push(topic, weather),
    context_set(weatherPlace, P), context_set(weatherTime, EvT),
    say_eoa(en, format_str("%s it will be mostly cloudy in %s with little precipitation.", DeEvT, DeP)).
answerWeatherPrecCloud(de, PREC, CLDS, DeEvT, DeP, P, EvT) :-
    PREC < 0.5,
    CLDS >= 50,
    context_push(topic, weather),
    context_set(weatherPlace, P), context_set(weatherTime, EvT),
    say_eoa(de, format_str("%s ist es in %s überwiegend bewölkt, aber es gibt wenig Niederschlag.", DeEvT, DeP)).

answerWeatherPrecCloud(en, PREC, CLDS, DeEvT, DeP, P, EvT) :-
    PREC >= 0.5,
    CLDS >= 50,
    context_push(topic, weather),
    context_set(weatherPlace, P), context_set(weatherTime, EvT),
    say_eoa(en, format_str("%s it will be mostly cloudy in %s with %d millimeters of precipitation.", DeEvT, DeP, PREC)).
answerWeatherPrecCloud(de, PREC, CLDS, DeEvT, DeP, P, EvT) :-
    PREC >= 0.5,
    CLDS >= 50,
    context_push(topic, weather),
    context_set(weatherPlace, P), context_set(weatherTime, EvT),
    say_eoa(de, format_str("%s ist es in %s überwiegend bewölkt, und es gibt %d Millimeter Niederschlag.", DeEvT, DeP, PREC)).

%
% nlp processing (english/german)
%

nlp_macro('TIMESPEC_EN', W, P) :- W is ''                           , P is 'context_get(weatherTime, EvT)'.
nlp_macro('TIMESPEC_EN', W, P) :- W is 'today'                      , P is 'EvT is today'.
nlp_macro('TIMESPEC_EN', W, P) :- W is 'tomorrow'                   , P is 'EvT is tomorrow'.
nlp_macro('TIMESPEC_EN', W, P) :- W is 'the day after tomorrow'     , P is 'EvT is dayAfterTomorrow'.
nlp_macro('TIMESPEC_EN', W, P) :- W is 'in the next three days'     , P is 'EvT is nextThreeDays'.

nlp_macro('TIMESPEC_DE', W, P) :- W is ''                           , P is 'context_get(weatherTime, EvT)'.
nlp_macro('TIMESPEC_DE', W, P) :- W is 'heute'                      , P is 'EvT is today'.
nlp_macro('TIMESPEC_DE', W, P) :- W is 'morgen'                     , P is 'EvT is tomorrow'.
nlp_macro('TIMESPEC_DE', W, P) :- W is 'übermorgen'                 , P is 'EvT is dayAfterTomorrow'.
nlp_macro('TIMESPEC_DE', W, P) :- W is 'in den nächsten Tagen'      , P is 'EvT is nextThreeDays'.

nlp_macro('TIMESPECF_EN', W, P) :- W is ''                          , P is 'context_get(weatherTime, EvT)'.
nlp_macro('TIMESPECF_EN', W, P) :- W is 'for today'                 , P is 'EvT is today'.
nlp_macro('TIMESPECF_EN', W, P) :- W is 'for tomorrow'              , P is 'EvT is tomorrow'.
nlp_macro('TIMESPECF_EN', W, P) :- W is 'for the day after tomorrow', P is 'EvT is dayAfterTomorrow'.
nlp_macro('TIMESPECF_EN', W, P) :- W is 'for the next three days'   , P is 'EvT is nextThreeDays'.

nlp_macro('TIMESPECF_DE', W, P) :- W is ''                          , P is 'context_get(weatherTime, EvT)'.
nlp_macro('TIMESPECF_DE', W, P) :- W is 'für heute'                 , P is 'EvT is today'.
nlp_macro('TIMESPECF_DE', W, P) :- W is 'für morgen'                , P is 'EvT is tomorrow'.
nlp_macro('TIMESPECF_DE', W, P) :- W is 'für übermorgen'            , P is 'EvT is dayAfterTomorrow'.
nlp_macro('TIMESPECF_DE', W, P) :- W is 'für die nächsten Tage'     , P is 'EvT is nextThreeDays'.

% N: non empty

nlp_macro('TIMESPECN_EN', W, P) :- W is 'today'                      , P is 'EvT is today'.
nlp_macro('TIMESPECN_EN', W, P) :- W is 'tomorrow'                   , P is 'EvT is tomorrow'.
nlp_macro('TIMESPECN_EN', W, P) :- W is 'the day after tomorrow'     , P is 'EvT is dayAfterTomorrow'.
nlp_macro('TIMESPECN_EN', W, P) :- W is 'in the next three days'     , P is 'EvT is nextThreeDays'.

nlp_macro('TIMESPECN_DE', W, P) :- W is 'heute'                      , P is 'EvT is today'.
nlp_macro('TIMESPECN_DE', W, P) :- W is 'morgen'                     , P is 'EvT is tomorrow'.
nlp_macro('TIMESPECN_DE', W, P) :- W is 'übermorgen'                 , P is 'EvT is dayAfterTomorrow'.
nlp_macro('TIMESPECN_DE', W, P) :- W is 'in den nächsten Tagen'      , P is 'EvT is nextThreeDays'.

nlp_macro('TIMESPECNF_EN', W, P) :- W is 'for today'                 , P is 'EvT is today'.
nlp_macro('TIMESPECNF_EN', W, P) :- W is 'for tomorrow'              , P is 'EvT is tomorrow'.
nlp_macro('TIMESPECNF_EN', W, P) :- W is 'for the day after tomorrow', P is 'EvT is dayAfterTomorrow'.
nlp_macro('TIMESPECNF_EN', W, P) :- W is 'for the next three days'   , P is 'EvT is nextThreeDays'.

nlp_macro('TIMESPECNF_DE', W, P) :- W is 'für heute'                 , P is 'EvT is today'.
nlp_macro('TIMESPECNF_DE', W, P) :- W is 'für morgen'                , P is 'EvT is tomorrow'.
nlp_macro('TIMESPECNF_DE', W, P) :- W is 'für übermorgen'            , P is 'EvT is dayAfterTomorrow'.
nlp_macro('TIMESPECNF_DE', W, P) :- W is 'für die nächsten Tage'     , P is 'EvT is nextThreeDays'.


% W : 'in Stuttgart'     , P: 'P is "dbr:Stuttgart"'
% W : 'in Freudental'    , P: 'P is "dbr:Freudental"'
nlp_macro('PLACE_EN', W, P) :- W is '', P is 'context_get(weatherPlace, P)'.
nlp_macro('PLACE_EN', W, P) :- 
    rdf (distinct,
         LOCATION, ai:cityid, CITYID,
         LOCATION, rdfs:label, LABEL,
         filter(lang(LABEL) = 'en')),
    W is format_str('in %s', LABEL),
    P is format_str('P is "%s"', LOCATION).

% W : 'in Stuttgart'     , P: 'P is "dbr:Stuttgart"'
% W : 'in Freudental'    , P: 'P is "dbr:Freudental"'
nlp_macro('PLACE_DE', W, P) :- W is '', P is 'context_get(weatherPlace, P)'.
nlp_macro('PLACE_DE', W, P) :- 
    rdf (distinct,
         LOCATION, ai:cityid, CITYID,
         LOCATION, rdfs:label, LABEL,
         filter(lang(LABEL) = 'de')),
    W is format_str('in %s', LABEL),
    P is format_str('P is "%s"', LOCATION).

% W : 'for Stuttgart'     , P: 'P is "dbr:Stuttgart"'
% W : 'for Freudental'    , P: 'P is "dbr:Freudental"'
nlp_macro('PLACEF_EN', W, P) :- W is '', P is 'context_get(weatherPlace, P)'.
nlp_macro('PLACEF_EN', W, P) :- 
    rdf (distinct,
         LOCATION, ai:cityid, CITYID,
         LOCATION, rdfs:label, LABEL,
         filter(lang(LABEL) = 'en')),
    W is format_str('for %s', LABEL),
    P is format_str('P is "%s"', LOCATION).

% W : 'für Stuttgart'     , P: 'P is "dbr:Stuttgart"'
% W : 'für Freudental'    , P: 'P is "dbr:Freudental"'
nlp_macro('PLACEF_DE', W, P) :- W is '', P is 'context_get(weatherPlace, P)'.
nlp_macro('PLACEF_DE', W, P) :- 
    rdf (distinct,
         LOCATION, ai:cityid, CITYID,
         LOCATION, rdfs:label, LABEL,
         filter(lang(LABEL) = 'de')),
    W is format_str('für %s', LABEL),
    P is format_str('P is "%s"', LOCATION).

nlp_macro('PLACEN_EN', W, P) :- 
    rdf (distinct,
         LOCATION, ai:cityid, CITYID,
         LOCATION, rdfs:label, LABEL,
         filter(lang(LABEL) = 'en')),
    W is format_str('in %s', LABEL),
    P is format_str('P is "%s"', LOCATION).
nlp_macro('PLACEN_DE', W, P) :- 
    rdf (distinct,
         LOCATION, ai:cityid, CITYID,
         LOCATION, rdfs:label, LABEL,
         filter(lang(LABEL) = 'de')),
    W is format_str('in %s', LABEL),
    P is format_str('P is "%s"', LOCATION).

nlp_macro('PLACENF_EN', W, P) :- 
    rdf (distinct,
         LOCATION, ai:cityid, CITYID,
         LOCATION, rdfs:label, LABEL,
         filter(lang(LABEL) = 'en')),
    W is format_str('for %s', LABEL),
    P is format_str('P is "%s"', LOCATION).
nlp_macro('PLACENF_DE', W, P) :- 
    rdf (distinct,
         LOCATION, ai:cityid, CITYID,
         LOCATION, rdfs:label, LABEL,
         filter(lang(LABEL) = 'de')),
    W is format_str('für %s', LABEL),
    P is format_str('P is "%s"', LOCATION).


nlp_gen(en,
        '@SELF_ADDRESS_EN:LABEL will it rain @TIMESPEC_EN:W @PLACE_EN:W?',
        @TIMESPEC_EN:P, @PLACE_EN:P, answer (weatherPrecCloud, en, EvT, P)).
nlp_test(en,
         ivr(in('Computer, will it rain tomorrow in Freudental?'),
             out('tomorrow it will be mostly cloudy in Freudental with little precipitation.'))).
nlp_gen(de,
        '@SELF_ADDRESS_DE:LABEL wird es @TIMESPEC_DE:W @PLACE_DE:W (regnen|Regen geben)?',
        @TIMESPEC_DE:P, @PLACE_DE:P, answer (weatherPrecCloud, de, EvT, P)).
nlp_test(de,
         ivr(in('Computer, wird es morgen in Freudental regnen?'),
             out('morgen ist es in Freudental überwiegend bewölkt, aber es gibt wenig Niederschlag.'))).

nlp_gen(en,
        '@SELF_ADDRESS_EN:LABEL (what is the likelihood of|how likely is) rain @TIMESPEC_EN:W @PLACE_EN:W ?', 
        @TIMESPEC_EN:P, @PLACE_EN:P, answer (weatherPrecCloud, en, EvT, P)).
nlp_test(en,
         ivr(in('how likely is rain the day after tomorrow in Stuttgart?'),
             out('day after tomorrow it will be mostly sunny in Stuttgart with little precipitation.'))).
nlp_gen(de,
        '@SELF_ADDRESS_DE:LABEL (was ist die Wahrscheinlichkeit für|wie groß ist die Wahrscheinlichkeit für|wie wahrscheinlich ist) Regen @TIMESPEC_DE:W @PLACE_DE:W ?', 
        @TIMESPEC_DE:P, @PLACE_DE:P, answer (weatherPrecCloud, de, EvT, P)).
nlp_test(de,
         ivr(in('wie groß ist die Wahrscheinlichkeit für Regen übermorgen in Stuttgart?'),
             out('übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS_EN:LABEL how likely is it that it will rain @TIMESPEC_EN:W @PLACE_EN:W?', 
        @TIMESPEC_EN:P, @PLACE_EN:P, answer (weatherPrecCloud, en, EvT, P)).
nlp_test(en,
         ivr(in('Computer, how likely is it that it will rain today in Freudental?'),
             out('today it will be mostly sunny in Freudental with little precipitation.'))).
nlp_gen(de,
        '@SELF_ADDRESS_DE:LABEL wie wahrscheinlich ist es, dass es @TIMESPEC_DE:W @PLACE_DE:W regnen wird?', 
        @TIMESPEC_DE:P, @PLACE_DE:P, answer (weatherPrecCloud, de, EvT, P)).
nlp_test(de,
         ivr(in('Computer, wie wahrscheinlich ist es, dass es heute in Freudental regnen wird?'),
             out('heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS_EN:LABEL what (will the weather|is the weather gonna|is the weather going to) be like @TIMESPEC_EN:W @PLACE_EN:W?', 
        @TIMESPEC_EN:P, @PLACE_EN:P, answer (weather, en, EvT, P)).
nlp_test(en,
         ivr(in('Computer, what will the weather be like tomorrow in Tallinn?'),
             out('tomorrow there might be a little rain in Tallinn with temperatures between 1 and 3 degrees.'))).
nlp_gen(de,
        '@SELF_ADDRESS_DE:LABEL wie wird @TIMESPEC_DE:W @PLACE_DE:W das Wetter?', 
        @TIMESPEC_DE:P, @PLACE_DE:P, answer (weather, de, EvT, P)).
nlp_test(de,
         ivr(in('Computer, wie wird morgen in Tallinn das Wetter?'),
             out('morgen kann es etwas Niederschlag geben in Tallinn und es wird zwischen 1 und 3 Grad warm.'))).

nlp_gen(en,
        '@SELF_ADDRESS_EN:LABEL (will the sun shine|will there be sunshine) @TIMESPEC_EN:W @PLACE_EN:W ?', 
        @TIMESPEC_EN:P, @PLACE_EN:P, answer (weatherPrecCloud, en, EvT, P)).
nlp_test(en,
         ivr(in('computer, will there be sunshine the day after tomorrow in stuttgart?'),
             out('day after tomorrow it will be mostly sunny in Stuttgart with little precipitation.'))).
nlp_gen(de,
        '@SELF_ADDRESS_DE:LABEL scheint @TIMESPEC_DE:W @PLACE_DE:W die Sonne?', 
        @TIMESPEC_DE:P, @PLACE_DE:P, answer (weatherPrecCloud, de, EvT, P)).
nlp_test(de,
         ivr(in('computer, scheint übermorgen in Stuttgart die Sonne?'),
             out('übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS_EN:LABEL (will it|does it) rain @TIMESPECN_EN:W @PLACE_EN:W ?', 
        @TIMESPECN_EN:P, @PLACE_EN:P, answer (weatherPrecCloud, en, EvT, P)).
nlp_gen(en,
        '@SELF_ADDRESS_EN:LABEL (will it|does it) rain @PLACEN_EN:W ?', 
        context_get(weatherTime, EvT), @PLACEN_EN:P, answer (weatherPrecCloud, en, EvT, P)).
nlp_test(en,
         ivr(in('Will it rain in Freudental?'),
             out('today it will be mostly sunny in Freudental with little precipitation.'))).
nlp_gen(de,
        '@SELF_ADDRESS_DE:LABEL regnet es @TIMESPECN_DE:W @PLACE_DE:W ?', 
        @TIMESPECN_DE:P, @PLACE_DE:P, answer (weatherPrecCloud, de, EvT, P)).
nlp_gen(de,
        '@SELF_ADDRESS_DE:LABEL regnet es @PLACEN_DE:W ?', 
        context_get(weatherTime, EvT), @PLACEN_DE:P, answer (weatherPrecCloud, de, EvT, P)).
nlp_test(de,
         ivr(in('Regnet es in Freudental?'),
             out('heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS_EN:LABEL (will rain come|is rain coming) @TIMESPEC_EN:W @PLACE_EN:W ?', 
        @TIMESPEC_EN:P, @PLACE_EN:P, answer (weatherPrecCloud, en, EvT, P)).
nlp_test(en,
         ivr(in('Computer, is rain coming tomorrow in Tallinn?'),
             out('tomorrow it will be mostly cloudy in Tallinn with little precipitation.'))).
nlp_gen(de,
        '@SELF_ADDRESS_DE:LABEL kommt @TIMESPEC_DE:W noch Regen @PLACE_DE:W ?', 
        @TIMESPEC_DE:P, @PLACE_DE:P, answer (weatherPrecCloud, de, EvT, P)).
nlp_test(de,
         ivr(in('Computer, kommt morgen noch Regen in Tallinn?'),
             out('morgen ist es in tallinn überwiegend bewölkt aber es gibt wenig niederschlag'))).

nlp_gen(en,
        '@SELF_ADDRESS_EN:LABEL how (cold|warm) (is it going to|will it) (be|become) @TIMESPEC_EN:W @PLACE_EN:W ?', 
        @TIMESPEC_EN:P, @PLACE_EN:P, answer (weather, en, EvT, P)).
nlp_test(en,
         ivr(in('Computer, how warm will it be the day after tomorrow in Stuttgart?'),
             out('day after tomorrow the sun will show up occasionally in Stuttgart with temperatures between -9 and 1 degrees.'))).
nlp_gen(de,
        '@SELF_ADDRESS_DE:LABEL wie (kalt|warm) wird es @TIMESPEC_DE:W @PLACE_DE:W (werden|)?', 
        @TIMESPEC_DE:P, @PLACE_DE:P, answer (weather, de, EvT, P)).
nlp_test(de,
         ivr(in('Computer, wie warm wird es übermorgen in Stuttgart?'),
             out('übermorgen zeigt sich ab und an die sonne in stuttgart und es wird zwischen minus neun und eins grad warm'))).

nlp_gen(en,
        '@SELF_ADDRESS_EN:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) @TIMESPEC_EN:W @PLACEN_EN:W ?', 
        @TIMESPEC_EN:P, @PLACEN_EN:P, answer (weather, en, EvT, P)).
nlp_gen(en,
        '@SELF_ADDRESS_EN:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) @TIMESPECN_EN:W?', 
        @TIMESPECN_EN:P, context_get(weatherPlace, P), answer (weather, en, EvT, P)).
nlp_test(en,
         ivr(in('computer, what will the weather be like today in Tallinn?'),
             out('today there will be some clouds in Tallinn with temperatures between -8 and -4 degrees.'))).
nlp_gen(de,
        '@SELF_ADDRESS_DE:LABEL wie wird das Wetter @TIMESPEC_DE:W @PLACEN_DE:W ?', 
        @TIMESPEC_DE:P, @PLACEN_DE:P, answer (weather, de, EvT, P)).
nlp_gen(de,
        '@SELF_ADDRESS_DE:LABEL wie wird das Wetter @TIMESPECN_DE:W?', 
        @TIMESPECN_DE:P, context_get(weatherPlace, P), answer (weather, de, EvT, P)).
nlp_test(de,
         ivr(in('computer, wie wird das Wetter heute in Tallinn?'),
             out('heute wird es lockere wolken geben in tallinn und es wird zwischen minus acht und minus vier grad warm'))).

nlp_gen(en,
        '@SELF_ADDRESS_EN:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|)  @PLACEN_EN:W @TIMESPECN_EN:W ?', 
        @TIMESPECN_EN:P, @PLACEN_EN:P, answer (weather, en, EvT, P)).
nlp_test(en,
         ivr(in('what is the weather gonna be like in stuttgart tomorrow?'),
             out('tomorrow will be mostly clear skies in Stuttgart with temperatures between -8 and 1 degrees.'))).
nlp_gen(de,
        '@SELF_ADDRESS_DE:LABEL wie wird das Wetter @PLACEN_DE:W @TIMESPECN_DE:W ?', 
        @TIMESPECN_DE:P, @PLACEN_DE:P, answer (weather, de, EvT, P)).
nlp_test(de,
         ivr(in('wie wird das Wetter in Stuttgart morgen?'),
             out('morgen wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und eins grad warm'))).

nlp_gen(en,
        '@SELF_ADDRESS_EN:LABEL what (is the weather outlook|does the weather forecast look like|is the weather forecast|does the weather forecast say) @TIMESPECF_EN:W @PLACEF_EN:W ?', 
        @TIMESPECF_EN:P, @PLACEF_EN:P, answer (weather, en, EvT, P)).
nlp_test(en,
         ivr(in('Computer, what does the weather forecast say for today for stuttgart?'),
             out('today will be mostly clear skies in Stuttgart with temperatures between -7 and 3 degrees.'))).
nlp_gen(de,
        '@SELF_ADDRESS_DE:LABEL (wie sind die Wetteraussichten|was sagt die Wettervorhersage|was sagt der Wetterbericht) @TIMESPECF_DE:W @PLACEF_DE:W ?', 
        @TIMESPECF_DE:P, @PLACEF_DE:P, answer (weather, de, EvT, P)).
nlp_test(de,
         ivr(in('Computer, was sagt der Wetterbericht für heute für Stuttgart?'),
             out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus sieben und drei grad warm'))).

%
% context stack topic dependant productions
%

nlp_gen(en, 
        '@SELF_ADDRESS_EN:LABEL and @TIMESPECNF_EN:W @PLACEF_EN:W ?', 
        context_score (topic, weather, 100, S), @TIMESPECNF_EN:P, @PLACEF_EN:P, answer (weather, en, EvT, P, S)).
nlp_gen(de, 
        '@SELF_ADDRESS_DE:LABEL und @TIMESPECNF_DE:W @PLACEF_DE:W ?', 
        context_score (topic, weather, 100, S), @TIMESPECNF_DE:P, @PLACEF_DE:P, answer (weather, de, EvT, P, S)).

nlp_gen(en, 
        '@SELF_ADDRESS_EN:LABEL and @PLACENF_EN:W ?', 
        context_score (topic, weather, 100, S), context_get(weatherTime, EvT), @PLACENF_EN:P, answer (weather, en, EvT, P, S)).
nlp_gen(de, 
        '@SELF_ADDRESS_DE:LABEL und @PLACENF_DE:W ?', 
        context_score (topic, weather, 100, S), context_get(weatherTime, EvT), @PLACENF_DE:P, answer (weather, de, EvT, P, S)).

nlp_gen(en, 
        '@SELF_ADDRESS_EN:LABEL and @TIMESPEC_EN:W @PLACEN_EN:W ?', 
        context_score (topic, weather, 100, S), @TIMESPEC_EN:P, @PLACEN_EN:P, answer (weather, en, EvT, P, S)).
nlp_gen(de, 
        '@SELF_ADDRESS_DE:LABEL und @TIMESPEC_DE:W @PLACEN_DE:W ?', 
        context_score (topic, weather, 100, S), @TIMESPEC_DE:P, @PLACEN_DE:P, answer (weather, de, EvT, P, S)).

nlp_gen(en, 
        '@SELF_ADDRESS_EN:LABEL and @TIMESPECN_EN:W ?', 
        context_score (topic, weather, 100, S), @TIMESPECN_EN:P, context_get(weatherPlace, P), answer (weather, en, EvT, P, S)).
nlp_gen(de, 
        '@SELF_ADDRESS_DE:LABEL und @TIMESPECN_DE:W ?', 
        context_score (topic, weather, 100, S), @TIMESPECN_DE:P, context_get(weatherPlace, P), answer (weather, de, EvT, P, S)).


%
% test multiple iteraction steps
%
% FIXME: many more examples needed
%

nlp_test(en,
         ivr(in('computer, what is the weather going to be like?'),
             out('today will be mostly clear skies in Stuttgart with temperatures between -7 and 3 degrees.')),
         ivr(in('and in the next three days?'),
             out('in the next three days the sun will show up occasionally in Stuttgart with temperatures between -9 and 3 degrees.')),
         ivr(in('and in Freudental?'),
             out('in the next three days the sun will show up occasionally in Freudental with temperatures between -7 and 5 degrees.'))). 
nlp_test(de,
         ivr(in('computer, wie wird das wetter?'),
             out('heute wird es wenige Wolken geben in Stuttgart und es wird zwischen -7 und 3 Grad warm.')),
         ivr(in('und in den nächsten Tagen?'),
             out('in den nächsten drei Tagen zeigt sich ab und an die Sonne in Stuttgart und es wird zwischen -9 und 3 Grad warm.')),
         ivr(in('und in Freudental?'),
             out('in den nächsten drei Tagen zeigt sich ab und an die Sonne in Freudental und es wird zwischen -7 und 5 Grad warm.'))). 


% FIXME: implement
% Wann geht die Sonne unter?

%
% weather
%

% rain(E) :- rainProb(E, Prob), Prob >= 50 .

% time(e1,tomorrowAfternoon).
% place(e1,stuttgart).
% rainProb(e1,90).

%  % Wird es morgen regnen?
%  % ?- rain(X,TimeSpan,Place),future(TimeSpan),tomorrow(TimeSpan).
%  question(Prob, I), rain_intensity (E, I), rain_prob(E, Prob), time(E,EvT), tomorrow(EvT), place(E, P), context_get(P)
%  
%  % @nlp_de Wird es morgen regnen?
%  % @nlp_en Will it rain tomorrow?
%   
%  ?- rain(E),time(E,EvT),context_get(P),place(P),place(E,P),context_get(R),tomorrow(R,EvT).


% wird es regnen
% exists(A,and(rain(it,B),some(C,and(and(time(A),at(C,A)),fut1(A,now)))))
% ?- rain(X,Time,Place),future(Time).

% ( 3) Wird es morgen in Freudental regnen?
% ?- rain(X,Time,freudental),future(Time),tomorrow(Time).

% ( 4) Wird es Regen geben?
% ?- rain(X,Time,Place),future(Time).

% ( 5) Wie gross ist die Wahrscheinlichkeit fuer Regen?
% ?- rainProb(Time,Place,Prob).

% ( 6) Wie wahrscheinlich ist es, dass es regnen wird?
% ?- rainProb(Time,Place,Prob).

% ( 7) Wie wird das Wetter?

% question(Report), report(E, Report), time(E,Evt), near_future(EvT), place(E, P), context_get(P), topic(Report, weather)

% ( 8) Scheint morgen die Sonne?

% yesnoprob(E), sunshine_prob(E), time(E,EvT), tomorrow(EvT), place(E, P), context_get(P)

% ( 9) Regnet es?

% yesnoprob(E), rain_prob(E), time(E,EvT), now(EvT), place(E, P), context_get(P)

% (10) Wie wird das Wetter morgen?

% question(Report), report(E, Report), time(E,Evt), tomorrow(EvT), place(E, P), context_get(P), topic(Report, weather)

% (11) Und in den kommenden Tagen?

% question(Report), report(E, Report), time(E,Evt), next_days(EvT), place(E, P), context_get(P), topic(Report, weather)

% (12) Wie wird es naechste Woche werden?

% question(Report), report(E, Report), time(E,Evt), next_week(EvT), place(E, P), context_get(P), topic(Report, T), context_get(T)

% (13) Kommt heute noch Regen?

% yesnoprob(E), rain_prob(E), time(E,EvT), today(EvT), future(EvT), place(E, P), context_get(P)

% (14) Wie warm wird es heute?

% question(MaxTemp), max_temp(E, MaxTemp), time(E,EvT), today(EvT), place(E, P), context_get(P)

% (15) Wie wird das Wetter heute?

% question(Report), report(E, Report), time(E,Evt), today(EvT), place(E, P), context_get(P), topic(Report, weather)

% (16) Wie kalt wird es werden?

% question(MinTemp), min_temp(E, MinTemp), time(E,EvT), context_get(EvT), place(E, P), context_get(P)

% (17) Was sagt der Wetterbericht?

% question(Report), report(E, Report), time(E,Evt), context_get(EvT), place(E, P), context_get(P), topic(Report, weather)

% (18) Was sagt die Wettervorhersage?

% question(Report), report(E, Report), time(E,Evt), context_get(EvT), place(E, P), context_get(P), topic(Report, weather)

% (19) Wann geht die Sonne unter?

% question(SunsetTime), sunset_time(E, SunsetTime), time(E,EvT), context_get(EvT), place(E, P), context_get(P)

% (20) Wie sind die Wetteraussichten?

% question(Report), report(E, Report), time(E,Evt), context_get(EvT), place(E, P), context_get(P), topic(Report, weather)

% (21) Wie sind die Wetteraussichten fuer die naechsten Tage?

% question(Report), report(E, Report), time(E,Evt), next_days(EvT), place(E, P), context_get(P), topic(Report, weather)

