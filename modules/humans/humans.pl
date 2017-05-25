%prolog

%
% named entity recognition (NER)
%

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

nlp_macro (en, 'KNOWN_HUMANS', HUMAN, LABEL, LABELS) :-
    rdf (distinct, 
         % limit(10), % FIXME: debug
         HUMAN, wdpd:InstanceOf,   wde:Human,
         HUMAN, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'en')),
    LABELS is format_str("%s's", LABEL).

nlp_macro (de, 'KNOWN_HUMANS', HUMAN, LABEL) :-
    rdf (distinct, 
         % limit(10), % FIXME: debug
         HUMAN, wdpd:InstanceOf,   wde:Human,
         HUMAN, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')).

%
% questions about humans known
%

l2proc_knowHumanTokens(LANG) :-

    ner(LANG, I, NER1CLASS, @KNOWN_HUMANS:TSTART_LABEL_0, @KNOWN_HUMANS:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(ent, NER1ENTITY)),
    list_append(VMC, fe(entclass, NER1CLASS)),
    list_append(VMC, fe(cog, uriref(aiu:self))),
    list_append(VMC, frame(fnFamiliarity)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  existance)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    fnvm_exec (I, VMC).
   
% FIXME: distinguish who/what (put indication about human/thing/... into question frame)

nlp_gen (en, '@SELF_ADDRESS:LABEL (what about | do you know | do you happen to know | who is | what is) @KNOWN_HUMANS:LABEL',
         inline(l2proc_knowHumanTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (kennst du|kennst du eigentlich|wer ist|wer ist eigentlich|was ist mit|was ist eigentlich mit|was weisst du über|was weisst du eigentlich über) @KNOWN_HUMANS:LABEL',
         inline(l2proc_knowHumanTokens, de)).


% this test only works as long as the politics module is active (and knowns better)
% nlp_test(de,
%          ivr(in('Kennst Du Angela Merkel?'),
%              out('Ja, der Name ist mir bekannt'))).
% nlp_test(en,
%          ivr(in('What about Angela Merkel?'),
%              out('That name sounds familiar'))).

%
% birthplace and birtdate questions
%

l2proc_humanBornWhereTokens(LANG) :-

    ner(LANG, I, NER1CLASS, @KNOWN_HUMANS:TSTART_LABEL_0, @KNOWN_HUMANS:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(child, NER1ENTITY)),
    list_append(VMC, fe(childclass, NER1CLASS)),
    list_append(VMC, frame(fnBeingBorn)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  place)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    fnvm_exec (I, VMC).


nlp_gen (en, '@SELF_ADDRESS:LABEL (where|in which town|in which city) (was|is) @KNOWN_HUMANS:LABEL born?',
         inline(l2proc_humanBornWhereTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (wo|in welcher stadt) (wurde|ist) (eigentlich|) @KNOWN_HUMANS:LABEL geboren?',
         inline(l2proc_humanBornWhereTokens, de)).

nlp_gen (en, '@SELF_ADDRESS:LABEL which is (the birthplace|place of birth) of @KNOWN_HUMANS:LABEL?',
         inline(l2proc_humanBornWhereTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL welches ist (eigentlich|) (der Geburtsort|die Geburtsstadt) von @KNOWN_HUMANS:LABEL?',
         inline(l2proc_humanBornWhereTokens, de)).

l2proc_humanBornWhereContext :-

    list_append(VMC, frame(fnBeingBorn)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  place)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
   
    % trace(on),

    fnvm_exec (I, VMC).

nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) (where|in which town|in which city) (was|is) (she|he) born (again|)?',
         inline(l2proc_humanBornWhereContext)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) (wo|in welcher stadt) (wurde|ist) (eigentlich|) (er|sie) (nochmal|) geboren?',
         inline(l2proc_humanBornWhereContext)).

nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) which is (the birthplace|place of birth) of (him|her) (again|)?',
         inline(l2proc_humanBornWhereContext)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) welches ist (eigentlich|nochmal|) (der Geburtsort|die Geburtsstadt) von (ihm|ihr)?',
         inline(l2proc_humanBornWhereContext)).

nlp_test(en,
         ivr(in('Where was Angela Merkel born?'),
             out('angela merkel was born in barmbek-nord')),
         ivr(in('What were we talking about?'),
             out('angela merkels birthday')),
         ivr(in('and where was she born again?'),
             out('angela merkel was born in barmbek-nord'))).
nlp_test(de,
         ivr(in('Wo wurde Angela Merkel geboren?'),
             out('angela merkel wurde in barmbek-nord geboren')),
         ivr(in('Welches Thema hatten wir?'),
             out('angela merkels geburtstag.')),
         ivr(in('und wo wurde sie nochmal geboren?'),
             out('angela merkel wurde in barmbek-nord geboren'))).


l2proc_humanBornWhenTokens(LANG) :-

    ner(LANG, I, NER1CLASS, @KNOWN_HUMANS:TSTART_LABEL_0, @KNOWN_HUMANS:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(child, NER1ENTITY)),
    list_append(VMC, fe(childclass, NER1CLASS)),
    list_append(VMC, frame(fnBeingBorn)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  time)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
   
    % trace(on),

    fnvm_exec (I, VMC).

nlp_gen (en, '@SELF_ADDRESS:LABEL (when|in which year) (was|is) @KNOWN_HUMANS:LABEL born?',
         inline(l2proc_humanBornWhenTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (wann|in welchem Jahr) (wurde|ist) (eigentlich|) @KNOWN_HUMANS:LABEL geboren?',
         inline(l2proc_humanBornWhenTokens, de)).

nlp_gen (en, "@SELF_ADDRESS:LABEL (when is|on what day is) @KNOWN_HUMANS:LABELS birthday?",
         inline(l2proc_humanBornWhenTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (wann hat|an welchem Tag hat) (eigentlich|) @KNOWN_HUMANS:LABEL Geburtstag?',
         inline(l2proc_humanBornWhenTokens, de)).

l2proc_humanBornWhenContext :-

    list_append(VMC, frame(fnBeingBorn)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  time)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
   
    % trace(on),

    fnvm_exec (I, VMC).

% FIXME: he/she gender indicator
nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) (when|in which year) (was|is) (he|she) born (again|)?',
         inline(l2proc_humanBornWhenContext)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) (wann|in welchem Jahr) (wurde|ist) (eigentlich|) (sie|er) (nochmal|) geboren?',
         inline(l2proc_humanBornWhenContext)).

nlp_test(en,
         ivr(in('When was Angela Merkel born?'),
             out('Angela Merkel was born on july seventeen, 1954.')),
         ivr(in('What were we talking about?'),
             out('angela merkels birthday')),
         ivr(in('and when was she born?'),
             out('Angela Merkel was born on july seventeen, 1954.')),
         ivr(in('and where?'),
             out('she was born in barmbek nord'))
        ).

nlp_test(de,
         ivr(in('Wann wurde Angela Merkel geboren?'),
             out('Angela Merkel wurde am siebzehnten juli 1954 geboren.')),
         ivr(in('Welches Thema hatten wir?'),
             out('angela merkels geburtstag')),
         ivr(in('und wann wurde sie nochmal geboren?'),
             out('Angela Merkel wurde am siebzehnten juli 1954 geboren.')),
         ivr(in('und wo?'),
             out('Angela Merkel wurde in barmbek nord geboren.'))
        ).

