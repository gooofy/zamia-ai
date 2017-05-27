%prolog

answerz (I, en, yes)   :- sayz(I, en, "Yes").
answerz (I, en, yes)   :- sayz(I, en, "Sure").
answerz (I, de, yes)   :- sayz(I, de, "Ja").
answerz (I, de, yes)   :- sayz(I, de, "Ja klar").

l4proc (I, F, fnAffirmOrDeny) :-

    frame (F, act, affirm),

    ias (I, uttLang, LANG),

    scorez(I, 10),

    answerz (I, LANG, yes).

l4proc (I, F, fnAffirmOrDeny) :-

    frame (F, act, affirm),

    ias (I, uttLang, LANG),

    answerz (I, LANG, yes),

    frame (F,    msg,  MSGF),
    frame (MSGF, type, MSGFT),

    scorez(I, 20),

    l4proc (I, MSGF, MSGFT).

