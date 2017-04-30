% prolog

is_movie_director(PERSON) :- rdf (MOVIE, wdpd:Director, PERSON).

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

nlp_macro ('MOVIES_EN', MOVIE, LABEL) :-
    rdf (distinct,
         MOVIE, wdpd:InstanceOf,   wde:Film,
         MOVIE, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'en')).
nlp_macro ('MOVIES_DE', MOVIE, LABEL) :-
    rdf (distinct,
         MOVIE, wdpd:InstanceOf,   wde:Film,
         MOVIE, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')).

answer(topic, en) :-
    context_score(topic, movies, 100, SCORE), say_eoa(en, 'We were talking about movies.', SCORE).
answer(topic, de) :-
    context_score(topic, movies, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Filme.', SCORE).

answer (movieDirector, en, MOVIE, MOVIE_LABEL, SCORE) :-
    rdf (distinct, limit(1),
         MOVIE,    wdpd:Director, DIRECTOR,
         DIRECTOR, rdfs:label,    LABEL,
         filter (lang(LABEL) = 'en')),
    context_push(topic, movies),
    context_push(topic, MOVIE),
    context_push(topic, DIRECTOR),
    say_eoa(en, format_str('The director of %s is %s.', MOVIE_LABEL, LABEL), SCORE).
answer (movieDirector, de, MOVIE, MOVIE_LABEL, SCORE) :-
    rdf (distinct, limit(1),
         MOVIE,    wdpd:Director, DIRECTOR,
         DIRECTOR, rdfs:label,    LABEL,
         filter (lang(LABEL) = 'de')),
    context_push(topic, movies),
    context_push(topic, MOVIE),
    context_push(topic, DIRECTOR),
    say_eoa(de, format_str('Der Regisseur von %s ist %s.', MOVIE_LABEL, LABEL), SCORE).

answer (movieDirectorTokens, en, TSTART, TEND) :-
    ner(en, film, TSTART, TEND, MOVIE, MOVIE_LABEL, SCORE),
    answer (movieDirector, en, MOVIE, MOVIE_LABEL, SCORE).
answer (movieDirectorTokens, de, TSTART, TEND) :-
    ner(de, film, TSTART, TEND, MOVIE, MOVIE_LABEL, SCORE),
    answer (movieDirector, de, MOVIE, MOVIE_LABEL, SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL who (made|did) @MOVIES_EN:LABEL (by the way|)?',
             answer(movieDirectorTokens, en, @MOVIES_EN:TSTART_LABEL_0, @MOVIES_EN:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL wer hat (eigentlich|) @MOVIES_DE:LABEL gedreht?',
             answer(movieDirectorTokens, de, @MOVIES_DE:TSTART_LABEL_0, @MOVIES_DE:TEND_LABEL_0)). 

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (who is the director of|who directed) @MOVIES_EN:LABEL?',
             answer(movieDirectorTokens, en, @MOVIES_EN:TSTART_LABEL_0, @MOVIES_EN:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL wer ist (eigentlich|) der Regisseur von @MOVIES_DE:LABEL?',
             answer(movieDirectorTokens, de, @MOVIES_DE:TSTART_LABEL_0, @MOVIES_DE:TEND_LABEL_0)). 

nlp_test(en,
         ivr(in('who is the director of the third man?'),
             out('The director of The Third Man is Carol Reed.'))).
nlp_test(de,
         ivr(in('wer ist der regisseur von der dritte mann?'),
             out('Der Regisseur von Der dritte Mann ist Carol Reed.'))).

is_director(PERSON) :- 
    rdf(MOVIE, wdpd:Director, PERSON).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, movies, 100, SCORE),
    is_director(PERSON),
    is_male(PERSON),
    context_push(topic, movies),
    context_push(topic, PERSON),
    RS is SCORE + 100,
    say_eoa(en, 'He is a movie director.', RS).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, movies, 100, SCORE),
    is_director(PERSON),
    is_male(PERSON),
    context_push(topic, movies),
    context_push(topic, PERSON),
    RS is SCORE + 100,
    say_eoa(de, 'Er ist ein Regisseur.', RS).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, movies, 100, SCORE),
    is_director(PERSON),
    is_female(PERSON),
    context_push(topic, movies),
    context_push(topic, PERSON),
    RS is SCORE + 100,
    say_eoa(en, 'She is a movie director.', RS).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, movies, 100, SCORE),
    is_director(PERSON),
    is_female(PERSON),
    context_push(topic, movies),
    context_push(topic, PERSON),
    RS is SCORE + 100,
    say_eoa(de, 'Sie ist eine Regisseurin.', RS).

nlp_test(en,
         ivr(in('Who is Alfred Hitchcock?'),
             out('He is a movie director.'))).
nlp_test(de,
         ivr(in('wer ist Alfred Hitchcock?'),
             out('Er ist ein Regisseur.'))).

answer (movieCreationDate, en, MOVIE, MOVIE_LABEL, SCORE) :-
    rdf (distinct, limit(1),
         MOVIE,    wdpd:PublicationDate, TS),
    stamp_date_time(TS, date(Y,M,D,H,Mn,S,'local')),
    context_push(topic, movies),
    context_push(topic, MOVIE),
    say_eoa(en, format_str('%s was produced in %s.', MOVIE_LABEL, Y), SCORE).
answer (movieCreationDate, de, MOVIE, MOVIE_LABEL, SCORE) :-
    rdf (distinct, limit(1),
         MOVIE,    wdpd:PublicationDate, TS),
    stamp_date_time(TS, date(Y,M,D,H,Mn,S,'local')),
    context_push(topic, movies),
    context_push(topic, MOVIE),
    say_eoa(de, format_str('%s wurde %s gedreht.', MOVIE_LABEL, Y), SCORE).

answer (movieCreationDateTokens, en, TSTART, TEND) :-
    ner(en, film, TSTART, TEND, MOVIE, MOVIE_LABEL, SCORE),
    answer (movieCreationDate, en, MOVIE, MOVIE_LABEL, SCORE).
answer (movieCreationDateTokens, de, TSTART, TEND) :-
    ner(de, film, TSTART, TEND, MOVIE, MOVIE_LABEL, SCORE),
    answer (movieCreationDate, de, MOVIE, MOVIE_LABEL, SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL when was @MOVIES_EN:LABEL (produced|made)?',
             answer(movieCreationDateTokens, en, @MOVIES_EN:TSTART_LABEL_0, @MOVIES_EN:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL wann (ist|wurde) (eigentlich|) @MOVIES_DE:LABEL (gedreht|gemacht)?',
             answer(movieCreationDateTokens, de, @MOVIES_DE:TSTART_LABEL_0, @MOVIES_DE:TEND_LABEL_0)). 

nlp_test(en,
         ivr(in('when was the third man made?'),
             out('The Third Man was produced in 1949.'))).
nlp_test(de,
         ivr(in('wann wurde der dritte mann gedreht?'),
             out('Der dritte Mann wurde 1949 gedreht.'))).

answer (movieSeen, en, MOVIE, MOVIE_LABEL, SCORE) :-
    context_push(topic, movies),
    context_push(topic, MOVIE),
    say_eoa(en, format_str('Yes, I know %s - that is a well known movie.', MOVIE_LABEL), SCORE).
answer (movieSeen, de, MOVIE, MOVIE_LABEL, SCORE) :-
    context_push(topic, movies),
    context_push(topic, MOVIE),
    say_eoa(de, format_str('ja, %s kenne ich - ist ein bekannter Film.', MOVIE_LABEL), SCORE).

answer (movieSeenTokens, en, TSTART, TEND) :-
    ner(en, film, TSTART, TEND, MOVIE, MOVIE_LABEL, SCORE),
    answer (movieSeen, en, MOVIE, MOVIE_LABEL, SCORE).
answer (movieSeenTokens, de, TSTART, TEND) :-
    ner(de, film, TSTART, TEND, MOVIE, MOVIE_LABEL, SCORE),
    answer (movieSeen, de, MOVIE, MOVIE_LABEL, SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL do you (happen to|) know (the movie|) @MOVIES_EN:LABEL?',
             answer(movieSeenTokens, en, @MOVIES_EN:TSTART_LABEL_0, @MOVIES_EN:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL kennst du (eigentlich|) (den film|) @MOVIES_DE:LABEL?',
             answer(movieSeenTokens, de, @MOVIES_DE:TSTART_LABEL_0, @MOVIES_DE:TEND_LABEL_0)). 

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (have you seen|did you happen to see) (the movie|) @MOVIES_EN:LABEL?',
             answer(movieSeenTokens, en, @MOVIES_EN:TSTART_LABEL_0, @MOVIES_EN:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL hast du (eigentlich|) (den film|) @MOVIES_DE:LABEL gesehen?',
             answer(movieSeenTokens, de, @MOVIES_DE:TSTART_LABEL_0, @MOVIES_DE:TEND_LABEL_0)). 

nlp_test(en,
         ivr(in('do you happen to know the movie the third man?'),
             out('Yes, I know The Third Man - that is a well known movie.'))).
nlp_test(de,
         ivr(in('kennst du den film der dritte mann?'),
             out('ja, der dritte mann kenne ich - ist ein bekannter film.'))).

%
% movie context follow-up style questions
%

answer (movieCreationDateFromContext, en) :-
    context_score(topic, MOVIE, 100, S),
    rdf (distinct, limit(1),
         MOVIE, wdpd:InstanceOf, wde:Film,
         MOVIE, rdfs:label,      LABEL,
         filter (lang(LABEL) = 'en')),
    answer(movieCreationDate, en, MOVIE, LABEL, S). 
answer (movieCreationDateFromContext, de) :-
    context_score(topic, MOVIE, 100, S),
    rdf (distinct, limit(1),
         MOVIE, wdpd:InstanceOf, wde:Film,
         MOVIE, rdfs:label,      LABEL,
         filter (lang(LABEL) = 'de')),
    answer(movieCreationDate, de, MOVIE, LABEL, S). 

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (and|) do you (happen to|) know when it was (made|produced) (by the way|)?',
             answer(movieCreationDateFromContext, en)).
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (und|) weisst du (eigentlich|) wann er (gedreht|gemacht) wurde?',
             answer(movieCreationDateFromContext, de)).

answer(movieDirectorFromContext, en) :-
    context_score(topic, MOVIE, 100, S),
    rdf (distinct, limit(1),
         MOVIE, wdpd:InstanceOf, wde:Film,
         MOVIE, rdfs:label,      LABEL,
         filter (lang(LABEL) = 'en')),
    answer(movieDirector, en, MOVIE, LABEL, S). 
answer(movieDirectorFromContext, de) :-
    context_score(topic, MOVIE, 100, S),
    rdf (distinct, limit(1),
         MOVIE, wdpd:InstanceOf, wde:Film,
         MOVIE, rdfs:label,      LABEL,
         filter (lang(LABEL) = 'de')),
    answer(movieDirector, de, MOVIE, LABEL, S). 
    
nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (and|) do you (happen to|) know who (made|produced) it (by the way|)?',
             answer(movieDirectorFromContext, en)).
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (und|) weisst du (eigentlich|) wer ihn (gedreht|gemacht) hat?',
             answer(movieDirectorFromContext, de)).

nlp_test(en,
         ivr(in('do you happen to know the movie the third man?'),
             out('Yes, I know The Third Man - that is a well known movie.')),
         ivr(in('and do you know who made it?'),
             out('The director of The Third Man is Carol Reed.')),
         ivr(in('do you know when it was produced?'),
             out('The Third Man was produced in 1949.'))).

nlp_test(de,
         ivr(in('kennst du den film der dritte mann?'),
             out('ja, der dritte mann kenne ich - ist ein bekannter film.')),
         ivr(in('weisst du, wer ihn gedreht hat?'),
             out('Der Regisseur von Der dritte Mann ist Carol Reed.')),
         ivr(in('und weisst du, wann er gedreht wurde?'),
             out('Der dritte Mann wurde 1949 gedreht.'))).


%
% FIXME: cast members, genre, topics, ...
%

