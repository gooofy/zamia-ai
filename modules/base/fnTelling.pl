% prolog

%
% map telling with known msg frame to 2-layer l3proc search
%

l3proc (I, F, fnTelling) :-

    % look for message frame + type, run l3proc on it

    frame(F, msg, MSGF),
    frame(MSGF, type, MSGFT),

    l3proc (I, F, fnTelling, MSGF, MSGFT).

%
% tell user we don't know
%

answerz (I, en, iDontKnow) :- sayz(I, en, "Sorry, I don't know").
answerz (I, en, iDontKnow) :- sayz(I, en, "I am not sure").
answerz (I, en, iDontKnow) :- sayz(I, en, "I am not aware of that, sorry").
answerz (I, en, iDontKnow) :- sayz(I, en, "Please help me out here").

answerz (I, de, iDontKnow) :- sayz(I, de, "Das weiss ich leider nicht.").
answerz (I, de, iDontKnow) :- sayz(I, de, "Da bin ich mir nicht sicher").
answerz (I, de, iDontKnow) :- sayz(I, de, "Da ist mir leider nichts bewusst.").
answerz (I, de, iDontKnow) :- sayz(I, de, "Bitte hilf mir auf die Sprünge").

l4proc (I, F, fnTelling, topic, MSGF, fnAwareness) :-

    uriref (aiu:self, SELF),
    frame (F,    spkr, SELF),
    frame (MSGF, cog,  SELF),
    frame (MSGF, degr, none),

    ias (I, uttLang, LANG),

    answerz (I, LANG, iDontKnow).

%
% tell user about the topic of a recent conversation
%

answerz (I, en, recentTopicOfConversionWas, LABEL) :- sayz(I, en, format_str("I think we have been talking about %s", LABEL)).
answerz (I, en, recentTopicOfConversionWas, LABEL) :- sayz(I, en, format_str("Didn't we talk about %s ?", LABEL)).

answerz (I, de, recentTopicOfConversionWas, LABEL) :- sayz(I, de, format_str("Ich glaube wir hatten über %s gesprochen", LABEL)).
answerz (I, de, recentTopicOfConversionWas, LABEL) :- sayz(I, de, format_str("Hatten wir es nicht von %s ?", LABEL)).

l4proc (I, F, fnTelling, topic, MSGF, fnCommunication) :-

    uriref (aiu:self, SELF),
    frame (F,    spkr, SELF),
    frame (MSGF, time, recently),
    frame (MSGF, com,  we),
    frame (MSGF, top,  entity),

    ias (I, uttLang, LANG),

    scorez(I, 100),

    frame (MSGF, msg, ENTITY),
    entity_label (LANG, ENTITY, LABEL),

    answerz (I, LANG, recentTopicOfConversionWas, LABEL).

