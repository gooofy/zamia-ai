%prolog

%
% time and date (pretty crude so far, but we have to get started somewhere...)
%

%
% time/date calculations
%

% time_span(CT, today, TS, TE) :-
%     stamp_date_time(CT, date(Y,M,D,_,_,_,_,_,_), local),
%     date_time_stamp(date(Y,M,D, 0, 0, 0,'local'), TS),
%     date_time_stamp(date(Y,M,D,23,59,59,'local'), TE).

% time_span(CT, tomorrow, TS, TE) :-
%     stamp_date_time(CT, date(Y,M,D,H,Mn,S,'local')),
%     date_time_stamp(date(Y,M,D + 1, 0, 0, 0,'local'), TS),
%     date_time_stamp(date(Y,M,D + 1,23,59,59,'local'), TE).
% 
% time_span(CT, dayAfterTomorrow, TS, TE) :-
%     stamp_date_time(CT, date(Y,M,D,H,Mn,S,'local')),
%     date_time_stamp(date(Y,M,D + 2, 0, 0, 0,'local'), TS),
%     date_time_stamp(date(Y,M,D + 2,23,59,59,'local'), TE).
% 
% time_span(CT, nextThreeDays, TS, TE) :-
%     stamp_date_time(CT, date(Y,M,D,H,Mn,S,'local')),
%     date_time_stamp(date(Y,M,D,H,Mn,S,'local'), TS),
%     date_time_stamp(date(Y,M,D+3,H,Mn,S,'local'), TE).
% 
% %
% % time strings
% %
% 
% time_label(CT, en, today,            "today").
% time_label(CT, en, tomorrow,         "tomorrow").
% time_label(CT, en, dayAfterTomorrow, "day after tomorrow").
% time_label(CT, en, nextThreeDays,    "in the next three days").
% 
% time_label(CT, de, today,            "heute").
% time_label(CT, de, tomorrow,         "morgen").
% time_label(CT, de, dayAfterTomorrow, "übermorgen").
% time_label(CT, de, nextThreeDays,    "in den nächsten drei Tagen").
% 
% 
% %
% % time and dates
% %
% 
% before_noon(TS) :- stamp_date_time(TS,date(Y,M,D,H,MIN,S,'local')), H < 12.
% after_noon(TS) :- stamp_date_time(TS,date(Y,M,D,H,MIN,S,'local')), H >= 12.
% 
% before_evening(TS)  :- stamp_date_time(TS,date(Y,M,D,H,MIN,S,'local')), H < 18.
% % before_evening(now) :- get_time(T), before_evening(T).
% 
% after_evening(TS)   :- stamp_date_time(TS,date(Y,M,D,H,MIN,S,'local')), H >= 18.
% % after_evening(now)  :- get_time(T), after_evening(T).
% 
% % startTime(tomorrowAfternoon,X) :- date_time_stamp(date(2015,12,03,11,0,0,'local'),X).
% % endTime(tomorrowAfternoon,X)   :- date_time_stamp(date(2015,12,03,17,0,0,'local'),X).
% %  %future(TimeSpan) :- startTime(TimeSpan,StartTime), getTime(Now), Now <= StartTime.
% %  %future(TimeSpan) :- startTime(TimeSpan,StartTime), get_time(Now), Now =< StartTime.
% %  
% %  tomorrow(RefT,EvT) :- startTime(EvT,EvStartTime), 
% %                        stamp_date_time(EvStartTime,EvStartStamp,local), 
% %                        date_time_value('day',EvStartStamp,EvStartDay),
% %                        stamp_date_time(RefT,RefTStamp,local),
% %                        date_time_value('day',RefTStamp,RefTDay),
% %                        TomorrowDay is RefTDay + 1,
% %                        EvStartDay = TomorrowDay.
% %                      
% %  context_get(T) :- get_time(T).
% %  % context_get(get_time(Now)).
% %  
% 
% % startTime(tomorrowAfternoon,X) :- get_time(TS),
% %                                   stamp_date_time(TS,date(Y,M,D,H,MIN,S,'local')),
% %                                   D2 is D+1,
% %                                   date_time_stamp(date(Y,M,D2,12,0,0,'local'), X).
% % 
% macro (en, timespec, TIME, LABEL) :- TIME is today           , LABEL is 'today'.
% macro (en, timespec, TIME, LABEL) :- TIME is tomorrow        , LABEL is 'tomorrow'.
% macro (en, timespec, TIME, LABEL) :- TIME is dayAfterTomorrow, LABEL is 'the day after tomorrow'.
% macro (en, timespec, TIME, LABEL) :- TIME is nextThreeDays   , LABEL is 'the next three days'.
% 
% macro (de, timespec, TIME, LABEL) :- TIME is today           , LABEL is 'heute'.
% macro (de, timespec, TIME, LABEL) :- TIME is tomorrow        , LABEL is 'morgen'.
% macro (de, timespec, TIME, LABEL) :- TIME is dayAfterTomorrow, LABEL is 'übermorgen'.
% macro (de, timespec, TIME, LABEL) :- TIME is nextThreeDays   , LABEL is 'die nächsten drei Tage'.
%  

