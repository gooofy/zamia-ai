% prolog

is_author(PERSON) :- rdf (LITERATURE, wdpd:Author, PERSON).

%
% named entity recognition (NER) stuff: extra points for authors, literature title NER
%

ner_score (person, PERSON, 200) :- is_author(PERSON).

ner_score (literature, LITERATURE, 100). % FIXME: we should probably score by literature popularity or smth

ner_literature(LANG, TITLE_TOKENS, LITERATURE, LABEL) :-

    atom_chars(LANG, LSTR),

    rdf (distinct,
         LITERATURE, wdpd:InstanceOf,   wde:Book,
         LITERATURE, rdfs:label,        LABEL,
         filter (lang(LABEL) = LSTR)),

    tokenize (LANG, LABEL, LABEL_TOKENS),

    TITLE_TOKENS = LABEL_TOKENS.

ner(LANG, literature, TSTART, TEND, LITERATURE, LABEL, SCORE) :-

    rdf(ai:curin, ai:tokens, TOKENS),
    list_slice(TSTART, TEND, TOKENS, NAME_TOKENS),
   
    ner_literature(LANG, NAME_TOKENS, LITERATURE, LABEL),

    ner_score (literature, LITERATURE, SCORE).

nlp_macro ('LITERATURE_EN', LITERATURE, LABEL) :-
    rdf (distinct,
         LITERATURE, wdpd:InstanceOf,   wde:Book,
         LITERATURE, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'en')).
nlp_macro ('LITERATURE_DE', LITERATURE, LABEL) :-
    rdf (distinct,
         LITERATURE, wdpd:InstanceOf,   wde:Book,
         LITERATURE, rdfs:label,        LABEL,
         filter (lang(LABEL) = 'de')).

answer(topic, en) :-
    context_score(topic, literature, 100, SCORE), say_eoa(en, 'We were talking about literature.', SCORE).
answer(topic, de) :-
    context_score(topic, literature, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Literatur.', SCORE).

answer (literatureAuthor, en, LITERATURE, LITERATURE_LABEL, SCORE) :-
    rdf (distinct, limit(1),
         LITERATURE,    wdpd:Author, AUTHOR,
         AUTHOR,        rdfs:label,  LABEL,
         filter (lang(LABEL) = 'en')),
    context_push(topic, literature),
    context_push(topic, LITERATURE),
    context_push(topic, AUTHOR),
    say_eoa(en, format_str('The author of %s is %s.', LITERATURE_LABEL, LABEL), SCORE).
answer (literatureAuthor, de, LITERATURE, LITERATURE_LABEL, SCORE) :-
    rdf (distinct, limit(1),
         LITERATURE,    wdpd:Author,   AUTHOR,
         AUTHOR,        rdfs:label,    LABEL,
         filter (lang(LABEL) = 'de')),
    context_push(topic, literature),
    context_push(topic, LITERATURE),
    context_push(topic, AUTHOR),
    say_eoa(de, format_str('Der Autor von %s ist %s.', LITERATURE_LABEL, LABEL), SCORE).

answer (literatureAuthorTokens, en, TSTART, TEND) :-
    ner(en, literature, TSTART, TEND, LITERATURE, LITERATURE_LABEL, SCORE),
    answer (literatureAuthor, en, LITERATURE, LITERATURE_LABEL, SCORE).
answer (literatureAuthorTokens, de, TSTART, TEND) :-
    ner(de, literature, TSTART, TEND, LITERATURE, LITERATURE_LABEL, SCORE),
    answer (literatureAuthor, de, LITERATURE, LITERATURE_LABEL, SCORE).


nlp_gen (en, '@SELF_ADDRESS_EN:LABEL who (wrote|authored|created) @LITERATURE_EN:LABEL (by the way|)?',
             answer(literatureAuthorTokens, en, @LITERATURE_EN:TSTART_LABEL_0, @LITERATURE_EN:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL wer hat (eigentlich|) @LITERATURE_DE:LABEL geschrieben?',
             answer(literatureAuthorTokens, de, @LITERATURE_DE:TSTART_LABEL_0, @LITERATURE_DE:TEND_LABEL_0)). 

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (who is the author of|who authored) @LITERATURE_EN:LABEL?',
             answer(literatureAuthorTokens, en, @LITERATURE_EN:TSTART_LABEL_0, @LITERATURE_EN:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL wer ist (eigentlich|) der Autor von @LITERATURE_DE:LABEL?',
             answer(literatureAuthorTokens, de, @LITERATURE_DE:TSTART_LABEL_0, @LITERATURE_DE:TEND_LABEL_0)). 
 
nlp_test(en,
         ivr(in('who is the author of the stand?'),
             out('The author of The Stand is Stephen King.'))).
nlp_test(de,
         ivr(in('wer ist der autor von the stand?'),
             out('Der Autor von The Stand ist Stephen King.'))).

is_author(PERSON) :- 
    rdf(LITERATURE, wdpd:Author, PERSON).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, literature, 100, SCORE),
    is_author(PERSON),
    is_male(PERSON),
    context_push(topic, literature),
    context_push(topic, PERSON),
    say_eoa(en, 'He is an author.', SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, literature, 100, SCORE),
    is_author(PERSON),
    is_male(PERSON),
    context_push(topic, literature),
    context_push(topic, PERSON),
    say_eoa(de, 'Er ist ein Autor.', SCORE).

answer (knownPerson, en, PERSON, LABEL, SCORE) :-
    context_score (topic, literature, 100, SCORE),
    is_author(PERSON),
    is_female(PERSON),
    context_push(topic, literature),
    context_push(topic, PERSON),
    say_eoa(en, 'She is an author.', SCORE).
answer (knownPerson, de, PERSON, LABEL, SCORE) :-
    context_score (topic, literature, 100, SCORE),
    is_author(PERSON),
    is_female(PERSON),
    context_push(topic, literature),
    context_push(topic, PERSON),
    say_eoa(de, 'Sie ist eine Autorin.', SCORE).

nlp_test(en,
         ivr(in('Who is Dan Brown?'),
             out('He is an author.'))).
nlp_test(de,
         ivr(in('wer ist Dan Brown?'),
             out('Er ist ein Autor.'))).
 
answer (literatureCreationDate, en, LITERATURE, LITERATURE_LABEL, SCORE) :-
    rdf (distinct, limit(1),
         LITERATURE,    wdpd:PublicationDate, TS),
    stamp_date_time(TS, date(Y,M,D,H,Mn,S,'local')),
    context_push(topic, literature),
    context_push(topic, LITERATURE),
    say_eoa(en, format_str('%s was written in %s.', LITERATURE_LABEL, Y), SCORE).
answer (literatureCreationDate, de, LITERATURE, LITERATURE_LABEL, SCORE) :-
    rdf (distinct, limit(1),
         LITERATURE,    wdpd:PublicationDate, TS),
    stamp_date_time(TS, date(Y,M,D,H,Mn,S,'local')),
    context_push(topic, literature),
    context_push(topic, LITERATURE),
    say_eoa(de, format_str('%s wurde %s geschrieben.', LITERATURE_LABEL, Y), SCORE).

answer (literatureCreationDateTokens, en, TSTART, TEND) :-
    ner(en, literature, TSTART, TEND, LITERATURE, LITERATURE_LABEL, SCORE),
    answer (literatureCreationDate, en, LITERATURE, LITERATURE_LABEL, SCORE).
answer (literatureCreationDateTokens, de, TSTART, TEND) :-
    ner(de, literature, TSTART, TEND, LITERATURE, LITERATURE_LABEL, SCORE),
    answer (literatureCreationDate, de, LITERATURE, LITERATURE_LABEL, SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL when was @LITERATURE_EN:LABEL (created|written|made)?',
             answer(literatureCreationDateTokens, en, @LITERATURE_EN:TSTART_LABEL_0, @LITERATURE_EN:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL wann (ist|wurde) (eigentlich|) @LITERATURE_DE:LABEL (geschrieben|geschaffen)?',
             answer(literatureCreationDateTokens, de, @LITERATURE_DE:TSTART_LABEL_0, @LITERATURE_DE:TEND_LABEL_0)). 

nlp_test(en,
         ivr(in('when was the stand written?'),
             out('The Stand was written in 1978.'))).
nlp_test(de,
         ivr(in('wann wurde the stand geschrieben?'),
             out('The Stand wurde 1978 geschrieben.'))).

answer (literatureKnown, en, LITERATURE, LITERATURE_LABEL, SCORE) :-
    context_push(topic, literature),
    context_push(topic, LITERATURE),
    say_eoa(en, format_str('Yes, I know %s - that is a well known piece of literature.', LITERATURE_LABEL), SCORE).
answer (literatureKnown, de, LITERATURE, LITERATURE_LABEL, SCORE) :-
    context_push(topic, literature),
    context_push(topic, LITERATURE),
    say_eoa(de, format_str('ja, %s kenne ich - ist ein bekanntes Stück Literatur.', LITERATURE_LABEL), SCORE).

answer (literatureKnownTokens, en, TSTART, TEND) :-
    ner(en, literature, TSTART, TEND, LITERATURE, LITERATURE_LABEL, SCORE),
    answer (literatureKnown, en, LITERATURE, LITERATURE_LABEL, SCORE).
answer (literatureKnownTokens, de, TSTART, TEND) :-
    ner(de, literature, TSTART, TEND, LITERATURE, LITERATURE_LABEL, SCORE),
    answer (literatureKnown, de, LITERATURE, LITERATURE_LABEL, SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL do you (happen to|) know (the book|) @LITERATURE_EN:LABEL?',
             answer(literatureKnownTokens, en, @LITERATURE_EN:TSTART_LABEL_0, @LITERATURE_EN:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL kennst du (eigentlich|) (das Buch|) @LITERATURE_DE:LABEL?',
             answer(literatureKnownTokens, de, @LITERATURE_DE:TSTART_LABEL_0, @LITERATURE_DE:TEND_LABEL_0)). 

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (have you read|did you happen to read) (the book|) @LITERATURE_EN:LABEL?',
             answer(literatureKnownTokens, en, @LITERATURE_EN:TSTART_LABEL_0, @LITERATURE_EN:TEND_LABEL_0)). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL hast du (eigentlich|) (das Buch|) @LITERATURE_DE:LABEL gelesen?',
             answer(literatureKnownTokens, de, @LITERATURE_DE:TSTART_LABEL_0, @LITERATURE_DE:TEND_LABEL_0)). 

nlp_test(en,
         ivr(in('do you happen to know the book the stand?'),
             out('Yes, I know The Stand - that is a well known piece of literature.'))).
nlp_test(de,
         ivr(in('kennst du das buch the stand?'),
             out('ja, The Stand kenne ich - ist ein bekanntes Stück Literatur.'))).

%
% literature context follow-up style questions
%

answer (literatureCreationDateFromContext, en) :-
    context_score(topic, LITERATURE, 100, S),
    rdf (distinct, limit(1),
         LITERATURE, wdpd:InstanceOf, wde:Book,
         LITERATURE, rdfs:label,      LABEL,
         filter (lang(LABEL) = 'en')),
    answer(literatureCreationDate, en, LITERATURE, LABEL, S).
answer (literatureCreationDateFromContext, de) :-
    context_score(topic, LITERATURE, 100, S),
    rdf (distinct, limit(1),
         LITERATURE, wdpd:InstanceOf, wde:Book,
         LITERATURE, rdfs:label,      LABEL,
         filter (lang(LABEL) = 'de')),
    answer(literatureCreationDate, de, LITERATURE, LABEL, S).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (and|) do you (happen to|) know when it was (written|created) (by the way|)?',
             answer(literatureCreationDateFromContext, en)).
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (und|) weisst du (eigentlich|) wann es (geschrieben|geschaffen) wurde?',
             answer(literatureCreationDateFromContext, de)).

answer(literatureAuthorFromContext, en) :-
    context_score(topic, LITERATURE, 100, S),
    rdf (distinct, limit(1),
         LITERATURE, wdpd:InstanceOf, wde:Book,
         LITERATURE, rdfs:label,      LABEL,
         filter (lang(LABEL) = 'en')),
    answer(literatureAuthor, en, LITERATURE, LABEL, S). 
answer(literatureAuthorFromContext, de) :-
    context_score(topic, LITERATURE, 100, S),
    rdf (distinct, limit(1),
         LITERATURE, wdpd:InstanceOf, wde:Book,
         LITERATURE, rdfs:label,      LABEL,
         filter (lang(LABEL) = 'de')),
    answer(literatureAuthor, de, LITERATURE, LABEL, S). 
    
nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (and|) do you (happen to|) know who (wrote|created) it (by the way|)?',
             answer(literatureAuthorFromContext, en)).
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (und|) weisst du (eigentlich|) wer es (geschrieben|geschaffen) hat?',
             answer(literatureAuthorFromContext, de)).

nlp_test(en,
         ivr(in('do you happen to know the book the stand?'),
             out('Yes, I know The Stand - that is a well known piece of literature.')),
         ivr(in('and do you know who wrote it?'),
             out('The author of The Stand is Stephen King.')),
         ivr(in('do you know when it was written?'),
             out('The Stand was written in 1978.'))).

nlp_test(de,
         ivr(in('kennst du das buch the stand?'),
             out('ja, The Stand kenne ich - ist ein bekanntes Stück Literatur.')),
         ivr(in('weisst du, wer es geschrieben hat?'),
             out('Der Autor von The Stand ist Stephen King.')),
         ivr(in('und weisst du, wann es geschrieben wurde?'),
             out('The Stand wurde 1978 geschrieben.'))).


%
% FIXME: genre, topics, ...
%

%
% misc / random stuff
%

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL agatha christie',
             'I like Miss Marple...').
nlp_gen (de, '@SELF_ADDRESS_EN:LABEL agatha christie',
             'Ich mag Miss Marple...').

