% prolog

%
% time and date (very crude so far, but we have to get started somewhere...)
%

%
% time/date calculations
%

time_span(today, TS, TE) :-
    rdf(ai:curin, ai:currentTime, T),
    stamp_date_time(T, date(Y,M,D,H,Mn,S,'local')),
    date_time_stamp(date(Y,M,D, 0, 0, 0,'local'), TS),
    date_time_stamp(date(Y,M,D,23,59,59,'local'), TE).

time_span(tomorrow, TS, TE) :-
    rdf(ai:curin, ai:currentTime, T),
    stamp_date_time(T, date(Y,M,D,H,Mn,S,'local')),
    date_time_stamp(date(Y,M,D + 1, 0, 0, 0,'local'), TS),
    date_time_stamp(date(Y,M,D + 1,23,59,59,'local'), TE).

time_span(dayAfterTomorrow, TS, TE) :-
    rdf(ai:curin, ai:currentTime, T),
    stamp_date_time(T, date(Y,M,D,H,Mn,S,'local')),
    date_time_stamp(date(Y,M,D + 2, 0, 0, 0,'local'), TS),
    date_time_stamp(date(Y,M,D + 2,23,59,59,'local'), TE).

time_span(nextThreeDays, TS, TE) :-
    rdf(ai:curin, ai:currentTime, T),
    stamp_date_time(T, date(Y,M,D,H,Mn,S,'local')),
    date_time_stamp(date(Y,M,D,H,Mn,S,'local'), TS),
    date_time_stamp(date(Y,M,D+3,H,Mn,S,'local'), TE).

%
% time strings
%

time_str(en, today,            "today").
time_str(en, tomorrow,         "tomorrow").
time_str(en, dayAfterTomorrow, "day after tomorrow").
time_str(en, nextThreeDays,    "in the next three days").

time_str(de, today,            "heute").
time_str(de, tomorrow,         "morgen").
time_str(de, dayAfterTomorrow, "übermorgen").
time_str(de, nextThreeDays,    "in den nächsten drei Tagen").

transcribe_month(en,  1, 'january').
transcribe_month(en,  2, 'feburary').
transcribe_month(en,  3, 'march').
transcribe_month(en,  4, 'april').
transcribe_month(en,  5, 'may').
transcribe_month(en,  6, 'june').
transcribe_month(en,  7, 'july').
transcribe_month(en,  8, 'august').
transcribe_month(en,  9, 'september').
transcribe_month(en, 10, 'october').
transcribe_month(en, 11, 'november').
transcribe_month(en, 12, 'december').

transcribe_month(de,  1, 'januar').
transcribe_month(de,  2, 'feburar').
transcribe_month(de,  3, 'märz').
transcribe_month(de,  4, 'april').
transcribe_month(de,  5, 'mai').
transcribe_month(de,  6, 'juni').
transcribe_month(de,  7, 'juli').
transcribe_month(de,  8, 'august').
transcribe_month(de,  9, 'september').
transcribe_month(de, 10, 'oktober').
transcribe_month(de, 11, 'november').
transcribe_month(de, 12, 'dezember').

transcribe_date(en, dativ, TS, SCRIPT) :-
    stamp_date_time(TS, date(Y,M,D,H,Mn,S,'local')),
    transcribe_number(en, nominative, D, DS),
    transcribe_month(en, M, MS),
    SCRIPT is format_str('%s %s, %s', MS, DS, Y).

transcribe_date(de, dativ, TS, SCRIPT) :-
    stamp_date_time(TS, date(Y,M,D,H,Mn,S,'local')),
    transcribe_number(de, ord_gen, D, DS),
    transcribe_month(de, M, MS),
    SCRIPT is format_str('%s %s %s', DS, MS, Y).

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
%  context_get(T) :- get_time(T).
%  % context_get(get_time(Now)).
%  

% startTime(tomorrowAfternoon,X) :- get_time(TS),
%                                   stamp_date_time(TS,date(Y,M,D,H,MIN,S,'local')),
%                                   D2 is D+1,
%                                   date_time_stamp(date(Y,M,D2,12,0,0,'local'), X).

