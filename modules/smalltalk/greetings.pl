% prolog

% 
% answer(greeting, en, anonymous) :-
%     rdf(ai:curin, ai:currentTime, TS),
%     before_noon(TS),
%     action(attention, on),
%     say_eoa(en, "Good Morning!").
% answer(greeting, de, anonymous) :-
%     rdf(ai:curin, ai:currentTime, TS),
%     before_noon(TS),
%     action(attention, on),
%     say_eoa(de, "Guten Morgen!").
% 
% answer(greeting, en, anonymous) :-
%     rdf(ai:curin, ai:currentTime, TS),
%     before_evening(TS),
%     after_noon(TS),
%     action(attention, on),
%     say_eoa(en, "Good Day to you!"),
%     action(attention, on),
%     say_eoa(en, "Hello!").
% answer(greeting, de, anonymous) :-
%     rdf(ai:curin, ai:currentTime, TS),
%     before_evening(TS),
%     after_noon(TS),
%     action(attention, on),
%     say_eoa(de, "Guten Tag!"),
%     action(attention, on),
%     say_eoa(de, "Hallo!").
% 
% answer(greeting, en, anonymous) :-
%     rdf(ai:curin, ai:currentTime, TS),
%     after_evening(TS),
%     action(attention, on),
%     say_eoa(en, "Good Evening!").
% answer(greeting, de, anonymous) :-
%     rdf(ai:curin, ai:currentTime, TS),
%     after_evening(TS),
%     action(attention, on),
%     say_eoa(de, "Guten Abend!").
% 
% answer(goodbye, en, anonymous) :-
%     action(attention,off),
%     say_eoa(en, "Goodbye!").
% answer(goodbye, de, anonymous) :-
%     action(attention,off),
%     say_eoa(de, "Auf Wiedersehen!").

%
% hello
%

nlp_greetings_s (en, hello, S) :- hears (en, S, 'greetings').
nlp_greetings_s (en, hello, S) :- hears (en, S, 'good morning').
nlp_greetings_s (en, hello, S) :- hears (en, S, 'hello').
nlp_greetings_s (en, hello, S) :- hears (en, S, 'hallo').
nlp_greetings_s (en, hello, S) :- hears (en, S, 'hi').
nlp_greetings_s (en, hello, S) :- hears (en, S, 'good day').
nlp_greetings_s (en, hello, S) :- hears (en, S, 'morning').
nlp_greetings_s (en, hello, S) :- hears (en, S, 'good evening').
nlp_greetings_s (en, hello, S) :- hears (en, S, 'good night').
nlp_greetings_s (en, hello, S) :- hears (en, S, 'Cooee').
nlp_greetings_s (en, hello, S) :- hears (en, S, 'Cooey').
nlp_greetings_s (en, hello, S) :- hears (en, S, 'hi there').

nlp_greetings_s (de, hello, S) :- hears (de, S, 'grüß dich').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'hallo').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'hi').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'guten morgen').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'guten tag').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'guten abend').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'guten nachmittag').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'gute nacht').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'schönen guten morgen').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'schönen guten tag').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'schönen guten abend').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'schönen guten nachmittag').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'gute nacht').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'tag').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'morgen').
nlp_greetings_s (de, hello, S) :- hears (de, S, 'huhu').

nlp_greetings_r (en, hello, R) :- acts(R, attention(on)), says (en, R, "Hello!").
nlp_greetings_r (en, hello, R) :- acts(R, attention(on)), says (en, R, "Hi!").
nlp_greetings_r (en, hello, R) :- acts(R, attention(on)), says (en, R, "Greetings!").
nlp_greetings_r (en, hello, R) :- acts(R, attention(on)), says (en, R, "Hey!").

nlp_greetings_r (de, hello, R) :- acts(R, attention(on)), says (de, R, "Hallo!").
nlp_greetings_r (de, hello, R) :- acts(R, attention(on)), says (de, R, "Hi!").
nlp_greetings_r (de, hello, R) :- acts(R, attention(on)), says (de, R, "Grüß Dich!").
nlp_greetings_r (de, hello, R) :- acts(R, attention(on)), says (de, R, "Hey!").

nlp_train('smalltalk', en, [[], S1, [], R1]) :-
    self_address(en, S1, _),
    nlp_greetings_s (en, hello, S1),
    nlp_greetings_r (en, hello, R1).
nlp_train('smalltalk', de, [[], S1, [], R1]) :-
    self_address(de, S1, _),
    nlp_greetings_s (de, hello, S1),
    nlp_greetings_r (de, hello, R1).

nlp_test('smalltalk', en, 'hello1', [],
         ['Hi!', 'hello!', [attention(on)]]).
nlp_test('smalltalk', de, 'hello2', [],
         ['Hi!', 'hallo!', [attention(on)]]).
nlp_test('smalltalk', en, 'hello3', [],
         ['Computer, Hi!', 'hello!', [attention(on)]]).
nlp_test('smalltalk', de, 'hello4', [],
         ['Computer, Hi!', 'hallo!', [attention(on)]]).

%
% bye
%

nlp_greetings_s (en, goodbye, S) :- hears (en, S, 'goodbye').
nlp_greetings_s (en, goodbye, S) :- hears (en, S, 'bye').
nlp_greetings_s (en, goodbye, S) :- hears (en, S, 'ciao').
nlp_greetings_s (en, goodbye, S) :- hears (en, S, 'so long').
nlp_greetings_s (en, goodbye, S) :- hears (en, S, 'bye for now').
nlp_greetings_s (en, goodbye, S) :- hears (en, S, 'see ya').
nlp_greetings_s (en, goodbye, S) :- hears (en, S, 'see you later').
nlp_greetings_s (en, goodbye, S) :- hears (en, S, 'till next time').

nlp_greetings_s (de, goodbye, S) :- hears (de, S, 'auf wiedersehen').
nlp_greetings_s (de, goodbye, S) :- hears (de, S, 'tschüss').
nlp_greetings_s (de, goodbye, S) :- hears (de, S, 'ciao').
nlp_greetings_s (de, goodbye, S) :- hears (de, S, 'ade').
nlp_greetings_s (de, goodbye, S) :- hears (de, S, 'bye').
nlp_greetings_s (de, goodbye, S) :- hears (de, S, 'cu').
nlp_greetings_s (de, goodbye, S) :- hears (de, S, 'bis bald').
nlp_greetings_s (de, goodbye, S) :- hears (de, S, 'bis zum nächsten mal').

nlp_greetings_r (en, goodbye, R) :- acts(R, attention(off)), says (en, R, "Bye").
nlp_greetings_r (en, goodbye, R) :- acts(R, attention(off)), says (en, R, "So long").
nlp_greetings_r (en, goodbye, R) :- acts(R, attention(off)), says (en, R, "See you later").
nlp_greetings_r (en, goodbye, R) :- acts(R, attention(off)), says (en, R, "Bye for now").

nlp_greetings_r (de, goodbye, R) :- acts(R, attention(off)), says (de, R, "Ade").
nlp_greetings_r (de, goodbye, R) :- acts(R, attention(off)), says (de, R, "Tschüss").
nlp_greetings_r (de, goodbye, R) :- acts(R, attention(off)), says (de, R, "Bis bald").
nlp_greetings_r (de, goodbye, R) :- acts(R, attention(off)), says (de, R, "Ciao").

nlp_train('smalltalk', en, [[], S1, [], R1]) :-
    nlp_greetings_s (en, goodbye, S1),
    self_address(en, S1, _),
    nlp_greetings_r (en, goodbye, R1).
nlp_train('smalltalk', de, [[], S1, [], R1]) :-
    nlp_greetings_s (de, goodbye, S1),
    self_address(de, S1, _),
    nlp_greetings_r (de, goodbye, R1).

nlp_test('smalltalk', en, 'goodbye1', [],
         ['bye!', 'bye', [attention(off)]]).
nlp_test('smalltalk', de, 'goodbye2', [],
         ['Tschüss computer!', 'Tschüss!', [attention(off)]]).

%
% howdy
%

nlp_greetings_s (en, howdy, S) :- hears (en, S, [["how are you","howdy","how do you do","how are you feeling"], ["today",""], "?"]).
nlp_greetings_s (de, howdy, S) :- hears (de, S, [["wie geht es dir","wie gehts","was geht","wie fühlst du dich"], ["heute",""], "?"]).

nlp_greetings_r (en, howdy, R) :- says (en, R, "Great, thanks. How do you feel today?").
nlp_greetings_r (en, howdy, R) :- says (en, R, "Very well - and you?").
nlp_greetings_r (en, howdy, R) :- says (en, R, "I am doing great, how are you doing?").
nlp_greetings_r (en, howdy, R) :- says (en, R, "Great as always!").
nlp_greetings_r (en, howdy, R) :- says (en, R, "Thanks for asking, I am doing fine. How about you?").

nlp_greetings_r (de, howdy, R) :- says (de, R, "Sehr gut, danke. Und selber?").
nlp_greetings_r (de, howdy, R) :- says (de, R, "Gut, danke. Wie geht es Dir?").
nlp_greetings_r (de, howdy, R) :- says (de, R, "Mir geht es prima, und Dir?").
nlp_greetings_r (de, howdy, R) :- says (de, R, "Mir geht es gut, und selber?").
nlp_greetings_r (de, howdy, R) :- says (de, R, "Super, wie immer!").
nlp_greetings_r (de, howdy, R) :- says (de, R, "Gut, danke der Nachfrage. Wie geht es Dir?").

nlp_train('smalltalk', en, [[], S1, [], R1]) :-
    self_address(en, S1, _),
    nlp_greetings_s (en, howdy, S1),
    nlp_greetings_r (en, howdy, R1).
nlp_train('smalltalk', de, [[], S1, [], R1]) :-
    self_address(de, S1, _),
    nlp_greetings_s (de, howdy, S1),
    nlp_greetings_r (de, howdy, R1).

nlp_test('smalltalk', en, 'howdy1', [],
         ['Computer, how are you?', 'very well and you?', []]).
nlp_test('smalltalk', de, 'howdy2', [],
         ['Computer, wie geht es Dir?', 'Super, wie immer!', []]).

