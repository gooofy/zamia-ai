% prolog

%
% test setup and context
%

% test_setup('weather') :-
% 
%     % these are the same defaults as in init above, but
%     % the point here is to reset the 'test' user back to defaults
%     % before each test is run (so tests will independently from 
%     % each other always start with the same context)
% 
%     % by default, give weather forecast for location of self
%     rdf (aiu:self, wdpd:P131, PLACE),
%     context_set (weatherPlace, PLACE),
% 
%     % by default, give weather forecast for the near future
%     context_set (weatherTime, weatherNearFuture),
%     eoa.

%
% weather reasoning / common sense
%

time_span(I, weatherNearFuture, TS, TE) :-
    ias(I, currentTime, CT),
    before_evening(CT),
    time_span(I, today, TS, TE).

time_span(I, weatherNearFuture, TS, TE) :-
    ias(I, currentTime, CT),
    after_evening(CT),
    time_span(I, tomorrow, TS, TE).

time_label(I, en, weatherNearFuture, "today") :- 
    ias(I, currentTime, CT),
    before_evening(CT).
time_label(I, de, weatherNearFuture, "heute") :- 
    ias(I, currentTime, CT),
    before_evening(CT).

time_label(I, en, weatherNearFuture, "tomorrow") :- 
    ias(I, currentTime, CT),
    after_evening(CT).
time_label(I, de, weatherNearFuture, "morgen") :- 
    ias(I, currentTime, CT),
    after_evening(CT).

%
% weather answers 
%

weather_report(all, en, "01", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s will be clear skies in %s with temperatures between %d and %d degrees.", T_LABEL, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, en, "02", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s will be mostly clear skies in %s with temperatures between %d and %d degrees.", T_LABEL, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, en, "03", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s there will be some clouds in %s with temperatures between %d and %d degrees.", T_LABEL, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, en, "04", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s the sun will show up occasionally in %s with temperatures between %d and %d degrees.", T_LABEL, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, en, "09", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s there will be rain showers of %d millimeters in %s with temperatures between %d and %d degrees.", T_LABEL, PREC, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, en, "10", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    PREC >= 1.0,
    S is format_str("%s it will rain %d millimeters in %s with temperatures between %d and %d degrees.", T_LABEL, PREC, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, en, "10", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    PREC < 1.0,
    S is format_str("%s there might be a little rain in %s with temperatures between %d and %d degrees.", T_LABEL, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, en, "11", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s we will have thunderstorms and %d millimeters of rain in %s with temperatures between %d and %d degrees.", T_LABEL, PREC, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, en, "13", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s it will snow %d millimeters in %s with temperatures between %d and %d degrees.", T_LABEL, PREC, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, en, "50", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s it will be foggy in %s with temperatures between %d and %d degrees", T_LABEL, P_LABEL, TEMP_MIN, TEMP_MAX).

weather_report(all, de, "01", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s wird der Himmel klar sein in %s und es wird zwischen %d und %d Grad warm.", T_LABEL, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, de, "02", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s wird es wenige Wolken geben in %s und es wird zwischen %d und %d Grad warm.", T_LABEL, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, de, "03", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s wird es lockere Wolken geben in %s und es wird zwischen %d und %d Grad warm.", T_LABEL, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, de, "04", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s zeigt sich ab und an die Sonne in %s und es wird zwischen %d und %d Grad warm.", T_LABEL, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, de, "09", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s wird es %d Millimeter Schauer geben in %s und es wird zwischen %d und %d Grad warm.", T_LABEL, PREC, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, de, "10", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    PREC >= 1.0,
    S is format_str("%s regnet es %d Millimeter in %s und es wird zwischen %d und %d Grad warm.", T_LABEL, PREC, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, de, "10", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    PREC < 1.0,
    S is format_str("%s kann es etwas Niederschlag geben in %s und es wird zwischen %d und %d Grad warm.", T_LABEL, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, de, "11", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s wird es Gewitter geben mit %d Millimeter Niederschlag in %s und es wird zwischen %d und %d Grad warm.", T_LABEL, PREC, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, de, "13", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s schneit es %d Millimeter in %s und es wird zwischen %d und %d Grad kalt.", T_LABEL, PREC, P_LABEL, TEMP_MIN, TEMP_MAX).
weather_report(all, de, "50", PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :- 
    S is format_str("%s wird es neblich in %s und es wird zwischen %d und %d Grad geben.", T_LABEL, P_LABEL, TEMP_MIN, TEMP_MAX).

weather_report(prec_cloud, en, CODE, PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :-
    PREC < 0.5,
    CLDS < 50,
    S is format_str("%s it will be mostly sunny in %s with little precipitation.", T_LABEL, P_LABEL).
weather_report(prec_cloud, de, CODE, PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :-
    PREC < 0.5,
    CLDS < 50,
    S is format_str("%s scheint in %s überwiegend die Sonne und es wird kaum Niederschlag geben.", T_LABEL, P_LABEL).

weather_report(prec_cloud, en, CODE, PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :-
    PREC >= 0.5,
    CLDS < 50,
    S is format_str("%s the sun will shine quite often in %s but there might be some precipitation of %d millimeters.", T_LABEL, P_LABEL, CODE, PREC).
weather_report(prec_cloud, de, CODE, PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :-
    PREC >= 0.5,
    CLDS < 50,
    S is format_str("%s scheint in %s oft die Sonne, aber es gibt auch %d Millimeter Niederschlag.", T_LABEL, P_LABEL, CODE, PREC).

weather_report(prec_cloud, en, CODE, PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :-
    PREC < 0.5,
    CLDS >= 50,
    S is format_str("%s it will be mostly cloudy in %s with little precipitation.", T_LABEL, P_LABEL).
weather_report(prec_cloud, de, CODE, PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :-
    PREC < 0.5,
    CLDS >= 50,
    S is format_str("%s ist es in %s überwiegend bewölkt, aber es gibt wenig Niederschlag.", T_LABEL, P_LABEL).

weather_report(prec_cloud, en, CODE, PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :-
    PREC >= 0.5,
    CLDS >= 50,
    S is format_str("%s it will be mostly cloudy in %s with %d millimeters of precipitation.", T_LABEL, P_LABEL, CODE, PREC).
weather_report(prec_cloud, de, CODE, PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, S) :-
    PREC >= 0.5,
    CLDS >= 50,
    S is format_str("%s ist es in %s überwiegend bewölkt, und es gibt %d Millimeter Niederschlag.", T_LABEL, P_LABEL, CODE, PREC).


l4proc (I, F, fnTelling, TOPIC, MSGF, zfWeatherForecast) :-

    frame (MSGF, time,     TIME),
    frame (MSGF, place,    PLACE),    
    frame (MSGF, clouds,   CLDS),
    frame (MSGF, temp_max, TEMP_MAX),
    frame (MSGF, temp_min, TEMP_MIN),
    frame (MSGF, prec,     PREC),
    frame (MSGF, code,     CODE),

    ias (I, uttLang, LANG),

    entity_label(LANG, PLACE, P_LABEL),
    time_label(I, LANG, TIME, T_LABEL),

    weather_report(TOPIC, LANG, CODE, PREC, CLDS, TEMP_MIN, TEMP_MAX, P_LABEL, T_LABEL, STR),

    sayz (I, LANG, STR ).

fill_blanks (I, F, zfWeatherForecast, place) :- frame(F, place, P).
fill_blanks (I, F, zfWeatherForecast, place) :- 
    not (frame (F, place, P)),
    % by default, give weather forecast for location of self
    rdf (aiu:self, wdpd:P131, PLACE),
    assertz(frame(F, place, PLACE)).

fill_blanks (I, F, zfWeatherForecast, time) :- frame(F, time, T).
fill_blanks (I, F, zfWeatherForecast, time) :- 
    not (frame (F, time, T)),
    % by default, give weather forecast for the near future
    assertz(frame(F, time, weatherNearFuture)).

fill_blanks (I, F, zfWeatherForecast) :-
    fill_blanks (I, F, zfWeatherForecast, place),
    fill_blanks (I, F, zfWeatherForecast, time).

weather_data(I, EvT, P, Code, Precipitation, TempMin, TempMax, Clouds) :-
    time_span(I, EvT, EvTS, EvTE),

    rdf_lists(distinct,
              WEV, ai:dt_end,        DT_END,
              WEV, ai:dt_start,      DT_START,
              WEV, ai:location,      P,
              WEV, ai:temp_min,      TempMin,
              WEV, ai:temp_max,      TempMax,
              WEV, ai:precipitation, Precipitation,
              WEV, ai:clouds,        Clouds,
              WEV, ai:icon,          Icon,
              filter (DT_START >= EvTS,
                      DT_END   =< EvTE)
             ),
    sub_string (list_max(Icon), 0, 2, _, Code).

l3proc (I, F, fnQuestioning, MSGF, zfWeatherForecast) :-

    frame (F, top, TOP),

    fill_blanks (I, MSGF),

    % remember our utterance interpretation

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user about weather forecast)
    
    frame(MSGF, time,  TIME),
    frame(MSGF, place, PLACE),

    weather_data(I, TIME, PLACE, CODE, PRECIPITATION, TEMP_MIN, TEMP_MAX, CLOUDS),

    list_append(VMC, fe(place,       PLACE)),
    list_append(VMC, fe(time,        TIME)),
    list_append(VMC, fe(code,        CODE)),
    list_append(VMC, fe(prec,        list_sum(PRECIPITATION))),
    list_append(VMC, fe(temp_min,    list_min(TEMP_MIN))),
    list_append(VMC, fe(temp_max,    list_max(TEMP_MAX))),
    list_append(VMC, fe(clouds,      list_avg(CLOUDS))),
    list_append(VMC, fe(eventuality, weather)),
    list_append(VMC, frame(zfWeatherForecast)),

    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  TOP)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,  USER)),
    list_append(VMC, fe(spkr, uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 100),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    l4proc (I).

%
% nlp processing (english/german)
%

%
% context time and place
%

l2proc_askWeatherPrecCloudContext(LANG) :-

    list_append(VMC, fe(eventuality, weather)),
    list_append(VMC, frame(zfWeatherForecast)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  prec_cloud)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    fnvm_exec (I, VMC).
   
l2proc_askWeatherReportContext(LANG) :-

    list_append(VMC, fe(eventuality, weather)),
    list_append(VMC, frame(zfWeatherForecast)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  all)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),

    fnvm_exec (I, VMC).
   
nlp_gen(en,
        '@SELF_ADDRESS:LABEL will it rain?',
        inline(l2proc_askWeatherPrecCloudContext, en)).
nlp_test(en,
         ivr(in('Computer, will it rain?'),
             out('today it will be mostly sunny in stuttgart with little precipitation'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL wird es (regnen|Regen geben)?',
        inline(l2proc_askWeatherPrecCloudContext, de)).
nlp_test(de,
         ivr(in('Computer, wird es regnen?'),
             out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL (what is the likelihood of|how likely is) rain ?', 
        inline(l2proc_askWeatherPrecCloudContext, en)).
nlp_test(en,
         ivr(in('how likely is rain?'),
             out('today it will be mostly sunny in stuttgart with little precipitation'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL (was ist die Wahrscheinlichkeit für|wie groß ist die Wahrscheinlichkeit für|wie wahrscheinlich ist) Regen ?', 
        inline(l2proc_askWeatherPrecCloudContext, de)).
nlp_test(de,
         ivr(in('wie groß ist die Wahrscheinlichkeit für Regen?'),
             out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL how likely is it that it will rain ?', 
        inline(l2proc_askWeatherPrecCloudContext, en)).
nlp_test(en,
         ivr(in('Computer, how likely is it that it will rain ?'),
             out('today it will be mostly sunny in stuttgart with little precipitation'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL wie wahrscheinlich ist es, dass es regnen wird?', 
        inline(l2proc_askWeatherPrecCloudContext, de)).
nlp_test(de,
         ivr(in('Computer, wie wahrscheinlich ist es, dass es regnen wird?'),
             out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL what (will the weather|is the weather gonna|is the weather going to) be like ?', 
        inline(l2proc_askWeatherReportContext, en)).
nlp_test(en,
         ivr(in('Computer, what will the weather be like?'),
             out('today will be mostly clear skies in stuttgart with temperatures between minus seven and three degrees'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL wie wird das Wetter?', 
        inline(l2proc_askWeatherReportContext, de)).
nlp_test(de,
         ivr(in('Computer, wie wird das Wetter?'),
             out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus sieben und drei grad warm'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL (will the sun shine|will there be sunshine) ?', 
        inline(l2proc_askWeatherPrecCloudContext, en)).
nlp_test(en,
         ivr(in('computer, will there be sunshine?'),
             out('today it will be mostly sunny in stuttgart with little precipitation'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL scheint die Sonne?', 
        inline(l2proc_askWeatherPrecCloudContext, de)).
nlp_test(de,
         ivr(in('computer, scheint die Sonne?'),
             out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL (will it|does it) rain ?', 
        inline(l2proc_askWeatherPrecCloudContext, en)).
nlp_test(en,
         ivr(in('Will it rain?'),
             out('today it will be mostly sunny in stuttgart with little precipitation'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL regnet es ?', 
        inline(l2proc_askWeatherPrecCloudContext, de)).
nlp_test(de,
         ivr(in('Regnet es?'),
             out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL (will rain come|is rain coming)?', 
        inline(l2proc_askWeatherPrecCloudContext, en)).
nlp_test(en,
         ivr(in('Computer, is rain coming?'),
             out('today it will be mostly sunny in stuttgart with little precipitation'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL kommt noch Regen ?', 
        inline(l2proc_askWeatherPrecCloudContext, de)).
nlp_test(de,
         ivr(in('Computer, kommt noch Regen?'),
             out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL how (cold|warm) (is it going to|will it) (be|become) ?', 
        inline(l2proc_askWeatherReportContext, en)).
nlp_test(en,
         ivr(in('Computer, how warm will it be ?'),
             out('today will be mostly clear skies in stuttgart with temperatures between minus seven and three degrees'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL wie (kalt|warm) wird es (werden|)?', 
        inline(l2proc_askWeatherReportContext, de)).
nlp_test(de,
         ivr(in('Computer, wie warm wird es?'),
             out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus sieben und drei grad warm'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) ?', 
        inline(l2proc_askWeatherReportContext, en)).
nlp_test(en,
         ivr(in('computer, what will the weather be like?'),
             out('today will be mostly clear skies in stuttgart with temperatures between minus seven and three degrees'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL wie wird das Wetter ?', 
        inline(l2proc_askWeatherReportContext, de)).
nlp_test(de,
         ivr(in('computer, wie wird das Wetter?'),
             out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus sieben und drei grad warm'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) ?', 
        inline(l2proc_askWeatherReportContext, en)).
nlp_test(en,
         ivr(in('what is the weather gonna be like?'),
             out('today will be mostly clear skies in stuttgart with temperatures between minus seven and three degrees'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL wie wird das Wetter ?', 
        inline(l2proc_askWeatherReportContext, de)).
nlp_test(de,
         ivr(in('wie wird das Wetter?'),
             out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus sieben und drei grad warm'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL what (is the weather outlook|does the weather forecast look like|is the weather forecast|does the weather forecast say) ?', 
        inline(l2proc_askWeatherReportContext, en)).
nlp_test(en,
         ivr(in('Computer, what does the weather forecast say?'),
             out('today will be mostly clear skies in Stuttgart with temperatures between -7 and 3 degrees.'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL (wie sind die Wetteraussichten|was sagt die Wettervorhersage|was sagt der Wetterbericht) ?', 
        inline(l2proc_askWeatherReportContext, de)).
nlp_test(de,
         ivr(in('Computer, was sagt der Wetterbericht?'),
             out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus sieben und drei grad warm'))).

%
% explicit time and place
%


l2proc_askWeatherPrecCloudGeoTime(LANG) :-

    ner(LANG, I, geo_location, @GEO_LOCATION:TSTART_LABEL_0, @GEO_LOCATION:TEND_LABEL_0, GEO_LOCATION_ENTITY), 
    list_append(VMC, fe(place, GEO_LOCATION_ENTITY)),
    list_append(VMC, fe(time, @TIMESPEC:TIME)),
    list_append(VMC, fe(eventuality, weather)),
    list_append(VMC, frame(zfWeatherForecast)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  prec_cloud)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    fnvm_exec (I, VMC).
   
l2proc_askWeatherReportGeoTime(LANG) :-

    ner(LANG, I, geo_location, @GEO_LOCATION:TSTART_LABEL_0, @GEO_LOCATION:TEND_LABEL_0, GEO_LOCATION_ENTITY), 
    list_append(VMC, fe(place, GEO_LOCATION_ENTITY)),
    list_append(VMC, fe(time, @TIMESPEC:TIME)),
    list_append(VMC, fe(eventuality, weather)),
    list_append(VMC, frame(zfWeatherForecast)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  all)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),

    fnvm_exec (I, VMC).
   
nlp_gen(en,
        '@SELF_ADDRESS:LABEL will it rain @TIMESPEC:W in @GEO_LOCATION:LABEL?',
        inline(l2proc_askWeatherPrecCloudGeoTime, en)).
nlp_test(en,
         ivr(in('Computer, will it rain tomorrow in Freudental?'),
             out('tomorrow it will be mostly cloudy in Freudental with little precipitation.'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL wird es @TIMESPEC:W in @GEO_LOCATION:LABEL (regnen|Regen geben)?',
        inline(l2proc_askWeatherPrecCloudGeoTime, de)).
nlp_test(de,
         ivr(in('Computer, wird es morgen in Freudental regnen?'),
             out('morgen ist es in Freudental überwiegend bewölkt, aber es gibt wenig Niederschlag.'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL (what is the likelihood of|how likely is) rain @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
        inline(l2proc_askWeatherPrecCloudGeoTime, en)).
nlp_test(en,
         ivr(in('how likely is rain the day after tomorrow in Stuttgart?'),
             out('day after tomorrow it will be mostly sunny in Stuttgart with little precipitation.'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL (was ist die Wahrscheinlichkeit für|wie groß ist die Wahrscheinlichkeit für|wie wahrscheinlich ist) Regen @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
        inline(l2proc_askWeatherPrecCloudGeoTime, de)).
nlp_test(de,
         ivr(in('wie groß ist die Wahrscheinlichkeit für Regen übermorgen in Stuttgart?'),
             out('übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL how likely is it that it will rain @TIMESPEC:W in @GEO_LOCATION:LABEL?', 
        inline(l2proc_askWeatherPrecCloudGeoTime, en)).
nlp_test(en,
         ivr(in('Computer, how likely is it that it will rain today in Freudental?'),
             out('today it will be mostly sunny in Freudental with little precipitation.'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL wie wahrscheinlich ist es, dass es @TIMESPEC:W in @GEO_LOCATION:LABEL regnen wird?', 
        inline(l2proc_askWeatherPrecCloudGeoTime, de)).
nlp_test(de,
         ivr(in('Computer, wie wahrscheinlich ist es, dass es heute in Freudental regnen wird?'),
             out('heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL what (will the weather|is the weather gonna|is the weather going to) be like @TIMESPEC:W in @GEO_LOCATION:LABEL?', 
        inline(l2proc_askWeatherReportGeoTime, en)).
nlp_test(en,
         ivr(in('Computer, what will the weather be like tomorrow in Tallinn?'),
             out('tomorrow there might be a little rain in Tallinn with temperatures between 1 and 3 degrees.'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL wie wird @TIMESPEC:W in @GEO_LOCATION:LABEL das Wetter?', 
        inline(l2proc_askWeatherReportGeoTime, de)).
nlp_test(de,
         ivr(in('Computer, wie wird morgen in Tallinn das Wetter?'),
             out('morgen kann es etwas Niederschlag geben in Tallinn und es wird zwischen 1 und 3 Grad warm.'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL (will the sun shine|will there be sunshine) @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
        inline(l2proc_askWeatherPrecCloudGeoTime, en)).
nlp_test(en,
         ivr(in('computer, will there be sunshine the day after tomorrow in stuttgart?'),
             out('day after tomorrow it will be mostly sunny in Stuttgart with little precipitation.'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL scheint @TIMESPEC:W in @GEO_LOCATION:LABEL die Sonne?', 
        inline(l2proc_askWeatherPrecCloudGeoTime, de)).
nlp_test(de,
         ivr(in('computer, scheint übermorgen in Stuttgart die Sonne?'),
             out('übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL (will it|does it) rain @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
        inline(l2proc_askWeatherPrecCloudGeoTime, en)).
nlp_test(en,
         ivr(in('Will it rain today in Freudental?'),
             out('today it will be mostly sunny in Freudental with little precipitation.'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL regnet es @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
        inline(l2proc_askWeatherPrecCloudGeoTime, de)).
nlp_test(de,
         ivr(in('Regnet es heute in Freudental?'),
             out('heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL (will rain come|is rain coming) @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
        inline(l2proc_askWeatherPrecCloudGeoTime, en)).
nlp_test(en,
         ivr(in('Computer, is rain coming tomorrow in Tallinn?'),
             out('tomorrow it will be mostly cloudy in Tallinn with little precipitation.'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL kommt @TIMESPEC:W noch Regen in @GEO_LOCATION:LABEL ?', 
        inline(l2proc_askWeatherPrecCloudGeoTime, de)).
nlp_test(de,
         ivr(in('Computer, kommt morgen noch Regen in Tallinn?'),
             out('morgen ist es in tallinn überwiegend bewölkt aber es gibt wenig niederschlag'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL how (cold|warm) (is it going to|will it) (be|become) @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
        inline(l2proc_askWeatherReportGeoTime, en)).
nlp_test(en,
         ivr(in('Computer, how warm will it be the day after tomorrow in Stuttgart?'),
             out('day after tomorrow the sun will show up occasionally in Stuttgart with temperatures between -9 and 1 degrees.'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL wie (kalt|warm) wird es @TIMESPEC:W in @GEO_LOCATION:LABEL (werden|)?', 
        inline(l2proc_askWeatherReportGeoTime, de)).
nlp_test(de,
         ivr(in('Computer, wie warm wird es übermorgen in Stuttgart?'),
             out('übermorgen zeigt sich ab und an die sonne in stuttgart und es wird zwischen minus neun und eins grad warm'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
        inline(l2proc_askWeatherReportGeoTime, en)).
nlp_test(en,
         ivr(in('computer, what will the weather be like today in Tallinn?'),
             out('today there will be some clouds in Tallinn with temperatures between -8 and -4 degrees.'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL wie wird das Wetter @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
        inline(l2proc_askWeatherReportGeoTime, de)).
nlp_test(de,
         ivr(in('computer, wie wird das Wetter heute in Tallinn?'),
             out('heute wird es lockere wolken geben in tallinn und es wird zwischen minus acht und minus vier grad warm'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) in @GEO_LOCATION:LABEL @TIMESPEC:W ?', 
        inline(l2proc_askWeatherReportGeoTime, en)).
nlp_test(en,
         ivr(in('what is the weather gonna be like in stuttgart tomorrow?'),
             out('tomorrow will be mostly clear skies in Stuttgart with temperatures between -8 and 1 degrees.'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL wie wird das Wetter in @GEO_LOCATION:LABEL @TIMESPEC:W ?', 
        inline(l2proc_askWeatherReportGeoTime, de)).
nlp_test(de,
         ivr(in('wie wird das Wetter in Stuttgart morgen?'),
             out('morgen wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und eins grad warm'))).

nlp_gen(en,
        '@SELF_ADDRESS:LABEL what (is the weather outlook|does the weather forecast look like|is the weather forecast|does the weather forecast say) for @TIMESPEC:W for @GEO_LOCATION:LABEL ?', 
        inline(l2proc_askWeatherReportGeoTime, en)).
nlp_test(en,
         ivr(in('Computer, what does the weather forecast say for today for stuttgart?'),
             out('today will be mostly clear skies in Stuttgart with temperatures between -7 and 3 degrees.'))).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL (wie sind die Wetteraussichten|was sagt die Wettervorhersage|was sagt der Wetterbericht) für @TIMESPEC:W für @GEO_LOCATION:LABEL ?', 
        inline(l2proc_askWeatherReportGeoTime, de)).
nlp_test(de,
         ivr(in('Computer, was sagt der Wetterbericht für heute für Stuttgart?'),
             out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus sieben und drei grad warm'))).

% % %
% % % context stack topic dependant productions
% % %
% % 
% % nlp_gen(en, 
% %         '@SELF_ADDRESS:LABEL and @TIMESPECNF_EN:W @PLACEF_EN:W ?', 
% %         context_score (topic, weather, 100, S), @TIMESPECNF_EN:P, @PLACEF_EN:P, answer (weather, en, EvT, P, S)).
% % nlp_gen(de, 
% %         '@SELF_ADDRESS:LABEL und @TIMESPECNF_DE:W @PLACEF_DE:W ?', 
% %         context_score (topic, weather, 100, S), @TIMESPECNF_DE:P, @PLACEF_DE:P, answer (weather, de, EvT, P, S)).
% % 
% % nlp_gen(en, 
% %         '@SELF_ADDRESS:LABEL and @PLACENF_EN:W ?', 
% %         context_score (topic, weather, 100, S), context_get(weatherTime, EvT), @PLACENF_EN:P, answer (weather, en, EvT, P, S)).
% % nlp_gen(de, 
% %         '@SELF_ADDRESS:LABEL und @PLACENF_DE:W ?', 
% %         context_score (topic, weather, 100, S), context_get(weatherTime, EvT), @PLACENF_DE:P, answer (weather, de, EvT, P, S)).
% % 
% % nlp_gen(en, 
% %         '@SELF_ADDRESS:LABEL and @TIMESPEC:W @PLACEN_EN:W ?', 
% %         context_score (topic, weather, 100, S), @TIMESPEC:P, @PLACEN_EN:P, answer (weather, en, EvT, P, S)).
% % nlp_gen(de, 
% %         '@SELF_ADDRESS:LABEL und @TIMESPEC:W @PLACEN_DE:W ?', 
% %         context_score (topic, weather, 100, S), @TIMESPEC:P, @PLACEN_DE:P, answer (weather, de, EvT, P, S)).
% % 
% % nlp_gen(en, 
% %         '@SELF_ADDRESS:LABEL and @TIMESPECN_EN:W ?', 
% %         context_score (topic, weather, 100, S), @TIMESPECN_EN:P, context_get(weatherPlace, P), answer (weather, en, EvT, P, S)).
% % nlp_gen(de, 
% %         '@SELF_ADDRESS:LABEL und @TIMESPECN_DE:W ?', 
% %         context_score (topic, weather, 100, S), @TIMESPECN_DE:P, context_get(weatherPlace, P), answer (weather, de, EvT, P, S)).
% % 
% %

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
             out('in the next three days the sun will show up occasionally in freudental with temperatures between minus seven and five degrees')),
         ivr(in('and tomorrow for Tallinn?'),
             out('tomorrow there might be a little rain in tallinn with temperatures between one and three degrees'))). 
nlp_test(de,
         ivr(in('computer, wie wird das wetter?'),
             out('heute wird es wenige Wolken geben in Stuttgart und es wird zwischen -7 und 3 Grad warm.')),
         ivr(in('und in den nächsten Tagen?'),
             out('in den nächsten drei Tagen zeigt sich ab und an die Sonne in Stuttgart und es wird zwischen -9 und 3 Grad warm.')),
         ivr(in('und in Freudental?'),
             out('in den nächsten drei tagen zeigt sich ab und an die sonne in freudental und es wird zwischen minus sieben und fünf grad warm')),
         ivr(in('und morgen für Tallinn?'),
             out('morgen kann es etwas niederschlag geben in tallinn und es wird zwischen eins und drei grad warm'))). 


% % FIXME: implement
% % Wann geht die Sonne unter?
% 
% %
% % weather
% %
% 
% % rain(E) :- rainProb(E, Prob), Prob >= 50 .
% 
% % time(e1,tomorrowAfternoon).
% % place(e1,stuttgart).
% % rainProb(e1,90).
% 
% %  % Wird es morgen regnen?
% %  % ?- rain(X,TimeSpan,Place),future(TimeSpan),tomorrow(TimeSpan).
% %  question(Prob, I), rain_intensity (E, I), rain_prob(E, Prob), time(E,EvT), tomorrow(EvT), place(E, P), context_get(P)
% %  
% %  % @nlp_de Wird es morgen regnen?
% %  % @nlp_en Will it rain tomorrow?
% %   
% %  ?- rain(E),time(E,EvT),context_get(P),place(P),place(E,P),context_get(R),tomorrow(R,EvT).
% 
% 
% % wird es regnen
% % exists(A,and(rain(it,B),some(C,and(and(time(A),at(C,A)),fut1(A,now)))))
% % ?- rain(X,Time,Place),future(Time).
% 
% % ( 3) Wird es morgen in Freudental regnen?
% % ?- rain(X,Time,freudental),future(Time),tomorrow(Time).
% 
% % ( 4) Wird es Regen geben?
% % ?- rain(X,Time,Place),future(Time).
% 
% % ( 5) Wie gross ist die Wahrscheinlichkeit fuer Regen?
% % ?- rainProb(Time,Place,Prob).
% 
% % ( 6) Wie wahrscheinlich ist es, dass es regnen wird?
% % ?- rainProb(Time,Place,Prob).
% 
% % ( 7) Wie wird das Wetter?
% 
% % question(Report), report(E, Report), time(E,Evt), near_future(EvT), place(E, P), context_get(P), topic(Report, weather)
% 
% % ( 8) Scheint morgen die Sonne?
% 
% % yesnoprob(E), sunshine_prob(E), time(E,EvT), tomorrow(EvT), place(E, P), context_get(P)
% 
% % ( 9) Regnet es?
% 
% % yesnoprob(E), rain_prob(E), time(E,EvT), now(EvT), place(E, P), context_get(P)
% 
% % (10) Wie wird das Wetter morgen?
% 
% % question(Report), report(E, Report), time(E,Evt), tomorrow(EvT), place(E, P), context_get(P), topic(Report, weather)
% 
% % (11) Und in den kommenden Tagen?
% 
% % question(Report), report(E, Report), time(E,Evt), next_days(EvT), place(E, P), context_get(P), topic(Report, weather)
% 
% % (12) Wie wird es naechste Woche werden?
% 
% % question(Report), report(E, Report), time(E,Evt), next_week(EvT), place(E, P), context_get(P), topic(Report, T), context_get(T)
% 
% % (13) Kommt heute noch Regen?
% 
% % yesnoprob(E), rain_prob(E), time(E,EvT), today(EvT), future(EvT), place(E, P), context_get(P)
% 
% % (14) Wie warm wird es heute?
% 
% % question(MaxTemp), max_temp(E, MaxTemp), time(E,EvT), today(EvT), place(E, P), context_get(P)
% 
% % (15) Wie wird das Wetter heute?
% 
% % question(Report), report(E, Report), time(E,Evt), today(EvT), place(E, P), context_get(P), topic(Report, weather)
% 
% % (16) Wie kalt wird es werden?
% 
% % question(MinTemp), min_temp(E, MinTemp), time(E,EvT), context_get(EvT), place(E, P), context_get(P)
% 
% % (17) Was sagt der Wetterbericht?
% 
% % question(Report), report(E, Report), time(E,Evt), context_get(EvT), place(E, P), context_get(P), topic(Report, weather)
% 
% % (18) Was sagt die Wettervorhersage?
% 
% % question(Report), report(E, Report), time(E,Evt), context_get(EvT), place(E, P), context_get(P), topic(Report, weather)
% 
% % (19) Wann geht die Sonne unter?
% 
% % question(SunsetTime), sunset_time(E, SunsetTime), time(E,EvT), context_get(EvT), place(E, P), context_get(P)
% 
% % (20) Wie sind die Wetteraussichten?
% 
% % question(Report), report(E, Report), time(E,Evt), context_get(EvT), place(E, P), context_get(P), topic(Report, weather)
% 
% % (21) Wie sind die Wetteraussichten fuer die naechsten Tage?
% 
% % question(Report), report(E, Report), time(E,Evt), next_days(EvT), place(E, P), context_get(P), topic(Report, weather)
% 
