%prolog

%
% named entity recognition (NER)
%

nlp_known_humans_debug_limit(10). % set to 0 for unlimited (production)

ner_learn_humans(LANG) :-
    atom_chars(LANG, LSTR),

    rdf_lists (distinct,
               HUMAN_ENTITIES, wdpd:InstanceOf,   wde:Human,
               HUMAN_ENTITIES, rdfs:label,        HUMAN_LABELS,
               filter (lang(HUMAN_LABELS) = LSTR)),

    ner_learn(LANG, human, HUMAN_ENTITIES, HUMAN_LABELS).

init('humans') :-
    ner_learn_humans(en),
    ner_learn_humans(de).

%
% macros listing all known humans with their LABELs
%

nlp_known_humans_s (en, S, HUMAN, LABEL, TSTART, TEND) :-
    nlp_known_humans_debug_limit(LIMIT),
    rdf (distinct, 
         limit(LIMIT),
         HUMAN, wdpd:InstanceOf,   wde:Human,
         HUMAN, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'en')),
    length(S, TSTART),
    hears (en, S, LABEL),
    length(S, TEND).
    
nlp_known_humans_gen_s (en, S, HUMAN, LABEL, TSTART, TEND) :-
    nlp_known_humans_debug_limit(LIMIT),
    rdf (distinct, 
         limit(LIMIT),
         HUMAN, wdpd:InstanceOf,   wde:Human,
         HUMAN, rdfs:label,        L,
         filter (lang(L) = 'en')),
    LABEL is format_str("%s's", L),
    length(S, TSTART),
    hears (en, S, LABEL),
    length(S, TEND).

nlp_known_humans_s (de, S, HUMAN, LABEL, TSTART, TEND) :-
    nlp_known_humans_debug_limit(LIMIT),
    rdf (distinct, 
         limit(LIMIT),
         HUMAN, wdpd:InstanceOf,   wde:Human,
         HUMAN, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')),
    length(S, TSTART),
    hears (de, S, LABEL),
    length(S, TEND).
    
%
% questions about humans known
%

nlp_knowHumanTokens_s (en, S, TSTART, TEND) :- hears (en, S, "do you know"),           nlp_known_humans_s (en, S, _, _, TSTART, TEND).
nlp_knowHumanTokens_s (en, S, TSTART, TEND) :- hears (en, S, "do you happen to know"), nlp_known_humans_s (en, S, _, _, TSTART, TEND).

nlp_knowHumanTokens_s (de, S, TSTART, TEND) :- hears (de, S, "kennst Du"),             nlp_known_humans_s (de, S, _, _, TSTART, TEND).
nlp_knowHumanTokens_s (de, S, TSTART, TEND) :- hears (de, S, "kennst Du eigentlich"),  nlp_known_humans_s (de, S, _, _, TSTART, TEND).

nlp_knowHumanTokens_r (en, R) :- says (en, R, "Sure I know %(f1_entlabel)s.").
nlp_knowHumanTokens_r (en, R) :- says (en, R, "Yes I know %(f1_entlabel)s.").
nlp_knowHumanTokens_r (de, R) :- says (de, R, "Klar kenne ich %(f1_entlabel)s.").
nlp_knowHumanTokens_r (de, R) :- says (de, R, "Ja ich kenne %(f1_entlabel)s.").

nlp_knowHumanTokens_g(LANG, G) :-
    G is [
        % trace(on),
        ner(LANG, I, NER1CLASS, TSTART, TEND, NER1ENTITY),

        setz(ias(I, f1_type,     _), question),
        setz(ias(I, f1_topic,    _), familiarity),
        setz(ias(I, f1_entclass, _), NER1CLASS),
        setz(ias(I, f1_ent,      _), NER1ENTITY),

        entity_label(LANG, NER1ENTITY, ENT1LABEL),

        setz(ias(I, f1_entlabel, _), ENT1LABEL)
        ].

nlp_train('humans', en, [[], S1, G1, R1]) :-

    self_address(en, S1, _),
    nlp_knowHumanTokens_s (en, S1, TSTART, TEND),

    nlp_knowHumanTokens_g (en, G1),

    nlp_knowHumanTokens_r (en, R1).

nlp_train('humans', de, [[], S1, G1, R1]) :-

    self_address(de, S1, _),
    nlp_knowHumanTokens_s (de, S1, TSTART, TEND),

    nlp_knowHumanTokens_g (de, G1),

    nlp_knowHumanTokens_r (de, R1).

nlp_test('humans', de, 'know1', [],
         ['Kennst Du Stephen King?', 'Ja ich kenne Stephen King', []]).
nlp_test('humans', en, 'know2', [],
         ['Do you know Stephen King?', 'Sure I know Stephen King', []]).

%
% if we don't know anything else, we can tell the user about the human's birthplace
%

nlp_whatabouttokens_g (LANG, G, TSTART, TEND) :-
    G is [
        % trace(on),
        ner(LANG, I, NER1CLASS, TSTART, TEND, NER1ENTITY),

        setz(ias(I, f1_type,     _), question),
        setz(ias(I, f1_topic,    _), familiarity),
        setz(ias(I, f1_entclass, _), NER1CLASS),
        setz(ias(I, f1_ent,      _), NER1ENTITY),

        entity_label(LANG, NER1ENTITY, ENT1LABEL),
        setz(ias(I, f1_entlabel, _), ENT1LABEL),

        rdf (distinct, limit(1),
             NER1ENTITY, wdpd:PlaceOfBirth, BIRTHPLACE),
        setz(ias(I, f1_loc, _), BIRTHPLACE),

        entity_label(LANG, BIRTHPLACE, BPLABEL),

        setz(ias(I, f1_loclabel, _), BPLABEL)
        ].

nlp_train('humans', en, [[], S1, G1, R1]) :-

    self_address(en, S1, _),
    hears (en, S1, [ [ "what about", "who is", "what is", "what do you know about", "what do you know of" ] ] ),
    nlp_known_humans_s (en, S1, _, _, TSTART, TEND),    

    nlp_whatabouttokens_g(en, G1, TSTART, TEND),

    says (en, R1, "%(f1_entlabel)s was born in %(f1_loclabel)s.").

nlp_train('humans', de, [[], S1, G1, R1]) :-

    self_address(de, S1, _),
    hears (de, S1, [ [ "wer ist", "wer ist eigentlich", "was ist mit", "was ist eigentlich mit", "was weisst du über", "was weisst du eigentlich über" ] ] ),
    nlp_known_humans_s (de, S1, _, _, TSTART, TEND),    

    nlp_whatabouttokens_g(de, G1, TSTART, TEND),

    says (de, R1, "%(f1_entlabel)s wurde in %(f1_loclabel)s geboren.").

nlp_test('humans', en, 'whatabout1', [],
         ['What about Stephen King?', 'Stephen King was born in Portland.', []]).
 
nlp_test('humans', de, 'whatabout2', [],
         ['Was ist mit Stephen King?', 'Stephen King wurde in Portland geboren.', []]).
 
% %
% % birthplace and birtdate questions
% %
% 
% l2proc_humanBornWhereTokens(LANG) :-
% 
%     ner(LANG, I, NER1CLASS, @KNOWN_HUMANS:TSTART_LABEL_0, @KNOWN_HUMANS:TEND_LABEL_0, NER1ENTITY),
% 
%     list_append(VMC, fe(child, NER1ENTITY)),
%     list_append(VMC, fe(childclass, NER1CLASS)),
%     list_append(VMC, frame(fnBeingBorn)),
%     
%     list_append(VMC, fe(msg,  vm_frame_pop)),
%     list_append(VMC, fe(top,  place)),
%     list_append(VMC, fe(add,  uriref(aiu:self))),
%     ias(I, user, USER),
%     list_append(VMC, fe(spkr, USER)),
%     list_append(VMC, frame(fnQuestioning)),
%     
%     fnvm_exec (I, VMC).
% 
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL (where|in which town|in which city) (was|is) @KNOWN_HUMANS:LABEL born?',
%          inline(l2proc_humanBornWhereTokens, en)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL (wo|in welcher stadt) (wurde|ist) (eigentlich|) @KNOWN_HUMANS:LABEL geboren?',
%          inline(l2proc_humanBornWhereTokens, de)).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL which is (the birthplace|place of birth) of @KNOWN_HUMANS:LABEL?',
%          inline(l2proc_humanBornWhereTokens, en)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL welches ist (eigentlich|) (der Geburtsort|die Geburtsstadt) von @KNOWN_HUMANS:LABEL?',
%          inline(l2proc_humanBornWhereTokens, de)).
% 
% l2proc_humanBornWhereContext :-
% 
%     list_append(VMC, frame(fnBeingBorn)),
%     
%     list_append(VMC, fe(msg,  vm_frame_pop)),
%     list_append(VMC, fe(top,  place)),
%     list_append(VMC, fe(add,  uriref(aiu:self))),
%     ias(I, user, USER),
%     list_append(VMC, fe(spkr, USER)),
%     list_append(VMC, frame(fnQuestioning)),
%    
%     % trace(on),
% 
%     fnvm_exec (I, VMC).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) (where|in which town|in which city) (was|is) (she|he) born (again|)?',
%          inline(l2proc_humanBornWhereContext)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) (wo|in welcher stadt) (wurde|ist) (eigentlich|) (er|sie) (nochmal|) geboren?',
%          inline(l2proc_humanBornWhereContext)).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) which is (the birthplace|place of birth) of (him|her) (again|)?',
%          inline(l2proc_humanBornWhereContext)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) welches ist (eigentlich|nochmal|) (der Geburtsort|die Geburtsstadt) von (ihm|ihr)?',
%          inline(l2proc_humanBornWhereContext)).
% 
% nlp_test(en,
%          ivr(in('Where was Angela Merkel born?'),
%              out('angela merkel was born in barmbek-nord')),
%          ivr(in('What were we talking about?'),
%              out('angela merkels birthday')),
%          ivr(in('and where was she born again?'),
%              out('angela merkel was born in barmbek-nord'))).
% nlp_test(de,
%          ivr(in('Wo wurde Angela Merkel geboren?'),
%              out('angela merkel wurde in barmbek-nord geboren')),
%          ivr(in('Welches Thema hatten wir?'),
%              out('angela merkels geburtstag.')),
%          ivr(in('und wo wurde sie nochmal geboren?'),
%              out('angela merkel wurde in barmbek-nord geboren'))).
% 
% 
% l2proc_humanBornWhenTokens(LANG) :-
% 
%     ner(LANG, I, NER1CLASS, @KNOWN_HUMANS:TSTART_LABEL_0, @KNOWN_HUMANS:TEND_LABEL_0, NER1ENTITY),
% 
%     list_append(VMC, fe(child, NER1ENTITY)),
%     list_append(VMC, fe(childclass, NER1CLASS)),
%     list_append(VMC, frame(fnBeingBorn)),
%     
%     list_append(VMC, fe(msg,  vm_frame_pop)),
%     list_append(VMC, fe(top,  time)),
%     list_append(VMC, fe(add,  uriref(aiu:self))),
%     ias(I, user, USER),
%     list_append(VMC, fe(spkr, USER)),
%     list_append(VMC, frame(fnQuestioning)),
%    
%     % trace(on),
% 
%     fnvm_exec (I, VMC).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL (when|in which year) (was|is) @KNOWN_HUMANS:LABEL born?',
%          inline(l2proc_humanBornWhenTokens, en)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL (wann|in welchem Jahr) (wurde|ist) (eigentlich|) @KNOWN_HUMANS:LABEL geboren?',
%          inline(l2proc_humanBornWhenTokens, de)).
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL (when is|on what day is) @KNOWN_HUMANS:LABELS birthday?",
%          inline(l2proc_humanBornWhenTokens, en)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL (wann hat|an welchem Tag hat) (eigentlich|) @KNOWN_HUMANS:LABEL Geburtstag?',
%          inline(l2proc_humanBornWhenTokens, de)).
% 
% l2proc_humanBornWhenContext :-
% 
%     list_append(VMC, frame(fnBeingBorn)),
%     
%     list_append(VMC, fe(msg,  vm_frame_pop)),
%     list_append(VMC, fe(top,  time)),
%     list_append(VMC, fe(add,  uriref(aiu:self))),
%     ias(I, user, USER),
%     list_append(VMC, fe(spkr, USER)),
%     list_append(VMC, frame(fnQuestioning)),
%    
%     % trace(on),
% 
%     fnvm_exec (I, VMC).
% 
% % FIXME: he/she gender indicator
% nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) (when|in which year) (was|is) (he|she) born (again|)?',
%          inline(l2proc_humanBornWhenContext)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) (wann|in welchem Jahr) (wurde|ist) (eigentlich|) (sie|er) (nochmal|) geboren?',
%          inline(l2proc_humanBornWhenContext)).
% 
% nlp_test(en,
%          ivr(in('When was Angela Merkel born?'),
%              out('Angela Merkel was born on july seventeen, 1954.')),
%          ivr(in('What were we talking about?'),
%              out('angela merkels birthday')),
%          ivr(in('and when was she born?'),
%              out('Angela Merkel was born on july seventeen, 1954.')),
%          ivr(in('and where?'),
%              out('she was born in barmbek nord'))
%         ).
% 
% nlp_test(de,
%          ivr(in('Wann wurde Angela Merkel geboren?'),
%              out('Angela Merkel wurde am siebzehnten juli 1954 geboren.')),
%          ivr(in('Welches Thema hatten wir?'),
%              out('angela merkels geburtstag')),
%          ivr(in('und wann wurde sie nochmal geboren?'),
%              out('Angela Merkel wurde am siebzehnten juli 1954 geboren.')),
%          ivr(in('und wo?'),
%              out('Angela Merkel wurde in barmbek nord geboren.'))
%         ).

