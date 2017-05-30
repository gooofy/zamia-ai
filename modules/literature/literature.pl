% prolog

is_author(PERSON) :- rdf (LITERATURE, wdpd:Author, PERSON).
is_book(ENTITY) :- rdf (ENTITY, wdpd:InstanceOf, wde:Book).

lookup_entity_creation_info (BOOK, AUTHOR, PDATE) :-
    rdf (distinct, limit(1),
         BOOK,    wdpd:Author,          AUTHOR,
         BOOK,    wdpd:PublicationDate, PDATE).

%
% named entity recognition (NER) stuff: extra points for authors, literature title NER
%

ner_learn_books(LANG) :-
    atom_chars(LANG, LSTR),

    rdf_lists (distinct,
               BOOK_ENTITIES, wdpd:InstanceOf,   wde:Book,
               BOOK_ENTITIES, rdfs:label,        BOOK_LABELS,
               filter (lang(BOOK_LABELS) = LSTR)),

    ner_learn(LANG, book, BOOK_ENTITIES, BOOK_LABELS).

init('literature') :-
    ner_learn_books(en),
    ner_learn_books(de).

nlp_macro (en, 'LITERATURE', LITERATURE, LABEL) :-
    rdf (distinct,
         LITERATURE, wdpd:InstanceOf,   wde:Book,
         LITERATURE, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'en')).
nlp_macro (de, 'LITERATURE', LITERATURE, LABEL) :-
    rdf (distinct,
         LITERATURE, wdpd:InstanceOf,   wde:Book,
         LITERATURE, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')).

%
% book author questions
%

% provide nicer answers for books than stock entity creation answers

answerz (I, en, bookWrittenBy, E_LABEL, C_LABEL) :- sayz(I, en, format_str("%s was written by %s", E_LABEL, C_LABEL)).
answerz (I, de, bookWrittenBy, E_LABEL, C_LABEL) :- sayz(I, de, format_str("%s wurde von %s geschrieben", E_LABEL, C_LABEL)).

l4proc (I, F, fnTelling, creator, MSGF, fnIntentionallyCreate) :-

    frame (MSGF, ent,     ENTITY),
    frame (MSGF, creator, CREATOR),

    ias (I, uttLang, LANG),

    is_book(ENTITY),

    scorez(I, 100),

    entity_label(LANG, ENTITY,  E_LABEL),
    entity_label(LANG, CREATOR, C_LABEL),

    answerz (I, LANG, bookWrittenBy, E_LABEL, C_LABEL).

l2proc_bookAuthorTokens(LANG) :-

    ner(LANG, I, book, @LITERATURE:TSTART_LABEL_0, @LITERATURE:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(ent,  NER1ENTITY)),
    list_append(VMC, frame(fnIntentionallyCreate)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  creator)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),

    log (debug, 'l2proc_bookAuthorTokens for', NER1ENTITY),

    fnvm_exec (I, VMC).

nlp_gen (en, '@SELF_ADDRESS:LABEL who (wrote|authored|created) @LITERATURE:LABEL (by the way|)?',
         inline(l2proc_bookAuthorTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL wer hat (eigentlich|) @LITERATURE:LABEL geschrieben?',
         inline(l2proc_bookAuthorTokens, de)).

nlp_gen (en, '@SELF_ADDRESS:LABEL (who is the author of|who authored) @LITERATURE:LABEL?',
         inline(l2proc_bookAuthorTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL wer ist (eigentlich|) der Autor von @LITERATURE:LABEL?',
         inline(l2proc_bookAuthorTokens, de)).
 
nlp_test(en,
         ivr(in('who is the author of the stand?'),
             out('The stand was written by Stephen King.'))).
nlp_test(de,
         ivr(in('wer ist der autor von the stand?'),
             out('The Stand wurde von Stephen King geschrieben.'))).

l3proc (I, F, fnQuestioning) :-

    frame (F, top,      general_info),
    frame (F, ent,      HUMAN),
    frame (F, entclass, human),

    is_author(HUMAN),

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user about person's status)
    
    CAT is uriref (wde:Writer),

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
         ivr(in('Who is Dan Brown?'),
             out('Dan Brown is categorized as writer.'))).
nlp_test(de,
         ivr(in('wer ist Dan Brown?'),
             out('Dan Brown ist in der Kategorie Schriftsteller.'))).

%
% book creation date questions
%

% provide nicer answers for books than stock entity creation answers

answerz (I, en, whenWasBookWritten, E_LABEL, Y)   :- sayz(I, en, format_str("%s was written in %s", E_LABEL, Y)).
answerz (I, de, whenWasBookWritten, E_LABEL, Y)   :- sayz(I, de, format_str("%s wurde %s geschrieben",        E_LABEL, Y)).

l4proc (I, F, fnTelling, time, MSGF, fnIntentionallyCreate) :-

    frame (MSGF, ent,  ENTITY),
    frame (MSGF, time, TIME),

    ias (I, uttLang, LANG),

    is_book(ENTITY),

    scorez(I, 100),

    entity_label(LANG, ENTITY, E_LABEL),
    stamp_date_time(TIME, date(Y,M,D,H,Mn,S,'local')),

    answerz (I, LANG, whenWasBookWritten, E_LABEL, Y).

l2proc_bookWrittenWhenTokens(LANG) :-

    ner(LANG, I, book, @LITERATURE:TSTART_LABEL_0, @LITERATURE:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(ent,  NER1ENTITY)),
    list_append(VMC, frame(fnIntentionallyCreate)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  time)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),

    log (debug, 'l2proc_bookWrittenWhenTokens for', NER1ENTITY),

    fnvm_exec (I, VMC).

nlp_gen (en, '@SELF_ADDRESS:LABEL when was @LITERATURE:LABEL (created|written|made)?',
         inline(l2proc_bookWrittenWhenTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL wann (ist|wurde) (eigentlich|) @LITERATURE:LABEL (geschrieben|geschaffen)?',
         inline(l2proc_bookWrittenWhenTokens, de)).

nlp_test(en,
         ivr(in('when was the stand written?'),
             out('The Stand was written in 1978.'))).
nlp_test(de,
         ivr(in('wann wurde the stand geschrieben?'),
             out('The Stand wurde 1978 geschrieben.'))).

l2proc_knowBookTokens(LANG) :-

    ner(LANG, I, book, @LITERATURE:TSTART_LABEL_0, @LITERATURE:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(ent, NER1ENTITY)),
    list_append(VMC, fe(entclass, book)),
    list_append(VMC, fe(cog, uriref(aiu:self))),
    list_append(VMC, frame(fnFamiliarity)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  existance)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    fnvm_exec (I, VMC).

nlp_gen (en, '@SELF_ADDRESS:LABEL do you (happen to|) know (the book|) @LITERATURE:LABEL?',
         inline(l2proc_knowBookTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL kennst du (eigentlich|) (das Buch|) @LITERATURE:LABEL?',
         inline(l2proc_knowBookTokens, de)).

nlp_gen (en, '@SELF_ADDRESS:LABEL (have you read|did you happen to read) (the book|) @LITERATURE:LABEL?',
         inline(l2proc_knowBookTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL hast du (eigentlich|) (das Buch|) @LITERATURE:LABEL gelesen?',
         inline(l2proc_knowBookTokens, de)).

nlp_test(en,
         ivr(in('do you happen to know the book the stand?'),
             out('sure i know the stand'))).
nlp_test(de,
         ivr(in('kennst du das buch the stand?'),
             out('ja ich kenne the stand'))).

%
% literature context follow-up style questions
%

nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) do you (happen to|) know when it was written (by the way|)?',
         inline(l2proc_whenWasEntityCreatedContext)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) weisst du (eigentlich|) wann (es|das) geschrieben wurde?',
         inline(l2proc_whenWasEntityCreatedContext)).
 
nlp_gen (en, '@SELF_ADDRESS:LABEL (and|) do you (happen to|) know who wrote it (by the way|)?',
         inline(l2proc_whoCreatedEntityContext)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (und|) weisst du (eigentlich|) wer (es|das) geschrieben hat?',
         inline(l2proc_whoCreatedEntityContext)).
 
nlp_test(en,
         ivr(in('do you happen to know the book the stand?'),
             out('sure i know the stand')),
         ivr(in('and do you know who wrote it?'),
             out('the stand was created by stephen king')),
         ivr(in('do you know when it was written?'),
             out('The Stand was written in 1978.'))).

nlp_test(de,
         ivr(in('kennst du das buch the stand?'),
             out('ja klar ich kenne the stand')),
         ivr(in('weisst du, wer es geschrieben hat?'),
             out('the stand wurde von stephen king geschrieben')),
         ivr(in('und weisst du, wann es geschrieben wurde?'),
             out('The Stand wurde 1978 geschrieben.'))).


%
% FIXME: genre, topics, ...
%
 
%
% misc / random stuff
%

nlp_gens(en, '@SELF_ADDRESS:LABEL agatha christie',
             'I like Miss Marple...').
nlp_gens(de, '@SELF_ADDRESS:LABEL agatha christie',
             'Ich mag Miss Marple...').

