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

time_span(CT, weatherNearFuture, TS, TE) :-
    before_evening(CT),
    time_span(CT, today, TS, TE).

time_span(CT, weatherNearFuture, TS, TE) :-
    after_evening(CT),
    time_span(CT, tomorrow, TS, TE).

time_label(CT, en, weatherNearFuture, "today") :- 
    before_evening(CT).
time_label(CT, de, weatherNearFuture, "heute") :- 
    before_evening(CT).

time_label(CT, en, weatherNearFuture, "tomorrow") :- 
    after_evening(CT).
time_label(CT, de, weatherNearFuture, "morgen") :- 
    after_evening(CT).

%
% weather answers 
%

nlp_weather_r (en, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "01", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (en, R, "%(t_label)s will be clear skies in %(p_label)s with temperatures between %(f1_temp_min)d and %(f1_temp_max)d degrees.").
nlp_weather_r (en, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "02", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (en, R, "%(t_label)s will be mostly clear skies in %(p_label)s with temperatures between %(f1_temp_min)d and %(f1_temp_max)d degrees.").
nlp_weather_r (en, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "03", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (en, R, "%(t_label)s there will be some clouds in %(p_label)s with temperatures between %(f1_temp_min)d and %(f1_temp_max)d degrees.").
nlp_weather_r (en, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "04", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (en, R, "%(t_label)s the sun will show up occasionally in %(p_label)s with temperatures between %(f1_temp_min)d and %(f1_temp_max)d degrees.").
nlp_weather_r (en, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "09", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (en, R, "%(t_label)s there will be rain showers of %(f1_precipitation)d millimeters in %(p_label)s with temperatures between %(f1_temp_min)d and %(f1_temp_max)d degrees.").
nlp_weather_r (en, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "10", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    R_PREC >= 1.0,
    says (en, R, "%(t_label)s it will rain %(f1_precipitation)d millimeters in %(p_label)s with temperatures between %(f1_temp_min)d and %(f1_temp_max)d degrees.").
nlp_weather_r (en, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "10", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    R_PREC < 1.0,
    says (en, R, "%(t_label)s there might be a little rain in %(p_label)s with temperatures between %(f1_temp_min)d and %(f1_temp_max)d degrees.").
nlp_weather_r (en, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "11", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (en, R, "%(t_label)s we will have thunderstorms and %(f1_precipitation)d millimeters of rain in %(p_label)s with temperatures between %(f1_temp_min)d and %(f1_temp_max)d degrees.").
nlp_weather_r (en, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "13", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (en, R, "%(t_label)s it will snow %(f1_precipitation)d millimeters in %(p_label)s with temperatures between %(f1_temp_min)d and %(f1_temp_max)d degrees.").
nlp_weather_r (en, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "50", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (en, R, "%(t_label)s it will be foggy in %(p_label)s with temperatures between %(f1_temp_min)d and %(f1_temp_max)d degrees").

nlp_weather_r (de, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "01", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (de, R, "%(t_label)s wird der Himmel klar sein in %(p_label)s und es wird zwischen %(f1_temp_min)d und %(f1_temp_max)d Grad warm.").
nlp_weather_r (de, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "02", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (de, R, "%(t_label)s wird es wenige Wolken geben in %(p_label)s und es wird zwischen %(f1_temp_min)d und %(f1_temp_max)d Grad warm.").
nlp_weather_r (de, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "03", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (de, R, "%(t_label)s wird es lockere Wolken geben in %(p_label)s und es wird zwischen %(f1_temp_min)d und %(f1_temp_max)d Grad warm.").
nlp_weather_r (de, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "04", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (de, R, "%(t_label)s zeigt sich ab und an die Sonne in %(p_label)s und es wird zwischen %(f1_temp_min)d und %(f1_temp_max)d Grad warm.").
nlp_weather_r (de, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "09", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (de, R, "%(t_label)s wird es %(f1_precipitation)d Millimeter Schauer geben in %(p_label)s und es wird zwischen %(f1_temp_min)d und %(f1_temp_max)d Grad warm.").
nlp_weather_r (de, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "10", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    R_PREC >= 1.0,
    says (de, R, "%(t_label)s regnet es %(f1_precipitation)d Millimeter in %(p_label)s und es wird zwischen %(f1_temp_min)d und %(f1_temp_max)d Grad warm.").
nlp_weather_r (de, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "10", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    R_PREC < 1.0,
    says (de, R, "%(t_label)s kann es etwas Niederschlag geben in %(p_label)s und es wird zwischen %(f1_temp_min)d und %(f1_temp_max)d Grad warm.").
nlp_weather_r (de, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "11", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (de, R, "%(t_label)s wird es Gewitter geben mit %(f1_precipitation)d Millimeter Niederschlag in %(p_label)s und es wird zwischen %(f1_temp_min)d und %(f1_temp_max)d Grad warm.").
nlp_weather_r (de, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "13", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (de, R, "%(t_label)s schneit es %(f1_precipitation)d Millimeter in %(p_label)s und es wird zwischen %(f1_temp_min)d und %(f1_temp_max)d Grad kalt.").
nlp_weather_r (de, PLACE1, TIME1, full, R, R_CT, R_TIME, R_PLACE, "50", R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    says (de, R, "%(t_label)s wird es neblich in %(p_label)s und es wird zwischen %(f1_temp_min)d und %(f1_temp_max)d Grad geben.").
 

nlp_weather_r (en, PLACE1, TIME1, prec_cloud, R, R_CT, R_TIME, R_PLACE, R_CODE, R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    R_PREC < 1.0,
    R_CLOUDS < 50,
    says (en, R, "%(t_label)s it will be mostly sunny in %(p_label)s with little precipitation.").
nlp_weather_r (de, PLACE1, TIME1, prec_cloud, R, R_CT, R_TIME, R_PLACE, R_CODE, R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    R_PREC < 1.0,
    R_CLOUDS < 50,
    says (de, R, "%(t_label)s scheint in %(p_label)s überwiegend die Sonne und es wird kaum Niederschlag geben.").
nlp_weather_r (en, PLACE1, TIME1, prec_cloud, R, R_CT, R_TIME, R_PLACE, R_CODE, R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    R_PREC >= 1.0,
    R_CLOUDS < 50,
    says (en, R, "%(t_label)s the sun will shine quite often in %(p_label)s but there might be some precipitation of %(f1_precipitation)d millimeters.").
nlp_weather_r (de, PLACE1, TIME1, prec_cloud, R, R_CT, R_TIME, R_PLACE, R_CODE, R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    R_PREC >= 1.0,
    R_CLOUDS < 50,
    says (de, R, "%(t_label)s scheint in %(p_label)s oft die Sonne, aber es gibt auch %(f1_precipitation)d Millimeter Niederschlag.").
nlp_weather_r (en, PLACE1, TIME1, prec_cloud, R, R_CT, R_TIME, R_PLACE, R_CODE, R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    R_PREC < 1.0,
    R_CLOUDS >= 50,
    says (en, R, "%(t_label)s it will be mostly cloudy in %(p_label)s with little precipitation.").
nlp_weather_r (de, PLACE1, TIME1, prec_cloud, R, R_CT, R_TIME, R_PLACE, R_CODE, R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    R_PREC < 1.0,
    R_CLOUDS >= 50,
    says (de, R, "%(t_label)s ist es in %(p_label)s überwiegend bewölkt, aber es gibt wenig Niederschlag.").
nlp_weather_r (en, PLACE1, TIME1, prec_cloud, R, R_CT, R_TIME, R_PLACE, R_CODE, R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    R_PREC >= 1.0,
    R_CLOUDS >= 50,
    says (en, R, "%(t_label)s it will be mostly cloudy in %(p_label)s with %(f1_precipitation)d millimeters of precipitation.").
nlp_weather_r (de, PLACE1, TIME1, prec_cloud, R, R_CT, R_TIME, R_PLACE, R_CODE, R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    R_PREC >= 1.0,
    R_CLOUDS >= 50,
    says (de, R, "%(t_label)s ist es in %(p_label)s überwiegend bewölkt, und es gibt %(f1_precipitation)d Millimeter Niederschlag.").


weather_data(CT, EvT, P, Code, Precipitation, TempMin, TempMax, Clouds) :-
    time_span(CT, EvT, EvTS, EvTE),

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

%
% nlp processing (english/german)
%
 
nlp_weather_g_ext(LANG, G, R_CT, R_TIME, R_PLACE, R_CODE, R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-

    list_extend(G, [
        ias(I, currentTime, CT),
        ias(I, f1_place,    PLACE),
        ias(I, f1_time,     TIME),

        weather_data(CT, TIME, PLACE, CODE, PRECIPITATION, TEMP_MIN, TEMP_MAX, CLOUDS),

        assertz(ias(I, f1_type,          weather_report)),
        assertz(ias(I, f1_code,          CODE)), 
        assertz(ias(I, f1_precipitation, list_sum(PRECIPITATION))), 
        assertz(ias(I, f1_temp_min,      list_min(TEMP_MIN))), 
        assertz(ias(I, f1_temp_max,      list_max(TEMP_MAX))), 
        assertz(ias(I, f1_clouds,        list_avg(CLOUDS))),

        entity_label(LANG, PLACE, P_LABEL),
        time_label(CT, LANG, TIME, T_LABEL),

        assertz(ias(I, p_label,          P_LABEL)),
        assertz(ias(I, t_label,          T_LABEL))]),

    weather_data(R_CT, R_TIME, R_PLACE, R_CODE, R_PREC_L, R_TEMP_MIN_L, R_TEMP_MAX_L, R_CLOUDS_L),
    R_PREC     is list_sum(R_PREC_L),
    R_TEMP_MIN is list_min(R_TEMP_MIN_L),
    R_TEMP_MAX is list_max(R_TEMP_MAX_L),
    R_CLOUDS   is list_avg(R_CLOUDS_L).
    
nlp_weather_sgr(LANG, ROUND, PLACE1, TIME1, TOPIC, S, G, R, R_CT) :-
    nlp_weather_s (LANG, ROUND, PLACE1, TIME1, TOPIC, S),
    nlp_weather_g (LANG, PLACE1, TIME1, TOPIC, G, R_CT, R_TIME, R_PLACE, R_CODE, R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS),
    nlp_weather_r (LANG, PLACE1, TIME1, TOPIC, R, R_CT, R_TIME, R_PLACE, R_CODE, R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS).

nlp_train('weather', en, [P1, S1, G1, R1]) :-

    date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS),
    P1 is [ setz(ias(I, currentTime, _), TS) ], 

    self_address(en, S1, _),
    nlp_weather_sgr(en, start, PLACE1, TIME1, TOPIC1, S1, G1, R1, TS).
 
nlp_train('weather', de, [P1, S1, G1, R1]) :-

    date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS),
    P1 is [ setz(ias(I, currentTime, _), TS) ], 

    self_address(de, S1, _),
    nlp_weather_sgr(de, start, PLACE1, TIME1, TOPIC1, S1, G1, R1, TS).
 
%
% start, default time and place
%

nlp_weather_s(en, start, default, default, prec_cloud, S) :- hears(en, S, ["will it rain?"]).
nlp_weather_s(de, start, default, default, prec_cloud, S) :- hears(de, S, ["wird es",["regnen","Regen geben"],"?"]).
nlp_weather_s(en, start, default, default, prec_cloud, S) :- hears(en, S, [["what is the likelihood of","how likely is"],"rain ?"]).
nlp_weather_s(de, start, default, default, prec_cloud, S) :- hears(de, S, [["was ist die Wahrscheinlichkeit für","wie groß ist die Wahrscheinlichkeit für","wie wahrscheinlich ist"],"Regen ?"]).
nlp_weather_s(en, start, default, default, prec_cloud, S) :- hears(en, S, ["how likely is it that it will rain ?"]).
nlp_weather_s(de, start, default, default, prec_cloud, S) :- hears(de, S, ["wie wahrscheinlich ist es, dass es regnen wird?"]).
nlp_weather_s(en, start, default, default, full, S)       :- hears(en, S, ["what",["will the weather","is the weather gonna","is the weather going to"],"be like ?"]).
nlp_weather_s(de, start, default, default, full, S)       :- hears(de, S, ["wie wird das Wetter?"]).
nlp_weather_s(en, start, default, default, prec_cloud, S) :- hears(en, S, [["will the sun shine","will there be sunshine"],"?"]).
nlp_weather_s(de, start, default, default, prec_cloud, S) :- hears(de, S, ["scheint die Sonne?"]).
nlp_weather_s(en, start, default, default, prec_cloud, S) :- hears(en, S, [["will it","does it"],"rain ?"]).
nlp_weather_s(de, start, default, default, prec_cloud, S) :- hears(de, S, ["regnet es ?"]).
nlp_weather_s(en, start, default, default, prec_cloud, S) :- hears(en, S, [["will rain come","is rain coming"],"?"]).
nlp_weather_s(de, start, default, default, prec_cloud, S) :- hears(de, S, ["kommt noch Regen ?"]).
nlp_weather_s(en, start, default, default, full, S)       :- hears(en, S, ["how",["cold","warm"],["is it going to","will it"],["be","become"],"?"]).
nlp_weather_s(de, start, default, default, full, S)       :- hears(de, S, ["wie",["kalt","warm"],"wird es",["werden",""],"?"]).
nlp_weather_s(en, start, default, default, full, S)       :- hears(en, S, [["what will the weather be","what is the weather gonna be","what is the weather going to be"],["like",""],"?"]).
nlp_weather_s(de, start, default, default, full, S)       :- hears(de, S, ["wie wird das Wetter ?"]).
nlp_weather_s(en, start, default, default, full, S)       :- hears(en, S, [["what will the weather be","what is the weather gonna be","what is the weather going to be"],["like",""],"?"]).
nlp_weather_s(de, start, default, default, full, S)       :- hears(de, S, ["wie wird das Wetter ?"]).
nlp_weather_s(en, start, default, default, full, S)       :- hears(en, S, ["what",["is the weather outlook","does the weather forecast look like","is the weather forecast","does the weather forecast say"],"?"]).
nlp_weather_s(de, start, default, default, full, S)       :- hears(de, S, [["wie sind die Wetteraussichten","was sagt die Wettervorhersage","was sagt der Wetterbericht"],"?"]).

nlp_weather_g(LANG, default, default, TOPIC, G, R_CT, R_TIME, R_PLACE, R_CODE, R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS) :-
    G is [
        assertz(ias(I, f1_topic,  TOPIC)),

        % by default, give weather forecast for location of self
        rdf (aiu:self, wdpd:P131, P),
        assertz(ias(I, f1_place,  P)),

        % by default, give weather forecast for the near future
        assertz(ias(I, f1_time, weatherNearFuture))],

    % we need some weather data for answer code generation also
    rdf (aiu:self, wdpd:P131, R_PLACE),
    is(R_TIME, weatherNearFuture),

    nlp_weather_g_ext(LANG, G, R_CT, R_TIME, R_PLACE, R_CODE, R_PREC, R_TEMP_MIN, R_TEMP_MAX, R_CLOUDS).

nlp_test('weather', en, 't0000', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ['Computer, will it rain?', 'today it will be mostly sunny in stuttgart with little precipitation', []]).
nlp_test("weather", en, 't0001', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Computer, will it rain?","today it will be mostly sunny in stuttgart with little precipitation",[]]).
nlp_test("weather", de, 't0002', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Computer, wird es regnen?","heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben",[]]).
nlp_test("weather", en, 't0003', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["how likely is rain?","today it will be mostly sunny in stuttgart with little precipitation",[]]).
nlp_test("weather", de, 't0004', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["wie groß ist die Wahrscheinlichkeit für Regen?","heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben",[]]).
nlp_test("weather", en, 't0005', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Computer, how likely is it that it will rain ?","today it will be mostly sunny in stuttgart with little precipitation",[]]).
nlp_test("weather", de, 't0006', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Computer, wie wahrscheinlich ist es, dass es regnen wird?","heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben",[]]).
nlp_test("weather", en, 't0007', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Computer, what will the weather be like?","today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees",[]]).
nlp_test("weather", de, 't0008', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Computer, wie wird das Wetter?","heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm",[]]).
nlp_test("weather", en, 't0009', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["computer, will there be sunshine?","today it will be mostly sunny in stuttgart with little precipitation",[]]).
nlp_test("weather", de, 't0010', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["computer, scheint die Sonne?","heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben",[]]).
nlp_test("weather", en, 't0011', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Will it rain?","today it will be mostly sunny in stuttgart with little precipitation",[]]).
nlp_test("weather", de, 't0012', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Regnet es?","heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben",[]]).
nlp_test("weather", en, 't0013', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Computer, is rain coming?","today it will be mostly sunny in stuttgart with little precipitation",[]]).
nlp_test("weather", de, 't0014', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Computer, kommt noch Regen?","heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben",[]]).
nlp_test("weather", en, 't0015', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Computer, how warm will it be ?","today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees",[]]).
nlp_test("weather", de, 't0016', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Computer, wie warm wird es?","heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm",[]]).
nlp_test("weather", en, 't0017', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["computer, what will the weather be like?","today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees",[]]).
nlp_test("weather", de, 't0018', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["computer, wie wird das Wetter?","heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm",[]]).
nlp_test("weather", en, 't0019', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["what is the weather gonna be like?","today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees",[]]).
nlp_test("weather", de, 't0020', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["wie wird das Wetter?","heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm",[]]).
nlp_test("weather", en, 't0021', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Computer, what does the weather forecast say?","today will be mostly clear skies in Stuttgart with temperatures between -8 and 4 degrees.",[]]).
nlp_test("weather", de, 't0022', 
         [ date_time_stamp(date(2016,12,06,11, 0, 0, 'local'), TS), setz(ias(I, currentTime, _), TS) ],
         ["Computer, was sagt der Wetterbericht?","heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm",[]]).


% %
% % context time and place
% %
% 
% l2proc_askWeatherPrecCloudContext(LANG) :-
% 
%     list_append(VMC, fe(eventuality, weather)),
%     list_append(VMC, frame(zfWeatherForecast)),
%     
%     list_append(VMC, fe(msg,  vm_frame_pop)),
%     list_append(VMC, fe(top,  prec_cloud)),
%     list_append(VMC, fe(add,  uriref(aiu:self))),
%     ias(I, user, USER),
%     list_append(VMC, fe(spkr, USER)),
%     list_append(VMC, frame(fnQuestioning)),
%     
%     fnvm_exec (I, VMC).
%    
% l2proc_askWeatherReportContext(LANG) :-
% 
%     list_append(VMC, fe(eventuality, weather)),
%     list_append(VMC, frame(zfWeatherForecast)),
%     
%     list_append(VMC, fe(msg,  vm_frame_pop)),
%     list_append(VMC, fe(top,  all)),
%     list_append(VMC, fe(add,  uriref(aiu:self))),
%     ias(I, user, USER),
%     list_append(VMC, fe(spkr, USER)),
%     list_append(VMC, frame(fnQuestioning)),
% 
%     fnvm_exec (I, VMC).
%    
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL will it rain?',
%         inline(l2proc_askWeatherPrecCloudContext, en)).
% nlp_test(en,
%          ivr(in('Computer, will it rain?'),
%              out('today it will be mostly sunny in stuttgart with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wird es (regnen|Regen geben)?',
%         inline(l2proc_askWeatherPrecCloudContext, de)).
% nlp_test(de,
%          ivr(in('Computer, wird es regnen?'),
%              out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (what is the likelihood of|how likely is) rain ?', 
%         inline(l2proc_askWeatherPrecCloudContext, en)).
% nlp_test(en,
%          ivr(in('how likely is rain?'),
%              out('today it will be mostly sunny in stuttgart with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL (was ist die Wahrscheinlichkeit für|wie groß ist die Wahrscheinlichkeit für|wie wahrscheinlich ist) Regen ?', 
%         inline(l2proc_askWeatherPrecCloudContext, de)).
% nlp_test(de,
%          ivr(in('wie groß ist die Wahrscheinlichkeit für Regen?'),
%              out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL how likely is it that it will rain ?', 
%         inline(l2proc_askWeatherPrecCloudContext, en)).
% nlp_test(en,
%          ivr(in('Computer, how likely is it that it will rain ?'),
%              out('today it will be mostly sunny in stuttgart with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wahrscheinlich ist es, dass es regnen wird?', 
%         inline(l2proc_askWeatherPrecCloudContext, de)).
% nlp_test(de,
%          ivr(in('Computer, wie wahrscheinlich ist es, dass es regnen wird?'),
%              out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL what (will the weather|is the weather gonna|is the weather going to) be like ?', 
%         inline(l2proc_askWeatherReportContext, en)).
% nlp_test(en,
%          ivr(in('Computer, what will the weather be like?'),
%              out('today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wird das Wetter?', 
%         inline(l2proc_askWeatherReportContext, de)).
% nlp_test(de,
%          ivr(in('Computer, wie wird das Wetter?'),
%              out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (will the sun shine|will there be sunshine) ?', 
%         inline(l2proc_askWeatherPrecCloudContext, en)).
% nlp_test(en,
%          ivr(in('computer, will there be sunshine?'),
%              out('today it will be mostly sunny in stuttgart with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL scheint die Sonne?', 
%         inline(l2proc_askWeatherPrecCloudContext, de)).
% nlp_test(de,
%          ivr(in('computer, scheint die Sonne?'),
%              out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (will it|does it) rain ?', 
%         inline(l2proc_askWeatherPrecCloudContext, en)).
% nlp_test(en,
%          ivr(in('Will it rain?'),
%              out('today it will be mostly sunny in stuttgart with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL regnet es ?', 
%         inline(l2proc_askWeatherPrecCloudContext, de)).
% nlp_test(de,
%          ivr(in('Regnet es?'),
%              out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (will rain come|is rain coming)?', 
%         inline(l2proc_askWeatherPrecCloudContext, en)).
% nlp_test(en,
%          ivr(in('Computer, is rain coming?'),
%              out('today it will be mostly sunny in stuttgart with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL kommt noch Regen ?', 
%         inline(l2proc_askWeatherPrecCloudContext, de)).
% nlp_test(de,
%          ivr(in('Computer, kommt noch Regen?'),
%              out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL how (cold|warm) (is it going to|will it) (be|become) ?', 
%         inline(l2proc_askWeatherReportContext, en)).
% nlp_test(en,
%          ivr(in('Computer, how warm will it be ?'),
%              out('today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie (kalt|warm) wird es (werden|)?', 
%         inline(l2proc_askWeatherReportContext, de)).
% nlp_test(de,
%          ivr(in('Computer, wie warm wird es?'),
%              out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) ?', 
%         inline(l2proc_askWeatherReportContext, en)).
% nlp_test(en,
%          ivr(in('computer, what will the weather be like?'),
%              out('today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wird das Wetter ?', 
%         inline(l2proc_askWeatherReportContext, de)).
% nlp_test(de,
%          ivr(in('computer, wie wird das Wetter?'),
%              out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) ?', 
%         inline(l2proc_askWeatherReportContext, en)).
% nlp_test(en,
%          ivr(in('what is the weather gonna be like?'),
%              out('today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wird das Wetter ?', 
%         inline(l2proc_askWeatherReportContext, de)).
% nlp_test(de,
%          ivr(in('wie wird das Wetter?'),
%              out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL what (is the weather outlook|does the weather forecast look like|is the weather forecast|does the weather forecast say) ?', 
%         inline(l2proc_askWeatherReportContext, en)).
% nlp_test(en,
%          ivr(in('Computer, what does the weather forecast say?'),
%              out('today will be mostly clear skies in Stuttgart with temperatures between -7 and 3 degrees.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL (wie sind die Wetteraussichten|was sagt die Wettervorhersage|was sagt der Wetterbericht) ?', 
%         inline(l2proc_askWeatherReportContext, de)).
% nlp_test(de,
%          ivr(in('Computer, was sagt der Wetterbericht?'),
%              out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm'))).
% 
% %
% % explicit time 
% %
% 
% 
% l2proc_askWeatherPrecCloudTime :-
% 
%     list_append(VMC, fe(time, @TIMESPEC:TIME)),
%     list_append(VMC, fe(eventuality, weather)),
%     list_append(VMC, frame(zfWeatherForecast)),
%     
%     list_append(VMC, fe(msg,  vm_frame_pop)),
%     list_append(VMC, fe(top,  prec_cloud)),
%     list_append(VMC, fe(add,  uriref(aiu:self))),
%     ias(I, user, USER),
%     list_append(VMC, fe(spkr, USER)),
%     list_append(VMC, frame(fnQuestioning)),
%     
%     fnvm_exec (I, VMC).
%    
% l2proc_askWeatherReportTime :-
% 
%     list_append(VMC, fe(time, @TIMESPEC:TIME)),
%     list_append(VMC, fe(eventuality, weather)),
%     list_append(VMC, frame(zfWeatherForecast)),
%     
%     list_append(VMC, fe(msg,  vm_frame_pop)),
%     list_append(VMC, fe(top,  all)),
%     list_append(VMC, fe(add,  uriref(aiu:self))),
%     ias(I, user, USER),
%     list_append(VMC, fe(spkr, USER)),
%     list_append(VMC, frame(fnQuestioning)),
% 
%     fnvm_exec (I, VMC).
%    
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL will it rain @TIMESPEC:W ?',
%         inline(l2proc_askWeatherPrecCloudTime)).
% nlp_test(en,
%          ivr(in('Computer, will it rain tomorrow?'),
%              out('tomorrow it will be mostly sunny in stuttgart with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wird es @TIMESPEC:W (regnen|Regen geben)?',
%         inline(l2proc_askWeatherPrecCloudTime)).
% nlp_test(de,
%          ivr(in('Computer, wird es morgen regnen?'),
%              out('morgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (what is the likelihood of|how likely is) rain @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherPrecCloudTime)).
% nlp_test(en,
%          ivr(in('how likely is rain the day after tomorrow?'),
%              out('day after tomorrow it will be mostly sunny in Stuttgart with little precipitation.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL (was ist die Wahrscheinlichkeit für|wie groß ist die Wahrscheinlichkeit für|wie wahrscheinlich ist) Regen @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherPrecCloudTime)).
% nlp_test(de,
%          ivr(in('wie groß ist die Wahrscheinlichkeit für Regen übermorgen?'),
%              out('übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL how likely is it that it will rain @TIMESPEC:W?', 
%         inline(l2proc_askWeatherPrecCloudTime)).
% nlp_test(en,
%          ivr(in('Computer, how likely is it that it will rain today?'),
%              out('today it will be mostly sunny in stuttgart with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wahrscheinlich ist es, dass es @TIMESPEC:W regnen wird?', 
%         inline(l2proc_askWeatherPrecCloudTime)).
% nlp_test(de,
%          ivr(in('Computer, wie wahrscheinlich ist es, dass es heute regnen wird?'),
%              out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL what (will the weather|is the weather gonna|is the weather going to) be like @TIMESPEC:W?', 
%         inline(l2proc_askWeatherReportTime)).
% nlp_test(en,
%          ivr(in('Computer, what will the weather be like tomorrow?'),
%              out('tomorrow will be mostly clear skies in stuttgart with temperatures between minus eight and one degrees'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wird @TIMESPEC:W das Wetter?', 
%         inline(l2proc_askWeatherReportTime)).
% nlp_test(de,
%          ivr(in('Computer, wie wird morgen das Wetter?'),
%              out('morgen wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und eins grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (will the sun shine|will there be sunshine) @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherPrecCloudTime)).
% nlp_test(en,
%          ivr(in('computer, will there be sunshine the day after tomorrow?'),
%              out('day after tomorrow it will be mostly sunny in Stuttgart with little precipitation.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL scheint @TIMESPEC:W die Sonne?', 
%         inline(l2proc_askWeatherPrecCloudTime)).
% nlp_test(de,
%          ivr(in('computer, scheint übermorgen die Sonne?'),
%              out('übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (will it|does it) rain @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherPrecCloudTime)).
% nlp_test(en,
%          ivr(in('Will it rain today?'),
%              out('today it will be mostly sunny in stuttgart with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL regnet es @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherPrecCloudTime)).
% nlp_test(de,
%          ivr(in('Regnet es heute?'),
%              out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (will rain come|is rain coming) @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherPrecCloudTime)).
% nlp_test(en,
%          ivr(in('Computer, is rain coming tomorrow?'),
%              out('tomorrow it will be mostly sunny in stuttgart with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL kommt @TIMESPEC:W noch Regen ?', 
%         inline(l2proc_askWeatherPrecCloudTime)).
% nlp_test(de,
%          ivr(in('Computer, kommt morgen noch Regen?'),
%              out('morgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL how (cold|warm) (is it going to|will it) (be|become) @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherReportTime)).
% nlp_test(en,
%          ivr(in('Computer, how warm will it be the day after tomorrow?'),
%              out('day after tomorrow the sun will show up occasionally in Stuttgart with temperatures between -9 and 1 degrees.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie (kalt|warm) wird es @TIMESPEC:W (werden|)?', 
%         inline(l2proc_askWeatherReportTime)).
% nlp_test(de,
%          ivr(in('Computer, wie warm wird es übermorgen?'),
%              out('übermorgen zeigt sich ab und an die sonne in stuttgart und es wird zwischen minus neun und eins grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherReportTime)).
% nlp_test(en,
%          ivr(in('computer, what will the weather be like today?'),
%              out('today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wird das Wetter @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherReportTime)).
% nlp_test(de,
%          ivr(in('computer, wie wird das Wetter heute?'),
%              out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherReportTime)).
% nlp_test(en,
%          ivr(in('what is the weather gonna be like tomorrow?'),
%              out('tomorrow will be mostly clear skies in Stuttgart with temperatures between -8 and 1 degrees.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wird das Wetter @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherReportTime)).
% nlp_test(de,
%          ivr(in('wie wird das Wetter morgen?'),
%              out('morgen wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und eins grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL what (is the weather outlook|does the weather forecast look like|is the weather forecast|does the weather forecast say) for @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherReportTime)).
% nlp_test(en,
%          ivr(in('Computer, what does the weather forecast say for today?'),
%              out('today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL (wie sind die Wetteraussichten|was sagt die Wettervorhersage|was sagt der Wetterbericht) für @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherReportTime)).
% nlp_test(de,
%          ivr(in('Computer, was sagt der Wetterbericht für heute?'),
%              out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm'))).
% 
% %
% % explicit place
% %
% 
% 
% l2proc_askWeatherPrecCloudGeo(LANG) :-
% 
%     ner(LANG, I, geo_location, @GEO_LOCATION:TSTART_LABEL_0, @GEO_LOCATION:TEND_LABEL_0, GEO_LOCATION_ENTITY), 
%     list_append(VMC, fe(place, GEO_LOCATION_ENTITY)),
%     list_append(VMC, fe(eventuality, weather)),
%     list_append(VMC, frame(zfWeatherForecast)),
%     
%     list_append(VMC, fe(msg,  vm_frame_pop)),
%     list_append(VMC, fe(top,  prec_cloud)),
%     list_append(VMC, fe(add,  uriref(aiu:self))),
%     ias(I, user, USER),
%     list_append(VMC, fe(spkr, USER)),
%     list_append(VMC, frame(fnQuestioning)),
%     
%     fnvm_exec (I, VMC).
%    
% l2proc_askWeatherReportGeo(LANG) :-
% 
%     ner(LANG, I, geo_location, @GEO_LOCATION:TSTART_LABEL_0, @GEO_LOCATION:TEND_LABEL_0, GEO_LOCATION_ENTITY), 
%     list_append(VMC, fe(place, GEO_LOCATION_ENTITY)),
%     list_append(VMC, fe(eventuality, weather)),
%     list_append(VMC, frame(zfWeatherForecast)),
%     
%     list_append(VMC, fe(msg,  vm_frame_pop)),
%     list_append(VMC, fe(top,  all)),
%     list_append(VMC, fe(add,  uriref(aiu:self))),
%     ias(I, user, USER),
%     list_append(VMC, fe(spkr, USER)),
%     list_append(VMC, frame(fnQuestioning)),
% 
%     fnvm_exec (I, VMC).
%    
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL will it rain in @GEO_LOCATION:LABEL?',
%         inline(l2proc_askWeatherPrecCloudGeo, en)).
% nlp_test(en,
%          ivr(in('Computer, will it rain in Freudental?'),
%              out('today it will be mostly sunny in freudental with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wird es in @GEO_LOCATION:LABEL (regnen|Regen geben)?',
%         inline(l2proc_askWeatherPrecCloudGeo, de)).
% nlp_test(de,
%          ivr(in('Computer, wird es in Freudental regnen?'),
%              out('heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (what is the likelihood of|how likely is) rain in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeo, en)).
% nlp_test(en,
%          ivr(in('how likely is rain in Stuttgart?'),
%              out('today it will be mostly sunny in stuttgart with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL (was ist die Wahrscheinlichkeit für|wie groß ist die Wahrscheinlichkeit für|wie wahrscheinlich ist) Regen in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeo, de)).
% nlp_test(de,
%          ivr(in('wie groß ist die Wahrscheinlichkeit für Regen in Stuttgart?'),
%              out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL how likely is it that it will rain in @GEO_LOCATION:LABEL?', 
%         inline(l2proc_askWeatherPrecCloudGeo, en)).
% nlp_test(en,
%          ivr(in('Computer, how likely is it that it will rain in Freudental?'),
%              out('today it will be mostly sunny in Freudental with little precipitation.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wahrscheinlich ist es, dass es in @GEO_LOCATION:LABEL regnen wird?', 
%         inline(l2proc_askWeatherPrecCloudGeo, de)).
% nlp_test(de,
%          ivr(in('Computer, wie wahrscheinlich ist es, dass es in Freudental regnen wird?'),
%              out('heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL what (will the weather|is the weather gonna|is the weather going to) be like in @GEO_LOCATION:LABEL?', 
%         inline(l2proc_askWeatherReportGeo, en)).
% nlp_test(en,
%          ivr(in('Computer, what will the weather be like in Tallinn?'),
%              out('today there will be some clouds in tallinn with temperatures between minus eight and minus four degrees'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wird in @GEO_LOCATION:LABEL das Wetter?', 
%         inline(l2proc_askWeatherReportGeo, de)).
% nlp_test(de,
%          ivr(in('Computer, wie wird in Tallinn das Wetter?'),
%              out('heute wird es lockere wolken geben in tallinn und es wird zwischen minus acht und minus vier grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (will the sun shine|will there be sunshine) in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeo, en)).
% nlp_test(en,
%          ivr(in('computer, will there be sunshine in stuttgart?'),
%              out('today it will be mostly sunny in stuttgart with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL scheint in @GEO_LOCATION:LABEL die Sonne?', 
%         inline(l2proc_askWeatherPrecCloudGeo, de)).
% nlp_test(de,
%          ivr(in('computer, scheint in Stuttgart die Sonne?'),
%              out('heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (will it|does it) rain in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeo, en)).
% nlp_test(en,
%          ivr(in('Will it rain in Freudental?'),
%              out('today it will be mostly sunny in Freudental with little precipitation.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL regnet es in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeo, de)).
% nlp_test(de,
%          ivr(in('Regnet es in Freudental?'),
%              out('heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (will rain come|is rain coming) in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeo, en)).
% nlp_test(en,
%          ivr(in('Computer, is rain coming in Tallinn?'),
%              out('today it will be mostly sunny in tallinn with little precipitation'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL kommt noch Regen in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeo, de)).
% nlp_test(de,
%          ivr(in('Computer, kommt noch Regen in Tallinn?'),
%              out('heute scheint in tallinn überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL how (cold|warm) (is it going to|will it) (be|become) in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherReportGeo, en)).
% nlp_test(en,
%          ivr(in('Computer, how warm will it be in Stuttgart?'),
%              out('today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie (kalt|warm) wird es in @GEO_LOCATION:LABEL (werden|)?', 
%         inline(l2proc_askWeatherReportGeo, de)).
% nlp_test(de,
%          ivr(in('Computer, wie warm wird es in Stuttgart?'),
%              out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherReportGeo, en)).
% nlp_test(en,
%          ivr(in('computer, what will the weather be like in Tallinn?'),
%              out('today there will be some clouds in Tallinn with temperatures between -8 and -4 degrees.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wird das Wetter in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherReportGeo, de)).
% nlp_test(de,
%          ivr(in('computer, wie wird das Wetter in Tallinn?'),
%              out('heute wird es lockere wolken geben in tallinn und es wird zwischen minus acht und minus vier grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherReportGeo, en)).
% nlp_test(en,
%          ivr(in('what is the weather gonna be like in stuttgart?'),
%              out('today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wird das Wetter in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherReportGeo, de)).
% nlp_test(de,
%          ivr(in('wie wird das Wetter in Stuttgart?'),
%              out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL what (is the weather outlook|does the weather forecast look like|is the weather forecast|does the weather forecast say) for @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherReportGeo, en)).
% nlp_test(en,
%          ivr(in('Computer, what does the weather forecast say for stuttgart?'),
%              out('today will be mostly clear skies in Stuttgart with temperatures between -7 and 3 degrees.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL (wie sind die Wetteraussichten|was sagt die Wettervorhersage|was sagt der Wetterbericht) für @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherReportGeo, de)).
% nlp_test(de,
%          ivr(in('Computer, was sagt der Wetterbericht für Stuttgart?'),
%              out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm'))).
% 
% %
% % explicit time and place
% %
% 
% 
% l2proc_askWeatherPrecCloudGeoTime(LANG) :-
% 
%     ner(LANG, I, geo_location, @GEO_LOCATION:TSTART_LABEL_0, @GEO_LOCATION:TEND_LABEL_0, GEO_LOCATION_ENTITY), 
%     list_append(VMC, fe(place, GEO_LOCATION_ENTITY)),
%     list_append(VMC, fe(time, @TIMESPEC:TIME)),
%     list_append(VMC, fe(eventuality, weather)),
%     list_append(VMC, frame(zfWeatherForecast)),
%     
%     list_append(VMC, fe(msg,  vm_frame_pop)),
%     list_append(VMC, fe(top,  prec_cloud)),
%     list_append(VMC, fe(add,  uriref(aiu:self))),
%     ias(I, user, USER),
%     list_append(VMC, fe(spkr, USER)),
%     list_append(VMC, frame(fnQuestioning)),
%     
%     fnvm_exec (I, VMC).
%    
% l2proc_askWeatherReportGeoTime(LANG) :-
% 
%     ner(LANG, I, geo_location, @GEO_LOCATION:TSTART_LABEL_0, @GEO_LOCATION:TEND_LABEL_0, GEO_LOCATION_ENTITY), 
%     list_append(VMC, fe(place, GEO_LOCATION_ENTITY)),
%     list_append(VMC, fe(time, @TIMESPEC:TIME)),
%     list_append(VMC, fe(eventuality, weather)),
%     list_append(VMC, frame(zfWeatherForecast)),
%     
%     list_append(VMC, fe(msg,  vm_frame_pop)),
%     list_append(VMC, fe(top,  all)),
%     list_append(VMC, fe(add,  uriref(aiu:self))),
%     ias(I, user, USER),
%     list_append(VMC, fe(spkr, USER)),
%     list_append(VMC, frame(fnQuestioning)),
% 
%     fnvm_exec (I, VMC).
%    
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL will it rain @TIMESPEC:W in @GEO_LOCATION:LABEL?',
%         inline(l2proc_askWeatherPrecCloudGeoTime, en)).
% nlp_test(en,
%          ivr(in('Computer, will it rain tomorrow in Freudental?'),
%              out('tomorrow it will be mostly cloudy in Freudental with little precipitation.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wird es @TIMESPEC:W in @GEO_LOCATION:LABEL (regnen|Regen geben)?',
%         inline(l2proc_askWeatherPrecCloudGeoTime, de)).
% nlp_test(de,
%          ivr(in('Computer, wird es morgen in Freudental regnen?'),
%              out('morgen ist es in Freudental überwiegend bewölkt, aber es gibt wenig Niederschlag.'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (what is the likelihood of|how likely is) rain @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeoTime, en)).
% nlp_test(en,
%          ivr(in('how likely is rain the day after tomorrow in Stuttgart?'),
%              out('day after tomorrow it will be mostly sunny in Stuttgart with little precipitation.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL (was ist die Wahrscheinlichkeit für|wie groß ist die Wahrscheinlichkeit für|wie wahrscheinlich ist) Regen @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeoTime, de)).
% nlp_test(de,
%          ivr(in('wie groß ist die Wahrscheinlichkeit für Regen übermorgen in Stuttgart?'),
%              out('übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL how likely is it that it will rain @TIMESPEC:W in @GEO_LOCATION:LABEL?', 
%         inline(l2proc_askWeatherPrecCloudGeoTime, en)).
% nlp_test(en,
%          ivr(in('Computer, how likely is it that it will rain today in Freudental?'),
%              out('today it will be mostly sunny in Freudental with little precipitation.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wahrscheinlich ist es, dass es @TIMESPEC:W in @GEO_LOCATION:LABEL regnen wird?', 
%         inline(l2proc_askWeatherPrecCloudGeoTime, de)).
% nlp_test(de,
%          ivr(in('Computer, wie wahrscheinlich ist es, dass es heute in Freudental regnen wird?'),
%              out('heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL what (will the weather|is the weather gonna|is the weather going to) be like @TIMESPEC:W in @GEO_LOCATION:LABEL?', 
%         inline(l2proc_askWeatherReportGeoTime, en)).
% nlp_test(en,
%          ivr(in('Computer, what will the weather be like tomorrow in Tallinn?'),
%              out('tomorrow there might be a little rain in Tallinn with temperatures between 1 and 3 degrees.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wird @TIMESPEC:W in @GEO_LOCATION:LABEL das Wetter?', 
%         inline(l2proc_askWeatherReportGeoTime, de)).
% nlp_test(de,
%          ivr(in('Computer, wie wird morgen in Tallinn das Wetter?'),
%              out('morgen kann es etwas Niederschlag geben in Tallinn und es wird zwischen 1 und 3 Grad warm.'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (will the sun shine|will there be sunshine) @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeoTime, en)).
% nlp_test(en,
%          ivr(in('computer, will there be sunshine the day after tomorrow in stuttgart?'),
%              out('day after tomorrow it will be mostly sunny in Stuttgart with little precipitation.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL scheint @TIMESPEC:W in @GEO_LOCATION:LABEL die Sonne?', 
%         inline(l2proc_askWeatherPrecCloudGeoTime, de)).
% nlp_test(de,
%          ivr(in('computer, scheint übermorgen in Stuttgart die Sonne?'),
%              out('übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (will it|does it) rain @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeoTime, en)).
% nlp_test(en,
%          ivr(in('Will it rain today in Freudental?'),
%              out('today it will be mostly sunny in Freudental with little precipitation.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL regnet es @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeoTime, de)).
% nlp_test(de,
%          ivr(in('Regnet es heute in Freudental?'),
%              out('heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (will rain come|is rain coming) @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeoTime, en)).
% nlp_test(en,
%          ivr(in('Computer, is rain coming tomorrow in Tallinn?'),
%              out('tomorrow it will be mostly cloudy in Tallinn with little precipitation.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL kommt @TIMESPEC:W noch Regen in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherPrecCloudGeoTime, de)).
% nlp_test(de,
%          ivr(in('Computer, kommt morgen noch Regen in Tallinn?'),
%              out('morgen ist es in tallinn überwiegend bewölkt aber es gibt wenig niederschlag'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL how (cold|warm) (is it going to|will it) (be|become) @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherReportGeoTime, en)).
% nlp_test(en,
%          ivr(in('Computer, how warm will it be the day after tomorrow in Stuttgart?'),
%              out('day after tomorrow the sun will show up occasionally in Stuttgart with temperatures between -9 and 1 degrees.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie (kalt|warm) wird es @TIMESPEC:W in @GEO_LOCATION:LABEL (werden|)?', 
%         inline(l2proc_askWeatherReportGeoTime, de)).
% nlp_test(de,
%          ivr(in('Computer, wie warm wird es übermorgen in Stuttgart?'),
%              out('übermorgen zeigt sich ab und an die sonne in stuttgart und es wird zwischen minus neun und eins grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherReportGeoTime, en)).
% nlp_test(en,
%          ivr(in('computer, what will the weather be like today in Tallinn?'),
%              out('today there will be some clouds in Tallinn with temperatures between -8 and -4 degrees.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wird das Wetter @TIMESPEC:W in @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherReportGeoTime, de)).
% nlp_test(de,
%          ivr(in('computer, wie wird das Wetter heute in Tallinn?'),
%              out('heute wird es lockere wolken geben in tallinn und es wird zwischen minus acht und minus vier grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL (what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) in @GEO_LOCATION:LABEL @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherReportGeoTime, en)).
% nlp_test(en,
%          ivr(in('what is the weather gonna be like in stuttgart tomorrow?'),
%              out('tomorrow will be mostly clear skies in Stuttgart with temperatures between -8 and 1 degrees.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL wie wird das Wetter in @GEO_LOCATION:LABEL @TIMESPEC:W ?', 
%         inline(l2proc_askWeatherReportGeoTime, de)).
% nlp_test(de,
%          ivr(in('wie wird das Wetter in Stuttgart morgen?'),
%              out('morgen wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und eins grad warm'))).
% 
% nlp_gen(en,
%         '@SELF_ADDRESS:LABEL what (is the weather outlook|does the weather forecast look like|is the weather forecast|does the weather forecast say) for @TIMESPEC:W for @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherReportGeoTime, en)).
% nlp_test(en,
%          ivr(in('Computer, what does the weather forecast say for today for stuttgart?'),
%              out('today will be mostly clear skies in Stuttgart with temperatures between -7 and 3 degrees.'))).
% nlp_gen(de,
%         '@SELF_ADDRESS:LABEL (wie sind die Wetteraussichten|was sagt die Wettervorhersage|was sagt der Wetterbericht) für @TIMESPEC:W für @GEO_LOCATION:LABEL ?', 
%         inline(l2proc_askWeatherReportGeoTime, de)).
% nlp_test(de,
%          ivr(in('Computer, was sagt der Wetterbericht für heute für Stuttgart?'),
%              out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm'))).
% 
% % % %
% % % % context stack topic dependant productions
% % % %
% % % 
% % % nlp_gen(en, 
% % %         '@SELF_ADDRESS:LABEL and @TIMESPECNF_EN:W @PLACEF_EN:W ?', 
% % %         context_score (topic, weather, 100, S), @TIMESPECNF_EN:P, @PLACEF_EN:P, answer (weather, en, EvT, P, S)).
% % % nlp_gen(de, 
% % %         '@SELF_ADDRESS:LABEL und @TIMESPECNF_DE:W @PLACEF_DE:W ?', 
% % %         context_score (topic, weather, 100, S), @TIMESPECNF_DE:P, @PLACEF_DE:P, answer (weather, de, EvT, P, S)).
% % % 
% % % nlp_gen(en, 
% % %         '@SELF_ADDRESS:LABEL and @PLACENF_EN:W ?', 
% % %         context_score (topic, weather, 100, S), context_get(weatherTime, EvT), @PLACENF_EN:P, answer (weather, en, EvT, P, S)).
% % % nlp_gen(de, 
% % %         '@SELF_ADDRESS:LABEL und @PLACENF_DE:W ?', 
% % %         context_score (topic, weather, 100, S), context_get(weatherTime, EvT), @PLACENF_DE:P, answer (weather, de, EvT, P, S)).
% % % 
% % % nlp_gen(en, 
% % %         '@SELF_ADDRESS:LABEL and @TIMESPEC:W @PLACEN_EN:W ?', 
% % %         context_score (topic, weather, 100, S), @TIMESPEC:P, @PLACEN_EN:P, answer (weather, en, EvT, P, S)).
% % % nlp_gen(de, 
% % %         '@SELF_ADDRESS:LABEL und @TIMESPEC:W @PLACEN_DE:W ?', 
% % %         context_score (topic, weather, 100, S), @TIMESPEC:P, @PLACEN_DE:P, answer (weather, de, EvT, P, S)).
% % % 
% % % nlp_gen(en, 
% % %         '@SELF_ADDRESS:LABEL and @TIMESPECN_EN:W ?', 
% % %         context_score (topic, weather, 100, S), @TIMESPECN_EN:P, context_get(weatherPlace, P), answer (weather, en, EvT, P, S)).
% % % nlp_gen(de, 
% % %         '@SELF_ADDRESS:LABEL und @TIMESPECN_DE:W ?', 
% % %         context_score (topic, weather, 100, S), @TIMESPECN_DE:P, context_get(weatherPlace, P), answer (weather, de, EvT, P, S)).
% % % 
% % %
% 
% %
% % test multiple iteraction steps
% %
% % FIXME: many more examples needed
% %
% 
% nlp_test(en,
%          ivr(in('computer, what is the weather going to be like?'),
%              out('today will be mostly clear skies in Stuttgart with temperatures between -7 and 3 degrees.')),
%          ivr(in('and in the next three days?'),
%              out('in the next three days the sun will show up occasionally in Stuttgart with temperatures between -9 and 3 degrees.')),
%          ivr(in('and in Freudental?'),
%              out('in the next three days the sun will show up occasionally in freudental with temperatures between minus seven and five degrees')),
%          ivr(in('and tomorrow for Tallinn?'),
%              out('tomorrow there might be a little rain in tallinn with temperatures between one and three degrees'))). 
% nlp_test(de,
%          ivr(in('computer, wie wird das wetter?'),
%              out('heute wird es wenige Wolken geben in Stuttgart und es wird zwischen -7 und 3 Grad warm.')),
%          ivr(in('und in den nächsten Tagen?'),
%              out('in den nächsten drei Tagen zeigt sich ab und an die Sonne in Stuttgart und es wird zwischen -9 und 3 Grad warm.')),
%          ivr(in('und in Freudental?'),
%              out('in den nächsten drei tagen zeigt sich ab und an die sonne in freudental und es wird zwischen minus sieben und fünf grad warm')),
%          ivr(in('und morgen für Tallinn?'),
%              out('morgen kann es etwas niederschlag geben in tallinn und es wird zwischen eins und drei grad warm'))). 
% 
% 
% % % FIXME: implement
% % % Wann geht die Sonne unter?
% % 
% % %
% % % weather
% % %
% % 
% % % rain(E) :- rainProb(E, Prob), Prob >= 50 .
% % 
% % % time(e1,tomorrowAfternoon).
% % % place(e1,stuttgart).
% % % rainProb(e1,90).
% % 
% % %  % Wird es morgen regnen?
% % %  % ?- rain(X,TimeSpan,Place),future(TimeSpan),tomorrow(TimeSpan).
% % %  question(Prob, I), rain_intensity (E, I), rain_prob(E, Prob), time(E,EvT), tomorrow(EvT), place(E, P), context_get(P)
% % %  
% % %  % @nlp_de Wird es morgen regnen?
% % %  % @nlp_en Will it rain tomorrow?
% % %   
% % %  ?- rain(E),time(E,EvT),context_get(P),place(P),place(E,P),context_get(R),tomorrow(R,EvT).
% % 
% % 
% % % wird es regnen
% % % exists(A,and(rain(it,B),some(C,and(and(time(A),at(C,A)),fut1(A,now)))))
% % % ?- rain(X,Time,Place),future(Time).
% % 
% % % ( 3) Wird es morgen in Freudental regnen?
% % % ?- rain(X,Time,freudental),future(Time),tomorrow(Time).
% % 
% % % ( 4) Wird es Regen geben?
% % % ?- rain(X,Time,Place),future(Time).
% % 
% % % ( 5) Wie gross ist die Wahrscheinlichkeit fuer Regen?
% % % ?- rainProb(Time,Place,Prob).
% % 
% % % ( 6) Wie wahrscheinlich ist es, dass es regnen wird?
% % % ?- rainProb(Time,Place,Prob).
% % 
% % % ( 7) Wie wird das Wetter?
% % 
% % % question(Report), report(E, Report), time(E,Evt), near_future(EvT), place(E, P), context_get(P), topic(Report, weather)
% % 
% % % ( 8) Scheint morgen die Sonne?
% % 
% % % yesnoprob(E), sunshine_prob(E), time(E,EvT), tomorrow(EvT), place(E, P), context_get(P)
% % 
% % % ( 9) Regnet es?
% % 
% % % yesnoprob(E), rain_prob(E), time(E,EvT), now(EvT), place(E, P), context_get(P)
% % 
% % % (10) Wie wird das Wetter morgen?
% % 
% % % question(Report), report(E, Report), time(E,Evt), tomorrow(EvT), place(E, P), context_get(P), topic(Report, weather)
% % 
% % % (11) Und in den kommenden Tagen?
% % 
% % % question(Report), report(E, Report), time(E,Evt), next_days(EvT), place(E, P), context_get(P), topic(Report, weather)
% % 
% % % (12) Wie wird es naechste Woche werden?
% % 
% % % question(Report), report(E, Report), time(E,Evt), next_week(EvT), place(E, P), context_get(P), topic(Report, T), context_get(T)
% % 
% % % (13) Kommt heute noch Regen?
% % 
% % % yesnoprob(E), rain_prob(E), time(E,EvT), today(EvT), future(EvT), place(E, P), context_get(P)
% % 
% % % (14) Wie warm wird es heute?
% % 
% % % question(MaxTemp), max_temp(E, MaxTemp), time(E,EvT), today(EvT), place(E, P), context_get(P)
% % 
% % % (15) Wie wird das Wetter heute?
% % 
% % % question(Report), report(E, Report), time(E,Evt), today(EvT), place(E, P), context_get(P), topic(Report, weather)
% % 
% % % (16) Wie kalt wird es werden?
% % 
% % % question(MinTemp), min_temp(E, MinTemp), time(E,EvT), context_get(EvT), place(E, P), context_get(P)
% % 
% % % (17) Was sagt der Wetterbericht?
% % 
% % % question(Report), report(E, Report), time(E,Evt), context_get(EvT), place(E, P), context_get(P), topic(Report, weather)
% % 
% % % (18) Was sagt die Wettervorhersage?
% % 
% % % question(Report), report(E, Report), time(E,Evt), context_get(EvT), place(E, P), context_get(P), topic(Report, weather)
% % 
% % % (19) Wann geht die Sonne unter?
% % 
% % % question(SunsetTime), sunset_time(E, SunsetTime), time(E,EvT), context_get(EvT), place(E, P), context_get(P)
% % 
% % % (20) Wie sind die Wetteraussichten?
% % 
% % % question(Report), report(E, Report), time(E,Evt), context_get(EvT), place(E, P), context_get(P), topic(Report, weather)
% % 
% % % (21) Wie sind die Wetteraussichten fuer die naechsten Tage?
% % 
% % % question(Report), report(E, Report), time(E,Evt), next_days(EvT), place(E, P), context_get(P), topic(Report, weather)
% % 
