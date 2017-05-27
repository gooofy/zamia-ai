% prolog

is_movie_director(HUMAN) :- rdf (MOVIE, wdpd:Director, HUMAN).

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

answerz (I, en, movieDirector, M_LABEL, D_LABEL)   :- sayz(I, en, format_str("The director of %s is %s", M_LABEL, D_LABEL)).
answerz (I, de, movieDirector, M_LABEL, D_LABEL)   :- sayz(I, de, format_str("Der Regisseur von %s ist %s", M_LABEL, D_LABEL)).

l4proc (I, F, fnTelling, director, MSGF, zfMovieCreation) :-

    frame (MSGF, movie,    MOVIE),
    frame (MSGF, director, DIRECTOR),

    ias (I, uttLang, LANG),

    entity_label(LANG, DIRECTOR, D_LABEL),
    entity_label(LANG, MOVIE,    M_LABEL),

    answerz (I, LANG, movieDirector, M_LABEL, D_LABEL).

l3proc (I, F, fnQuestioning, MSGF, zfMovieCreation) :-

    frame (F,    top,   TOP),
    frame (MSGF, movie, MOVIE),

    % remember our utterance interpretation

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user about some aspect of that movie)

    rdf (distinct, limit(1),
         MOVIE,    wdpd:Director,        DIRECTOR,
         MOVIE,    wdpd:PublicationDate, PDATE),

    list_append(VMC, fe(movie,       MOVIE)),
    list_append(VMC, fe(director,    DIRECTOR)),
    list_append(VMC, fe(pdate,       PDATE)),
    list_append(VMC, frame(zfMovieCreation)),

    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  TOP)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,  USER)),
    list_append(VMC, fe(spkr, uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 100),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    l4proc (I).

l2proc_movieDirectorTokens(LANG) :-

    ner(LANG, I, film, @MOVIES:TSTART_LABEL_0, @MOVIES:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(movie, NER1ENTITY)),
    list_append(VMC, frame(zfMovieCreation)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  director)),
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
             out('The director of The Third Man is Carol Reed.'))).
nlp_test(de,
         ivr(in('wer ist der regisseur von der dritte mann?'),
             out('Der Regisseur von Der dritte Mann ist Carol Reed.'))).

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

answerz (I, en, movieCreationDate, M_LABEL, Y)   :- sayz(I, en, format_str("%s was produced in %s", M_LABEL, Y)).
answerz (I, de, movieCreationDate, M_LABEL, Y)   :- sayz(I, de, format_str("%s wurde %s gedreht", M_LABEL, Y)).

l4proc (I, F, fnTelling, pdate, MSGF, zfMovieCreation) :-

    frame (MSGF, movie,    MOVIE),
    frame (MSGF, pdate,    PDATE),

    ias (I, uttLang, LANG),

    entity_label(LANG, MOVIE,    M_LABEL),
    stamp_date_time(PDATE, date(Y,M,D,H,Mn,S,'local')),

    answerz (I, LANG, movieCreationDate, M_LABEL, Y).

l2proc_movieCreationDateTokens(LANG) :-

    ner(LANG, I, film, @MOVIES:TSTART_LABEL_0, @MOVIES:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(movie, NER1ENTITY)),
    list_append(VMC, frame(zfMovieCreation)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(top,  pdate)),
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
             out('The Third Man was produced in 1949.'))).
nlp_test(de,
         ivr(in('wann wurde der dritte mann gedreht?'),
             out('Der dritte Mann wurde 1949 gedreht.'))).

% answer (movieSeen, en, MOVIE, MOVIE_LABEL, SCORE) :-
%     context_push(topic, movies),
%     context_push(topic, MOVIE),
%     say_eoa(en, format_str('Yes, I know %s - that is a well known movie.', MOVIE_LABEL), SCORE).
% answer (movieSeen, de, MOVIE, MOVIE_LABEL, SCORE) :-
%     context_push(topic, movies),
%     context_push(topic, MOVIE),
%     say_eoa(de, format_str('ja, %s kenne ich - ist ein bekannter Film.', MOVIE_LABEL), SCORE).
% 
% answer (movieSeenTokens, en, TSTART, TEND) :-
%     ner(en, film, TSTART, TEND, MOVIE, MOVIE_LABEL, SCORE),
%     answer (movieSeen, en, MOVIE, MOVIE_LABEL, SCORE).
% answer (movieSeenTokens, de, TSTART, TEND) :-
%     ner(de, film, TSTART, TEND, MOVIE, MOVIE_LABEL, SCORE),
%     answer (movieSeen, de, MOVIE, MOVIE_LABEL, SCORE).
% 
% nlp_gen (en, '@SELF_ADDRESS_EN:LABEL do you (happen to|) know (the movie|) @MOVIES_EN:LABEL?',
%              answer(movieSeenTokens, en, @MOVIES_EN:TSTART_LABEL_0, @MOVIES_EN:TEND_LABEL_0)). 
% nlp_gen (de, '@SELF_ADDRESS_DE:LABEL kennst du (eigentlich|) (den film|) @MOVIES_DE:LABEL?',
%              answer(movieSeenTokens, de, @MOVIES_DE:TSTART_LABEL_0, @MOVIES_DE:TEND_LABEL_0)). 
% 
% nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (have you seen|did you happen to see) (the movie|) @MOVIES_EN:LABEL?',
%              answer(movieSeenTokens, en, @MOVIES_EN:TSTART_LABEL_0, @MOVIES_EN:TEND_LABEL_0)). 
% nlp_gen (de, '@SELF_ADDRESS_DE:LABEL hast du (eigentlich|) (den film|) @MOVIES_DE:LABEL gesehen?',
%              answer(movieSeenTokens, de, @MOVIES_DE:TSTART_LABEL_0, @MOVIES_DE:TEND_LABEL_0)). 
% 
% nlp_test(en,
%          ivr(in('do you happen to know the movie the third man?'),
%              out('Yes, I know The Third Man - that is a well known movie.'))).
% nlp_test(de,
%          ivr(in('kennst du den film der dritte mann?'),
%              out('ja, der dritte mann kenne ich - ist ein bekannter film.'))).
% 
% %
% % movie context follow-up style questions
% %
% 
% answer (movieCreationDateFromContext, en) :-
%     context_score(topic, MOVIE, 100, S),
%     rdf (distinct, limit(1),
%          MOVIE, wdpd:InstanceOf, wde:Film,
%          MOVIE, rdfs:label,      LABEL,
%          filter (lang(LABEL) = 'en')),
%     answer(movieCreationDate, en, MOVIE, LABEL, S). 
% answer (movieCreationDateFromContext, de) :-
%     context_score(topic, MOVIE, 100, S),
%     rdf (distinct, limit(1),
%          MOVIE, wdpd:InstanceOf, wde:Film,
%          MOVIE, rdfs:label,      LABEL,
%          filter (lang(LABEL) = 'de')),
%     answer(movieCreationDate, de, MOVIE, LABEL, S). 
% 
% nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (and|) do you (happen to|) know when it was (made|produced) (by the way|)?',
%              answer(movieCreationDateFromContext, en)).
% nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (und|) weisst du (eigentlich|) wann er (gedreht|gemacht) wurde?',
%              answer(movieCreationDateFromContext, de)).
% 
% answer(movieDirectorFromContext, en) :-
%     context_score(topic, MOVIE, 100, S),
%     rdf (distinct, limit(1),
%          MOVIE, wdpd:InstanceOf, wde:Film,
%          MOVIE, rdfs:label,      LABEL,
%          filter (lang(LABEL) = 'en')),
%     answer(movieDirector, en, MOVIE, LABEL, S). 
% answer(movieDirectorFromContext, de) :-
%     context_score(topic, MOVIE, 100, S),
%     rdf (distinct, limit(1),
%          MOVIE, wdpd:InstanceOf, wde:Film,
%          MOVIE, rdfs:label,      LABEL,
%          filter (lang(LABEL) = 'de')),
%     answer(movieDirector, de, MOVIE, LABEL, S). 
%     
% nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (and|) do you (happen to|) know who (made|produced) it (by the way|)?',
%              answer(movieDirectorFromContext, en)).
% nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (und|) weisst du (eigentlich|) wer ihn (gedreht|gemacht) hat?',
%              answer(movieDirectorFromContext, de)).
% 
% nlp_test(en,
%          ivr(in('do you happen to know the movie the third man?'),
%              out('Yes, I know The Third Man - that is a well known movie.')),
%          ivr(in('and do you know who made it?'),
%              out('The director of The Third Man is Carol Reed.')),
%          ivr(in('do you know when it was produced?'),
%              out('The Third Man was produced in 1949.'))).
% 
% nlp_test(de,
%          ivr(in('kennst du den film der dritte mann?'),
%              out('ja, der dritte mann kenne ich - ist ein bekannter film.')),
%          ivr(in('weisst du, wer ihn gedreht hat?'),
%              out('Der Regisseur von Der dritte Mann ist Carol Reed.')),
%          ivr(in('und weisst du, wann er gedreht wurde?'),
%              out('Der dritte Mann wurde 1949 gedreht.'))).


%
% FIXME: cast members, genre, topics, ...
%

