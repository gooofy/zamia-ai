%prolog

% test_setup('smalltalk') :- context_set(topic, []), eoa.

% answer(topic, en) :-
%     context_score(topic, language, 100, SCORE), say_eoa(en, 'We were talking about languages.', SCORE).
% answer(topic, de) :-
%     context_score(topic, language, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Sprachen.', SCORE).

nlp_gens(en, "@SELF_ADDRESS:LABEL (isn't that a wonderful|wonderful|a very nice|terrible) language",
             "do you speak any foreign languages?", 
             "du you like foreign languages?").
nlp_gens(de, '@SELF_ADDRESS:LABEL (ist das nicht eine wunderbare|wunderbare|eine sehr schöne|furchtbare) sprache',
             'Sprichst Du irgendwelche Fremdsprachen?',
             'Magst Du Fremdsprachen?').


nlp_test(en,
         ivr(in('What did we talk about?'),
             out('Please help me out here.')),
         ivr(in('terrible language'),
             out('do you speak any foreign languages?'))
             ).
nlp_test(de,
         ivr(in('Worüber haben wir gesprochen?'),
             out('Da bin ich mir nicht sicher')),
         ivr(in('wunderbare sprache'),
             out('Magst Du Fremdsprachen?'))
             ).

