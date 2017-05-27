%prolog

% macros listing all known entities with their LABELs

% nlp_macro (en, 'KNOWN_ENTITIES', ENTITY, LABEL, LABELS) :-
%     rdf (distinct,
%          ENTITY, rdfs:label,        LABEL,
%          filter (lang(LABEL) = 'en')),
%     LABELS is format_str("%s's", LABEL).
% 
% nlp_macro (de, 'KNOWN_ENTITIES', ENTITY, LABEL) :-
%     rdf (distinct,
%          ENTITY, rdfs:label,        LABEL,
%          filter (lang(LABEL) = 'de')).


l3proc (I, F, fnQuestioning, MSGF, fnFamiliarity) :-

    frame (F,    top,        existance),

    % FIXME: ? ias(I, uCog,        uriref(aiu:self)),
    uriref (aiu:self, SELF),
    frame (MSGF, cog,        SELF),

    % check if we have an ENT result (which implies we are familiar with this entity)

    frame (MSGF, ent,        ENT),
    frame (MSGF, entclass,   ENTCLASS),

    % remember our utterance interpretation

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: confirmation)
    
    list_append(VMC, fe(msg,  MSGF)),
    list_append(VMC, fe(top,  existance)),
    list_append(VMC, fe(act,  affirm)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,  USER)),
    list_append(VMC, fe(spkr, uriref(aiu:self))),
    list_append(VMC, frame(fnAffirmOrDeny)),

    fnvm_graph(VMC, RFRAME),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    l4proc (I).

answerz (I, en, iAmFamiliar, LABEL) :- sayz(I, en, format_str("I know %s", LABEL)).
answerz (I, en, iAmFamiliar, LABEL) :- sayz(I, en, format_str("%s sounds familiar", LABEL)).
answerz (I, de, iAmFamiliar, LABEL) :- sayz(I, en, format_str("Ich kenne %s", LABEL)).
answerz (I, de, iAmFamiliar, LABEL) :- sayz(I, en, format_str("%s ist mir ein Begriff", LABEL)).

l4proc (I, F, fnFamiliarity) :-

    frame (MSGF, ent,        ENT),
    uriref (aiu:self, SELF),
    frame (MSGF, cog,        SELF),

    ias (I, uttLang, LANG),

    entity_label(LANG, ENT, LABEL),

    answerz (I, LANG, iAmFamiliar, LABEL).

