% prolog

%! module common-sense

%
% time strings
%

timeStrDe(today, "heute").
timeStrDe(tomorrow, "morgen").
timeStrDe(dayAfterTomorrow, "übermorgen").
timeStrDe(nextThreeDays, "in den nächsten drei Tagen").

%
% geography
%

%! doc place
% A place in this universe.

place(stuttgart).
placeStrDe(stuttgart, "Stuttgart").
place(freudental).
placeStrDe(freudental, "Freudental").

%
% time and dates
%

before_evening(TS)  :- stamp_date_time(TS,date(Y,M,D,H,MIN,S,'local')), H < 18.
% before_evening(now) :- get_time(T), before_evening(T).

after_evening(TS)   :- stamp_date_time(TS,date(Y,M,D,H,MIN,S,'local')), H >= 18.
% after_evening(now)  :- get_time(T), after_evening(T).

% startTime(tomorrowAfternoon,X) :- date_time_stamp(date(2015,12,03,11,0,0,'local'),X).
% endTime(tomorrowAfternoon,X)   :- date_time_stamp(date(2015,12,03,17,0,0,'local'),X).
%  %future(TimeSpan) :- startTime(TimeSpan,StartTime), getTime(Now), Now <= StartTime.
%  %future(TimeSpan) :- startTime(TimeSpan,StartTime), get_time(Now), Now =< StartTime.
%  
%  tomorrow(RefT,EvT) :- startTime(EvT,EvStartTime), 
%                        stamp_date_time(EvStartTime,EvStartStamp,local), 
%                        date_time_value('day',EvStartStamp,EvStartDay),
%                        stamp_date_time(RefT,RefTStamp,local),
%                        date_time_value('day',RefTStamp,RefTDay),
%                        TomorrowDay is RefTDay + 1,
%                        EvStartDay = TomorrowDay.
%                      
%  context(T) :- get_time(T).
%  % context(get_time(Now)).
%  

% startTime(tomorrowAfternoon,X) :- get_time(TS),
%                                   stamp_date_time(TS,date(Y,M,D,H,MIN,S,'local')),
%                                   D2 is D+1,
%                                   date_time_stamp(date(Y,M,D2,12,0,0,'local'), X).

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

