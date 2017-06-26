% prolog

% this will switch to much smaller training sets so we can keep 
% debug turn-around cycle times low
% debug_mode('dt').


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

