% prolog

is_computer_scientist(PERSON) :- rdf (PERSON, wdpd:Occupation, wde:ComputerScientist).

operating_system_category (CAT) :- CAT is uriref(wde:MultitaskingOperatingSystem).
operating_system_category (CAT) :- CAT is uriref(wde:OperatingSystem).

operating_system_rdf (OS) :-
    operating_system_category(CAT),
    rdf(OS, wdpd:InstanceOf, CAT).

operating_systems (S)  :- set_findall(OS, operating_system_rdf(OS), S).

operating_system (OS) :- operating_systems(S), set_get(S, OS).


%
% named entity recognition (NER) stuff: extra points for computer scientists, programming language and home computer
%

ner_learn_programming_languages(LANG) :-
    atom_chars(LANG, LSTR),

    rdf_lists (distinct,
               PROGRAMMING_LANGUAGE_ENTITIES, wdpd:InstanceOf,   wde:ProgrammingLanguage,
               PROGRAMMING_LANGUAGE_ENTITIES, rdfs:label,        PROGRAMMING_LANGUAGE_LABELS,
               filter (lang(PROGRAMMING_LANGUAGE_LABELS) = LSTR)),

    ner_learn(LANG, programming_language, PROGRAMMING_LANGUAGE_ENTITIES, PROGRAMMING_LANGUAGE_LABELS).

ner_learn_home_computers(LANG) :-
    atom_chars(LANG, LSTR),

    rdf_lists (distinct,
               HOME_COMPUTER_ENTITIES, wdpd:InstanceOf,   wde:HomeComputer,
               HOME_COMPUTER_ENTITIES, rdfs:label,        HOME_COMPUTER_LABELS,
               filter (lang(HOME_COMPUTER_LABELS) = LSTR)),

    ner_learn(LANG, home_computer, HOME_COMPUTER_ENTITIES, HOME_COMPUTER_LABELS).

ner_learn_operating_systems(LANG) :-
    atom_chars(LANG, LSTR),

    operating_system_category(CAT),

    rdf_lists (distinct,
               OS_ENTITIES, wdpd:InstanceOf,   CAT,
               OS_ENTITIES, rdfs:label,        OS_LABELS,
               filter (lang(OS_LABELS) = LSTR)),

    ner_learn(LANG, operating_system, OS_ENTITIES, OS_LABELS).

init('tech') :-
    ner_learn_operating_systems(en),
    ner_learn_operating_systems(de),
    ner_learn_home_computers(en),
    ner_learn_home_computers(de),
    ner_learn_programming_languages(en),
    ner_learn_programming_languages(de).

nlp_macro(en, 'OPERATING_SYSTEM', LABEL) :- 
    operating_system(OS),
    rdf (limit(1),
         OS, rdfs:label, LABEL,
         filter(lang(LABEL) = 'en')).

nlp_macro(de, 'OPERATING_SYSTEM', LABEL) :- 
    operating_system(OS),
    rdf (limit(1),
         OS, rdfs:label, LABEL,
         filter(lang(LABEL) = 'de')).

l2proc_knowOSTokens(LANG) :-

    ner(LANG, I, operating_system, @OPERATING_SYSTEM:TSTART_LABEL_0, @OPERATING_SYSTEM:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(ent, NER1ENTITY)),
    list_append(VMC, fe(entclass, operating_system)),
    list_append(VMC, fe(cog, uriref(aiu:self))),
    list_append(VMC, frame(fnFamiliarity)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  existance)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    fnvm_exec (I, VMC).

nlp_gen (en, '@SELF_ADDRESS:LABEL (do you know|what do you think about|have you tried|do you run|do you like) @OPERATING_SYSTEM:LABEL',
         inline(l2proc_knowOSTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (kennst du|was hältst du von|was denkst du über|läufst du unter|magst du) @OPERATING_SYSTEM:LABEL',
         inline(l2proc_knowOSTokens, en)).

nlp_test(en,
         ivr(in('do you know linux?'),
             out("sure I know Linux"))).
nlp_test(de,
         ivr(in('magst du linux?'),
             out('ja ich kenne linux'))).

l3proc (I, F, fnQuestioning) :-

    frame (F, top,      general_info),
    frame (F, ent,      HUMAN),
    frame (F, entclass, human),

    is_computer_scientist(HUMAN),

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user about person's status)
    
    CAT is uriref (wde:ComputerScientist),

    list_append(VMC, fe(cat,   CAT)),
    list_append(VMC, fe(item,  HUMAN)),
    list_append(VMC, frame(fnCategorization)),

    list_append(VMC, fe(msg,   vm_frame_pop)),
    list_append(VMC, fe(top,   category)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,   USER)),
    list_append(VMC, fe(spkr,  uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 150),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    l4proc (I).

nlp_test(en,
         ivr(in('Who is Niklaus Wirth?'),
             out('niklaus wirth is categorized as computer scientist'))).
nlp_test(de,
         ivr(in('wer ist Niklaus Wirth?'),
             out('niklaus wirth ist in der kategorie informatiker'))).

nlp_macro(en, 'PROGRAMMING_LANGUAGE', NAME, LABEL) :- 
    rdf(distinct,
        NAME, wdpd:InstanceOf, wde:ProgrammingLanguage,
        NAME, rdfs:label, LABEL,
        filter(lang(LABEL) = 'en')).
nlp_macro(de, 'PROGRAMMING_LANGUAGE', NAME, LABEL) :- 
    rdf(distinct,
        NAME, wdpd:InstanceOf, wde:ProgrammingLanguage,
        NAME, rdfs:label, LABEL,
        filter(lang(LABEL) = 'de')).

l2proc_knowProgrammingLanguageTokens(LANG) :-

    ner(LANG, I, programming_language, @PROGRAMMING_LANGUAGE:TSTART_LABEL_0, @PROGRAMMING_LANGUAGE:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(ent, NER1ENTITY)),
    list_append(VMC, fe(entclass, programming_language)),
    list_append(VMC, fe(cog, uriref(aiu:self))),
    list_append(VMC, frame(fnFamiliarity)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  existance)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    fnvm_exec (I, VMC).

nlp_gen(en, '@SELF_ADDRESS:LABEL (do you know|what is) @PROGRAMMING_LANGUAGE:LABEL?',
         inline(l2proc_knowProgrammingLanguageTokens, en)).
nlp_gen(de, '@SELF_ADDRESS:LABEL (kennst Du|was ist) @PROGRAMMING_LANGUAGE:LABEL?',
         inline(l2proc_knowProgrammingLanguageTokens, de)).
 
nlp_test(en,
         ivr(in('do you know prolog?'),
             out("yes i know prolog")),
         ivr(in('what was our topic, again?'),
             out("we have been talking about prolog"))).
nlp_test(de,
         ivr(in('kennst du prolog?'),
             out('ja klar ich kenne prolog')),
         ivr(in('Worüber hatten wir gesprochen?'),
             out("Wir hatten über prolog gesprochen."))).

nlp_macro(en, 'HOME_COMPUTER', NAME, LABEL) :- 
    rdf(distinct,
        NAME, wdpd:InstanceOf, wde:HomeComputer,
        NAME, rdfs:label, LABEL,
        filter(lang(LABEL) = 'en')).
nlp_macro(de, 'HOME_COMPUTER', NAME, LABEL) :- 
    rdf(distinct,
        NAME, wdpd:InstanceOf, wde:HomeComputer,
        NAME, rdfs:label, LABEL,
        filter(lang(LABEL) = 'de')).

l2proc_knowHomeComputerTokens(LANG) :-

    ner(LANG, I, home_computer, @HOME_COMPUTER:TSTART_LABEL_0, @HOME_COMPUTER:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(ent, NER1ENTITY)),
    list_append(VMC, fe(entclass, home_computer)),
    list_append(VMC, fe(cog, uriref(aiu:self))),
    list_append(VMC, frame(fnFamiliarity)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  existance)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    fnvm_exec (I, VMC).

nlp_gen(en, '@SELF_ADDRESS:LABEL (do you know|what is) @HOME_COMPUTER:LABEL?',
         inline(l2proc_knowHomeComputerTokens, en)).
nlp_gen(de, '@SELF_ADDRESS:LABEL (kennst Du|was ist) @HOME_COMPUTER:LABEL?',
         inline(l2proc_knowHomeComputerTokens, de)).

nlp_test(en,
         ivr(in('do you know commodore 64?'),
             out("yes commodore 64 sounds familiar")),
         ivr(in('what was our topic, again?'),
             out("our topic was commodore 64."))).
nlp_test(de,
         ivr(in('kennst du sinclair zx spectrum?'),
             out('ja ich kenne sinclair zx spectrum')),
         ivr(in('Worüber hatten wir gesprochen?'),
             out("Wir hatten über Sinclair ZX Spectrum gesprochen."))).

%
% random / misc
%

nlp_gens(en, '@SELF_ADDRESS:LABEL bill gates',
             'What do you think about Bill Gates?').
nlp_gens(de, '@SELF_ADDRESS:LABEL bill gates',
             'Wie denkst Du über Bill Gates?').
