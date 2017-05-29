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
 
answerz (I, en, hello) :- sayz(I, en, "Hello!").
answerz (I, en, hello) :- sayz(I, en, "Hi!").
answerz (I, en, hello) :- sayz(I, en, "Greetings!").
answerz (I, en, hello) :- sayz(I, en, "Hey!").

answerz (I, de, hello) :- sayz(I, de, "Hallo!").
answerz (I, de, hello) :- sayz(I, de, "Hi!").
answerz (I, de, hello) :- sayz(I, de, "Grüß Dich!").
answerz (I, de, hello) :- sayz(I, de, "Hey!").

l4proc (I, F, pbGreet01) :-

    SELF is uriref(aiu:self),
    frame(F, arg0,     SELF),

    ias (I, uttLang, LANG),

    answerz (I, LANG, hello),
    
    assertz (ias(I, action, attention(on))).

l3proc (I, F, pbGreet01) :-

    SELF is uriref(aiu:self),
    frame(F, arg1, SELF),

    % remember our utterance interpretation

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: greet user)
    
    ias(I, user, USER),
    list_append(VMC, fe(arg1,    USER)),
    list_append(VMC, fe(arg0,    SELF)),
    list_append(VMC, frame(pbGreet01)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 100),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    l4proc (I).

l2proc_greeting(LANG) :-

    list_append(VMC, fe(arg1,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(arg0, USER)),
    list_append(VMC, frame(pbGreet01)),

    fnvm_exec (I, VMC).
   

nlp_gen(en, '@SELF_ADDRESS:LABEL (greetings| good morning | hello | hallo | hi | good day | morning | good evening | good night | Cooee| Cooey | hi there)',
        inline(l2proc_greeting, en)).
nlp_gen(en, '(greetings| good morning | hello | hallo | hi | good day | morning | good evening | good night | Cooee| Cooey | hi there) @SELF_ADDRESS:LABEL',
        inline(l2proc_greeting, en)).
nlp_gen(de, '@SELF_ADDRESS:LABEL (grüß dich|guten morgen | hallo | hi | guten tag | tag | morgen | guten abend | gute nacht | huhu)',
        inline(l2proc_greeting, en)).
nlp_gen(de, '(grüß dich|guten morgen | hallo | hi | guten tag | tag | morgen | guten abend | gute nacht | huhu) @SELF_ADDRESS:LABEL',
        inline(l2proc_greeting, en)).

answerz (I, en, bye) :- sayz(I, en, "Bye").
answerz (I, en, bye) :- sayz(I, en, "So long").
answerz (I, en, bye) :- sayz(I, en, "See you later").
answerz (I, en, bye) :- sayz(I, en, "Bye for now").

answerz (I, de, bye) :- sayz(I, de, "Ade").
answerz (I, de, bye) :- sayz(I, de, "Tschüss").
answerz (I, de, bye) :- sayz(I, de, "Bis bald").
answerz (I, de, bye) :- sayz(I, de, "Ciao").

l4proc (I, F, zfBye) :-

    SELF is uriref(aiu:self),
    frame(F, arg0,     SELF),

    ias (I, uttLang, LANG),

    answerz (I, LANG, bye),
    
    assertz (ias(I, action, attention(off))).

l3proc (I, F, zfBye) :-

    SELF is uriref(aiu:self),
    frame(F, arg1, SELF),

    % remember our utterance interpretation

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: greet user)
    
    ias(I, user, USER),
    list_append(VMC, fe(arg1,    USER)),
    list_append(VMC, fe(arg0,    SELF)),
    list_append(VMC, frame(zfBye)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 100),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    l4proc (I).

l2proc_bye(LANG) :-

    list_append(VMC, fe(arg1,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(arg0, USER)),
    list_append(VMC, frame(zfBye)),

    fnvm_exec (I, VMC).
   
nlp_gen (en, '@SELF_ADDRESS:LABEL (goobye | bye | ciao | so long | bye for now | see ya | see you later | till next time)',
        inline(l2proc_bye, en)).
nlp_gen (en, '(goobye | bye | ciao | so long | bye for now | see ya | see you later | till next time) @SELF_ADDRESS:LABEL',
        inline(l2proc_bye, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (auf wiedersehen | tschüss | ciao | ade | bye | cu | bis bald | bis zum nächsten mal)',
        inline(l2proc_bye, de)).
nlp_gen (de, '(auf wiedersehen | tschüss | ciao | ade | bye | cu | bis bald | bis zum nächsten mal) @SELF_ADDRESS:LABEL',
        inline(l2proc_bye, de)).

nlp_test(en,
         ivr(in('hi'),
             out('hello!'),
             action(attention(on)))).
nlp_test(de,
         ivr(in('hi'),
             out('Hallo!'),
             action(attention(on)))).

nlp_test(en,
         ivr(in('computer hello'),
             out('Hi!'),
             action(attention(on)))).
nlp_test(de,
         ivr(in('computer hallo'),
             out('Hi!'),
             action(attention(on)))).

nlp_test(en,
         ivr(in('bye computer'),
             out('bye'),
             action(attention(off)))).
nlp_test(de,
         ivr(in('Tschüss computer'),
             out('Tschüss!'),
             action(attention(off)))).

nlp_test(en,
         ivr(in('bye'),
             out('so long'),
             action(attention(off)))).
nlp_test(de,
         ivr(in('Ciao'),
             out('Bis bald'),
             action(attention(off)))).

answerz (I, en, howdy) :- sayz(I, en, "Great, thanks. How do you feel today?").
answerz (I, en, howdy) :- sayz(I, en, "Very well - and you?").
answerz (I, en, howdy) :- sayz(I, en, "I am doing great, how are you doing?").
answerz (I, en, howdy) :- sayz(I, en, "Great as always!").
answerz (I, en, howdy) :- sayz(I, en, "Thanks for asking, I am doing fine. How about you?").
answerz (I, de, howdy) :- sayz(I, de, "Sehr gut, danke. Und selber?").
answerz (I, de, howdy) :- sayz(I, de, "Gut, danke. Wie geht es Dir?").
answerz (I, de, howdy) :- sayz(I, de, "Mir geht es prima, und Dir?").
answerz (I, de, howdy) :- sayz(I, de, "Mir geht es gut, und selber?").
answerz (I, de, howdy) :- sayz(I, de, "Super, wie immer!").
answerz (I, de, howdy) :- sayz(I, de, "Gut, danke der Nachfrage. Wie geht es Dir?").

l4proc (I, F, zfHowdy) :-

    SELF is uriref(aiu:self),
    frame(F, arg0,     SELF),

    ias (I, uttLang, LANG),

    answerz (I, LANG, howdy).

l3proc (I, F, zfHowdy) :-

    SELF is uriref(aiu:self),
    frame(F, arg1, SELF),

    % remember our utterance interpretation

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: greet user)
    
    ias(I, user, USER),
    list_append(VMC, fe(arg1,    USER)),
    list_append(VMC, fe(arg0,    SELF)),
    list_append(VMC, frame(zfHowdy)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 100),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    l4proc (I).

l2proc_howdy(LANG) :-

    list_append(VMC, fe(arg1,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(arg0, USER)),
    list_append(VMC, frame(zfHowdy)),

    fnvm_exec (I, VMC).
   
nlp_gen(en,'@SELF_ADDRESS:LABEL (how are you|howdy|how do you do|how are you feeling) (today|)?',
        inline(l2proc_howdy, en)).
nlp_gen(de,'@SELF_ADDRESS:LABEL (wie geht es dir|wie gehts|was geht|wie fühlst du dich) (heute|)?',
        inline(l2proc_howdy, de)).

nlp_test(en,
         ivr(in('Computer, how are you?'),
             out('very well and you?'))).
nlp_test(de,
         ivr(in('Computer, wie geht es dir?'),
             out('Super, wie immer!'))).

