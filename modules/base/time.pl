% prolog

%
% time and date (very crude so far, but we have to get started somewhere...)
%

%
% time/date calculations
%

time_span(today, TS, TE) :-
    context(currentTime, T),
    stamp_date_time(T, date(Y,M,D,H,Mn,S,'local')),
    date_time_stamp(date(Y,M,D, 0, 0, 0,'local'), TS),
    date_time_stamp(date(Y,M,D,23,59,59,'local'), TE).

time_span(tomorrow, TS, TE) :-
    context(currentTime, T),
    stamp_date_time(T, date(Y,M,D,H,Mn,S,'local')),
    date_time_stamp(date(Y,M,D + 1, 0, 0, 0,'local'), TS),
    date_time_stamp(date(Y,M,D + 1,23,59,59,'local'), TE).

time_span(dayAfterTomorrow, TS, TE) :-
    context(currentTime, T),
    stamp_date_time(T, date(Y,M,D,H,Mn,S,'local')),
    date_time_stamp(date(Y,M,D + 2, 0, 0, 0,'local'), TS),
    date_time_stamp(date(Y,M,D + 2,23,59,59,'local'), TE).

time_span(nextThreeDays, TS, TE) :-
    context(currentTime, T),
    stamp_date_time(T, date(Y,M,D,H,Mn,S,'local')),
    date_time_stamp(date(Y,M,D,H,Mn,S,'local'), TS),
    date_time_stamp(date(Y,M,D+3,H,Mn,S,'local'), TE).

%
% time strings
%

time_str(de, today,            "heute").
time_str(de, tomorrow,         "morgen").
time_str(de, dayAfterTomorrow, "übermorgen").
time_str(de, nextThreeDays,    "in den nächsten drei Tagen").

%
% time and dates
%

before_noon(TS) :- stamp_date_time(TS,date(Y,M,D,H,MIN,S,'local')), H < 12.
after_noon(TS) :- stamp_date_time(TS,date(Y,M,D,H,MIN,S,'local')), H >= 12.

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

