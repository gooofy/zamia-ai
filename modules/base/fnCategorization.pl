%prolog

%
% tell user about item categorization
%

% fixme: nicer wording for specific cases, e.g. humans
answerz (I, en, category, I_LABEL, C_LABEL)  :- sayz(I, en, format_str("%s is categorized as %s", I_LABEL, C_LABEL) ).
answerz (I, de, category, I_LABEL, C_LABEL)  :- sayz(I, de, format_str("%s ist in der Kategorie %s", I_LABEL, C_LABEL) ).

l4proc (I, F, fnTelling, category, MSGF, fnCategorization) :-

    % trace(on),

    frame (MSGF, item, ITEM),
    frame (MSGF, cat,  CAT),    

    ias (I, uttLang, LANG),

    entity_label(LANG, ITEM, I_LABEL),
    entity_label(LANG, CAT,  C_LABEL),

    answerz (I, LANG, category, I_LABEL, C_LABEL ).

