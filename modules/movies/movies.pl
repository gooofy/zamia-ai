% prolog

is_movie_director(HUMAN) :- rdf (MOVIE, wdpd:Director, HUMAN).

lookup_entity_creation_info (MOVIE, DIRECTOR, PDATE) :-
    rdf (distinct, limit(1),
         MOVIE,    wdpd:Director,        DIRECTOR,
         MOVIE,    wdpd:PublicationDate, PDATE).

%
% named entity recognition (NER) stuff: extra points for movie directors, movie title NER
%

ner_learn_films(LANG) :-
    atom_chars(LANG, LSTR),

    rdf_lists (distinct,
               FILM_ENTITIES, wdpd:InstanceOf,   wde:Film,
               FILM_ENTITIES, rdfs:label,        FILM_LABELS,
               filter (lang(FILM_LABELS) = LSTR)),

    ner_learn(LANG, film, FILM_ENTITIES, FILM_LABELS).

init('movies') :-
    ner_learn_films(en),
    ner_learn_films(de).

%
% movie related NLP macros/processing
%

nlp_macro (en, 'MOVIES', LABEL) :-
    rdf (distinct,
         MOVIE, wdpd:InstanceOf,   wde:Film,
         MOVIE, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'en')).
nlp_macro (de, 'MOVIES', LABEL) :-
    rdf (distinct,
         MOVIE, wdpd:InstanceOf,   wde:Film,
         MOVIE, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')).

l2proc_movieDirectorTokens(LANG) :-

    ner(LANG, I, film, @MOVIES:TSTART_LABEL_0, @MOVIES:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(ent,  NER1ENTITY)),
    list_append(VMC, frame(fnIntentionallyCreate)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  creator)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    fnvm_exec (I, VMC).
   
nlp_gen (en, '@SELF_ADDRESS:LABEL who (made|did) @MOVIES:LABEL (by the way|)?',
         inline(l2proc_movieDirectorTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL wer hat (eigentlich|) @MOVIES:LABEL gedreht?',
         inline(l2proc_movieDirectorTokens, de)).

nlp_gen (en, '@SELF_ADDRESS:LABEL (who is the director of|who directed) @MOVIES:LABEL?',
         inline(l2proc_movieDirectorTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL wer ist (eigentlich|) der Regisseur von @MOVIES:LABEL?',
         inline(l2proc_movieDirectorTokens, de)).

nlp_test(en,
         ivr(in('who is the director of the third man?'),
             out('The Third Man was created by Carol Reed.'))).
nlp_test(de,
         ivr(in('wer ist der regisseur von der dritte mann?'),
             out('Der Dritte Mann wurde von Carol Reed gemacht.'))).

%
% human movie director categorization
%

l3proc (I, F, fnQuestioning) :-

    frame (F, top,      general_info),
    frame (F, ent,      HUMAN),
    frame (F, entclass, human),

    is_movie_director(HUMAN),

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user about person's status)
    
    CAT is uriref (wde:FilmDirector),

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
         ivr(in('Do you know Alfred Hitchcock?'),
             out('Yes, I know Alfred Hitchcock.'))).
nlp_test(en,
         ivr(in('Who is Alfred Hitchcock?'),
             out('alfred hitchcock is categorized as film director'))).
nlp_test(de,
         ivr(in('Kennst Du Alfred Hitchcock?'),
             out('ja klar alfred hitchcock ist mir ein begriff'))).
nlp_test(de,
         ivr(in('wer ist Alfred Hitchcock?'),
             out('Alfred Hitchcock ist in der Kategorie Filmregisseur.'))).

l2proc_movieCreationDateTokens(LANG) :-

    ner(LANG, I, film, @MOVIES:TSTART_LABEL_0, @MOVIES:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(ent, NER1ENTITY)),
    list_append(VMC, frame(fnIntentionallyCreate)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  time)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    fnvm_exec (I, VMC).
   
nlp_gen (en, '@SELF_ADDRESS:LABEL when was @MOVIES:LABEL (produced|made)?',
         inline(l2proc_movieCreationDateTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL wann (ist|wurde) (eigentlich|) @MOVIES:LABEL (gedreht|gemacht)?',
         inline(l2proc_movieCreationDateTokens, de)).

nlp_test(en,
         ivr(in('when was the third man made?'),
             out('The Third Man was created in 1949.'))).
nlp_test(de,
         ivr(in('wann wurde der dritte mann gedreht?'),
             out('Der Dritte Mann ist aus 1949.'))).

l2proc_knowFilmTokens(LANG) :-

    ner(LANG, I, film, @MOVIES:TSTART_LABEL_0, @MOVIES:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(ent, NER1ENTITY)),
    list_append(VMC, fe(entclass, film)),
    list_append(VMC, fe(cog, uriref(aiu:self))),
    list_append(VMC, frame(fnFamiliarity)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  existance)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    fnvm_exec (I, VMC).
   
nlp_gen (en, '@SELF_ADDRESS:LABEL do you (happen to|) know (the movie|) @MOVIES:LABEL?',
         inline(l2proc_knowFilmTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL kennst du (eigentlich|) (den film|) @MOVIES:LABEL?',
         inline(l2proc_knowFilmTokens, de)).

nlp_gen (en, '@SELF_ADDRESS:LABEL (have you seen|did you happen to see) (the movie|) @MOVIES:LABEL?',
         inline(l2proc_knowFilmTokens, en)).
nlp_gen (de, '@SELF_ADDRESS:LABEL hast du (eigentlich|) (den film|) @MOVIES:LABEL gesehen?',
         inline(l2proc_knowFilmTokens, de)).


nlp_test(en,
         ivr(in('do you happen to know the movie the third man?'),
             out('Yes, I know The Third Man.'))).
nlp_test(de,
         ivr(in('kennst du den film der dritte mann?'),
             out('ja, ich kenne der dritte mann.'))).

%
% movie context follow-up style questions
%

nlp_test(en,
         ivr(in('do you happen to know the movie the third man?'),
             out('Yes, I know The Third Man.')),
         ivr(in('and do you know who made it?'),
             out('The Third Man was created by Carol Reed.')),
         ivr(in('do you know when it was produced?'),
             out('The Third Man was created in 1949.'))).

nlp_test(de,
         ivr(in('kennst du den film der dritte mann?'),
             out('ja, ich kenne der dritte mann.')),
         ivr(in('weisst du, wer ihn gedreht hat?'),
             out('Der Dritte Mann wurde von Carol Reed gemacht')),
         ivr(in('und weisst du, wann er gedreht wurde?'),
             out('Der dritte Mann ist aus 1949.'))).

%
% FIXME: cast members, genre, topics, ...
%

