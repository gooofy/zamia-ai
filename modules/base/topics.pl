% prolog

%
% very basic building blocks for topic handling
%

% answer(topic, en) :-
%     say_eoa(en, 'We have had many topics.'), 
%     say_eoa(en, 'We were talking about you for the most part, I believe.').
% 
% answer(topic, de) :-
%     say_eoa(de, 'Wir hatten schon viele Themen.'), 
%     say_eoa(de, 'Ich glaube vor allem über Dich!').
% 
% answer(topic, en) :-
%     context_score(topic, ENTITY, 100, S),
%     rdf (limit(1),
%          ENTITY, rdfs:label, LABEL,
%          filter (lang(LABEL) = 'en')),
%     say_eoa(en, format_str('We were talking about %s.', LABEL), S).
% 
% answer(topic, de) :-
%     context_score(topic, ENTITY, 100, S),
%     rdf (limit(1),
%          ENTITY, rdfs:label, LABEL,
%          filter (lang(LABEL) = 'de')),
%     say_eoa(de, format_str('Wir hatten über %s gesprochen.', LABEL), S).

answerz (I, en, weHaveBeenTalkingAbout, LABEL) :- sayz(I, en, format_str("We have been talking about %s", LABEL)).
answerz (I, en, weHaveBeenTalkingAbout, LABEL) :- sayz(I, en, format_str("Our topic was %s", LABEL)).
answerz (I, en, weHaveBeenTalkingAbout, LABEL) :- sayz(I, en, format_str("Didn't we talk about %s", LABEL)).

answerz (I, de, weHaveBeenTalkingAbout, LABEL) :- sayz(I, de, format_str("Wir hatten über %s gesprochen", LABEL)).
answerz (I, de, weHaveBeenTalkingAbout, LABEL) :- sayz(I, de, format_str("Unser Thema war %s", LABEL)).
answerz (I, de, weHaveBeenTalkingAbout, LABEL) :- sayz(I, de, format_str("Sprachen wir nicht über %s ?", LABEL)).

l4proc (LANG, I, F, fnTelling, topic, MSGF, fnCommunication) :-

    frame (MSGF, com,  we),
    frame (MSGF, top,  entity),    
    frame (MSGF, time, recently),    
    frame (MSGF, msg,  ENTITY),    

    entity_label(LANG, ENTITY, LABEL),

    answerz (I, LANG, weHaveBeenTalkingAbout, LABEL).

%
% look for entity we have been talking about with the user
%

l3proc (I, F, fnQuestioning) :-

    uriref (aiu:self, SELF),
    frame (F, add, SELF),
    frame (F, top, topic),
    not (frame (F, msg, MSGF)),

    log (info, "l3proc looking for fnQuestioning topic frame..."),

    context_search_l2(I, I, 8, 1, URFRAME, L1T, L1F, L1FE, L2FT, L2F),

    log (info, "l3proc looking for fnQuestioning topic frame... found one."),

    assertz (ias(I, score, 10)),

    % remember our utterance interpretation

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user about last topic entity)
    
    list_append(VMC, fe(msg,  L2F)),
    list_append(VMC, fe(top,  topic)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,  USER)),
    list_append(VMC, fe(spkr, uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    % trace(on),

    l4proc (I).

l2proc_whatWasOurTopic :-
    list_append(VMC, fe(top,  topic)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
   
    fnvm_exec (I, VMC).

nlp_gen(en, '@SELF_ADDRESS:LABEL What (were we talking|did we talk) about (again|)?', inline (l2proc_whatWasOurTopic)).
nlp_gen(en, '@SELF_ADDRESS:LABEL (Which|What) was our topic (again|)?', inline (l2proc_whatWasOurTopic)).
nlp_gen(en, '@SELF_ADDRESS:LABEL Give me a hint', inline (l2proc_whatWasOurTopic)).
nlp_gen(en, '@SELF_ADDRESS:LABEL Which topic did we have (again|)?', inline (l2proc_whatWasOurTopic)).
nlp_gen(en, '@SELF_ADDRESS:LABEL I (think|believe) I lost my train of thought (just now|).', inline (l2proc_whatWasOurTopic)).
nlp_gen(en, '@SELF_ADDRESS:LABEL (lets get|) Back to our topic', inline (l2proc_whatWasOurTopic)).

nlp_gen(de, '@SELF_ADDRESS:LABEL (Wovon|Worüber|Was) (hatten|haben) wir (eben|) gesprochen?', inline (l2proc_whatWasOurTopic)).
nlp_gen(de, '@SELF_ADDRESS:LABEL (Wie|Was) war (doch gleich|gleich|) unser Thema?', inline (l2proc_whatWasOurTopic)).
nlp_gen(de, '@SELF_ADDRESS:LABEL Hilf mir auf die Sprünge?', inline (l2proc_whatWasOurTopic)).
nlp_gen(de, '@SELF_ADDRESS:LABEL Welches Thema hatten wir (doch gleich|)?', inline (l2proc_whatWasOurTopic)).
nlp_gen(de, '@SELF_ADDRESS:LABEL Ich (glaub|glaube|) ich habe (jetzt|) den Faden verloren.', inline (l2proc_whatWasOurTopic)).
nlp_gen(de, '@SELF_ADDRESS:LABEL jetzt habe ich (glaube ich|) den Faden verloren.', inline (l2proc_whatWasOurTopic)).
nlp_gen(de, '@SELF_ADDRESS:LABEL also zurück zum thema', inline (l2proc_whatWasOurTopic)).

nlp_test(en,
         ivr(in('what did we talk about'),
             out("sorry i dont know"))
             ).

nlp_gen(en, '@SELF_ADDRESS:LABEL (uh|) now for a different subject!', 'What would you like to talk about?').
nlp_gen(de, '@SELF_ADDRESS:LABEL (ach|) (jetzt ein|mal ein|) anderes thema', 'Worüber möchtest Du sprechen?').

