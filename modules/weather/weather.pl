% prolog

%
% test setup and context
%

set_context_default('test', place, URI) :- uriref(wde:Q1022, URI).
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
    atom_chars(Lang, L2),

    rdf_lists(distinct,
              WEV, hal:dt_end,        DT_END,
              WEV, hal:dt_start,      DT_START,
              WEV, hal:location,      P,
              P,   rdfs:label,        Label,
              WEV, hal:temp_min,      TempMin,
              WEV, hal:temp_max,      TempMax,
              WEV, hal:precipitation, Precipitation,
              WEV, hal:clouds,        Clouds,
              WEV, hal:icon,          Icon,
              filter (DT_START >= isoformat(EvTS, 'local'),
                      DT_END   =< isoformat(EvTE, 'local'),
                      lang(Label) = L2)
             ),

    % sparql_query (format_str(
    %                   "SELECT DISTINCT ?temp_min ?temp_max ?precipitation ?clouds ?icon ?label
    %                    WHERE {
    %                        ?wev hal:dt_end ?dt_end. 
    %                        ?wev hal:dt_start ?dt_start.
    %                        ?wev hal:location <%s>.
    %                        <%s> rdfs:label ?label .
    %                        ?wev hal:temp_min ?temp_min .
    %                        ?wev hal:temp_max ?temp_max .
    %                        ?wev hal:precipitation ?precipitation .
    %                        ?wev hal:clouds ?clouds .
    %                        ?wev hal:icon ?icon .
    %                        FILTER (?dt_start >= \"%s\"^^xsd:dateTime && 
    %                                ?dt_end   <= \"%s\"^^xsd:dateTime &&
    %                                lang(?label) = '%s') 
    %                    }", 
    %                    P, P,
    %                    isoformat(EvTS, 'local'), 
    %                    isoformat(EvTE, 'local'), L2
    %               ), 
    %               TempMin, TempMax, Precipitation, Clouds, Icon, Labels
    %              ),
    list_nth(0, Label, PLoc),
    time_str(Lang, EvT, EvTLoc),
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

nlp_macro('TIMESPEC', W, P) :- W is ''          , P is 'near_future(weather, EvT)'.
nlp_macro('TIMESPEC', W, P) :- W is 'heute'     , P is 'EvT is today'.
nlp_macro('TIMESPEC', W, P) :- W is 'morgen'    , P is 'EvT is tomorrow'.
nlp_macro('TIMESPEC', W, P) :- W is 'übermorgen', P is 'EvT is dayAfterTomorrow'.

nlp_macro('TIMESPECF', W, P) :- W is ''              , P is 'near_future(weather, EvT)'.
nlp_macro('TIMESPECF', W, P) :- W is 'für heute'     , P is 'EvT is today'.
nlp_macro('TIMESPECF', W, P) :- W is 'für morgen'    , P is 'EvT is tomorrow'.
nlp_macro('TIMESPECF', W, P) :- W is 'für übermorgen', P is 'EvT is dayAfterTomorrow'.

nlp_macro('HELLO', W) :- W is ''          .
nlp_macro('HELLO', W) :- W is 'Computer, '.
nlp_macro('HELLO', W) :- W is 'HAL, '     .
nlp_macro('HELLO', W) :- W is 'Hi, '      .
nlp_macro('HELLO', W) :- W is 'Hallo, '   .

nlp_macro('PLACE', W, P) :- W is '', P is 'context(place, P)'.

% W : 'in Stuttgart'     , P: 'P is "dbr:Stuttgart"'
% W : 'in Freudental'    , P: 'P is "dbr:Freudental"'
nlp_macro('PLACE', W, P) :- 
    rdf (LOCATION, hal:cityid, CITYID,
         LOCATION, rdfs:label, LABEL,
         filter(lang(LABEL) = 'de')),
    W is format_str('in %s', LABEL),
    P is format_str('P is "%s"', LOCATION).

nlp_macro('PLACEF', W, P) :- W is '', P is 'context(place, P)'.

% W : 'für Stuttgart'     , P: 'P is "dbr:Stuttgart"'
% W : 'für Freudental'    , P: 'P is "dbr:Freudental"'
nlp_macro('PLACEF', W, P) :- 
    rdf (LOCATION, hal:cityid, CITYID,
         LOCATION, rdfs:label, LABEL,
         filter(lang(LABEL) = 'de')),
    W is format_str('für %s', LABEL),
    P is format_str('P is "%s"', LOCATION).


nlp_gen(de,
        '@HELLO:W wird es @TIMESPEC:W @PLACE:W regnen?',
        @TIMESPEC:P, @PLACE:P, answer (weatherPrecCloud, de, EvT, P), set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hi, wird es morgen in Freudental regnen?'),
             out('morgen ist es in Freudental überwiegend bewölkt, aber es gibt wenig Niederschlag.'))).

nlp_gen(de,
        '@HELLO:W wird es @TIMESPEC:W @PLACE:W Regen geben?', 
        @TIMESPEC:P, @PLACE:P, answer (weatherPrecCloud, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Computer, wird es heute in Tallinn regnen?'),
             out('heute scheint in tallinn überwiegend die sonne und es wird kaum niederschlag geben.'))).

nlp_gen(de,
        '@HELLO:W wie groß ist die Wahrscheinlichkeit für Regen @TIMESPEC:W @PLACE:W ?', 
        @TIMESPEC:P, @PLACE:P, answer (weatherPrecCloud, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('wie groß ist die Wahrscheinlichkeit für Regen übermorgen in Stuttgart?'),
             out('übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(de,
        '@HELLO:W wie wahrscheinlich ist es, dass es @TIMESPEC:W @PLACE:W regnen wird?', 
        @TIMESPEC:P, @PLACE:P, answer (weatherPrecCloud, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('HAL, wie wahrscheinlich ist es, dass es heute in Freudental regnen wird?'),
             out('heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(de,
        '@HELLO:W wie wird @TIMESPEC:W @PLACE:W das Wetter?', 
        @TIMESPEC:P, @PLACE:P, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hi, wie wird morgen in Tallinn das Wetter?'),
             out('morgen regnet es null millimeter in tallinn und es wird zwischen eins und drei grad warm'))).

nlp_gen(de,
        '@HELLO:W scheint @TIMESPEC:W @PLACE:W die Sonne?', 
        @TIMESPEC:P, @PLACE:P, answer (weatherPrecCloud, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hallo, scheint übermorgen in Stuttgart die Sonne?'),
             out('übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(de,
        '@HELLO:W regnet es @TIMESPEC:W @PLACE:W ?', 
        @TIMESPEC:P, @PLACE:P, answer (weatherPrecCloud, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Regnet es in Freudental?'),
             out('heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben'))).

nlp_gen(de,
        '@HELLO:W kommt @TIMESPEC:W noch Regen @PLACE:W ?', 
        @TIMESPEC:P, @PLACE:P, answer (weatherPrecCloud, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Computer, kommt morgen noch Regen in Tallinn?'),
             out('morgen ist es in tallinn überwiegend bewölkt aber es gibt wenig niederschlag'))).

nlp_gen(de,
        '@HELLO:W wie warm wird es @TIMESPEC:W @PLACE:W ?', 
        @TIMESPEC:P, @PLACE:P, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('HAL, wie warm wird es übermorgen in Stuttgart?'),
             out('übermorgen zeigt sich ab und an die sonne in stuttgart und es wird zwischen minus neun und eins grad warm'))).

nlp_gen(de,
        '@HELLO:W wie warm wird es @TIMESPEC:W @PLACE:W werden ?', 
        @TIMESPEC:P, @PLACE:P, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hi, wie warm wird es in Freudental werden?'),
             out('heute wird es wenige wolken geben in freudental und es wird zwischen minus sieben und zwei grad warm'))).

nlp_gen(de,
        '@HELLO:W wie wird das Wetter @TIMESPEC:W @PLACE:W ?', 
        @TIMESPEC:P, @PLACE:P, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hallo, wie wird das Wetter heute in Tallinn?'),
             out('heute wird es lockere wolken geben in tallinn und es wird zwischen minus acht und minus vier grad warm'))).

nlp_gen(de,
        '@HELLO:W wie wird das Wetter @PLACE:W @TIMESPEC:W ?', 
        @TIMESPEC:P, @PLACE:P, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('wie wird das Wetter in Stuttgart morgen?'),
             out('morgen wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und eins grad warm'))).

nlp_gen(de,
        '@HELLO:W wie kalt wird es @TIMESPEC:W @PLACE:W ?', 
        @TIMESPEC:P, @PLACE:P, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Computer, wie kalt wird es übermorgen in Freudental?'),
             out('übermorgen zeigt sich ab und an die sonne in freudental und es wird zwischen minus sechs und eins grad warm'))).

nlp_gen(de,
        '@HELLO:W wie kalt wird es @TIMESPEC:W @PLACE:W werden ?', 
        @TIMESPEC:P, @PLACE:P, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('HAL, wie kalt wird es in Tallinn?'),
             out('heute wird es lockere wolken geben in tallinn und es wird zwischen minus acht und minus vier grad warm'))).

nlp_gen(de,
        '@HELLO:W was sagt der Wetterbericht @TIMESPECF:W @PLACEF:W ?', 
        @TIMESPECF:P, @PLACEF:P, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hi, was sagt der Wetterbericht für heute für Stuttgart?'),
             out('heute wird es wenige wolken geben in stuttgart und es wird zwischen minus sieben und drei grad warm'))).

nlp_gen(de,
        '@HELLO:W was sagt die Wettervorhersage @TIMESPECF:W @PLACEF:W ?', 
        @TIMESPECF:P, @PLACEF:P, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Hallo, was sagt die Wettervorhersage für morgen für Freudental?'),
             out('morgen zeigt sich ab und an die sonne in freudental und es wird zwischen minus sechs und minus zwei grad warm'))).

nlp_gen(de, 
        '@HELLO:W wie sind die Wetteraussichten @TIMESPECF:W @PLACEF:W ?', 
        @TIMESPECF:P, @PLACEF:P, answer (weather, de, EvT, P),set_context(place, P), set_context(time, EvT)).
nlp_test(de,
         ivr(in('Wie sind die Wetteraussichten für übermorgen?'),
             out('übermorgen zeigt sich ab und an die sonne in stuttgart und es wird zwischen -9 und 1 grad warm'))).

%
% test multiple iteraction steps
%
% FIXME: many more examples needed
%

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
%  question(Prob, I), rain_intensity (E, I), rain_prob(E, Prob), time(E,EvT), tomorrow(EvT), place(E, P), context(P)
%  
%  % @nlp_de Wird es morgen regnen?
%  % @nlp_en Will it rain tomorrow?
%   
%  ?- rain(E),time(E,EvT),context(P),place(P),place(E,P),context(R),tomorrow(R,EvT).


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

% question(Report), report(E, Report), time(E,Evt), near_future(EvT), place(E, P), context(P), topic(Report, weather)

% ( 8) Scheint morgen die Sonne?

% yesnoprob(E), sunshine_prob(E), time(E,EvT), tomorrow(EvT), place(E, P), context(P)

% ( 9) Regnet es?

% yesnoprob(E), rain_prob(E), time(E,EvT), now(EvT), place(E, P), context(P)

% (10) Wie wird das Wetter morgen?

% question(Report), report(E, Report), time(E,Evt), tomorrow(EvT), place(E, P), context(P), topic(Report, weather)

% (11) Und in den kommenden Tagen?

% question(Report), report(E, Report), time(E,Evt), next_days(EvT), place(E, P), context(P), topic(Report, weather)

% (12) Wie wird es naechste Woche werden?

% question(Report), report(E, Report), time(E,Evt), next_week(EvT), place(E, P), context(P), topic(Report, T), context(T)

% (13) Kommt heute noch Regen?

% yesnoprob(E), rain_prob(E), time(E,EvT), today(EvT), future(EvT), place(E, P), context(P)

% (14) Wie warm wird es heute?

% question(MaxTemp), max_temp(E, MaxTemp), time(E,EvT), today(EvT), place(E, P), context(P)

% (15) Wie wird das Wetter heute?

% question(Report), report(E, Report), time(E,Evt), today(EvT), place(E, P), context(P), topic(Report, weather)

% (16) Wie kalt wird es werden?

% question(MinTemp), min_temp(E, MinTemp), time(E,EvT), context(EvT), place(E, P), context(P)

% (17) Was sagt der Wetterbericht?

% question(Report), report(E, Report), time(E,Evt), context(EvT), place(E, P), context(P), topic(Report, weather)

% (18) Was sagt die Wettervorhersage?

% question(Report), report(E, Report), time(E,Evt), context(EvT), place(E, P), context(P), topic(Report, weather)

% (19) Wann geht die Sonne unter?

% question(SunsetTime), sunset_time(E, SunsetTime), time(E,EvT), context(EvT), place(E, P), context(P)

% (20) Wie sind die Wetteraussichten?

% question(Report), report(E, Report), time(E,Evt), context(EvT), place(E, P), context(P), topic(Report, weather)

% (21) Wie sind die Wetteraussichten fuer die naechsten Tage?

% question(Report), report(E, Report), time(E,Evt), next_days(EvT), place(E, P), context(P), topic(Report, weather)

