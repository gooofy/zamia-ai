% prolog

%
% time and date (pretty crude so far, but we have to get started somewhere...)
%

% this will switch to much smaller training sets so we can keep 
% debug turn-around cycle times low
% debug_mode('dt').

%
% time/date calculations
%

time_span(I, today, TS, TE) :-
    ias(I, currentTime, T),
    stamp_date_time(T, date(Y,M,D,H,Mn,S,'local')),
    date_time_stamp(date(Y,M,D, 0, 0, 0,'local'), TS),
    date_time_stamp(date(Y,M,D,23,59,59,'local'), TE).

time_span(I, tomorrow, TS, TE) :-
    ias(I, currentTime, T),
    stamp_date_time(T, date(Y,M,D,H,Mn,S,'local')),
    date_time_stamp(date(Y,M,D + 1, 0, 0, 0,'local'), TS),
    date_time_stamp(date(Y,M,D + 1,23,59,59,'local'), TE).

time_span(I, dayAfterTomorrow, TS, TE) :-
    ias(I, currentTime, T),
    stamp_date_time(T, date(Y,M,D,H,Mn,S,'local')),
    date_time_stamp(date(Y,M,D + 2, 0, 0, 0,'local'), TS),
    date_time_stamp(date(Y,M,D + 2,23,59,59,'local'), TE).

time_span(I, nextThreeDays, TS, TE) :-
    ias(I, currentTime, T),
    stamp_date_time(T, date(Y,M,D,H,Mn,S,'local')),
    date_time_stamp(date(Y,M,D,H,Mn,S,'local'), TS),
    date_time_stamp(date(Y,M,D+3,H,Mn,S,'local'), TE).

%
% time strings
%

time_label(I, en, today,            "today").
time_label(I, en, tomorrow,         "tomorrow").
time_label(I, en, dayAfterTomorrow, "day after tomorrow").
time_label(I, en, nextThreeDays,    "in the next three days").

time_label(I, de, today,            "heute").
time_label(I, de, tomorrow,         "morgen").
time_label(I, de, dayAfterTomorrow, "übermorgen").
time_label(I, de, nextThreeDays,    "in den nächsten drei Tagen").

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

nlp_timespec(en, S, today)            :- hears(en, S, 'today').
nlp_timespec(en, S, tomorrow)         :- hears(en, S, 'tomorrow').
nlp_timespec(en, S, dayAfterTomorrow) :- hears(en, S, 'the day after tomorrow').
nlp_timespec(en, S, nextThreeDays)    :- hears(en, S, 'the next three days').

nlp_timespec(de, S, today)            :- hears(de, S, 'heute').
nlp_timespec(de, S, tomorrow)         :- hears(de, S, 'morgen').
nlp_timespec(de, S, dayAfterTomorrow) :- hears(de, S, 'übermorgen').
nlp_timespec(de, S, nextThreeDays)    :- hears(de, S, 'die nächsten drei Tage').

nlp_say_time(en, R, T_H,     1) :- says (en, R, "one minute past %(f1_hour)d"),!.
nlp_say_time(en, R, T_H,     0) :- says (en, R, "exactly %(f1_hour)d o'clock"),!.
nlp_say_time(en, R, T_H,    15) :- says (en, R, "a quarter past %(f1_hour)d"),!.
nlp_say_time(en, R, T_H,    30) :- says (en, R, "half past %(f1_hour)d"),!.
nlp_say_time(en, R, T_H, T_MIN) :- says (en, R, "%(f1_minute)d minutes past %(f1_hour)d").

nlp_say_date(en, R) :- says (en, R, "%(f1_wday_label)s %(f1_month_label)s %(f1_day)d, %(f1_year)d").

nlp_day_of_the_week_label(en, 1, 'Monday').
nlp_day_of_the_week_label(en, 2, 'Tuesday').
nlp_day_of_the_week_label(en, 3, 'Wednesday').
nlp_day_of_the_week_label(en, 4, 'Thursday').
nlp_day_of_the_week_label(en, 5, 'Friday').
nlp_day_of_the_week_label(en, 6, 'Saturday').
nlp_day_of_the_week_label(en, 7, 'Sunday').

nlp_month_label(en,  1, 'January').
nlp_month_label(en,  2, 'February').
nlp_month_label(en,  3, 'March').
nlp_month_label(en,  4, 'April').
nlp_month_label(en,  5, 'May').
nlp_month_label(en,  6, 'June').
nlp_month_label(en,  7, 'July').
nlp_month_label(en,  8, 'August').
nlp_month_label(en,  9, 'September').
nlp_month_label(en, 10, 'October').
nlp_month_label(en, 11, 'November').
nlp_month_label(en, 12, 'December').


%
% time questions
%

nlp_datetime_s(en, S, time) :- hears(en, S, "do you know what time it is").
nlp_datetime_s(en, S, time) :- hears(en, S, "what time is it").
nlp_datetime_s(en, S, time) :- hears(en, S, "what's the time?").

nlp_datetime_r(en, R, T_H, T_MIN) :- says (en, R, "It is"), nlp_say_time(en, R, T_H, T_MIN).
nlp_datetime_r(en, R, T_H, T_MIN) :- says (en, R, "It is now"), nlp_say_time(en, R, T_H, T_MIN).
nlp_datetime_r(en, R, T_H, T_MIN) :- says (en, R, "The time is"), nlp_say_time(en, R, T_H, T_MIN).
nlp_datetime_r(en, R, T_H, T_MIN) :- says (en, R, "The time is now"), nlp_say_time(en, R, T_H, T_MIN).

time_hour_12(T_H, T_H2) :- T_H < 13, T_H2 is T_H, !.
time_hour_12(T_H, T_H2) :- T_H2 is T_H - 12.

nlp_datetime_g(LANG, G, time) :-
    G is [

        ias(I, currentTime, TIME),

        setz(ias(I, f1_type,   _), question),
        setz(ias(I, f1_topic,  _), time),

        stamp_date_time(TIME, date(T_Y,T_M,T_D,T_H,T_MIN,T_S,'local')),

        time_hour_12 (T_H, T_H12),

        setz(ias(I, f1_minute, _), T_MIN),
        setz(ias(I, f1_hour,   _), T_H12)

        ].

nlp_datetime (LANG, S, G, R, start, time, TT_H, TT_MIN) :-

    self_address(LANG, S, LABEL),
    nlp_datetime_s(LANG, S, time),

    nlp_datetime_g(LANG, G, time),

    nlp_datetime_r(LANG, R, TT_H, TT_MIN).

nlp_datetime_train_hour (H) :- between (0, 23, H).

nlp_datetime_train_minute (M) :- between (0, 59, M).

nlp_datetime_train_time_ts_large(X, TT_H, TT_MIN) :- 
    nlp_datetime_train_hour(TT_H),
    nlp_datetime_train_minute(TT_MIN),
    date_time_stamp(date(2017, 6, 12, TT_H, TT_MIN, 0, 'local'), X).

nlp_datetime_train_time_ts_small(X,  5, 30) :- date_time_stamp(date(2017, 6, 12,  5, 30, 0, 'local'), X).
nlp_datetime_train_time_ts_small(X, 12, 15) :- date_time_stamp(date(2017, 6, 12, 12, 15, 0, 'local'), X).

nlp_datetime_train_time_ts(X, TT_H, TT_MIN) :- 
    debug_mode('dt'),
    nlp_datetime_train_time_ts_small(X, TT_H, TT_MIN), !.
    
nlp_datetime_train_time_ts(X, TT_H, TT_MIN) :- 
    nlp_datetime_train_time_ts_large(X, TT_H, TT_MIN).

nlp_train('dt', en, [P1, S1, G1, R1]) :-

    nlp_datetime_train_time_ts(TS, TT_H, TT_MIN),

    P1 is [ setz(ias(I, currentTime, _), TS) ],

    nlp_datetime (en, S1, G1, R1, start, time, TT_H, TT_MIN)
    .

nlp_test('dt', en, 'time1', 
         [ date_time_stamp(date(2017, 6, 12, 5, 30, 0, 'local'), TS),
           setz(ias(I, currentTime, _), TS) ],
         ["what time is it", "It is half past 6.", []]).

nlp_test('dt', en, 'time2', 
         [ date_time_stamp(date(2017, 6, 12, 12, 15, 0, 'local'), TS),
           setz(ias(I, currentTime, _), TS) ],
         ["what time is it", "It is a quarter past 1.", []]).

%
% multi-round time questions
%

nlp_datetime (LANG, S, G, R, followup, time, TT_H, TT_MIN) :-

    % self_address(LANG, S, LABEL),
    nlp_sayagain_s(LANG, S),

    G is [],

    nlp_isaid_r (LANG, R),
    nlp_datetime_r(LANG, R, TT_H, TT_MIN).

nlp_datetime_r(en, R, timetopic) :- says (en, R, "We were talking about the time").
nlp_datetime_r(en, R, timetopic) :- says (en, R, "The time was our topic").

nlp_datetime (LANG, S, G, R, followup, time, TT_H, TT_MIN) :-

    % self_address(LANG, S, LABEL),
    nlp_whatwasourtopic_s(LANG, S),

    G is [],

    nlp_datetime_r(en, R, timetopic).

nlp_train('dt', en, [P1, S1, G1, R1, P2, S2, G2, R2]) :-

    nlp_datetime_train_time_ts_small(TS1, TT_H, TT_MIN),

    P1 is [ setz(ias(I, currentTime, _), TS1) ],
    P2 is P1,

    nlp_datetime (en, S1, G1, R1, start, time, TT_H, TT_MIN),

    nlp_datetime (en, S2, G2, R2, followup, time, TT_H, TT_MIN)
    .

nlp_test('dt', en, 'time3', 
         [ date_time_stamp(date(2017, 6, 12, 5, 30, 0, 'local'), TS),
           setz(ias(I, currentTime, _), TS) ],
         ["what time is it", "It is half past 6.", [],
          "huh?", "I said it is half past 6.", []]).

nlp_test('dt', en, 'time4', 
         [ date_time_stamp(date(2017, 6, 12, 5, 30, 0, 'local'), TS),
           setz(ias(I, currentTime, _), TS) ],
         ["what time is it", "It is half past 6.", [],
          "what was our topic?", "We were talking about the time.", []]).

%
% date questions
%

nlp_datetime_s(en, S, date) :- hears(en, S, "do you know what day it is").
nlp_datetime_s(en, S, date) :- hears(en, S, "do you know what day it is today").
nlp_datetime_s(en, S, date) :- hears(en, S, "do you know what date it is").
nlp_datetime_s(en, S, date) :- hears(en, S, "do you know what date it is today").
nlp_datetime_s(en, S, date) :- hears(en, S, "what date is it").
nlp_datetime_s(en, S, date) :- hears(en, S, "what date is it today").
nlp_datetime_s(en, S, date) :- hears(en, S, "what day is it").
nlp_datetime_s(en, S, date) :- hears(en, S, "what day is it today").
nlp_datetime_s(en, S, date) :- hears(en, S, "what's the date?").

nlp_datetime_r(en, R) :- says (en, R, "The date is %(f1_wday_label)s %(f1_month_label)s %(f1_day)d, %(f1_year)d").
nlp_datetime_r(en, R) :- says (en, R, "Today is %(f1_wday_label)s %(f1_month_label)s %(f1_day)d, %(f1_year)d").

nlp_datetime_g(LANG, G, date) :-
    G is [

        ias(I, currentTime, TS),

        setz(ias(I, f1_type,   _), question),
        setz(ias(I, f1_topic,  _), date),

        stamp_date_time(TS, date(T_Y,T_M,T_D,T_H,T_MIN,T_S,'local')),

        day_of_the_week (TS, T_WD),

        nlp_day_of_the_week_label(LANG, T_WD, T_WD_LABEL),
        nlp_month_label(LANG, T_M, T_M_LABEL),

        setz(ias(I, f1_wday_label,  _), T_WD_LABEL),
        setz(ias(I, f1_day,         _), T_D),
        setz(ias(I, f1_month_label, _), T_M_LABEL),
        setz(ias(I, f1_year,        _), T_Y)

        ].

nlp_datetime (LANG, S, G, R, start, date) :-

    self_address(LANG, S, LABEL),
    nlp_datetime_s(LANG, S, date),

    nlp_datetime_g(LANG, G, date),

    nlp_datetime_r(LANG, R).

nlp_datetime_train_date_ts_large(X) :- between(1,31,D), date_time_stamp(date(2017,  1, D, 10, 0, 0, 'local'), X).
nlp_datetime_train_date_ts_large(X) :- between(1,28,D), date_time_stamp(date(2017,  2, D, 10, 0, 0, 'local'), X).
nlp_datetime_train_date_ts_large(X) :- between(1,31,D), date_time_stamp(date(2017,  3, D, 10, 0, 0, 'local'), X).
nlp_datetime_train_date_ts_large(X) :- between(1,30,D), date_time_stamp(date(2017,  4, D, 10, 0, 0, 'local'), X).
nlp_datetime_train_date_ts_large(X) :- between(1,31,D), date_time_stamp(date(2017,  5, D, 10, 0, 0, 'local'), X).
nlp_datetime_train_date_ts_large(X) :- between(1,30,D), date_time_stamp(date(2017,  6, D, 10, 0, 0, 'local'), X).
nlp_datetime_train_date_ts_large(X) :- between(1,31,D), date_time_stamp(date(2017,  7, D, 10, 0, 0, 'local'), X).
nlp_datetime_train_date_ts_large(X) :- between(1,31,D), date_time_stamp(date(2017,  8, D, 10, 0, 0, 'local'), X).
nlp_datetime_train_date_ts_large(X) :- between(1,30,D), date_time_stamp(date(2017,  9, D, 10, 0, 0, 'local'), X).
nlp_datetime_train_date_ts_large(X) :- between(1,31,D), date_time_stamp(date(2017, 10, D, 10, 0, 0, 'local'), X).
nlp_datetime_train_date_ts_large(X) :- between(1,30,D), date_time_stamp(date(2017, 11, D, 10, 0, 0, 'local'), X).
nlp_datetime_train_date_ts_large(X) :- between(1,31,D), date_time_stamp(date(2017, 12, D, 10, 0, 0, 'local'), X).

nlp_datetime_train_date_ts_small(X) :- date_time_stamp(date(2017, 6, 12,  5, 30, 0, 'local'), X).
nlp_datetime_train_date_ts_small(X) :- date_time_stamp(date(2017, 2,  8, 12, 15, 0, 'local'), X).

nlp_datetime_train_date_ts(X) :- 
    debug_mode('dt'),
    nlp_datetime_train_date_ts_small(X), !.
    
nlp_datetime_train_date_ts(X) :- 
    nlp_datetime_train_date_ts_large(X).

nlp_train('dt', en, [P1, S1, G1, R1]) :-

    nlp_datetime_train_date_ts(TS1),

    P1 is [ setz(ias(I, currentTime, _), TS1) ],

    nlp_datetime (en, S1, G1, R1, start, date)
    .

nlp_test('dt', en, 'date1', 
         [ date_time_stamp(date(2017, 6, 12, 5, 30, 0, 'local'), TS),
           setz(ias(I, currentTime, _), TS) ],
         ["what date is it", "Today is Monday, June 12 2017.", []]).

%
% multi-round date questions
%

nlp_datetime (LANG, S, G, R, followup, date) :-

    % self_address(LANG, S, LABEL),
    nlp_sayagain_s(LANG, S),

    G is [],

    nlp_isaid_r (LANG, R),
    nlp_datetime_r(LANG, R).

nlp_datetime_r(en, R, datetopic) :- says (en, R, "We were talking about the date").
nlp_datetime_r(en, R, datetopic) :- says (en, R, "The date was our topic").

nlp_datetime (LANG, S, G, R, followup, date) :-

    % self_address(LANG, S, LABEL),
    nlp_whatwasourtopic_s(LANG, S),

    G is [],

    nlp_datetime_r(en, R, datetopic).

nlp_train('dt', en, [P1, S1, G1, R1, P2, S2, G2, R2]) :-

    nlp_datetime_train_date_ts_small(TS1),

    P1 is [ setz(ias(I, currentTime, _), TS1) ],
    P2 is P1,

    nlp_datetime (en, S1, G1, R1, start, date),

    nlp_datetime (en, S2, G2, R2, followup, date)
    .

nlp_test('dt', en, 'date3', 
         [ date_time_stamp(date(2017, 6, 12, 5, 30, 0, 'local'), TS),
           setz(ias(I, currentTime, _), TS) ],
         ["what date is it", "Today is Monday, June 12 2017.", [],
          "huh?", "I said Today is Monday, June 12 2017.", []]).

nlp_test('dt', en, 'date4', 
         [ date_time_stamp(date(2017, 6, 12, 5, 30, 0, 'local'), TS),
           setz(ias(I, currentTime, _), TS) ],
         ["what date is it", "Today is Monday, June 12 2017.", [],
          "what was our topic?", "We were talking about the date.", []]).

