%prolog

%
% named entity recognition (NER)
%

% this will switch to much smaller training sets so we can keep 
% debug turn-around cycle times low
debug_mode('humans').

known_humans_data(en, HUMAN, LABEL) :-
    debug_mode('humans'),
    HUMAN is 'http://www.wikidata.org/entity/Q39829',
    LABEL is 'Stephen King'.

known_humans_data(de, HUMAN, LABEL) :-
    debug_mode('humans'),
    HUMAN is 'http://www.wikidata.org/entity/Q39829',
    LABEL is 'Stephen King'.

known_humans_data(LANG, HUMAN, LABEL) :-
    not(debug_mode('humans')),
    atom_chars(LANG, LSTR),
    rdf (distinct, 
         HUMAN, wdpd:InstanceOf,   wde:Human,
         HUMAN, rdfs:label,        LABEL,
         filter (lang(LABEL) = LSTR)).

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
% utils
%

nlp_f1_ent_pp(en, I, ENTITY) :-
    is_male(ENTITY),
    setz(ias(I, f1_ent_pp3s, _), "he"),
    setz(ias(I, f1_ent_pp3o, _), "him"),
    !.
nlp_f1_ent_pp(en, I, ENTITY) :-
    is_female(ENTITY),
    setz(ias(I, f1_ent_pp3s, _), "she"),
    setz(ias(I, f1_ent_pp3o, _), "her"),
    !.
nlp_f1_ent_pp(en, I, ENTITY) :-
    setz(ias(I, f1_ent_pp3s, _), "it"),
    setz(ias(I, f1_ent_pp3o, _), "it").

nlp_f1_ent_pp(de, I, ENTITY) :-
    is_male(ENTITY),
    setz(ias(I, f1_ent_pp3s, _), "er"),
    setz(ias(I, f1_ent_pp3o, _), "ihn"),
    !.
nlp_f1_ent_pp(de, I, ENTITY) :-
    is_female(ENTITY),
    setz(ias(I, f1_ent_pp3s, _), "sie"),
    setz(ias(I, f1_ent_pp3o, _), "sie"),
    !.
nlp_f1_ent_pp(de, I, ENTITY) :-
    setz(ias(I, f1_ent_pp3s, _), "es"),
    setz(ias(I, f1_ent_pp3o, _), "es").

nlp_f1_ent_human(LANG, I, HUMAN) :-
    
    entity_label(LANG, HUMAN, LABEL),
    setz(ias(I, f1_entlabel, _), LABEL),

    nlp_f1_ent_pp(LANG, I, HUMAN).

%
% macros listing all known humans with their LABELs
%

nlp_known_humans_s (en, S, HUMAN, LABEL, TSTART, TEND) :-
    known_humans_data(en, HUMAN, LABEL),
    length(S, TSTART),
    hears (en, S, LABEL),
    length(S, TEND).
    
nlp_known_humans_gen_s (en, S, HUMAN, LABEL, TSTART, TEND) :-
    known_humans_data(en, HUMAN, L),
    LABEL is format_str("%s's", L),
    length(S, TSTART),
    hears (en, S, LABEL),
    length(S, TEND).

nlp_known_humans_s (de, S, HUMAN, LABEL, TSTART, TEND) :-
    known_humans_data(de, HUMAN, LABEL),
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
nlp_knowHumanTokens_r (en, R) :- says (en, R, "Sure I know %(f1_ent_pp3o)s.").
nlp_knowHumanTokens_r (en, R) :- says (en, R, "Yes I know %(f1_ent_pp3o)s.").
nlp_knowHumanTokens_r (de, R) :- says (de, R, "Klar kenne ich %(f1_entlabel)s.").
nlp_knowHumanTokens_r (de, R) :- says (de, R, "Ja ich kenne %(f1_entlabel)s.").
nlp_knowHumanTokens_r (de, R) :- says (de, R, "Klar kenne ich %(f1_ent_pp3o)s.").
nlp_knowHumanTokens_r (de, R) :- says (de, R, "Ja ich kenne %(f1_ent_pp3o)s.").

nlp_knowHumanTokens_g(LANG, G) :-
    G is [
        % trace(on),
        ner(LANG, I, NER1CLASS, TSTART, TEND, NER1ENTITY),

        setz(ias(I, f1_type,     _), question),
        setz(ias(I, f1_topic,    _), familiarity),
        setz(ias(I, f1_entclass, _), NER1CLASS),
        setz(ias(I, f1_ent,      _), NER1ENTITY),

        nlp_f1_ent_human(LANG, I, NER1ENTITY)
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
nlp_test('humans', en, 'know3', [],
         ['Do you know Stephen King?', 'Sure I know him', []]).

%
% birthplace and birtdate questions
%

nlp_whereborntokens_g (LANG, G, TSTART, TEND) :-
    G is [
        % trace(on),
        ner(LANG, I, NER1CLASS, TSTART, TEND, NER1ENTITY),

        setz(ias(I, f1_type,     _), question),
        setz(ias(I, f1_topic,    _), birthplace),
        setz(ias(I, f1_entclass, _), NER1CLASS),
        setz(ias(I, f1_ent,      _), NER1ENTITY),

        nlp_f1_ent_human (LANG, I, NER1ENTITY),

        rdf (distinct, limit(1),
             NER1ENTITY, wdpd:PlaceOfBirth, BIRTHPLACE),
        setz(ias(I, f1_loc, _), BIRTHPLACE),

        entity_label(LANG, BIRTHPLACE, BPLABEL),

        setz(ias(I, f1_loclabel, _), BPLABEL)
        ].

nlp_whereborntokens_s (en, S, TSTART, TEND) :-
    hears (en, S, [ [ "where", "in which town", "in which city"], ["was", "is"] ] ),
    nlp_known_humans_s (en, S, _, _, TSTART, TEND),    
    hears (en, S, "born?").
nlp_whereborntokens_s (en, S, TSTART, TEND) :-
    hears (en, S, [ "which is", [ "the birthplace", "the place of birth"], "of" ] ),
    nlp_known_humans_s (en, S, _, _, TSTART, TEND).

nlp_whereborntokens_s (de, S, TSTART, TEND) :-
    hears (de, S, [ [ "wo", "in welcher Stadt", "an welchem Ort"], ["wurde", "ist"], ["eigentlich", ""] ] ),
    nlp_known_humans_s (de, S, _, _, TSTART, TEND),    
    hears (de, S, "geboren?").
nlp_whereborntokens_s (de, S, TSTART, TEND) :-
    hears (de, S, [ ["welches", "was"], "ist", [ "der Geburtsort", "die Geburtsstadt"], "von" ] ),
    nlp_known_humans_s (de, S, _, _, TSTART, TEND).

nlp_whereborn_r (en, R) :- says (en, R, "%(f1_entlabel)s was born in %(f1_loclabel)s.").
nlp_whereborn_r (en, R) :- says (en, R, "%(f1_ent_pp3s)s was born in %(f1_loclabel)s.").
nlp_whereborn_r (de, R) :- says (de, R, "%(f1_entlabel)s wurde in %(f1_loclabel)s geboren.").
nlp_whereborn_r (de, R) :- says (de, R, "%(f1_ent_pp3s)s wurde in %(f1_loclabel)s geboren.").

nlp_train('humans', en, [[], S1, G1, R1]) :-

    self_address(en, S1, _),
    nlp_whereborntokens_s (en, S1, TSTART, TEND),

    nlp_whereborntokens_g (en, G1, TSTART, TEND),

    nlp_whereborn_r (en, R1).

nlp_train('humans', de, [[], S1, G1, R1]) :-

    self_address(de, S1, _),
    nlp_whereborntokens_s (de, S1, TSTART, TEND),

    nlp_whereborntokens_g(de, G1, TSTART, TEND),

    nlp_whereborn_r (de, R1).

nlp_test('humans', en, 'whereborn1', [],
         ['Where was Stephen King born?', 'Stephen King was born in Portland.', []]).

nlp_test('humans', de, 'whereborn2', [],
         ['Wo wurde Stephen King geboren?', 'Stephen King wurde in Portland geboren.', []]).
 
% % l2proc_humanBornWhereContext :-
% % 
% %     list_append(VMC, frame(fnBeingBorn)),
% %     
% %     list_append(VMC, fe(msg,  vm_frame_pop)),
% %     list_append(VMC, fe(top,  place)),
% %     list_append(VMC, fe(add,  uriref(aiu:self))),
% %     ias(I, user, USER),
% %     list_append(VMC, fe(spkr, USER)),
% %     list_append(VMC, frame(fnQuestioning)),
% %    
% %     % trace(on),
% % 
% %     fnvm_exec (I, VMC).
% % 
% % nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) (where|in which town|in which city) (was|is) (she|he) born (again|)?',
% %          inline(l2proc_humanBornWhereContext)).
% % nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) (wo|in welcher stadt) (wurde|ist) (eigentlich|) (er|sie) (nochmal|) geboren?',
% %          inline(l2proc_humanBornWhereContext)).
% % 
% % nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) which is (the birthplace|place of birth) of (him|her) (again|)?',
% %          inline(l2proc_humanBornWhereContext)).
% % nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) welches ist (eigentlich|nochmal|) (der Geburtsort|die Geburtsstadt) von (ihm|ihr)?',
% %          inline(l2proc_humanBornWhereContext)).
% % 
% % nlp_test(en,
% %          ivr(in('Where was Angela Merkel born?'),
% %              out('angela merkel was born in barmbek-nord')),
% %          ivr(in('What were we talking about?'),
% %              out('angela merkels birthday')),
% %          ivr(in('and where was she born again?'),
% %              out('angela merkel was born in barmbek-nord'))).
% % nlp_test(de,
% %          ivr(in('Wo wurde Angela Merkel geboren?'),
% %              out('angela merkel wurde in barmbek-nord geboren')),
% %          ivr(in('Welches Thema hatten wir?'),
% %              out('angela merkels geburtstag.')),
% %          ivr(in('und wo wurde sie nochmal geboren?'),
% %              out('angela merkel wurde in barmbek-nord geboren'))).
% % 
% % 
% % l2proc_humanBornWhenTokens(LANG) :-
% % 
% %     ner(LANG, I, NER1CLASS, @KNOWN_HUMANS:TSTART_LABEL_0, @KNOWN_HUMANS:TEND_LABEL_0, NER1ENTITY),
% % 
% %     list_append(VMC, fe(child, NER1ENTITY)),
% %     list_append(VMC, fe(childclass, NER1CLASS)),
% %     list_append(VMC, frame(fnBeingBorn)),
% %     
% %     list_append(VMC, fe(msg,  vm_frame_pop)),
% %     list_append(VMC, fe(top,  time)),
% %     list_append(VMC, fe(add,  uriref(aiu:self))),
% %     ias(I, user, USER),
% %     list_append(VMC, fe(spkr, USER)),
% %     list_append(VMC, frame(fnQuestioning)),
% %    
% %     % trace(on),
% % 
% %     fnvm_exec (I, VMC).
% % 
% % nlp_gen (en, '@SELF_ADDRESS:LABEL (when|in which year) (was|is) @KNOWN_HUMANS:LABEL born?',
% %          inline(l2proc_humanBornWhenTokens, en)).
% % nlp_gen (de, '@SELF_ADDRESS:LABEL (wann|in welchem Jahr) (wurde|ist) (eigentlich|) @KNOWN_HUMANS:LABEL geboren?',
% %          inline(l2proc_humanBornWhenTokens, de)).
% % 
% % nlp_gen (en, "@SELF_ADDRESS:LABEL (when is|on what day is) @KNOWN_HUMANS:LABELS birthday?",
% %          inline(l2proc_humanBornWhenTokens, en)).
% % nlp_gen (de, '@SELF_ADDRESS:LABEL (wann hat|an welchem Tag hat) (eigentlich|) @KNOWN_HUMANS:LABEL Geburtstag?',
% %          inline(l2proc_humanBornWhenTokens, de)).
% % 
% % l2proc_humanBornWhenContext :-
% % 
% %     list_append(VMC, frame(fnBeingBorn)),
% %     
% %     list_append(VMC, fe(msg,  vm_frame_pop)),
% %     list_append(VMC, fe(top,  time)),
% %     list_append(VMC, fe(add,  uriref(aiu:self))),
% %     ias(I, user, USER),
% %     list_append(VMC, fe(spkr, USER)),
% %     list_append(VMC, frame(fnQuestioning)),
% %    
% %     % trace(on),
% % 
% %     fnvm_exec (I, VMC).
% % 
% % % FIXME: he/she gender indicator
% % nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) (when|in which year) (was|is) (he|she) born (again|)?',
% %          inline(l2proc_humanBornWhenContext)).
% % nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) (wann|in welchem Jahr) (wurde|ist) (eigentlich|) (sie|er) (nochmal|) geboren?',
% %          inline(l2proc_humanBornWhenContext)).
% % 
% % nlp_test(en,
% %          ivr(in('When was Angela Merkel born?'),
% %              out('Angela Merkel was born on july seventeen, 1954.')),
% %          ivr(in('What were we talking about?'),
% %              out('angela merkels birthday')),
% %          ivr(in('and when was she born?'),
% %              out('Angela Merkel was born on july seventeen, 1954.')),
% %          ivr(in('and where?'),
% %              out('she was born in barmbek nord'))
% %         ).
% % 
% % nlp_test(de,
% %          ivr(in('Wann wurde Angela Merkel geboren?'),
% %              out('Angela Merkel wurde am siebzehnten juli 1954 geboren.')),
% %          ivr(in('Welches Thema hatten wir?'),
% %              out('angela merkels geburtstag')),
% %          ivr(in('und wann wurde sie nochmal geboren?'),
% %              out('Angela Merkel wurde am siebzehnten juli 1954 geboren.')),
% %          ivr(in('und wo?'),
% %              out('Angela Merkel wurde in barmbek nord geboren.'))
% %         ).

%
% if we don't know anything else, we can tell the user about the human's birthplace
%

nlp_train('humans', en, [[], S1, G1, R1]) :-

    self_address(en, S1, _),
    hears (en, S1, [ [ "what about", "who is", "what is", "what do you know about", "what do you know of" ] ] ),
    nlp_known_humans_s (en, S1, _, _, TSTART, TEND),    

    nlp_whereborntokens_g (en, G1, TSTART, TEND),

    says (en, R1, "%(f1_entlabel)s was born in %(f1_loclabel)s.").

nlp_train('humans', de, [[], S1, G1, R1]) :-

    self_address(de, S1, _),
    hears (de, S1, [ [ "wer ist", "wer ist eigentlich", "was ist mit", "was ist eigentlich mit", "was weisst du über", "was weisst du eigentlich über" ] ] ),
    nlp_known_humans_s (de, S1, _, _, TSTART, TEND),    

    nlp_whereborntokens_g (de, G1, TSTART, TEND),

    says (de, R1, "%(f1_entlabel)s wurde in %(f1_loclabel)s geboren.").

nlp_test('humans', en, 'whatabout1', [],
         ['What about Stephen King?', 'Stephen King was born in Portland.', []]).
 
nlp_test('humans', de, 'whatabout2', [],
         ['Was ist mit Stephen King?', 'Stephen King wurde in Portland geboren.', []]).
 

