% prolog

answer(greeting, en, personal) :-
    action(attention, on), say_eoa(en, "Hello!"),
    action(attention, on), say_eoa(en, "Hi!"),
    action(attention, on), say_eoa(en, "Greetings!"),
    action(attention, on), say_eoa(en, "Hey!").
answer(greeting, de, personal) :-
    action(attention, on), say_eoa(de, "Hallo!"),
    action(attention, on), say_eoa(de, "Hi!"),
    action(attention, on), say_eoa(de, "Grüß Dich!"),
    action(attention, on), say_eoa(de, "Hey!").

answer(greeting, en, anonymous) :-
    rdf(ai:curin, ai:currentTime, TS),
    before_noon(TS),
    action(attention, on),
    say_eoa(en, "Good Morning!").
answer(greeting, de, anonymous) :-
    rdf(ai:curin, ai:currentTime, TS),
    before_noon(TS),
    action(attention, on),
    say_eoa(de, "Guten Morgen!").

answer(greeting, en, anonymous) :-
    rdf(ai:curin, ai:currentTime, TS),
    before_evening(TS),
    after_noon(TS),
    action(attention, on),
    say_eoa(en, "Good Day to you!"),
    action(attention, on),
    say_eoa(en, "Hello!").
answer(greeting, de, anonymous) :-
    rdf(ai:curin, ai:currentTime, TS),
    before_evening(TS),
    after_noon(TS),
    action(attention, on),
    say_eoa(de, "Guten Tag!"),
    action(attention, on),
    say_eoa(de, "Hallo!").

answer(greeting, en, anonymous) :-
    rdf(ai:curin, ai:currentTime, TS),
    after_evening(TS),
    action(attention, on),
    say_eoa(en, "Good Evening!").
answer(greeting, de, anonymous) :-
    rdf(ai:curin, ai:currentTime, TS),
    after_evening(TS),
    action(attention, on),
    say_eoa(de, "Guten Abend!").

answer(goodbye, en, anonymous) :-
    action(attention,off),
    say_eoa(en, "Goodbye!").
answer(goodbye, de, anonymous) :-
    action(attention,off),
    say_eoa(de, "Auf Wiedersehen!").

answer(goodbye, en, personal) :-
    action(attention, off), say_eoa(en, "Bye"),
    action(attention, off), say_eoa(en, "So long"),
    action(attention, off), say_eoa(en, "See you later"),
    action(attention, off), say_eoa(en, "Bye for now").
answer(goodbye, de, personal) :-
    action(attention, off), say_eoa(de, "Ade"),
    action(attention, off), say_eoa(de, "Tschüss"),
    action(attention, off), say_eoa(de, "Bis bald"),
    action(attention, off), say_eoa(de, "Ciao").


nlp_gen (en, '(greetings| good morning | hello | hallo | hi | good day | morning | good evening | good night | Cooee| Cooey | hi there)',
             answer (greeting, en, anonymous)).
nlp_gen (en, '@SELF_ADDRESS_EN_NE:LABEL (greetings| good morning | hello | hallo | hi | good day | morning | good evening | good night | Cooee| Cooey | hi there)',
             answer (greeting, en, personal)).
nlp_gen (en, '(greetings| good morning | hello | hallo | hi | good day | morning | good evening | good night | Cooee| Cooey | hi there) @SELF_ADDRESS_EN_NE:LABEL',
             answer (greeting, en, personal)).
nlp_gen (de, '(grüß dich|guten morgen | hallo | hi | guten tag | tag | morgen | guten abend | gute nacht | huhu)',
             answer (greeting, de, anonymous)).
nlp_gen (de, '@SELF_ADDRESS_DE_NE:LABEL (grüß dich|guten morgen | hallo | hi | guten tag | tag | morgen | guten abend | gute nacht | huhu)',
             answer (greeting, de, personal)).
nlp_gen (de, '(grüß dich|guten morgen | hallo | hi | guten tag | tag | morgen | guten abend | gute nacht | huhu) @SELF_ADDRESS_DE_NE:LABEL',
             answer (greeting, de, personal)).


nlp_gen (en, '(goobye | bye | ciao | so long | bye for now | see ya | see you later | till next time)',
             answer (goodbye, en, anonymous)).
nlp_gen (en, '@SELF_ADDRESS_EN_NE:LABEL (goobye | bye | ciao | so long | bye for now | see ya | see you later | till next time)',
             answer (goodbye, en, personal)).
nlp_gen (en, '(goobye | bye | ciao | so long | bye for now | see ya | see you later | till next time) @SELF_ADDRESS_EN_NE:LABEL',
             answer (goodbye, en, personal)).
nlp_gen (de, '(auf wiedersehen | tschüss | ciao | ade | bye | cu | bis bald | bis zum nächsten mal)',
             answer (goodbye, de, anonymous)).
nlp_gen (de, '@SELF_ADDRESS_DE_NE:LABEL (auf wiedersehen | tschüss | ciao | ade | bye | cu | bis bald | bis zum nächsten mal)',
             answer (goodbye, de, personal)).
nlp_gen (de, '(auf wiedersehen | tschüss | ciao | ade | bye | cu | bis bald | bis zum nächsten mal) @SELF_ADDRESS_DE_NE:LABEL',
             answer (goodbye, de, personal)).



nlp_test(en,
         ivr(in('hi'),
             out('hello!'),
             action(attention, on))).
nlp_test(de,
         ivr(in('hi'),
             out('Hallo!'),
             action(attention, on))).

nlp_test(en,
         ivr(in('computer hello'),
             out('Hi!'),
             action(attention, on))).
nlp_test(de,
         ivr(in('computer hallo'),
             out('Hi!'),
             action(attention, on))).

nlp_test(en,
         ivr(in('bye computer'),
             out('bye'),
             action(attention, off))).
nlp_test(de,
         ivr(in('Tschüss computer'),
             out('Tschüss!'),
             action(attention, off))).

nlp_test(en,
         ivr(in('bye'),
             out('goodbye'),
             action(attention, off))).
nlp_test(de,
         ivr(in('Ciao'),
             out('Auf Wiedersehen!'),
             action(attention, off))).

answer(howdy, en) :-
    say_eoa(en, "Great, thanks. How do you feel today?"),
    say_eoa(en, "Very well - and you?"),
    say_eoa(en, "I am doing great, how are you doing?"),
    say_eoa(en, "Great as always!"),
    say_eoa(en, "Thanks for asking, I am doing fine. How about you?").

answer(howdy, de) :-
    say_eoa(de, "Sehr gut, danke. Und selber?"),
    say_eoa(de, "Gut, danke. Wie geht es Dir?"),
    say_eoa(de, "Mir geht's prima, und Dir?"),
    say_eoa(de, "Mir geht's gut, und selber?"),
    say_eoa(de, "Super, wie immer!"),
    say_eoa(de, "Gut, danke der Nachfrage. Wie geht es Dir?").

nlp_gen(en,'@SELF_ADDRESS_EN:LABEL (how are you|howdy|how do you do|how are you feeling today)?',
           answer (howdy, en)).
nlp_gen(de,'@SELF_ADDRESS_DE:LABEL (wie geht es dir|wie gehts|was geht|wie fühlst du dich)?',
           answer (howdy, de)).

