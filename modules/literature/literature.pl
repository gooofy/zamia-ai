% prolog

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

answer (literatureAuthor, en, LITERATURE, LITERATURE_LABEL) :-
    rdf (distinct, limit(1),
         LITERATURE,    wdpd:Author, AUTHOR,
         AUTHOR,        rdfs:label,  LABEL,
         filter (lang(LABEL) = 'en')),
    context_push(topic, literature),
    context_push(topic, LITERATURE),
    context_push(topic, AUTHOR),
    say_eoa(en, format_str('The author of %s is %s.', LITERATURE_LABEL, LABEL)).
answer (literatureAuthor, de, LITERATURE, LITERATURE_LABEL) :-
    rdf (distinct, limit(1),
         LITERATURE,    wdpd:Author,   AUTHOR,
         AUTHOR,        rdfs:label,    LABEL,
         filter (lang(LABEL) = 'de')),
    context_push(topic, literature),
    context_push(topic, LITERATURE),
    context_push(topic, AUTHOR),
    say_eoa(de, format_str('Der Author von %s ist %s.', LITERATURE_LABEL, LABEL)).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL who (wrote|authored|created) @LITERATURE_EN:LABEL (by the way|)?',
             answer(literatureAuthor, en, '@LITERATURE_EN:LITERATURE', "@LITERATURE_EN:LABEL")). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL wer hat (eigentlich|) @LITERATURE_DE:LABEL geschrieben?',
             answer(literatureAuthor, de, '@LITERATURE_DE:LITERATURE', "@LITERATURE_DE:LABEL")). 

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (who is the author of|who authored) @LITERATURE_EN:LABEL?',
             answer(literatureAuthor, en, '@LITERATURE_EN:LITERATURE', "@LITERATURE_EN:LABEL")). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL wer ist (eigentlich|) der Author von @LITERATURE_DE:LABEL?',
             answer(literatureAuthor, de, '@LITERATURE_DE:LITERATURE', "@LITERATURE_DE:LABEL")). 
 
nlp_test(en,
         ivr(in('who is the author of the stand?'),
             out('The author of The Stand is Stephen King.'))).
nlp_test(de,
         ivr(in('wer ist der author von the stand?'),
             out('Der Author von The Stand ist Stephen King.'))).

is_author(PERSON) :- 
    rdf(LITERATURE, wdpd:Author, PERSON).

answer (knownPerson, en, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, literature, 100, SCORE),
    is_author(PERSON),
    is_male(PERSON),
    context_push(topic, literature),
    context_push(topic, PERSON),
    say_eoa(en, 'He is an author.', SCORE).
answer (knownPerson, de, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, literature, 100, SCORE),
    is_author(PERSON),
    is_male(PERSON),
    context_push(topic, literature),
    context_push(topic, PERSON),
    say_eoa(de, 'Er ist ein Author.', SCORE).

answer (knownPerson, en, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, literature, 100, SCORE),
    is_author(PERSON),
    is_female(PERSON),
    context_push(topic, literature),
    context_push(topic, PERSON),
    say_eoa(en, 'She is an author.', SCORE).
answer (knownPerson, de, PERSON, LABEL) :-
    SCORE is 10,
    context_score (topic, literature, 100, SCORE),
    is_author(PERSON),
    is_female(PERSON),
    context_push(topic, literature),
    context_push(topic, PERSON),
    say_eoa(de, 'Sie ist eine Authorin.', SCORE).

nlp_test(en,
         ivr(in('Who is Dan Brown?'),
             out('He is an author.'))).
nlp_test(de,
         ivr(in('wer ist Dan Brown?'),
             out('Er ist ein Author.'))).
 
answer (literatureCreationDate, en, LITERATURE, LITERATURE_LABEL) :-
    rdf (distinct, limit(1),
         LITERATURE,    wdpd:PublicationDate, TS),
    stamp_date_time(TS, date(Y,M,D,H,Mn,S,'local')),
    context_push(topic, literature),
    context_push(topic, LITERATURE),
    say_eoa(en, format_str('%s was written in %s.', LITERATURE_LABEL, Y), 100).
answer (literatureCreationDate, de, LITERATURE, LITERATURE_LABEL) :-
    rdf (distinct, limit(1),
         LITERATURE,    wdpd:PublicationDate, TS),
    stamp_date_time(TS, date(Y,M,D,H,Mn,S,'local')),
    context_push(topic, literature),
    context_push(topic, LITERATURE),
    say_eoa(de, format_str('%s wurde %s geschrieben.', LITERATURE_LABEL, Y), 100).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL when was @LITERATURE_EN:LABEL (created|written|made)?',
             answer(literatureCreationDate, en, '@LITERATURE_EN:LITERATURE', "@LITERATURE_EN:LABEL")). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL wann (ist|wurde) (eigentlich|) @LITERATURE_DE:LABEL (geschrieben|geschaffen)?',
             answer(literatureCreationDate, de, '@LITERATURE_DE:LITERATURE', "@LITERATURE_DE:LABEL")). 

nlp_test(en,
         ivr(in('when was the stand written?'),
             out('The Stand was written in 1978.'))).
nlp_test(de,
         ivr(in('wann wurde the stand geschrieben?'),
             out('The Stand wurde 1978 geschrieben.'))).

answer (literatureKnown, en, LITERATURE, LITERATURE_LABEL) :-
    context_push(topic, literature),
    context_push(topic, LITERATURE),
    say_eoa(en, format_str('Yes, I know %s - that is a well known piece of literature.', LITERATURE_LABEL)).
answer (literatureKnown, de, LITERATURE, LITERATURE_LABEL) :-
    context_push(topic, literature),
    context_push(topic, LITERATURE),
    say_eoa(de, format_str('ja, %s kenne ich - ist ein bekanntes Stück Literatur.', LITERATURE_LABEL)).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL do you (happen to|) know (the book|) @LITERATURE_EN:LABEL?',
             answer(literatureKnown, en, '@LITERATURE_EN:LITERATURE', "@LITERATURE_EN:LABEL")). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL kennst du (eigentlich|) (das Buch|) @LITERATURE_DE:LABEL?',
             answer(literatureKnown, de, '@LITERATURE_DE:LITERATURE', "@LITERATURE_DE:LABEL")). 

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (have you read|did you happen to read) (the book|) @LITERATURE_EN:LABEL?',
             answer(literatureKnown, en, '@LITERATURE_EN:LITERATURE', "@LITERATURE_EN:LABEL")). 
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL hast du (eigentlich|) (das Buch|) @LITERATURE_DE:LABEL gelesen?',
             answer(literatureKnown, de, '@LITERATURE_DE:LITERATURE', "@LITERATURE_DE:LABEL")). 

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
    answer(literatureCreationDate, en, LITERATURE, LABEL). 
answer (literatureCreationDateFromContext, de) :-
    context_score(topic, LITERATURE, 100, S),
    rdf (distinct, limit(1),
         LITERATURE, wdpd:InstanceOf, wde:Book,
         LITERATURE, rdfs:label,      LABEL,
         filter (lang(LABEL) = 'de')),
    answer(literatureCreationDate, de, LITERATURE, LABEL). 

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
    answer(literatureAuthor, en, LITERATURE, LABEL). 
answer(literatureAuthorFromContext, de) :-
    context_score(topic, LITERATURE, 100, S),
    rdf (distinct, limit(1),
         LITERATURE, wdpd:InstanceOf, wde:Book,
         LITERATURE, rdfs:label,      LABEL,
         filter (lang(LABEL) = 'de')),
    answer(literatureAuthor, de, LITERATURE, LABEL). 
    
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
             out('Der Author von The Stand ist Stephen King.')),
         ivr(in('und weisst du, wann es geschrieben wurde?'),
             out('The Stand wurde 1978 geschrieben.'))).


%
% FIXME: genre, topics, ...
%

